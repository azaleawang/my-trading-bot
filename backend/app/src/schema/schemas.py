from uuid import UUID
from typing import Any, List, Union
from datetime import datetime

from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    user_id: int


class TokenPayload(BaseModel):
    username: str
    email: str
    exp: int = None


# User schema
class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserPublic(UserBase):
    id: int

    class Config:
        from_attributes = True

# Bot schema


class BotBase(BaseModel):
    # container_id: str
    # container_name
    name: str = "cool_bot"
    owner_id: int
    strategy: str = "supertrend"
    symbol: str = "ETH/USDT"
    description: Union[str, None] = None
    created_at: datetime
    t_frame: str = "1d"
    quantity: float = 0.1
    # status: str = 'running'


class BotCreate(BotBase):
    # owner_id: int
    container_id: str
    container_name: str
    status: str = "running"


# Backtest_result schema
class BacktestResultBase(BaseModel):
    info: dict
    result: Any


# 就是一般的message 回應格式
class Message_Resp(BaseModel):
    message: str = "some message"


class TradeHistoryCreate(BaseModel):
    container_name: str = "User1_supertrend_cool_bot"
    action: str = "buy"
    data: dict = {
        "orderId": "1211943298",
        "symbol": "ETHUSDT",
        "status": "FILLED",
        "clientOrderId": "x-xcKtGhcue8a91b792898fa6e749e21",
        "price": "0.00",
        "avgPrice": "2052.43000",
        "origQty": "0.100",
        "executedQty": "0.100",
        "cumQty": "0.100",
        "cumQuote": "205.24300",
        "timeInForce": "GTC",
        "type": "MARKET",
        "reduceOnly": False,
        "closePosition": False,
        "side": "BUY",
        "positionSide": "BOTH",
        "stopPrice": "0.00",
        "workingType": "CONTRACT_PRICE",
        "priceProtect": False,
        "origType": "MARKET",
        "priceMatch": "NONE",
        "selfTradePreventionMode": "NONE",
        "goodTillDate": "0",
        "updateTime": "1701054107239",
    }


class TradeHistory_Resp(BaseModel):
    id: int = 5
    container_name: str = "User1_supertrend_cool_bot"
    order_id: int
    qty: float = 0.1
    action: str = "buy"
    avg_price: float = 2052.43
    realizedPnl: Union[float, None]
    info: dict = {
        "orderId": "1211943298",
        "symbol": "ETHUSDT",
        "status": "FILLED",
        "clientOrderId": "x-xcKtGhcue8a91b792898fa6e749e21",
        "price": "0.00",
        "avgPrice": "2052.43000",
        "origQty": "0.100",
        "executedQty": "0.100",
        "cumQty": "0.100",
        "cumQuote": "205.24300",
        "timeInForce": "GTC",
        "type": "MARKET",
        "reduceOnly": False,
        "closePosition": False,
        "side": "BUY",
        "positionSide": "BOTH",
        "stopPrice": "0.00",
        "workingType": "CONTRACT_PRICE",
        "priceProtect": False,
        "origType": "MARKET",
        "priceMatch": "NONE",
        "selfTradePreventionMode": "NONE",
        "goodTillDate": "0",
        "updateTime": "1701054107239",
    }
    timestamp: int = 1701071929040


class Bot(BotCreate):
    id: int
    trade_history: List[TradeHistory_Resp]

    class Config:
        from_attributes = True


# req body of posting backtest
class Backtest_Strategy(BaseModel):
    name: str = "MaRsi"
    symbols: list = ["BTC/USDT"]
    t_frame: str = "1h"
    since: Union[str, None] = "2017-01-01T00:00:00Z"
    default_type: Union[str, None] = "future"
    params: Union[dict, None] = {"rsi_window": 20}


class StrategyCreate(BaseModel):
    name: str
    file_url: Union[str, None]
    params: Union[dict, None]
    provider_id: int
    is_public: bool


class Strategy(StrategyCreate):
    id: int

    class Config:
        from_attributes = True


class BotErrorSchema(BaseModel):
    container_name: str
    error: str


class BotError(BotErrorSchema):
    id: int
    timestamp: Any

    class Config:
        from_attributes = True


class ContainerState(BaseModel):
    bot_id: int
    container_id: str
    container_name: str
    state: str
    status: str
    running_for: str
    logs: list
    updated_at: Any


class ContainerStateDict(BaseModel):
    data: List[ContainerState]


class LoginForm(BaseModel):
    email: str
    password: str
