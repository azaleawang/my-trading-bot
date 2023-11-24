import subprocess
from typing import Union
from fastapi import HTTPException
from pydantic import BaseModel
from app.src.schema import schemas


class Bot_Created_Resp(BaseModel):
    data: schemas.Bot
    

 
def start_bot_container(owner_id: str, container_name: str, bot_info: schemas.BotBase) -> dict:
    try:
        # load the bot script from ??? the better design may be downloading from s3
        
        command = [
            "docker",
            "run",
            "-d",
            "--name",
            container_name,
            "-v",
            "/home/leah/my-trading-bot/trade/supertrend:/app",
            "py-tradingbot",
            "python",
            "-u",
            f"./{bot_info.strategy}.py",
        ]
        # Run the command and capture the output
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # The stdout will contain the container ID
        container_id = result.stdout.strip()
        # store information into db!
        return {
            "owner_id": owner_id,
            "container_id": container_id,
            "container_name": container_name,
            "status": "running",
        }

    except subprocess.CalledProcessError as e:
        # Capture and return any errors
        error_message = e.stderr or str(e)
        raise HTTPException(status_code=500, detail=error_message)

def stop_bot_container(container_id: str):
    command = ["docker", "stop", container_id]
    try:
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error stopping docker container {container_id}: {e.stderr}")
        raise HTTPException(status_code=500, detail="Error stopping bot in docker. Pls check docker's status" + str(e.stderr))
    
def delete_bot_container(container_id: str):
   
    command = ["docker", "rm", container_id]
    try:
        res = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if not res:
            raise HTTPException(status_code=500, detail="Error deleting bot in docker. Pls check docker's status")
    except subprocess.CalledProcessError as e:
        print(f"Error deleting docker container {container_id}: {e.stderr}")
        raise HTTPException(status_code=500, detail="Error deleting bot in docker: " + str(e.stderr))