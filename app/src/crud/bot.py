from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
import logging
from app.src.controller.bot import delete_bot_container, stop_bot_container
from app.src.model import models, schemas

def get_bots(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Bot).offset(skip).limit(limit).all()

def check_container_name(db: Session, container_name: str):
    return db.query(models.Bot).filter(models.Bot.container_name == container_name).all()

def get_user_bots(db: Session, user_id: int):
    return db.query(models.Bot).filter(models.Bot.owner_id == user_id).all()


def create_user_bot(db: Session, bot: schemas.BotCreate):
    # TODO 儲存失敗但docker已經開起來怎麼辦
    try:
        db_bot = models.Bot(**bot.model_dump())
        # Check if the bot name registered
        existed_name = db.query(models.Bot).filter(models.Bot.name == bot.name).first()
        if existed_name:
            raise HTTPException(
                status_code=400, detail="Bot name already registered. Pls rename it!"
            )

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
    except Exception as e:
        logging.error(f"Unexpected error in storing bot creation: {e}")
        raise HTTPException(status_code=500, detail="Unexpected database error.")


def stop_user_bot(user_id: int, bot_id: str, db: Session):
    bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()

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
    bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()

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
        bot.status = "deleted"
        db.commit()
        return bot
    else:
        raise HTTPException(
            status_code=500,
            detail=f"No operation on database during deleting bot: {bot.container_name}",
        )
