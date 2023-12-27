from typing import List, Union, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime
import re

from app.exceptions.bot import BotNameInvalid

class BotBase(BaseModel):
    name: str = Field("cool_bot", min_length=3, max_length=20)
    owner_id: int = 1
    strategy: str = "supertrend"
    symbol: str = "ETH/USDT"
    description: Union[str, None] = None
    t_frame: str = "1d"
    quantity: float = 110
    
    @validator('name')
    def remove_spaces(cls, v):
        return v.replace(' ', '')
    
    @validator('name')
    def validate_name(cls, v):
        name_regex = re.compile(r"^[A-Za-z-_1234567890]+$")
        match = name_regex.match(v)
        if not match:
            raise BotNameInvalid()
        return v


class BotCreate(BotBase):
    container_id: str
    container_name: str
    status: str = "running"
    worker_instance_id: str


class BotCreateResp(BaseModel):
    data: List[BotCreate]


class BotCheck(BaseModel):
    container_id: str
    container_name: str
    status: str = "running"


class BotCheckResp(BaseModel):
    data: List[BotCheck]


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


class TradeHistoryResp(BaseModel):
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
    created_at: datetime
    stopped_at: Any
    trade_history: List[TradeHistoryResp]

    class Config:
        from_attributes = True


class BotCreatedResp(BaseModel):
    data: Bot


class BotResp(BaseModel):
    data: List[Bot]


class BotHistoryResp(BaseModel):
    data: List[TradeHistoryResp]


class BotError(BaseModel):
    container_name: str
    error: str


class BotError(BotError):
    id: int
    timestamp: Any

    class Config:
        from_attributes = True


class PnlChart(BaseModel):
    data: list = [
        {"pnl": -4.83644, "timestamp": 1702080000000},
        {"pnl": -6.04348, "timestamp": 1702111500000},
    ]


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


class ContainerStatusResp(BaseModel):
    container_id: str
    container_name: str
    state: str = "exited"
    status: str = "Exited (137) 39 hours ago"
    RunningFor: str = "39 hours ago"


class ContainerInfoDict(BaseModel):
    data: list = [
        {"container_id": "123123123123", "state": [{}], "log": ["log1", "log2"]}
    ]


class ContainerLogResp(BaseModel):
    container_id: str
    container_name: str
    logs: list = [
        "20231130-180805: Checking for buy and sell signals",
        "20231130-180905: symbol: BNB/USDT, timeframe: 30m, limit: 100, in_position: True, quantity_buy_sell: 0.1",
    ]
