import logging
from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.crud.strategy import get_user_strategies
from app.src.schema import schemas
from app.src.config.database import get_db

router = APIRouter()

class Strategy_Resp(BaseModel):
    data: List[schemas.Strategy]
    
@router.get("/users/{user_id}/strategies", response_model=Strategy_Resp)
def read_strategies_for_user(user_id: int, db: Session = Depends(get_db)):
    # get public and personal strategies
    try:
        db_strategies = get_user_strategies(user_id = user_id, db = db)
        return {
            "data": db_strategies,
        }
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        logging.error(f"Error in get_bot_for_user: {e}")
        raise HTTPException(status_code=500, detail="Error fetching bots." + str(e))
