from backtesting import Strategy
from backtesting.lib import crossover
import talib

class MaRsi(Strategy):
    fast_ma = 10
    slow_ma = 20
    upper_bound = 65
    lower_bound = 45
    rsi_window = 14 
    
    params = {
        'fast_ma': fast_ma,
        'slow_ma': slow_ma,
        'upper_bound': upper_bound,
        'lower_bound': lower_bound,
        'rsi_window': rsi_window
    }
    
    def init(self):
        # 初始化指標
        self.fast_ma = self.I(talib.SMA, self.data.Close, self.params.get('fast_ma', self.fast_ma))
        self.slow_ma = self.I(talib.SMA, self.data.Close, self.params.get('slow_ma', self.slow_ma))
        self.rsi = self.I(talib.RSI, self.data.Close, self.params.get('rsi_window', self.rsi_window))
        self.lower_bound = self.params.get('lower_bound', self.lower_bound)
        self.upper_bound = self.params.get('upper_bound', self.upper_bound)
        
    def next(self):
        if crossover(self.fast_ma, self.slow_ma) and self.rsi[-1] < self.lower_bound:
            self.buy()

        # Close position condition: Fast MA crosses below Slow MA and RSI is above 70 (overbought)
        elif crossover(self.slow_ma, self.fast_ma) and self.rsi[-1] > self.upper_bound:
            if self.position:
                self.position.close()