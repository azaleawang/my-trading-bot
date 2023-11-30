import logging
from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.crud.strategy import *
from app.src.schema import schemas
from app.src.config.database import get_db

router = APIRouter()


class Strategy_Resp(BaseModel):
    data: List[schemas.Strategy]


# @router.get("/users/{user_id}/strategies/", response_model=Strategy_Resp)
# def read_strategies_for_user(user_id: int, db: Session = Depends(get_db)):
#     # get public and personal strategies
#     try:
#         db_strategies = get_user_strategies(user_id=user_id, db=db)
#         return {
#             "data": db_strategies,
#         }
#     except HTTPException as http_ex:
#         raise http_ex
#     except Exception as e:
#         logging.error(f"Error in get_bot_for_user: {e}")
#         raise HTTPException(status_code=500, detail="Error fetching bots." + str(e))


@router.get("/", response_model=List[schemas.Strategy])
def read_strategy_for_user(
    user_id: int, db: Session = Depends(get_db)
):
    db_strategy = get_user_all_strategies(db, user_id)
    # db_strategy = get_strategy(db, strategy_id)
    if db_strategy is None:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return db_strategy


@router.post("/", response_model=schemas.Strategy)
def create_strategy(
    strategy_create: schemas.StrategyCreate, db: Session = Depends(get_db)
):
    return insert_strategy(db, strategy_create)


@router.put("/{strategy_id}", response_model=schemas.Strategy)
def update_strategy_by_id(
    strategy_id: int,
    strategy_update: schemas.StrategyCreate,
    db: Session = Depends(get_db),
):
    return update_strategy(db, strategy_id, strategy_update)


@router.delete("/{strategy_id}", response_model=schemas.Strategy)
def delete_strategy_by_id(strategy_id: int, db: Session = Depends(get_db)):
    return delete_strategy(db, strategy_id)
