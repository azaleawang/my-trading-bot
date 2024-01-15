"""Module providing a function of FastAPI and WebSocket."""
from fastapi.responses import JSONResponse
from app.crud.trade_history import create_trade_history
from fastapi import (
    FastAPI,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.schema import bot as schemas
from app.utils.trade import get_order_realizedPnl
from app.crud.bot_error import create_error_log
from .routers import backtests, users, bots, strategies, workers
from app.models import Base
from .utils.database import SessionLocal, engine
from starlette.websockets import WebSocketDisconnect
from typing import Any, Dict, List
from starlette.responses import FileResponse
from .config import app_configs, API_VER
import os
from contextlib import asynccontextmanager
from app.utils.redis import get_redis_client
from app.utils.logger import logger
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, "../dist")
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # startup
        app.state.redis = await get_redis_client()
        yield
        # shutdown
        await app.state.redis.close()
    except Exception as e:
        logger.error(f"Redis connection error: {e}")


app = FastAPI(**app_configs, lifespan=lifespan)

routes = [
    (users.router, "users", "User"),
    (bots.router, "bots", "Bot"),
    (backtests.router, "backtests", "Backtest"),
    (strategies.router, "strategies", "Strategy"),
    (workers.router, "worker-servers", "Worker-Server"),
]

for router, path, tag in routes:
    app.include_router(router, prefix=f"/api/{API_VER}/{path}", tags=[tag])

app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500, content={"detail": "An unexpected error occurred!"}
    )


@app.get("/{full_path:path}")
async def serve_frontend(full_path: str, request: Request):
    # Check if the file exists in the static directory
    static_file_path = os.path.join(frontend_dir, full_path)
    if os.path.isfile(static_file_path):
        return FileResponse(static_file_path)
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
                        trade_data = schemas.TradeHistoryCreate(**data)

                        create_trade_history(db, trade_data, realizedPnl)
                        db.commit()
                except Exception as e:
                    logger.error(f"{e}")

            elif data.get("error"):
                try:
                    with SessionLocal() as db:
                        error_data = schemas.BotError(**data)
                        error = create_error_log(error_data, db)
                        db.commit()
                        logger.error(error)
                except Exception as e:
                    logger.error(f"Storing trading error logs failed: {e}")
            else:
                logger.info(f"Received message from trading-bot worker: {data}")

    except WebSocketDisconnect:
        pass


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, client_id: int, websocket: WebSocket):
        await websocket.accept()
        if client_id not in self.active_connections:
            self.active_connections[client_id] = []
        self.active_connections[client_id].append(websocket)

    def disconnect(self, client_id: int, websocket: WebSocket):
        if websocket in self.active_connections.get(client_id):
            self.active_connections[client_id].remove(websocket)
            if not self.active_connections.get(client_id):
                # If the list is empty, remove the client_id from the dictionary
                del self.active_connections[client_id]

    async def send_personal_message(self, message: Any, client_id: int):
        for websocket in self.active_connections.get(client_id):
            await websocket.send_json(message)


manager = ConnectionManager()

@app.websocket("/ws/backtest_result/{client_id}")
async def websocket_backtest_result_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(client_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.send_personal_message(data, client_id)
    except WebSocketDisconnect:
        manager.disconnect(client_id, websocket)
