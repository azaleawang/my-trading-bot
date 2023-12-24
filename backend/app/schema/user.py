# User schema
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserPublic(UserBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    user_id: int
    username: str


class TokenPayload(BaseModel):
    username: str
    email: str
    exp: int = None


class LoginForm(BaseModel):
    email: str
    password: str
