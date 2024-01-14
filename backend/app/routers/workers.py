from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.schema.worker import WorkerServerRead, WorkerServerCreate
from app.utils.database import get_db
from app.crud.worker_server import register_worker_server, get_worker_servers
import os

router = APIRouter()


@router.post("/", response_model=WorkerServerRead)
def create_worker_server(worker_server: WorkerServerCreate, db: Session = Depends(get_db), Auth: Union[str, None] = Header(default=None)):
    # If the header is empty, raise HTTPException
    if Auth != os.getenv("WORKER_SERVER_AUTH"):
        raise HTTPException(status_code=403, detail="You are not authorized to access this resource")
    return register_worker_server(db, worker_server)

