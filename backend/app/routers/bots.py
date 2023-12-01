import logging
from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.src.controller.bot import start_bot_container
from app.crud.bot import (
    check_name,
    create_user_bot,
    delete_user_bot,
    get_user_bots,
    stop_user_bot,
)
from app.src.schema import schemas
from app.src.config.database import get_db
from app.crud.trade_history import get_bot_trade_history

router = APIRouter()


class Bot_Resp(BaseModel):
    data: List[schemas.Bot]


class Bot_Created_Resp(BaseModel):
    data: schemas.Bot

class Bot_History_Resp(BaseModel):
    data: List[schemas.TradeHistory_Resp]

@router.get("/users/{user_id}/bots")
def get_bot_for_user(user_id: int, db: Session = Depends(get_db)):
    try:
        db_bot = get_user_bots(user_id=user_id, db=db)

        return {
            "data": db_bot,
        }
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        logging.error(f"Error in get_bot_for_user: {e}")
        raise HTTPException(status_code=500, detail="Error fetching bots." + str(e))


@router.post("/users/{user_id}/bots", response_model=Bot_Created_Resp)
def create_bot_for_user(
    user_id: int, bot: schemas.BotBase, db: Session = Depends(get_db)
):
    try:
        container_name = f"User{user_id}_{bot.strategy}_{bot.name}"
        check_name(db, container_name, bot.name, user_id)
        bot_docker_info = start_bot_container(user_id, container_name, bot)
        # Convert Pydantic model to a dictionary
        bot_dict = bot.model_dump()

        bot_create = schemas.BotCreate(**bot_dict, **bot_docker_info)
        db_bot = create_user_bot(db, bot_create)
        return {
            "data": db_bot,
        }
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        logging.error(f"Error in create_bot_for_user: {e}")
        raise HTTPException(status_code=500, detail="Error creating bot." + str(e))


@router.put("/users/{user_id}/bots/{bot_id}")
def stop_bot_for_user(user_id: int, bot_id: int, db: Session = Depends(get_db)) -> dict:
    try:
        user_bot = stop_user_bot(user_id, bot_id, db)
        print(user_bot)

        return {"message": f"Bot #{bot_id} {user_bot.name} stopped!"}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error stopping bot." + str(e))


@router.delete("/users/{user_id}/bots/{bot_id}")
def delete_bot_for_user(
    user_id: int, bot_id: int, db: Session = Depends(get_db)
) -> dict:
    try:
        user_bot = delete_user_bot(user_id, bot_id, db)

        return {
            "message": f"Bot #{bot_id} {user_bot.name} removed from Docker containers!"
        }
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error stopping bot." + str(e))


@router.get("/users/{user_id}/bots/{bot_id}/trade-history", response_model=Bot_History_Resp)
def read_user(user_id: int, bot_id: int, db: Session = Depends(get_db)):
    db_bot_history = get_bot_trade_history(db, user_id, bot_id)
    if db_bot_history is None:
        raise HTTPException(status_code=404, detail="Trading bot not found")
    return {"data": db_bot_history}
