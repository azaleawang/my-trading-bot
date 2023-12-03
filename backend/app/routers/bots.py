import logging
from typing import List, Union, Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.src.controller.bot import start_bot_container
from app.crud.bot import (
    check_name,
    create_user_bot,
    delete_user_bot,
    get_bots,
    get_user_bots,
    stop_user_bot,
)
from app.src.schema import schemas
from app.src.config.database import get_db
from app.crud.trade_history import get_bot_trade_history
from app.crud.bot_error import get_error_log_by_container
from app.crud.container_status import get_container_status, get_user_containers_status, parse_and_store

router = APIRouter()


class Bot_Resp(BaseModel):
    data: List[schemas.Bot]


class Bot_Created_Resp(BaseModel):
    data: schemas.Bot


class Bot_History_Resp(BaseModel):
    data: List[schemas.TradeHistory_Resp]

class BotCreate_Resp(BaseModel):
    data: List[schemas.BotCreate]

@router.get("/", response_model=BotCreate_Resp)
def get_all_bots(db: Session = Depends(get_db)):
    try:
        db_all_bots = get_bots(db)
        return {"data": db_all_bots}
    except Exception as e:
        logging.error(f"Error in get_all_bots: {e}")
        raise HTTPException(status_code=500, detail="Error fetching bots." + str(e))


@router.get("/users/{user_id}/bots")
def get_bot_details_for_user(user_id: int, db: Session = Depends(get_db)):
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


@router.get(
    "/users/{user_id}/bots/{bot_id}/trade-history/", response_model=Bot_History_Resp
)
def read_bot_trade_history(user_id: int, bot_id: int, db: Session = Depends(get_db)):
    db_bot_history = get_bot_trade_history(db, user_id, bot_id)
    if db_bot_history is None:
        raise HTTPException(status_code=404, detail="Trading bot not found")
    return {"data": db_bot_history}


@router.get(
    "/users/{user_id}/bots/{bot_id}/bot-error/", response_model=List[schemas.BotError]
)
def read_bot_error_for_user(user_id: int, bot_id: int, db: Session = Depends(get_db)):
    try:
        db_bot_error = get_error_log_by_container(bot_id, db)
        return db_bot_error
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching error log." + str(e))

class ContainerStatus_Resp(BaseModel):
    container_id: str
    container_name: str
    state: str = "exited"
    status: str = "Exited (137) 39 hours ago"
    RunningFor: str = "39 hours ago"


class ContainerLog_Resp(BaseModel):
    container_id: str
    container_name: str
    logs: list = [
        "20231130-180805: Checking for buy and sell signals",
        "20231130-180905: symbol: BNB/USDT, timeframe: 30m, limit: 100, in_position: True, quantity_buy_sell: 0.1",
    ]


class ContainerInfoDict(BaseModel):
    data: list = [
        {"container_id": "123123123123", "state": [{}], "log": ["log1", "log2"]}
    ]


@router.post("/container-monitoring/")
def receive_and_store_container_monitoring_info(data: ContainerInfoDict):
    try:  # TODO store the data into database
        parse_and_store(container_data=data.data)
        return {"message": "Data from docker-monitoring worker received successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class ContainerStateDict(BaseModel):
    data: List[schemas.ContainerState]
    
@router.get("/users/{user_id}/bots/container-monitoring/", response_model=ContainerStateDict)
def get_container_monitoring_info(user_id: int, db: Session = Depends(get_db)):
        try:
            # get data from db
            containers_info = get_user_containers_status(db, user_id)
            return {"data": containers_info}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
@router.get("/users/{user_id}/bots/{bot_id}/container-monitoring/", response_model=ContainerStateDict)
def get_container_monitoring_logs(bot_id: int, db: Session = Depends(get_db)):
        try:
            # get data from db
            container_info = get_container_status(db, bot_id)
            return {"data": container_info}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))