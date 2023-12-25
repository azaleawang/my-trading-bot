from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os
from dotenv import load_dotenv
load_dotenv()

config_path = os.getenv("INFLUX_CONFIG_PATH")
client = InfluxDBClient.from_config_file(config_path)

write_api = client.write_api(write_options=SYNCHRONOUS)

def write_to_influxdb(data, bucket="mark-price"):
    point = (
        Point("crypto_prices")
        .tag("symbol", data["symbol"])
        .field("price", float(data["price"]))
        .time(int(data["timestamp"]) * 1000000)
    )
    write_api.write(bucket=bucket, record=point)
