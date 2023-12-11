import pandas as pd

from .influxdb.setup import get_history_mark_price


# Generating mock data in the required format
mock_data = [
    {
        "order_id": "1226958203",
        "qty": 0.006,
        "price": 43367.9,
        "timestamp": "1702259706000",
    },
    {
        "order_id": "1226958302",
        "qty": -0.006,
        "price": 41822.5,
        "timestamp": "1702262967000",
    },
    {
        "order_id": "1226958421",
        "qty": 0.006,
        "price": 41934.68,
        "timestamp": "1702263522000",
    },
]

# Creating a DataFrame from the mock data
trade_df = pd.DataFrame(mock_data)


# Sorting by timestamp from old to new
trade_df.sort_values(by="timestamp", inplace=True)
trade_df.reset_index(drop=True, inplace=True)
# print(trade_df)

# Fetching data from the history.py file
# eth_data = history_data(
#     symbols=["ETH/USDT"], t_frame="15m", since="2023-12-05T00:00:00Z"
# )

def calculate_pnl(symbol: str, bot_create_iso_str, bot_create_timestamp_ms, trade_df=trade_df):
    # TODO not sure if bot_start_timestamp is correct time format
    mark_data = get_history_mark_price(symbol=symbol, start=bot_create_iso_str)
    print(mark_data.tail())
    # print(mark_data.columns)

    # iterate over the dataframe

    q = 0
    result_df = pd.DataFrame({'pnl': [0], 'timestamp': bot_create_timestamp_ms})  # 以機器人啟動時間為初始化

    for index, row in trade_df.iterrows():
        q += row["qty"]
        # get the price data from timestamp now to next trade
        if index < len(trade_df) - 1:
            end_timestamp = int(trade_df.loc[index + 1, "timestamp"])
            start_timestamp = int(row["timestamp"])
            df_subset = mark_data[
                (mark_data["timestamp"] >= start_timestamp)
                & (mark_data["timestamp"] < end_timestamp)
            ]
        else:
            end_timestamp = mark_data.iloc[-1]["timestamp"]
            start_timestamp = int(row["timestamp"])
            df_subset = mark_data[
                (mark_data["timestamp"] >= start_timestamp)
                & (mark_data["timestamp"] <= end_timestamp)
            ]
        

        # please concat tall he result_df to the main dataframe
        pnl_result = (df_subset["price"] - row["price"]) * q
        temp_df = pd.DataFrame({'pnl': pnl_result, 'timestamp': df_subset['timestamp']}) # this should be timestamp of the mark_data not fixed start_timestamp

        # 將結果附加到 result_df 上
        result_df = pd.concat([result_df, temp_df])
        
    # result_df.sort_values(by="timestamp", inplace=True)
    # result_df.reset_index(drop=True, inplace=True)
    return result_df.to_dict(orient='records')
