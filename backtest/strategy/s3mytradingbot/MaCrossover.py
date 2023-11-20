from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import talib

class MaCrossover(Strategy):
    # Define the two moving average windows
    fast_ma = 10
    slow_ma = 20

    def init(self):
        # Initialize the two moving averages
        self.fast_ma = self.I(talib.SMA, self.data.Close, self.fast_ma)
        self.slow_ma = self.I(talib.SMA, self.data.Close, self.slow_ma)

    def next(self):
        # If the fast moving average crosses above the slow moving average, buy
        if crossover(self.fast_ma, self.slow_ma):
            self.buy()

        # If the fast moving average crosses below the slow moving average, sell
        elif crossover(self.slow_ma, self.fast_ma):
            self.position.close()

# Usage Example (assuming you have a DataFrame `data` with OHLC data)
# from backtesting.test import GOOG
# bt = Backtest(data, MovingAverageCrossover, cash=10000, commission=.002)
# output = bt.run()
# bt.plot()
