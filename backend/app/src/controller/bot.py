import subprocess

from typing import Union
from fastapi import HTTPException

from pydantic import BaseModel
import requests
from app.src.schema import schemas
import os, json


class Bot_Created_Resp(BaseModel):
    data: schemas.Bot


def stop_bot_container(container_id: str, worker_ip: str):
    response = requests.put(f"{worker_ip}/stop-container?container_id={container_id}")
    if response.status_code == 200:
        print(response.json())
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to stop container in worker server.",
        )


def delete_bot_container(container_id: str, worker_ip: str):
    response = requests.delete(
        f"{worker_ip}/delete-container?container_id={container_id}"
    )
    if response.status_code == 200:
        print(response.json())
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to stop container in worker server.",
        )
