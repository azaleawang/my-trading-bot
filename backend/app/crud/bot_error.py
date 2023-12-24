from sqlalchemy.orm import Session
from app.schema import bot as schemas
from app.models import BotError, Bot


def get_error_log_by_container(bot_id: int, db: Session):
    result = (
        db.query(BotError)
        .join(Bot, BotError.container_name == Bot.container_name)
        .filter(Bot.id == bot_id)
        .all()
    )
    return result


def create_error_log(error: schemas.BotError, db: Session):
    db_error = BotError(container_name=error.container_name, error=error.error)
    db.add(db_error)
    db.commit()
    db.refresh(db_error)
    return db_error
