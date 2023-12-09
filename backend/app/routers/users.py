import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.src.schema import schemas
from app.src.config.database import get_db
from app.crud.user import get_user, get_users
from app.crud.bot import check_name, create_user_bot, get_user_bots
from app.crud.container_status import get_container_status, get_user_containers_status

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/{user_id}/bots")
def get_user_bot_details(user_id: int, db: Session = Depends(get_db)):
    try:
        db_bot = get_user_bots(user_id=user_id, db=db)

        return {
            "data": db_bot,
        }
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        logging.error(f"Error in get_bot_for_user: {e}")
        raise HTTPException(status_code=500, detail="Error fetching bots." + str(e))


    
@router.get("/{user_id}/bots/container-monitoring", response_model=schemas.ContainerStateDict)
def get_user_container_monitoring(user_id: int, db: Session = Depends(get_db)):
        try:
            # get data from db
            containers_info = get_user_containers_status(db, user_id)
            return {"data": containers_info}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
