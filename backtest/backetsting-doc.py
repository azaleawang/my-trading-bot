# Example OHLC daily data for Google Inc.
from backtesting import Backtest, Strategy
from backtesting.test import GOOG
import pandas as pd
import talib
from backtesting.lib import crossover



def SMA(values, n):
    """
    Return simple moving average of `values`, at
    each step taking into account `n` previous values.
    """
    return pd.Series(values).rolling(n).mean()

# print(GOOG)

class SmaCross(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    n1 = 10
    n2 = 20
    
    def init(self):
        # Precompute the two moving averages
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)
    
    def next(self):
        # If sma1 crosses above sma2, close any existing
        # short trades, and buy the asset
        if crossover(self.sma1, self.sma2):
            self.position.close()
            self.buy()

        # Else, if sma1 crosses below sma2, close any existing
        # long trades, and sell the asset
        elif crossover(self.sma2, self.sma1):
            self.position.close()
            self.sell()

bt = Backtest(GOOG, SmaCross, cash=10_000, commission=.002)
# stats = bt.run()
# print(stats)

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

bt = Backtest(GOOG, RsiOscillator, cash=10_000, commission=.002)
# stats = bt.run()

# print(stats)
# bt.plot()

"""" for optimizing the strategy """
stats = bt.optimize(
    upper_bound = range(50, 85, 5),
    lower_bound = range(10, 60, 5),
    rsi_window = range(10, 30, 2),
    maximize = "Sharpe Ratio",
    constraint = lambda x: x.upper_bound > x.lower_bound,
)

print(stats)
bt.plot()