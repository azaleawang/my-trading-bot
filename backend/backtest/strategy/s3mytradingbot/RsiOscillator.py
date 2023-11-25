from backtesting import Strategy
from backtesting.lib import crossover
import talib

class RsiOscillator(Strategy):
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    params = {'upper_bound': upper_bound, 'lower_bound': lower_bound, 'rsi_window': rsi_window}
    # Do as much initial computation as possible
    def init(self):
        self.upper_bound = self.params.get('upper_bound', self.upper_bound)
        self.lower_bound = self.params.get('lower_bound', self.lower_bound)
        self.rsi = self.I(talib.RSI, self.data.Close, self.params.get('rsi_window', self.rsi_window))

    # Step through bars one by one
    # Note that multiple buys are a thing here
    def next(self):
        if crossover(self.rsi, self.upper_bound):
            self.position.close()
        elif crossover(self.lower_bound, self.rsi):
            self.buy()
            