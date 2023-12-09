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


def get_bots(db: Session):
    return db.query(Bot).all()


def check_name(db: Session, container_name: str, bot_name: str, user_id: int):
    if (
        db.query(Bot)
        .filter(
            and_(Bot.name == bot_name, Bot.owner_id == user_id, Bot.status != "deleted")
        )
        .first()
    ):
        raise HTTPException(
            status_code=400, detail="Bot name already registered. Pls rename it!"
        )
    if (
        db.query(Bot)
        .filter(and_(Bot.container_name == container_name, Bot.status != "deleted"))
        .all()
    ):
        raise HTTPException(status_code=400, detail="Container name already exists.")


def get_user_bots(db: Session, user_id: int):
    # return db.query(Bot).filter(Bot.owner_id == user_id).all()
    return (
        db.query(Bot)
        .options(joinedload(Bot.trade_history))
        .filter(Bot.owner_id == user_id)
        .all()
    )


def create_user_bot(db: Session, bot: schemas.BotCreate):
    # TODO 儲存失敗但docker已經開起來怎麼辦(應該要分兩次存)
    try:
        db_bot = Bot(**bot.model_dump())
        # Check if the bot name registered

        # TODO check if the bot script existed (s3 or local?)
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
    # except Exception as e:
    #     logging.error(f"Unexpected error in storing bot creation: {e}")
    #     raise HTTPException(status_code=500, detail="Unexpected database error.")


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
    # if bot.owner_id != user_id:
    #     raise HTTPException(
    #         status_code=404,
    #         detail=f"No matched bot #{bot_id} for this user id {user_id}.",
    #     )
    if bot.status == "running":
        raise HTTPException(
            status_code=400, detail=f"Please stop Bot #{bot_id} manually first!"
        )
    if bot.status == "deleted":
        raise HTTPException(status_code=400, detail=f"Bot #{bot_id} already deleted.")

    if bot.status == "stopped" or bot.status == "exited":
        
        delete_bot_container(bot.container_id, worker_ip)
        db.delete(bot)
        db.commit()
        return bot
    else:
        raise HTTPException(
            status_code=500,
            detail=f"No operation on database during deleting bot: {bot.container_name}",
        )


def assign_worker_server(db: Session):
    try:  
        # Find a worker server with enough available memory
        suitable_server = (
            db.query(WorkerServer)
            .filter(WorkerServer.available_memory >= 128)
            .order_by(WorkerServer.available_memory.desc())
            .first()
        )

        if suitable_server:
            # Create and assign a new container
            # new_container = Container(name=container_name, worker_server=suitable_server)
            # session.add(new_container)
            # session.commit()
            print(f"Assigning container to server {suitable_server.private_ip}")
            return suitable_server.private_ip
        else:
            return "No suitable server found for the container."
    except SQLAlchemyError as e:
        logging.error(f"Error in assigning worker server: {e}")
        raise HTTPException(status_code=500, detail="Database error.")
    except Exception as e:
        logging.error(f"Unexpected error in assigning worker server: {e}")
        raise HTTPException(status_code=500, detail="Unexpected database error.")
    

# update worker server available memory
def update_worker_server_memory(db: Session, worker_server_ip: str, memory_usage: int):
    try:
        worker_server = db.query(WorkerServer).filter(WorkerServer.private_ip == worker_server_ip).first()
        if worker_server:
            worker_server.available_memory -= memory_usage
            db.commit()
            return worker_server
        else:
            raise HTTPException(status_code=404, detail=f"Worker server {worker_server_ip} not found.")
    except SQLAlchemyError as e:
        logging.error(f"Error in updating worker server available memory: {e}")
        raise HTTPException(status_code=500, detail="Database error.")
    except Exception as e:
        logging.error(f"Unexpected error in updating worker server available memory: {e}")
        raise HTTPException(status_code=500, detail="Unexpected database error.")
    
# find worker server by bot id
def find_worker_server(db: Session, bot_id: int):
    try:
        bot = db.query(Bot).filter(Bot.id == bot_id).first()
       
        if bot:
            if bot.worker_server:
                return bot.worker_server.private_ip
            raise HTTPException(status_code=404, detail=f"Bot's worker_server not found.")
        else:
            raise HTTPException(status_code=404, detail=f"Bot {bot_id} not found.")
    except SQLAlchemyError as e:
        logging.error(f"Error in finding worker server by bot id: {e}")
        raise HTTPException(status_code=500, detail="Database error.")
    except Exception as e:
        logging.error(f"Unexpected error in finding worker server by bot id: {e}")
        raise HTTPException(status_code=500, detail="Unexpected database error.")