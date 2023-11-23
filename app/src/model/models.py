import pytz
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.src.config.database import Base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import BIGINT, TIMESTAMP, ENUM
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    bots = relationship("Bot", back_populates="owner")


# create bot model


class Bot(Base):
    __tablename__ = "bots"

    id = Column(BIGINT, primary_key=True, index=True)
    container_id = Column(String)
    container_name = Column(String)
    name = Column(String, nullable=False)
    strategy = Column(String, default="supertrend")
    description = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(pytz.timezone('Asia/Taipei')), nullable=False)
    status = Column(
        ENUM("running", "stopped", "deleted", name="status_type"),
        default="running",
        nullable=False,
    )
    owner_id = Column(BIGINT, ForeignKey("users.id"))
    owner = relationship("User", back_populates="bots")


# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")
