from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.crud.user import get_user_by_email
from app.utils.database import get_db
from .auth import ALGORITHM, JWT_SECRET_KEY
from sqlalchemy.orm import Session

from jose import jwt
from pydantic import ValidationError
from app.src.schema.schemas import TokenPayload

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")

"""
It's a function run before the actual handler function. 
"""


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reuseable_oauth)
):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_email(db, token_data.email)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user
