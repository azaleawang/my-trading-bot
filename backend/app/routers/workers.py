from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.src.schema import schemas
from app.src.config.database import get_db
from app.crud.worker_server import register_worker_server, get_worker_servers

router = APIRouter()


@router.post("/", response_model=schemas.WorkerServerRead)
def create_worker_server(worker_server: schemas.WorkerServerCreate, db: Session = Depends(get_db)):
    return register_worker_server(db, worker_server)


@router.get("/", response_model=List[schemas.WorkerServerRead])
def read_all_worker_servers(db: Session = Depends(get_db)):
    db_worker_server = get_worker_servers(db)
    if db_worker_server is None:
        raise HTTPException(status_code=404, detail="WorkerServer not found")
    return db_worker_server
