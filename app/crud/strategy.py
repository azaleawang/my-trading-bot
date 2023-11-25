from app.src.models import Strategy
from sqlalchemy.orm import Session
from app.src.schema import schemas
from sqlalchemy import or_


def get_user_strategies(db: Session, user_id: int):
    return db.query(Strategy).filter(or_(Strategy.is_public, Strategy.provider_id == user_id)).all()

