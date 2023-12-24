from sqlalchemy.orm import Session
from app.schema import worker as schemas
from app.models.worker_server import WorkerServer


def register_worker_server(db: Session, worker_server: schemas.WorkerServerCreate):
    # update if existed
    db_worker_server = (
        db.query(WorkerServer)
        .filter(WorkerServer.instance_id == worker_server.instance_id)
        .first()
    )
    if db_worker_server:
        db_worker_server.private_ip = worker_server.private_ip
        db_worker_server.total_memory = worker_server.total_memory
        db_worker_server.status = "running"
        db.commit()

        return db_worker_server

    # else, create new record
    db_worker_server = WorkerServer(
        instance_id=worker_server.instance_id,
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
