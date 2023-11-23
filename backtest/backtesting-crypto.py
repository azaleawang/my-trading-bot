from backtesting import Backtest
import json
from history import history_data
from time import gmtime, strftime

strftime("%Y%m%d-%H%M%S", gmtime())
from strategy.s3mytradingbot.RsiOscillator import RsiOscillator
from strategy.s3mytradingbot.MaCrossover import MaCrossover

from strategy.s3mytradingbot.MaRsi import MaRsi
from strategy.s3mytradingbot.SuperTrend import SuperTrend
from config import res_attributes

strategy = RsiOscillator

params = {
    'rsi_window': 20,
    'upper_bound': 80,
}

def run_strategy(data, strategy, params):
    bt = Backtest(data, strategy, cash=1_000_000, commission=0.002)
    backtest_result = bt.run(params = params)
    try:
        bt.plot(
            filename=f"backtest/strategy/result/{strategy.__name__}_{strftime('%Y%m%d-%H%M%S', gmtime())}",
            resample=False,
            open_browser=False,
        )
    except Exception as e:
        print(f"Error when potting: {e}")
    print(backtest_result)

    result_dict = {
        attr: getattr(backtest_result, attr, None) for attr in res_attributes
    }
    result_dict["plot"] = "test"
    result_json = json.dumps(result_dict, default=str, indent=4)
    data = {"result": result_json}
    print(data)
    return data


df = history_data(symbols=["ETH/USDT"], t_frame="1d", since="2023-01-01T00:00:00Z")
if df.empty:
    raise ValueError("No data found")

else:
    print("Data found")
    print(df.tail())

    bt = run_strategy(df, strategy, params)
    print("res ", bt)

"""" for optimizing the strategy """
# stats = bt.optimize(
#     upper_bound = range(50, 85, 5),
#     lower_bound = range(10, 60, 5),
#     rsi_window = range(10, 30, 2),
#     maximize = "Sharpe Ratio",
#     constraint = lambda x: x.upper_bound > x.lower_bound,
# )

# print(stats)
