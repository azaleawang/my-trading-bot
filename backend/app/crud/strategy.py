from app.models import Strategy
from sqlalchemy.orm import Session
from app.schema import strategy as schemas
from sqlalchemy import or_


def get_user_all_strategies(db: Session, user_id: int):
    return (
        db.query(Strategy)
        .filter(or_(Strategy.is_public, Strategy.provider_id == user_id))
        .all()
    )


def get_strategy(db: Session, strategy_id: int):
    return db.query(Strategy).filter(Strategy.id == strategy_id).first()


def insert_strategy(db: Session, strategy_create: schemas.StrategyCreate):
    db_strategy = Strategy(**strategy_create.model_dump())
    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)
    return db_strategy


def update_strategy(
    db: Session, strategy_id: int, strategy_update: schemas.StrategyCreate
):
    db_strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    if db_strategy:
        update_data = strategy_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_strategy, key, value)
        db.commit()
        db.refresh(db_strategy)
    return db_strategy


def delete_strategy(db: Session, strategy_id: int):
    db_strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    if db_strategy:
        db.delete(db_strategy)
        db.commit()
    return db_strategy
