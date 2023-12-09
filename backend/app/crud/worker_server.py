from sqlalchemy.orm import Session
from app.src.schema import schemas
from app.models.worker_server import WorkerServer


def register_worker_server(db: Session, worker_server: schemas.WorkerServerCreate):
    db_worker_server = WorkerServer(
        private_ip=worker_server.private_ip,
        total_memory=worker_server.total_memory,
        available_memory=worker_server.total_memory,
    )
    db.add(db_worker_server)
    db.commit()
    db.refresh(db_worker_server)
    return db_worker_server

def get_worker_servers(db: Session):
    return db.query(WorkerServer).all()