"""
Check the docker container states regularly (every 1 min?)
"""

import json
import subprocess
import time
from fastapi import HTTPException
import requests
import os
from dotenv import load_dotenv

load_dotenv()


def fetch_all_containers():
    try:
        url = f"{os.getenv('HOST')}:{os.getenv('PORT')}/api/v1/bots/"
        response = requests.get(url)
        return response.json().get("data", [])
    except Exception as e:
        print("Error fetching all containers from server: ", e)


def send_data_to_server(data):
    try:
        url = f"http://127.0.0.1:8000/api/v1/bots/container-monitoring/"
        response = requests.post(url, json=data)
        print("server said: ", response.text)
    except Exception as e:
        print("Error sending data to server: ", e)


def get_container_status(container_id: str) -> list:
    command = [
        "docker",
        "ps",
        "-a",
        "-f",
        f"id={container_id}",
        "--format",
        "{{json .}}",
        "--no-trunc",
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        containers = [json.loads(line) for line in result.stdout.splitlines()]

        return containers
    except subprocess.CalledProcessError as e:
        print(f"Error getting status for docker container {container_id}: {e.stderr}")
        raise HTTPException(
            status_code=500,
            detail="Error getting status for docker container: " + str(e.stderr),
        )


def get_last_container_logs(container_id_or_name: str, line_count: int = 5) -> list:
    command = ["docker", "logs", "--tail", str(line_count), container_id_or_name]

    try:
        result = subprocess.run(command, capture_output=True, text=True)

        logs = result.stdout.splitlines()
        return logs
    except subprocess.CalledProcessError as e:
        print(
            f"Error getting logs for docker container {container_id_or_name}: {e.stderr}"
        )
        raise HTTPException(
            status_code=500,
            detail="Error getting logs for docker container: " + str(e.stderr),
        )


# container_name = "User1_supertrend_jiji"
# print(get_container_status(container_name))

# logs = get_last_container_logs(container_name)
# print(logs)

""" example outputs of docker ps:
[{'Command': '"python -u ./supertrend.py"', 'CreatedAt': '2023-12-01 02:06:03 +0800 CST', 'ID': 'e6e3af6c081c280dec922a8555b7ad98f0125f77aa8ebac2efce510e26945743', 'Image': 'yayin494/trading-bot:tagname', 'Labels': 'desktop.docker.io/binds/0/Source=/home/leah/my-trading-bot/backend/trade/supertrend,desktop.docker.io/binds/0/SourceKind=wsl2DistroFile,desktop.docker.io/binds/0/Target=/app,desktop.docker.io/wsl-distro=Ubuntu-20.04', 'LocalVolumes': '0', 'Mounts': '/run/desktop/mnt/host/wsl/docker-desktop-bind-mounts/Ubuntu-20.04/9c2097a38ac2c466ded257d418b8804c06a3d047a94457ebdace755cc5e52ae9', 'Names': 'User1_supertrend_jiji', 'Networks': 'bridge', 'Ports': '', 'RunningFor': '39 hours ago', 'Size': '93.6kB (virtual 1.21GB)', 'State': 'exited', 'Status': 'Exited (137) 39 hours ago'}]
"""

""" example outputs of logs:
['20231130-180805: Checking for buy and sell signals', '20231130-180905: symbol: BNB/USDT, timeframe: 30m, limit: 100, in_position: True, quantity_buy_sell: 0.1', '20231130-180905: Fetching new bars', '20231130-180906: Checking for buy and sell signals', '20231130-181006: symbol: BNB/USDT, timeframe: 30m, limit: 100, in_position: True, quantity_buy_sell: 0.1', '20231130-181006: Fetching new bars', '20231130-181006: Checking for buy and sell signals', '20231130-181106: symbol: BNB/USDT, timeframe: 30m, limit: 100, in_position: True, quantity_buy_sell: 0.1', '20231130-181106: Fetching new bars', '20231130-181106: Checking for buy and sell signals']
"""


if __name__ == "__main__":
    while True:
        data_to_server = []
        container_list = fetch_all_containers()
        if not container_list:
            print("No containers found")
        else:
            for container in container_list:
                container_id = container.get("container_id")
                if not container_id:
                    continue
                
                container_dict = {}
                container_dict["container_id"] = container_id
                print(f"Checking container {container['name']}")
                state = get_container_status(container_id)
                container_dict["state"] = state

                logs = get_last_container_logs(container_id)
                container_dict["log"] = logs

                data_to_server.append(container_dict)
            data_json = json.dumps({"data": data_to_server})
            # print(data_json)

            send_data_to_server(json.loads(data_json))
        
        time.sleep(60)


# data: [{"name": "m", "state": [], "logs": []}, {}]
