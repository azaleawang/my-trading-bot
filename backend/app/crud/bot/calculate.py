import pandas as pd
from .markprice import get_history_mark_price

def calculate_pnl(symbol: str, bot_create_iso_str, bot_create_timestamp_ms, bot_stop_iso_str, trade_df):
    mark_data = get_history_mark_price(symbol=symbol, start=bot_create_iso_str, stop=bot_stop_iso_str)

    q = 0
    sumPnl = 0

    result_df = pd.DataFrame({'pnl': [0], 'timestamp': bot_create_timestamp_ms})  # 以機器人啟動時間為初始化

    for index, row in trade_df.iterrows():
        q += row["qty"]
        sumPnl += row["pnl"]
        
        # Get the price data from timestamp now to next trade
        if index < len(trade_df) - 1:
            end_timestamp = int(trade_df.loc[index + 1, "timestamp"])
            start_timestamp = int(row["timestamp"])
            mark_data_subset = mark_data[
                (mark_data["timestamp"] >= start_timestamp)
                & (mark_data["timestamp"] < end_timestamp)
            ]
        else:
            end_timestamp = mark_data.iloc[-1]["timestamp"]
            start_timestamp = int(row["timestamp"])
            mark_data_subset = mark_data[
                (mark_data["timestamp"] >= start_timestamp)
                & (mark_data["timestamp"] <= end_timestamp)
            ]
        
        pnl_result = (mark_data_subset["price"] - row["price"]) * q + sumPnl
        temp_df = pd.DataFrame({'pnl': pnl_result, 'timestamp': mark_data_subset['timestamp']})

        result_df = pd.concat([result_df, temp_df])
        

    return result_df.to_dict(orient='records')
