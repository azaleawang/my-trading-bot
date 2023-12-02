"""Module providing a function of FastAPI and WebSocket."""
from app.crud.trade_history import create_trade_history
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.src.schema.schemas import BotErrorSchema, TradeHistoryCreate
from app.src.controller.trade import get_order_realizedPnl
from app.models.bot_error import Bot_Error
from app.crud.bot_error import create_error_log
from .routers import backtests, users, bots, strategies
from app.models import Base
from .src.config.database import SessionLocal, engine, get_db
from starlette.websockets import WebSocketDisconnect
from typing import List
import logging
from sqlalchemy.orm import Session
from starlette.responses import FileResponse
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, "../dist")
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
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/{full_path:path}")
async def serve_frontend(full_path: str, request: Request):
    # Check if the file exists in the static directory
    static_file_path = os.path.join(frontend_dir, full_path)
    if os.path.isfile(static_file_path):
        return FileResponse(static_file_path)
    print(static_file_path)
    # Fallback to serving index.html for SPA routing
    index_file = os.path.join(frontend_dir, "index.html")
    return FileResponse(index_file)


@app.websocket("/ws/trade_history")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            await websocket.send_json("Message received")

            # check if the trading action message
            if data.get("action"):
                try:
                    with SessionLocal() as db:
                        realizedPnl = None
                        if data["data"]["side"] == "SELL":
                            # get the realized pnl
                            realizedPnl = get_order_realizedPnl(
                                data["data"]["orderId"], data["data"]["symbol"]
                            )
                        trade_data = TradeHistoryCreate(**data)

                        db_trade_history = create_trade_history(
                            db, trade_data, realizedPnl
                        )
                        db.commit()
                        print("store: ", db_trade_history)
                except Exception as e:
                    print(f"Error: {e}")

            elif data.get("error"):
                try:
                    print("error", data)
                    with SessionLocal() as db:
                        error_data = BotErrorSchema(**data)
                        error = create_error_log(error_data, db)
                        db.commit()
                        print("error: ", error)
                except Exception as e:
                    print(f"Error logging failed: {e}")
            else:
                print("message", data)

    except WebSocketDisconnect:
        print("Client disconnected")


# @app.websocket("/ws/trade_history")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_json()
#             await websocket.send_json("Message received")

#             # check if the trading action message
#             if data.get("action"):
#                 # store trade info into database
#                 try:
#                     db = SessionLocal()
#                     realizedPnl = None
#                     if data["data"]["side"] == 'SELL':
#                         # get the realized pnl
#                         realizedPnl = get_order_realizedPnl(data["data"]["orderId"], data["data"]["symbol"])
#                     trade_data = TradeHistoryCreate(**data)

#                     db_trade_history = create_trade_history(db, trade_data, realizedPnl)
#                     print("store: ",  db_trade_history)
#                 except Exception as e:
#                     print(f"Error: {e}")
#                 finally:
#                     db.close()
#             elif data.get('error'):
#                 print("Get error from container", data)
#                 # how to deal with the error message from trading container? store to db first?
#                 error = create_error_log(BotErrorSchema(**data), db)
#                 print("error: ", error)

#     except WebSocketDisconnect:
#         print("Client disconnected")




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


# TODO this should be casted to certain user rather than broadcast QQ
async def broadcast(message: dict):
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except WebSocketDisconnect as wsd:
            # Handle disconnect during broadcast if needed
            logging.error("Client disconnected during broadcast: %s", wsd)
