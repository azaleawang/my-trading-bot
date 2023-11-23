from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import subprocess
import traceback
import logging
from .src.controller.sqs import send_message
from time import gmtime, strftime
import json

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


class Bot_Run_Info(BaseModel):
    user_id: Union[str, int] = 1
    script_name: str = "supertrend"


class Bot_Stop_Info(BaseModel):
    user_id: Union[str, int] = 1
    container_id: Union[str, None]
    container_name: str


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

# get
@app.post("/api/backtest", tags=["backtest"])
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


@app.post("/api/backtest/result", tags=["backtest"])
async def receive_lambda_result(data: dict = {"info": {}, "result": "{'json': 'need to parse'}"}):
    try:
        logging.info(f"Received data from Lambda: {data}")
        # TODO: Process the result as needed: use graphql or ws to inform client testing result
        parsed_result = json.loads(data.get('result'), parse_float=lambda x: None if x == 'NaN' else float(x))
        if(parsed_result.get("plot")):
            parsed_result["plot"] = os.getenv("S3_URL") + parsed_result["plot"]
        
        # store result into database or redis
        # notify frontend to fetch new data or refresh page
        
        return {"message": "Data received successfully", "result": parsed_result} # print to examine the format pls del when deployment
    except Exception as e:
        logging.error(f"Error in receive_lambda_result: {e}")
        raise HTTPException(status_code=500, detail="Error processing received data.")


@app.post("/api/bots", tags=["trade"])
def start_trading_bot(bot_info: Bot_Run_Info) -> dict:
    try:
        # load the bot script from ??? the better design may be downloading from s3
        container_name = (
            f"User{bot_info.user_id}_{bot_info.script_name}_{strftime('%m%d%H%M%S', gmtime())}"
        )
        command = [
            "docker",
            "run",
            "-d",
            "--name",
            container_name,
            "-v",
            "/home/leah/my-trading-bot/trade/supertrend:/app",
            "py-tradingbot",
            "python",
            "-u",
            f"./{bot_info.script_name}.py",
        ]
        # Run the command and capture the output
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # The stdout will contain the container ID
        container_id = result.stdout.strip()
        # store information into db!
        return {
            "message": "Trading bot started",
            "container_id": container_id,
            "container_name": container_name,
        }

    except subprocess.CalledProcessError as e:
        # Capture and return any errors
        error_message = e.stderr or str(e)
        raise HTTPException(status_code=500, detail=error_message)
    # try:
    #     # TODO add trading-bot id and save to db
    #     process = subprocess.Popen(
    #         ["nohup", "python", "trade/supertrend/supertrend.py"]
    #     )
    #     return {"message": f"Trading bot {process.pid} started running"}
    # except Exception as e:
    #     # Handle the exception
    #     raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/bots/{bot_id}", tags=["trade"])
def stop_trading_bot(bot_name: str) -> dict:
    container = bot_name
    command = ["docker", "stop", container]
    try:
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return {"message": f"User{bot_info.user_id}'s bot {container} stopped!"}
    except subprocess.CalledProcessError as e:
        print(f"Error stopping container: {e.stderr}")
        return {"message": e.stderr}
    # try:
    #     os.kill(int(bot_id), 0)
    # except OSError:
    #     raise HTTPException(status_code=404, detail="Process not found")
    # try:
    #     subprocess.run(["kill", str(bot_id)], check=True)
    #     return {"message": f"Process with PID {bot_id} has been terminated"}
    # except subprocess.CalledProcessError:
    #     raise HTTPException(status_code=500, detail="Failed to terminate process")


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
