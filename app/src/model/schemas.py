from typing import List, Union
from datetime import datetime

from pydantic import BaseModel

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