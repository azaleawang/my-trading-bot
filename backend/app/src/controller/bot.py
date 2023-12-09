import subprocess

from typing import Union
from fastapi import HTTPException

from pydantic import BaseModel
import requests
from app.src.schema import schemas
import os, json



class Bot_Created_Resp(BaseModel):
    data: schemas.Bot


# def start_bot_container(container_name: str, bot_info: schemas.BotBase, worker_ip: str) -> dict:
#     try:
#         # load the bot script from ??? the better design may be downloading from s3
#         command = [
#             "docker",
#             "run",
#             "-d",
#             "-m",
#             "128m",
#             "--name",
#             container_name,
#             "-e",
#             f"CONTAINER_NAME={container_name}",
#             "-e",
#             f"SYMBOL={bot_info.symbol}",
#             "-e",
#             f"TIMEFRAME={bot_info.t_frame}",
#             "-e",
#             "LIMIT=100",
#             "-e",
#             f"AMOUNT_IN_USDT={bot_info.quantity}",
#             "-v",
#             f"{os.getenv('BOT_SCRIPT_PATH')}:/app",
#             "yayin494/trading-bot:tagname",
#             "python",
#             "-u",
#             f"./{bot_info.strategy}.py",
#         ]

#         # Run the command and capture the output
#         result = subprocess.run(
#             command,
#             check=True,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True,
#         )

#         # The stdout will contain the container ID
#         container_id = result.stdout.strip()
#         # store information into db!
#         return {
#             # "owner_id": owner_id,
#             "container_id": container_id,
#             "container_name": container_name,
#             "status": "running",
#         }

#     except subprocess.CalledProcessError as e:
#         # Capture and return any errors
#         error_message = e.stderr or str(e)
#         raise HTTPException(status_code=500, detail=error_message)


def stop_bot_container(container_id: str, worker_ip: str):
    response = requests.put(f"{worker_ip}/stop-container?container_id={container_id}")
    if response.status_code == 200:
        print(response.json())
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to stop container in worker server.",
        )
    # command = ["docker", "stop", container_id]
    # try:
    #     subprocess.run(
    #         command,
    #         check=True,
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.PIPE,
    #         text=True,
    #     )
    # except subprocess.CalledProcessError as e:
    #     print(f"Error stopping docker container {container_id}: {e.stderr}")
    #     raise HTTPException(
    #         status_code=500,
    #         detail="Error stopping bot in docker. Pls check docker's status"
    #         + str(e.stderr),
    #     )


def delete_bot_container(container_id: str, worker_ip: str):
    response = requests.delete(f"{worker_ip}/delete-container?container_id={container_id}")
    if response.status_code == 200:
        print(response.json())
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to stop container in worker server.",
        )
    # command = ["docker", "rm", container_id]
    # try:
    #     res = subprocess.run(
    #         command,
    #         check=True,
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.PIPE,
    #         text=True,
    #     )
    #     if not res:
    #         raise HTTPException(
    #             status_code=500,
    #             detail="Error deleting bot in docker. Pls check docker's status",
    #         )
    # except subprocess.CalledProcessError as e:
    #     print(f"Error deleting docker container {container_id}: {e.stderr}")
    #     raise HTTPException(
    #         status_code=500, detail="Error deleting bot in docker: " + str(e.stderr)
    #     )
