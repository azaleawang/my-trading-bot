from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.src.schema.schemas import BotErrorSchema
from app.src import models


# Read error log for user by container name
def get_error_log_by_container(bot_id: int, db: Session):
    result = (
        db.query(models.Bot_Error)
        .join(models.Bot, models.Bot_Error.container_name == models.Bot.container_name)
        .filter(models.Bot.id == bot_id)
        .all()
    )

    if not result:
        raise HTTPException(status_code=404, detail="No error logs found for this bot")

    # Extract error logs and container names
   
    # print(result)
    return result


# Create
def create_error_log(error: BotErrorSchema, db: Session):
    db_error = models.Bot_Error(container_name=error.container_name, error=error.error)
    db.add(db_error)
    db.commit()
    db.refresh(db_error)
    return db_error
