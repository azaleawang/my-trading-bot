from typing import Any, List, Union
from datetime import datetime

from pydantic import BaseModel, JsonValue

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
    
# Bot schema
    
class BotBase(BaseModel):
    # container_id: str
    # container_name
    name: str = 'cool_bot'
    # owner_id: int
    strategy: str = 'supertrend'
    description: Union[str, None] = None
    created_at: datetime
    # status: str = 'running'
    
class BotCreate(BotBase):
    owner_id: int
    container_id: str
    container_name: str
    status: str = 'running'

class Bot(BotCreate):
    id: int

    class Config:
        from_attributes = True
      
# Backtest_result schema  
class BacktestResultBase(BaseModel):
    info: dict = {"name": "MaRsi",}
    result: dict = {"Start": "2023-01-01 00:00:00",}

class Strategy(BaseModel):
    id: int
    name: str
    file_url: Union[str, None]
    provider_id: int
    is_public: bool
    
    
# 就是一般的message 回應格式
class Message_Resp(BaseModel):
    message: str  = "some message"