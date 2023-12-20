from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import pandas as pd
from datetime import datetime
load_dotenv() 
# client = InfluxDBClient(url="http://localhost:8086", token=INFLUX_API_TOKEN, org=org)
current_directory = os.getcwd()
config_full_path = os.path.join(current_directory, "history_chart/influxdb", "config.ini")

client = InfluxDBClient.from_config_file(os.getenv("INFLUX_CONFIG_PATH"))
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

def write_to_influxdb(data, bucket="mark-price"):
    point = Point("crypto_prices").tag("symbol", data["symbol"]) \
                                  .field("price", float(data["price"])) \
                                  .time (int(data["timestamp"]) * 1000000)
    write_api.write(bucket=bucket, record=point)

def get_history_mark_price(symbol: str, start="2023-10-28T00:00:00Z", stop=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"), bucket="mark-price"):
    
    query = f"""
    from(bucket: "{bucket}")
    |> range(start: {start}, stop: {stop})
    |> filter(fn: (r) => r["_measurement"] == "crypto_prices")
    |> filter(fn: (r) => r["_field"] == "price")
    |> filter(fn: (r) => r["symbol"] == "{symbol}")
    |> sort(columns: ["_time"])
    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")

    """
    # print(query)
    # Execute the query
    result = query_api.query_data_frame(query=query)
    df = pd.DataFrame(result)
    df['timestamp'] = pd.to_datetime(df['_time']).astype(int) // 10**6
    return df