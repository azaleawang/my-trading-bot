from sqlalchemy import Column, Integer, String, ForeignKey, BIGINT
from sqlalchemy.orm import relationship
from .base import Base

class WorkerServer(Base):
    __tablename__ = 'worker_servers'

    id = Column(BIGINT, primary_key=True)
    instance_id = Column(String, unique=True, nullable=False)
    private_ip = Column(String, unique=True)
    total_memory = Column(Integer, default=650, nullable=False)  # Total memory in MB
    available_memory = Column(Integer, default=650, nullable=False)  # Available memory in MB
    bots = relationship("Bot", back_populates="worker_server")
    # TODO modify crud for separate worker server