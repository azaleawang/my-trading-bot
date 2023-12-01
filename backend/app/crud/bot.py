from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
import logging
from app.src.controller.bot import delete_bot_container, stop_bot_container
from app.src.models.bot import Bot
from app.src.schema import schemas
from sqlalchemy.sql import and_
from sqlalchemy.orm import joinedload

def get_bots(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Bot).offset(skip).limit(limit).all()

def check_name(db: Session, container_name: str, bot_name: str, user_id: int):
    if db.query(Bot).filter(and_(Bot.name == bot_name, Bot.owner_id == user_id, Bot.status != 'deleted')).first():
        raise HTTPException(
            status_code=400, detail="Bot name already registered. Pls rename it!"
        )
    if db.query(Bot).filter(and_(Bot.container_name == container_name, Bot.status != 'deleted')).all():
        raise HTTPException(status_code=400, detail="Container name already exists.")


def get_user_bots(db: Session, user_id: int):
    # return db.query(Bot).filter(Bot.owner_id == user_id).all()
    return db.query(Bot).options(joinedload(Bot.trade_history)).filter(Bot.owner_id == user_id).all()



def create_user_bot(db: Session, bot: schemas.BotCreate):
    # TODO 儲存失敗但docker已經開起來怎麼辦
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


def stop_user_bot(user_id: int, bot_id: str, db: Session):
    bot = db.query(Bot).filter(Bot.id == bot_id).first()

    if bot is None:
        raise HTTPException(status_code=404, detail=f"Bot #{bot_id} Bot not found.")
    elif bot.owner_id != user_id:
        raise HTTPException(
            status_code=404,
            detail=f"No matched bot #{bot_id} for this user id {user_id}.",
        )
    elif bot.status == "stopped":
        raise HTTPException(
            status_code=400, detail=f"Bot #{bot_id} is already stopped."
        )
    elif bot.status == "deleted":
        raise HTTPException(
            status_code=400, detail=f"Cannot stop since bot #{bot_id} was deleted."
        )

    elif bot.status == "running":
        stop_bot_container(bot.container_id)
        bot.status = "stopped"
        db.commit()
        return bot
    else:
        raise HTTPException(
            status_code=500,
            detail=f"No operation on database during stopping bot: {bot.container_name}",
        )


def delete_user_bot(user_id: int, bot_id: int, db: Session):
    bot = db.query(Bot).filter(Bot.id == bot_id).first()

    if bot is None:
        raise HTTPException(status_code=404, detail=f"Bot #{bot_id} Bot not found.")
    if bot.owner_id != user_id:
        raise HTTPException(
            status_code=404,
            detail=f"No matched bot #{bot_id} for this user id {user_id}.",
        )
    if bot.status == "running":
        raise HTTPException(
            status_code=400, detail=f"Please stop Bot #{bot_id} manually first!"
        )
    if bot.status == "deleted":
        raise HTTPException(status_code=400, detail=f"Bot #{bot_id} already deleted.")

    if bot.status == "stopped":
        delete_bot_container(bot.container_id)
        db.delete(bot)
        db.commit()
        return bot
    else:
        raise HTTPException(
            status_code=500,
            detail=f"No operation on database during deleting bot: {bot.container_name}",
        )
