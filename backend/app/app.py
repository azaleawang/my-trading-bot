"""Module providing a function of FastAPI and WebSocket."""
from app.crud.trade_history import create_trade_history
from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.src.schema.schemas import TradeHistoryCreate
from .routers import backtests, users, bots, strategies
from .src.models import Base
from .src.config.database import SessionLocal, engine, get_db
from starlette.websockets import WebSocketDisconnect
from typing import List
import logging
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()
API_VER = "v1"
app.include_router(users.router, prefix=f"/api/{API_VER}/users", tags=["User"])
app.include_router(bots.router, prefix=f"/api/{API_VER}/bots", tags=["Bot"])
app.include_router(
    backtests.router, prefix=f"/api/{API_VER}/backtests", tags=["Backtest"]
)
app.include_router(
    strategies.router, prefix=f"/api/{API_VER}/strategies", tags=["Strategy"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["ROOT"])
def get_root() -> dict:
    return {"Hello": "World"}

@app.post("/trade-history")
def create_trade_history_endpoint(trade_data: TradeHistoryCreate, db: Session = Depends(get_db)):
    try:
        return create_trade_history(db, trade_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_json()
#             await websocket.send_json("Message received")
#             print(f"Message received: {data.get('action')}")
            
#     except WebSocketDisconnect:
#         print("Client disconnected")


@app.websocket("/ws/trade_history")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            await websocket.send_json("Message received")
            
            # check if the trading action message
            if data.get("action"):
                # store trade info into database
                try:
                    print("data", data)
                    trade_data = TradeHistoryCreate(**data)
                    db = SessionLocal()
                    db_trade_history = create_trade_history(db, trade_data)
                    print("store: ",  db_trade_history)
                except Exception as e:
                    print(f"Error: {e}")
                finally:
                    db.close()
    except WebSocketDisconnect:
        print("Client disconnected")


active_connections: List[WebSocket] = []


@app.websocket("/ws/backtest_result")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            # Replace this with your logic to fetch or generate data
            data = await websocket.receive_json()
            print(f"Message received: {data}")
            # await websocket.send_json("Message received")
            await broadcast(data)
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print("Client disconnected")


async def broadcast(message: dict):
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except WebSocketDisconnect as wsd:
            # Handle disconnect during broadcast if needed
            logging.error("Client disconnected during broadcast: %s", wsd)
