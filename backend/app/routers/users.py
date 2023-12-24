import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.src.schema import schemas
from app.utils.database import get_db
from app.crud.user import create_user, get_user_by_email, get_users
from app.crud.bot import get_user_bots
from app.crud.container_status import get_user_containers_status
from app.utils.deps import get_current_user
from app.utils.auth import create_access_token, create_refresh_token, verify_password
from app.exceptions import EmailExisted, UnexpectedError, LoginFailed

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/profile", response_model=schemas.UserPublic)
def get_me(user: schemas.User = Depends(get_current_user)):
    return user


@router.post("/signup", response_model=schemas.User)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise EmailExisted()
    return create_user(db=db, user=user)


@router.post("/login", response_model=schemas.Token)
async def login(form_data: schemas.LoginForm, db: Session = Depends(get_db)):
    try:
        user = get_user_by_email(db, form_data.email)
        if user is None:
            raise LoginFailed()

        if not verify_password(form_data.password, user.hashed_password):
            raise LoginFailed()

        id, username, email = user.id, user.name, user.email

        return schemas.Token(
            access_token=create_access_token(username, email),
            refresh_token=create_refresh_token(username, email),
            user_id=id,
            username=username,
        )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        logging.error(f"Error in login: {e}")
        raise UnexpectedError(detail="Error in login!")


# TODO 可以把userid都拿掉了因為只會從token拿
@router.get("/{user_id}/bots", response_model=schemas.BotResp)
def get_user_bot_details(
    user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_bot = get_user_bots(user_id=user.id, db=db)
    return {"data": db_bot}


@router.get(
    "/{user_id}/bots/container-monitoring", response_model=schemas.ContainerStateDict
)
def get_user_container_monitoring(
    user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    containers_info = get_user_containers_status(db, user.id)
    return {"data": containers_info}
