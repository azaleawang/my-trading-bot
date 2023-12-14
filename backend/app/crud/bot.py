from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
import logging
from app.src.controller.bot import delete_bot_container, stop_bot_container
from app.models.bot import Bot
from app.models.worker_server import WorkerServer
from app.src.schema import schemas
from sqlalchemy.sql import and_
from sqlalchemy.orm import joinedload

from app.src.controller.ec2 import (
    create_ec2_instance,
    start_ec2_instance,
    stop_ec2_instance,
)
import re

ALLOW_CREATE = True


def get_bots(db: Session):
    return db.query(Bot).all()


def check_name(db: Session, container_name: str, bot_name: str, user_id: int):
    name_regex = re.compile(r"^[A-Za-z-_1234567890]+$")
    match = name_regex.match(bot_name)
    if not match:
        raise HTTPException(status_code=400, detail="名稱只能包含英文、數字、底線、減號，請重新命名！")
    if len(bot_name) < 0 or len(bot_name) > 20:
        raise HTTPException(status_code=400, detail="名稱長度不符合規定，請重新命名！")
    if (
        db.query(Bot)
        .filter(
            and_(Bot.name == bot_name, Bot.owner_id == user_id, Bot.status != "deleted")
        )
        .first()
    ):
        raise HTTPException(status_code=400, detail="名稱重複，請重新命名！")
    if (
        db.query(Bot)
        .filter(and_(Bot.container_name == container_name, Bot.status != "deleted"))
        .all()
    ):
        raise HTTPException(status_code=400, detail="Container name already exists.")


def get_user_bots(db: Session, user_id: int):
    return (
        db.query(Bot)
        .options(joinedload(Bot.trade_history))
        .filter(Bot.owner_id == user_id)
        .all()
    )


# get bot by bot id
def get_bot_by_id(db: Session, bot_id: int):
    db_bot = db.query(Bot).filter(Bot.id == bot_id).first()
    return db_bot, db_bot.trade_history


def create_user_bot(db: Session, bot: schemas.BotCreate):
    # TODO 儲存失敗但docker已經開起來怎麼辦(應該要分兩次存)
    try:
        db_bot = Bot(**bot.model_dump())
        # Check if the bot name registered
        db.add(db_bot)
        db.commit()
        db.refresh(db_bot)
        return db_bot
    except IntegrityError as e:
        if "ForeignKeyViolation" in str(e):
            logging.error(f"ForeignKeyViolation in storing bot creation: {e}")
            raise HTTPException(status_code=400, detail="Owner id not existed.")
        else:
            logging.error(f"IntegrityError in storing bot creation: {e}")
            raise HTTPException(status_code=400, detail="Data integrity error.")
    except SQLAlchemyError as e:
        logging.error(f"Error in storing bot creation: {e}")
        raise HTTPException(status_code=400, detail="Database error.")


def stop_user_bot(bot_id: str, worker_ip: str, db: Session):
    bot = db.query(Bot).filter(Bot.id == bot_id).first()

    if bot is None:
        raise HTTPException(status_code=404, detail=f"Bot #{bot_id} Bot not found.")
    elif bot.status == "stopped":
        raise HTTPException(
            status_code=400, detail=f"Bot #{bot_id} is already stopped."
        )
    elif bot.status == "deleted":
        raise HTTPException(
            status_code=400, detail=f"Cannot stop since bot #{bot_id} was deleted."
        )

    elif bot.status == "running":
        stop_bot_container(bot.container_id, worker_ip)
        bot.status = "stopped"
        db.commit()
        return bot
    else:
        raise HTTPException(
            status_code=500,
            detail=f"No operation on database during stopping bot: {bot.container_name}",
        )


def delete_user_bot(bot_id: int, worker_ip: str, db: Session):
    bot = db.query(Bot).filter(Bot.id == bot_id).first()

    if bot is None:
        raise HTTPException(status_code=404, detail=f"Bot #{bot_id} Bot not found.")
    if bot.status == "running":
        raise HTTPException(
            status_code=400, detail=f"Please stop Bot #{bot_id} manually first!"
        )
    if bot.status == "deleted":
        raise HTTPException(status_code=400, detail=f"Bot #{bot_id} already deleted.")

    if bot.status == "stopped" or bot.status == "exited":
        # Then check whether the worker server is still alive
        if bot.worker_server.private_ip:
            delete_bot_container(bot.container_id, worker_ip)
        db.delete(bot)
        db.commit()
        return bot
    else:
        raise HTTPException(
            status_code=500,
            detail=f"No operation on database during deleting bot: {bot.container_name}",
        )


def number_of_running_server(db: Session):
    return db.query(WorkerServer).filter(WorkerServer.status == "running").count()


def assign_worker_server(db: Session):
    # try:
    # Find a worker server with enough available memory
    global ALLOW_CREATE
    suitable_server = (
        db.query(WorkerServer)
        .filter(WorkerServer.status == "running")
        .filter(WorkerServer.private_ip != None)
        .filter(WorkerServer.available_memory >= 128)
        .order_by(WorkerServer.available_memory.desc())
        .first()
    )

    if suitable_server:
        ALLOW_CREATE = True
        print(f"Assigning container to server {suitable_server.private_ip}")
        return suitable_server

    else:
        # First, check if there is any preparing server
        preparing_server = (
            db.query(WorkerServer).filter(WorkerServer.status == "preparing").all()
        )
        if preparing_server:
            raise HTTPException(
                status_code=500,
                detail="New server is Preparing. PLEASE TRY AGAIN LATER.",
            )
        # No preparing server, Let's check if there is any existed stopped server
        candidate_server = (
            db.query(WorkerServer)
            .filter(WorkerServer.status == "stopped")
            .order_by(WorkerServer.updated_at.desc())
            .first()
        )
        if candidate_server:
            print(f"Starting server {candidate_server.instance_id}")
            start_ec2_instance(instance_id=candidate_server.instance_id)
            candidate_server.status = "preparing"
            db.commit()

        # No stopped server, Let's check if we can create a new server
        # Create a new worker server
        elif ALLOW_CREATE:
            create_ec2_instance()
            ALLOW_CREATE = False
        raise HTTPException(
            status_code=500,
            detail="No available worker-server found. New server is Starting. PLEASE TRY AGAIN LATER.",
        )


# update worker server available memory
def update_worker_server_memory(
    db: Session, worker_instance_id: str, memory_usage: int
):
    worker_server = (
        db.query(WorkerServer)
        .filter(WorkerServer.instance_id == worker_instance_id)
        .first()
    )
    if worker_server:
        worker_server.available_memory -= memory_usage
        db.commit()
        return worker_server
    else:
        raise HTTPException(
            status_code=404, detail=f"Worker server {worker_instance_id} not found."
        )


# find worker server by bot id
def find_worker_server(db: Session, bot_id: int):
    bot = db.query(Bot).filter(Bot.id == bot_id).first()
    if bot == None:
        raise HTTPException(status_code=404, detail=f"Bot {bot_id} not found.")
    if bot.worker_server:
        return bot.worker_server.private_ip

    raise HTTPException(status_code=404, detail=f"Bot's worker_server not data.")


def worker_scaling(db: Session, worker_ip: str):
    worker_server = (
        db.query(WorkerServer).filter(WorkerServer.private_ip == worker_ip).first()
    )
    if not worker_server:
        return False
    if worker_server.available_memory == worker_server.total_memory:
        print("Worker server need to be closed")
        # True if stop successfully
        return stop_ec2_instance(instance_id=worker_server.instance_id)

    return False


def update_worker_server_status(db: Session, worker_ip: str):
    worker_server = (
        db.query(WorkerServer).filter(WorkerServer.private_ip == worker_ip).first()
    )
    if not worker_server:
        raise HTTPException(status_code=404, detail=f"Worker server not found.")
    worker_server.status = "stopped"
    worker_server.private_ip = None
    db.commit()
    return True
