from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, Query, HTTPException
import subprocess

app = FastAPI()

@app.get("/", tags=['ROOT'])
def get_root() -> dict:
    return {"Hello": "World"}

@app.get("/api/run-backtest", tags=['backtest'])
async def run_backtest(strategy: str = "default_strategy"):
    try:
        # this is sync function (blocking)
        subprocess.run(["python", "backtest/backetsting-crypto.py"], check=True)
        return {"message": f"Backtesting script for strategy '{strategy}' executed successfully."}
    except:
        raise HTTPException(status_code=500, detail="Error occurred while executing the backtesting script.")


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