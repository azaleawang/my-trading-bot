import json
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import Depends, HTTPException
from app.src.schema import schemas
from sqlalchemy.sql import and_
from app.models.container_status import ContainerStatus
from app.utils.database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.models.bot import Bot


def get_container_status(db: Session, bot_id: int):
    # Query all containers for the user
    container_status = (
        db.query(ContainerStatus)
        .join(Bot)
        .filter(
            Bot.id == bot_id,
        )
        .all()
    )
    return container_status


def get_user_containers_status(db: Session, user_id: int):
    # Query all containers for the user
    user_container_status = (
        db.query(ContainerStatus)
        .join(Bot)
        .filter(
            Bot.owner_id == user_id,
        )
        .all()
    )
    return user_container_status


def parse_and_store(container_data):
    db = SessionLocal()

    for container in container_data:
        try:
            container_id = container["container_id"]

            # check if the container recorded before
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
                bot_id = get_bot_id_by_container_id(db, container_id)
                new_record = create_new_container_record(bot_id, container)
                db.add(new_record)


            db.commit()  # Commit changes for each container

            # check if container status is different from bot status
            check_bot_status_consistency(
                db, container_id, existing_record or new_record
            )

        except Exception as e:
            db.rollback()  # Rollback only affects the current container
            print(f"Error processing container {container_id}: {e}")

    db.close()


def check_bot_status_consistency(db, container_id, db_record):
    bot_status = db.query(Bot.status).filter(Bot.container_id == container_id).first()
    if (bot_status[0] and bot_status[0] != db_record.state):
        db.query(Bot).filter(Bot.container_id == container_id).update(
            {"status": db_record.state}
        )
        print(f"Container {container_id} status updated to {db_record.status}")
        db.commit() 
    # else:
    #     print(f"Bot status is consistent with container status")
    return


def update_container(existing_record, container):
    for st in container["state"]:
        existing_record.status = st.get("Status", None)
        existing_record.state = st.get("State", None)
        existing_record.running_for = st.get("RunningFor", None)
        existing_record.full_state = st

    existing_record.logs = container.get("log", [])  # Update logs


def get_bot_id_by_container_id(db: Session, container_id: str):
    bot_id = db.query(Bot.id).filter(Bot.container_id == container_id).first()
    bot_id = bot_id[0] if bot_id else None
    return bot_id


def create_new_container_record(bot_id, container):
    # bot_id
    new_record = ContainerStatus(container_id=container["container_id"])
    for st in container["state"]:
        new_record.container_name = st.get("Names", None)
        new_record.bot_id = bot_id
        new_record.status = st.get("Status", None)
        new_record.state = st.get("State", None)
        new_record.running_for = st.get("RunningFor", None)
        new_record.full_state = st

    new_record.logs = container.get("log", [])
    return new_record
