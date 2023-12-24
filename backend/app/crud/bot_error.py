from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.src.schema.schemas import BotErrorSchema
from app import models


# Read error log for user by container name (for now, only trade-related logs)
def get_error_log_by_container(bot_id: int, db: Session):
    result = (
        db.query(models.BotError)
        .join(models.Bot, models.BotError.container_name == models.Bot.container_name)
        .filter(models.Bot.id == bot_id)
        .all()
    )
    return result


# Create
def create_error_log(error: BotErrorSchema, db: Session):
    db_error = models.BotError(container_name=error.container_name, error=error.error)
    db.add(db_error)
    db.commit()
    db.refresh(db_error)
    return db_error
