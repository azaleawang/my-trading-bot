from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import subprocess
import traceback
import logging
from .src.controller.sqs import send_message

app = FastAPI()

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


@app.get("/", tags=["ROOT"])
def get_root() -> dict:
    return {"Hello": "World"}


@app.post("/api/backtest", tags=["backtest"])
def run_backtest(strategy: Backtest_Strategy) -> dict:
    try:
        # TODO
        # 從DB中找到策略的位置
        # 取得策略ID？
        # send message into SQS queue
        strategy_config = {"s3_url": os.getenv("S3_BACKTEST_STRATEGY_URL")}
        message_body = dict(**strategy.model_dump(), **strategy_config)

        response = send_message(message_body = message_body)
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


@app.post("/api/backtest/result", tags=["backtest"])
async def receive_lambda_result(result: dict = {"data": "test"}):
    try:
        logging.info(f"Received data from Lambda: {result}")
        # TODO: Process the result as needed: use graphql or ws to inform client testing result

        return {"message": "Data received successfully"}
    except Exception as e:
        logging.error(f"Error in receive_lambda_result: {e}")
        raise HTTPException(status_code=500, detail="Error processing received data.")


@app.post("/api/user/{user_id}/trading-bot", tags=["trade"])
def start_trading_bot(
    user_id: Union[int, str] = 1, strategy: Backtest_Strategy = Backtest_Strategy()
) -> dict:
    try:
        # TODO add trading-bot id and save to db
        process = subprocess.Popen(
            ["nohup", "python", "trade/supertrend/supertrend.py"]
        )
        return {"message": f"Trading bot {process.pid} started running"}
    except Exception as e:
        # Handle the exception
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/user/{user_id}/trading-bot/stop", tags=["trade"])
def stop_trading_bot(user_id: Union[int, str], bot_id: int) -> dict:
    try:
        os.kill(int(bot_id), 0)
    except OSError:
        raise HTTPException(status_code=404, detail="Process not found")
    try:
        subprocess.run(["kill", str(bot_id)], check=True)
        return {"message": f"Process with PID {bot_id} has been terminated"}
    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="Failed to terminate process")


# # for learning notes
# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None

# @app.get("/items/{item_id}")
# def get_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}

# @app.get("/todo", tags=['todos'])
# async def get_todos() -> dict:
#     return {
#         "data": todos
#     }

# @app.post("/todo", tags=['todos'])
# async def add_todo(todo: dict) -> dict:
#     todos.append(todo)
#     return {
#         "data": "Add todo done!"
#     }

# @app.put("/todo/{id}", tags=['todos'])
# async def update_todo(id: int, body: dict) -> dict:
#     for todo in todos:
#         if int(todo["id"]) == id:
#             todo["description"] = body["description"]
#             return {
#                 "data": f"Todo with id {id} has been updated"
#             }
#     return {
#         "data": f"Todo with id {id} not found"
#     }

# @app.delete("/todo/{id}", tags=['todos'])
# async def delete_todo(id: int) -> dict:
#     for todo in todos:
#         if int(todo["id"] == id):
#             todos.remove(todo)
#             return {
#                 "data": f"Todo with id {id} has been deleted"
#             }
#     return {
#         "data": f"Todo with id {id} not found"
#     }


# todos = [
#     {
#         "id": 1,
#         "title": "First Todo",
#         "description": "This is my first todo"
#     },
#     {
#         "id": 2,
#         "title": "Second Todo",
#         "description": "This is my second todo"
#     }
# ]
