from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import talib



class RsiOscillator(Strategy):
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14
    # Do as much initial computation as possible
    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_window)

    # Step through bars one by one
    # Note that multiple buys are a thing here
    def next(self):
        if crossover(self.rsi, self.upper_bound):
            self.position.close()
        elif crossover(self.lower_bound, self.rsi):
            self.buy()

# def run_strategy(data):
        
#     bt = Backtest(data, RsiOscillator, cash=1_000_000, commission=.002)
#     backtest_result = bt.run()
#     print(backtest_result)


#     # 提取屬性並放入字典中
#     result_dict = {attr: getattr(backtest_result, attr, None) for attr in res_attributes}
#     result_json = json.dumps(result_dict, default=str, indent=4)
#     return result_json