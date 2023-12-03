import json
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import Depends, HTTPException
from app.src.schema import schemas
from sqlalchemy.sql import and_
from app.models.container_status import ContainerStatus
from app.src.config.database import SessionLocal
from sqlalchemy.orm import Session


def get_bots(db: Session, container_id: str):
    container_status = (
        db.query(ContainerStatus)
        .filter(ContainerStatus.container_id == container_id)
        .first()
    )
    return container_status


def parse_and_store(container_data):
    db = SessionLocal()

    for container in container_data:
        try:
            container_id = container["container_id"]
            existing_record = (
                db.query(ContainerStatus)
                .filter(ContainerStatus.container_id == container_id)
                .first()
            )

            if existing_record:
                # Update the existing record
                update_container(existing_record, container)
            else:
                # Create a new record
                new_record = create_new_container_record(container)
                db.add(new_record)

            db.commit()  # Commit changes for each container
        except Exception as e:
            db.rollback()  # Rollback only affects the current container
            print(f"Error processing container {container_id}: {e}")

    db.close()


def update_container(existing_record, container):
    for st in container["state"]:
        existing_record.status = st.get("Status", None)
        existing_record.state = st.get("State", None)
        existing_record.running_for = st.get("RunningFor", None)
        existing_record.full_state = st

    existing_record.logs = container.get("log", [])  # Update logs


def create_new_container_record(container):
    new_record = ContainerStatus(container_id=container["container_id"])
    for st in container["state"]:
        new_record.container_name = st.get("Names", None)
        new_record.status = st.get("Status", None)
        new_record.state = st.get("State", None)
        new_record.running_for = st.get("RunningFor", None)
        new_record.full_state = st

    new_record.logs = container.get("log", [])
    return new_record
