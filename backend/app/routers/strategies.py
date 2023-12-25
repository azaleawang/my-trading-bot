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
    if db_strategy is None:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return db_strategy
