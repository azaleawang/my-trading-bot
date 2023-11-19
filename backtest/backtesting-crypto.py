from backtesting import Backtest
import json
from history import history_data
from strategy.s3mytradingbot.RsiOscillator import RsiOscillator
from config import res_attributes

def run_strategy(data, strategy):
    bt = Backtest(data, strategy, cash=1_000_000, commission=.002)
    backtest_result = bt.run()
    try:
        bt.plot()
    except Exception as e:
        print(f"Error when potting: {e}")
    print(backtest_result)

    result_dict = {attr: getattr(backtest_result, attr, None) for attr in res_attributes}
    result_json = json.dumps(result_dict, default=str, indent=4)
    return result_json

df = history_data(symbols=['MEME/USDT'], t_frame='1h', since='2017-11-01T00:00:00Z')
if df.empty:
    raise ValueError("No data found")

else:
    print("Data found")
    print(df.tail())

    bt = run_strategy(df, RsiOscillator)
    print()
    print("res " + bt)

"""" for optimizing the strategy """
# stats = bt.optimize(
#     upper_bound = range(50, 85, 5),
#     lower_bound = range(10, 60, 5),
#     rsi_window = range(10, 30, 2),
#     maximize = "Sharpe Ratio",
#     constraint = lambda x: x.upper_bound > x.lower_bound,
# )

# print(stats)

