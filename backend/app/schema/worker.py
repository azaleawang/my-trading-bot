from typing import Any, Union
from pydantic import BaseModel

class WorkerServerCreate(BaseModel):
    instance_id: str
    private_ip: str
    total_memory: int = 550


class WorkerServerRead(WorkerServerCreate):
    id: int
    private_ip: Union[str, None]
    available_memory: int
    status: str
    updated_at: Any

    class Config:
        from_attributes = True
