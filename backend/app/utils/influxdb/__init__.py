from influxdb_client import InfluxDBClient
import os

client = InfluxDBClient.from_config_file(os.getenv("INFLUX_CONFIG_PATH"))

__all__ = ["client"]