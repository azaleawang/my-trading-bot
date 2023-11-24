from typing import Union, List
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import APIRouter
import os
import traceback
import logging

from app.src.crud.user import get_user, get_user_by_email, get_users, create_user
from .src.schema import schemas

from .src.crud.bot import check_container_name, create_user_bot, delete_user_bot, get_user_bots, stop_user_bot
from .src.controller.sqs import send_message
import json
from .src.models import Base
from .src.config.database import engine
from sqlalchemy.orm import Session
from .src.controller.bot import start_bot_container
from .src.config.database import get_db


Base.metadata.create_all(bind=engine)

app = FastAPI()
router = APIRouter()

# API_VER = "v1"
# app.include_router(users.router, prefix="/users", tags=["Users"]) 
# app.include_router(items.router, prefix="/items", tags=["Items"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class Backtest_Strategy(BaseModel):
    name: str = "MaRsi"
    symbols: list = ["BTC/USDT"]
    t_frame: str = "1h"
    since: Union[str, None] = "2017-01-01T00:00:00Z"
    default_type: Union[str, None] = "future"
    params: Union[dict, None] = {"rsi_window": 20}


class Bot_Created_Resp(BaseModel):
    data: Union[schemas.Bot, List[schemas.Bot]]


@app.get("/", tags=["ROOT"])
def get_root() -> dict:
    return {"Hello": "World"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            await websocket.send_json(f"Message received")
            print(f"Message received: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")


@app.post("/api/backtest", tags=["Backtest"])
def run_backtest(strategy: Backtest_Strategy) -> dict:
    try:
        # TODO
        # 從DB中找到策略的位置
        # 取得策略ID？
        # send message into SQS queue
        strategy_config = {"s3_url": os.getenv("S3_BACKTEST_STRATEGY_URL")}
        message_body = dict(**strategy.model_dump(), **strategy_config)

        response = send_message(message_body=message_body)
        # response = {}
        if "error" in response:
            print("Error occurred:", response.get("details"))
            return JSONResponse(
                content={
                    "message": f"Backtesting job push into SQS failed. {response.get('details')}"
                },
                status_code=500,
            )
        else:
            return {
                "message": f"Backtesting '{strategy}' job push into SQS id {response.get('MessageId')}."
            }

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/backtest/result", tags=["Backtest"])
async def receive_lambda_result(
    data: dict = {"info": {}, "result": "{'json': 'need to parse'}"}
):
    try:
        logging.info(f"Received data from Lambda: {data}")
        # TODO: Process the result as needed: use graphql or ws to inform client testing result
        parsed_result = json.loads(
            data.get("result"), parse_float=lambda x: None if x == "NaN" else float(x)
        )
        if parsed_result.get("plot"):
            parsed_result["plot"] = os.getenv("S3_URL") + parsed_result["plot"]

        # store result into database or redis
        # notify frontend to fetch new data or refresh page

        return {
            "message": "Data received successfully",
            "result": parsed_result,
        }  # print to examine the format pls del when deployment
    except Exception as e:
        logging.error(f"Error in receive_lambda_result: {e}")
        raise HTTPException(status_code=500, detail="Error processing received data.")

@router.get("/router1")

@app.get("/api/users/{user_id}/bots", response_model=Bot_Created_Resp, tags=["Bot"])
def get_bot_for_user(user_id: int, db: Session = Depends(get_db)):
    try:
        db_bot = get_user_bots(user_id = user_id, db = db)

        return {
            "data": db_bot,
        }
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        logging.error(f"Error in get_bot_for_user: {e}")
        raise HTTPException(status_code=500, detail="Error fetching bots." + str(e))


@app.post("/api/users/{user_id}/bots", response_model=Bot_Created_Resp, tags=["Bot"])
def create_bot_for_user(
    user_id: int, bot: schemas.BotBase, db: Session = Depends(get_db)
):
    try:
        container_name = f"User{user_id}_{bot.strategy}_{bot.name}"
        if check_container_name(db, container_name):
            raise HTTPException(status_code=400, detail="Container name already exists.")
        
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



@app.put("/api/users/{user_id}/bots/{bot_id}", tags=["Bot"])
def stop_bot_for_user(user_id: int, bot_id: int, db: Session = Depends(get_db)) -> dict:
    try:
        user_bot = stop_user_bot(user_id, bot_id, db)        
        print(user_bot)
        
        return {"message": f"Bot #{bot_id} {user_bot.name} stopped!"}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error stopping bot." + str(e))
 
@app.delete("/api/users/{user_id}/bots/{bot_id}", tags=["Bot"])
def delete_bot_for_user(user_id: int, bot_id: int, db: Session = Depends(get_db)) -> dict:
    try:
        user_bot = delete_user_bot(user_id, bot_id, db)        
        
        return {"message": f"Bot #{bot_id} {user_bot.name} removed from Docker containers!"}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error stopping bot." + str(e))
  
  
# for learning
@app.post("/users", response_model=schemas.User, tags=["User"])
def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)


@app.get("/users", response_model=List[schemas.User], tags=["User"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User, tags=["User"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
