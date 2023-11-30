from app.src.models import Strategy
from sqlalchemy.orm import Session
from app.src.schema import schemas
from sqlalchemy import or_


# Read
# def get_specific_user_strategy(db: Session, user_id: int, strategy_id: int):
#     db_strategy = (
#         db.query(Strategy)
#         .filter(Strategy.id == strategy_id, Strategy.provider_id == user_id)
#         .first()
#     )
#     return db_strategy


def get_user_all_strategies(db: Session, user_id: int):
    return (
        db.query(Strategy)
        .filter(or_(Strategy.is_public, Strategy.provider_id == user_id))
        .all()
    )

def get_strategy(db: Session, strategy_id: int):
    return db.query(Strategy).filter(Strategy.id == strategy_id).first()


# Create
def insert_strategy(db: Session, strategy_create: schemas.StrategyCreate):
    db_strategy = Strategy(**strategy_create.model_dump())
    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)
    return db_strategy


# Update
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


# Delete
def delete_strategy(db: Session, strategy_id: int):
    db_strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    if db_strategy:
        db.delete(db_strategy)
        db.commit()
    return db_strategy
