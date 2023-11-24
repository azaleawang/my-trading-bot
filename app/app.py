"""Module providing a function of FastAPI and WebSocket."""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .routers import backtests, users, bots
from .src.models import Base
from .src.config.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
API_VER = "v1"
app.include_router(users.router, prefix=f"/api/{API_VER}/users", tags=["User"])
app.include_router(bots.router, prefix=f"/api/{API_VER}/bots", tags=["Bot"])
app.include_router(
    backtests.router, prefix=f"/api/{API_VER}/backtests", tags=["Backtest"]
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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            await websocket.send_json("Message received")
            print(f"Message received: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
