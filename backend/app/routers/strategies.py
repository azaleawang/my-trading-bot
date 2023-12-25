import logging
from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.crud.strategy import *
from app.schema import strategy as schemas
from app.utils.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Strategy])
def read_strategy_for_user(user_id: int, db: Session = Depends(get_db)):
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
