from history import history_data
import pandas as pd

# Generating mock data in the required format
mock_data = [
    {
        "OrderId": "1226958203",
        "Qty": 0.046,
        "Price": 2373.99,
        "Timestamp": "1702137600000",
    },
    {
        "OrderId": "1226958302",
        "Qty": -0.046,
        "Price": 2368.00,
        "Timestamp": "1701964800332",
    },
    {
        "OrderId": "1226958421",
        "Qty": 0.046,
        "Price": 2373.99,
        "Timestamp": "1701878400332",
    },
]

# Creating a DataFrame from the mock data
trade_df = pd.DataFrame(mock_data)


# Sorting by timestamp from old to new
trade_df.sort_values(by="Timestamp", inplace=True)
trade_df.reset_index(drop=True, inplace=True)
print(trade_df)

# Fetching data from the history.py file
eth_data = history_data(
    symbols=["ETH/USDT"], t_frame="15m", since="2023-12-05T00:00:00Z"
)
print(eth_data.tail())
print(eth_data.columns)

# iterate over the dataframe
q = 0
result_df = pd.DataFrame()  # 初始化一個空的 DataFrame 儲存結果

for index, row in trade_df.iterrows():
    q += row["Qty"]
    print("q = ", q)
    # get the price data from timestamp now to next trade
    if index < len(trade_df) - 1:
        end_timestamp = int(trade_df.loc[index + 1, "Timestamp"])
        print("end_timestamp", end_timestamp)
    else:
        end_timestamp = eth_data.iloc[-1]["Timestamp"]
        print("end_timestamp", end_timestamp)
    start_timestamp = int(row["Timestamp"])
    df_subset = eth_data[
        (eth_data["Timestamp"] >= start_timestamp)
        & (eth_data["Timestamp"] < end_timestamp)
    ]

    # result = (df_subset["Close"] - row["Price"]) * q
    # please concat tall he result_df to the main dataframe
    pnl_result = (df_subset["Close"] - row["Price"]) * q
    temp_df = pd.DataFrame({'pnl': pnl_result, 'timestamp': start_timestamp})

    # 將結果附加到 result_df 上
    result_df = pd.concat([result_df, temp_df])
    
result_df.sort_values(by="timestamp", inplace=True)
result_df.reset_index(drop=True, inplace=True)
print(result_df)
