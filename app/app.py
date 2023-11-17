from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
# import subprocess
import traceback
import logging
from .src.controller.sqs import send_message
app = FastAPI()
SQS_URL = "https://sqs.ap-northeast-1.amazonaws.com/958720635143/lambda-queue"

class Backtest_Strategy(BaseModel):
    name: str = "default_strategy"
    symbols: list = ['BTC/USDT']
    t_frame: str = '1h'
    since: Union[str, None] = '2017-01-01T00:00:00Z'
    default_type: Union[str, None] = 'future'


@app.get("/", tags=['ROOT'])
def get_root() -> dict:
    return {"Hello": "World"}

@app.post("/api/backtest", tags=['backtest'])
def run_backtest(strategy: Backtest_Strategy)-> dict:
    
    try:
        print(f"strategy post: {strategy}")
        # this is sync function (blocking) 
        # TODO
        # 從DB中找到策略的位置
        # 取得策略ID？
        # subprocess.run(["python", "backtest/backetsting-crypto.py"], check=True)
        # send message into SQS queue
        # print(strategy.model_dump_json())
        # need to fix strategy.model_dump_json()讀到的格式錯誤的問題
        response = send_message(SQS_URL, {"name":"default_strategy","symbols":["BTC/USDT"],"t_frame":"1h","since":"2017-01-01T00:00:00Z","default_type":"future"})
        # return {"data": "stat"}
        return {"message": f"Backtesting '{strategy}' job push into SQS message id {response.get('MessageId')} successfully."}
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
        # raise HTTPException(status_code=500, detail="Error occurred while executing the backtesting script.")

@app.post("/api/backtest/result", tags=['backtest'])
async def receive_lambda_result(result: dict= {"data": "test"}):
    try:
        logging.info(f"Received data from Lambda: {result}")
        # TODO: Process the result as needed

        return {"message": "Data received successfully"}
    except Exception as e:
        logging.error(f"Error in receive_lambda_result: {e}")
        raise HTTPException(status_code=500, detail="Error processing received data.")


# for learning notes
class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/items/{item_id}")
def get_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.get("/todo", tags=['todos'])
async def get_todos() -> dict:
    return {
        "data": todos
    }

@app.post("/todo", tags=['todos'])
async def add_todo(todo: dict) -> dict:
    todos.append(todo)
    return {
        "data": "Add todo done!"
    }

@app.put("/todo/{id}", tags=['todos'])
async def update_todo(id: int, body: dict) -> dict:
    for todo in todos:
        if int(todo["id"]) == id:
            todo["description"] = body["description"]
            return {
                "data": f"Todo with id {id} has been updated"
            }
    return {
        "data": f"Todo with id {id} not found"
    }

@app.delete("/todo/{id}", tags=['todos'])
async def delete_todo(id: int) -> dict:
    for todo in todos: 
        if int(todo["id"] == id):
            todos.remove(todo)
            return {
                "data": f"Todo with id {id} has been deleted"
            }
    return {
        "data": f"Todo with id {id} not found"
    }
    

todos = [
    {
        "id": 1,
        "title": "First Todo",
        "description": "This is my first todo"
    },
    {
        "id": 2,
        "title": "Second Todo",
        "description": "This is my second todo"
    }
]