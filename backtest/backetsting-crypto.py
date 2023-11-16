from backtesting import Backtest, Strategy
import pandas as pd
import talib
import ccxt
import json
from datetime import datetime, timedelta
from backtesting.lib import crossover
from history import history_data
from strategy.RsiOscillator import RsiOscillator
from config import res_attributes


df = history_data(symbols=['BTC/USDT'], t_frame='4h', since='2023-01-01T00:00:00Z')
if df.empty:
    raise ValueError("No data found")
    quit()
else:
    print("Data found")
    print(df.tail())

def run_strategy(data, strategy):
    bt = Backtest(data, strategy, cash=1_000_000, commission=.002)
    backtest_result = bt.run()
    print(backtest_result)

    result_dict = {attr: getattr(backtest_result, attr, None) for attr in res_attributes}
    result_json = json.dumps(result_dict, default=str, indent=4)
    return result_json

print("res " + run_strategy(df, RsiOscillator))

"""" for optimizing the strategy """
# stats = bt.optimize(
#     upper_bound = range(50, 85, 5),
#     lower_bound = range(10, 60, 5),
#     rsi_window = range(10, 30, 2),
#     maximize = "Sharpe Ratio",
#     constraint = lambda x: x.upper_bound > x.lower_bound,
# )

# print(stats)
# bt.plot()

