import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.src.schema import schemas
from app.src.config.database import get_db
from app.crud.user import get_user, get_users
from app.crud.bot import get_user_bots
from app.crud.container_status import get_user_containers_status
from app.utils.deps import get_current_user

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


# @router.get("/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, user: schemas.User = Depends(get_current_user)):
#     # db_user = get_user(db, user_id=user_id)
#     if user_id != user.id:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="You are not allowed to access this user's information.",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user


@router.get("/{user_id}/bots")
def get_user_bot_details(user_id: int, user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        if user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to access this user's bot information.",
                headers={"WWW-Authenticate": "Bearer"},
            )
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
def get_user_container_monitoring(user_id: int, user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
        try:
            if user_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You are not allowed to access this user's bot information.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            # get data from db
            containers_info = get_user_containers_status(db, user_id)
            return {"data": containers_info}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
