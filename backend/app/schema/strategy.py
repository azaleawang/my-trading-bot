from typing import Union
from pydantic import BaseModel


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
