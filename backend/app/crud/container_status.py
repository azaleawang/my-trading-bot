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
    try:
        for container in container_data:
            container_id = container["container_id"]

            # Check if the container already exists
            existing_record = (
                db.query(ContainerStatus)
                .filter(ContainerStatus.container_id == container_id)
                .first()
            )

            if existing_record:
                # Update the existing record
                for st in container["state"]:
                    existing_record.status = st.get("Status", None)
                    existing_record.state = st.get("State", None)
                    existing_record.running_for = st.get("RunningFor", None)
                    existing_record.full_state = st

                existing_record.logs = container.get("log", [])  # Update logs
                db.add(existing_record)  # Not necessary but adds clarity
            else:
                # Create a new record
                new_record = ContainerStatus(container_id=container_id)

                for st in container["state"]:
                    new_record.container_name = st.get("Names", None)
                    new_record.status = st.get("Status", None)
                    new_record.state = st.get("State", None)
                    new_record.running_for = st.get("RunningFor", None)
                    new_record.full_state = st

                new_record.logs = container.get("log", [])
                db.add(new_record)  # Add the new record to the session

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()
