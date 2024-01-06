import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schema.user import User, UserCreate, Token, LoginForm, UserPublic
from app.schema.bot import BotResp, ContainerStateDict
from app.utils.database import get_db
from app.crud.user import create_user, get_user_by_email, get_users
from app.crud.bot import get_user_bots
from app.crud.container_status import get_user_containers_status
from app.utils.deps import get_current_user
from app.utils.auth import create_access_token, create_refresh_token, verify_password
from app.exceptions import PermissionDenied, EmailExisted, UnexpectedError, LoginFailed

router = APIRouter()


@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/profile", response_model=UserPublic)
def get_me(user: User = Depends(get_current_user)):
    return user


@router.post("/signup", response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise EmailExisted()
    return create_user(db=db, user=user)


@router.post("/login", response_model=Token)
async def login(form_data: LoginForm, db: Session = Depends(get_db)):
    try:
        user = get_user_by_email(db, form_data.email)
        if user is None:
            raise LoginFailed()

        if not verify_password(form_data.password, user.hashed_password):
            raise LoginFailed()

        id, username, email = user.id, user.name, user.email

        return Token(
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


@router.get("/{user_id}/bots", response_model=BotResp)
def get_user_bot_details(
    user_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user_id != user.id:
        raise PermissionDenied
    db_bot = get_user_bots(user_id=user.id, db=db)
    return {"data": db_bot}


@router.get("/{user_id}/bots/container-monitoring", response_model=ContainerStateDict)
def get_user_container_monitoring(
    user_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user_id != user.id:
        raise PermissionDenied
    containers_info = get_user_containers_status(db, user.id)
    return {"data": containers_info}
