from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.src.schema import schemas
from app.src.config.database import get_db
from app.crud.worker_server import register_worker_server, get_worker_servers
import os

router = APIRouter()


@router.post("/", response_model=schemas.WorkerServerRead)
def create_worker_server(worker_server: schemas.WorkerServerCreate, db: Session = Depends(get_db), Auth: Union[str, None] = Header(default=None)):
    # Read the header X-Auth
    # If the header is empty, raise HTTPException
    if Auth != os.getenv("WORKER_SERVER_AUTH"):
        raise HTTPException(status_code=403, detail="You are not authorized to access this resource")
    # If the header is not empty, check the token
    return register_worker_server(db, worker_server)


@router.get("/", response_model=List[schemas.WorkerServerRead])
def read_all_worker_servers(db: Session = Depends(get_db)):
    db_worker_server = get_worker_servers(db)
    if db_worker_server is None:
        raise HTTPException(status_code=404, detail="WorkerServer not found")
    return db_worker_server
