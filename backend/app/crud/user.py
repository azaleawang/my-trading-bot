from sqlalchemy.orm import Session
from app.schema import user as schemas
from app.models import User
from app.utils.auth import get_hashed_password


def get_user_by_email(db: Session, email: str):
    db_user = db.query(User).filter(User.email == email).first()
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_hashed_password(user.password)
    db_user = User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
