from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import pandas as pd

bucket = "my-bucket"
# client = InfluxDBClient(url="http://localhost:8086", token=INFLUX_API_TOKEN, org=org)
current_directory = os.getcwd()
config_full_path = os.path.join(current_directory, "history_chart/influxdb", "config.ini")
# print(config_full_path)
client = InfluxDBClient.from_config_file("/home/leah/my-trading-bot/backend/app/history_chart/influxdb/config.ini")
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

def write_to_influxdb(data, bucket="mark-price"):
    point = Point("crypto_prices").tag("symbol", data["symbol"]) \
                                  .field("price", float(data["price"])) \
                                  .time (int(data["timestamp"]) * 1000000)
    write_api.write(bucket=bucket, record=point)

# p = Point("my_measurement").tag("location", "Prague").field("temperature", 25.3)

# write_api.write(bucket=bucket, record=p)

def get_history_mark_price(symbol: str, start="2023-10-28T00:00:00Z", bucket="mark-price"):
    
    query = f"""
    from(bucket: "{bucket}")
    |> range(start: {start})
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

# print(get_history_mark_price("BTCUSDT"))
# Convert to DataFrame
# df = pd.DataFrame(result)

# Optionally, convert the time to a more friendly format
# df['_time'] = pd.to_datetime(df['_time']).dt.tz_localize(None)

# Print the DataFrame
# print(df)

# ## using Table structure
# tables = query_api.query('from(bucket:"my-bucket") |> range(start: -10m)')

# for table in tables:
#     print(table)
#     for row in table.records:
#         print (row.values)


# ## using csv library
# csv_result = query_api.query_csv('from(bucket:"my-bucket") |> range(start: -10m)')
# val_count = 0
# for row in csv_result:
#     for cell in row:
#         val_count += 1