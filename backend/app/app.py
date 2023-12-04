"""Module providing a function of FastAPI and WebSocket."""
from app.crud.trade_history import create_trade_history
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Request,
    WebSocket,
    WebSocketDisconnect,
    status,
    Response,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.src.schema.schemas import (
    BotErrorSchema,
    LoginForm,
    TokenSchema,
    TradeHistoryCreate,
)
from app.src.controller.trade import get_order_realizedPnl
from app.src.schema import schemas
from app.crud.bot_error import create_error_log
from app.crud.user import create_user, get_user_by_email
from app.utils.deps import get_current_user
from .routers import backtests, users, bots, strategies
from app.models import Base
from .src.config.database import SessionLocal, engine, get_db
from starlette.websockets import WebSocketDisconnect
from typing import List
import logging
from sqlalchemy.orm import Session
from starlette.responses import FileResponse
import os
from app.utils.auth import (
    verify_password,
    create_access_token,
    create_refresh_token,
)

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


@app.get("/me", summary="Get details of currently logged in user")
async def get_me(user: schemas.User = Depends(get_current_user)):
    return user


@app.post("/signup", response_model=schemas.User)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return create_user(db=db, user=user)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e) or "Something broke when creating user!",
        )


@app.post(
    "/login",
    summary="Create access and refresh tokens for user",
    response_model=TokenSchema,
)
async def login(
    response: Response, form_data: LoginForm, db: Session = Depends(get_db)
):
    try:
        user = get_user_by_email(db, form_data.email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password",
            )

        print("user want to login", user.name, user.email)
        hashed_pass = user.hashed_password
        if not verify_password(form_data.password, hashed_pass):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password",
            )

        access_token = create_access_token(username=user.name, email=user.email)
        refresh_token = create_refresh_token(username=user.name, email=user.email)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user.id
        }
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e) or "Something broke when login or creating JWT token!",
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
