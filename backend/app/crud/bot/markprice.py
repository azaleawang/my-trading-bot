import pandas as pd
from datetime import datetime
from app.utils.influxdb import client

query_api = client.query_api()


def get_history_mark_price(
    symbol: str,
    start="2023-10-28T00:00:00Z",
    stop=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
    bucket="mark-price",
):
    query = f"""
    from(bucket: "{bucket}")
    |> range(start: {start}, stop: {stop})
    |> filter(fn: (r) => r["_measurement"] == "crypto_prices")
    |> filter(fn: (r) => r["_field"] == "price")
    |> filter(fn: (r) => r["symbol"] == "{symbol}")
    |> sort(columns: ["_time"])
    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")

    """

    result = query_api.query_data_frame(query=query)
    df = pd.DataFrame(result)
    df["timestamp"] = pd.to_datetime(df["_time"]).astype(int) // 10**6
    return df
