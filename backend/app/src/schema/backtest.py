from typing import Any, Union
from pydantic import BaseModel


class BacktestResultBase(BaseModel):
    info: dict
    result: Any


class BacktestStrategy(BaseModel):
    name: str = "MaRsi"
    symbols: list = ["BTC/USDT"]
    t_frame: str = "1h"
    since: Union[str, None] = "2017-01-01T00:00:00Z"
    default_type: Union[str, None] = "future"
    params: Union[dict, None] = {"rsi_window": 20}
    user_id: int = 1
