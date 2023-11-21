from backtesting import Strategy
from backtesting.lib import crossover
import numpy as np
import pandas as pd
# https://github.com/webclinic017/algotrading-18/blob/e545dd4853261a7d1e5add7dec341f646d460b27/backtesting/indicators/SuperTrend.py

# SuperTrendBand function
def super_trend_band(df, period, multiplier):
    hl2 = (df["High"] + df["Low"]) / 2
    atr = df["TrueRange"].rolling(period).mean() * multiplier
    basic_ub = hl2 + atr
    basic_lb = hl2 - atr

    final_ub = basic_ub.copy()
    final_lb = basic_lb.copy()

    for i in range(period, len(df)):
        if df["Close"][i - 1] <= final_ub[i - 1]:
            final_ub[i] = min(basic_ub[i], final_ub[i - 1])
        else:
            final_ub[i] = basic_ub[i]

        if df["Close"][i - 1] >= final_lb[i - 1]:
            final_lb[i] = max(basic_lb[i], final_lb[i - 1])
        else:
            final_lb[i] = basic_lb[i]

    return final_ub, final_lb


# Calculate True Range for ATR
def true_range(df):
    df["HighLow"] = df["High"] - df["Low"]
    df["HighClose"] = np.abs(df["High"] - df["Close"].shift())
    df["LowClose"] = np.abs(df["Low"] - df["Close"].shift())
    tr = df[["HighLow", "HighClose", "LowClose"]].max(axis=1)
    return tr


class SuperTrend(Strategy):
    period = 7
    multiplier = 3
    params = {"period": period, "multiplier": multiplier}
    
    def init(self):
        # Calculate True Range and attach it to the dataframe
        self.data.df["TrueRange"] = true_range(self.data.df)
        self.period = self.params.get("period", self.period)
        self.multiplier = self.params.get("multiplier", self.multiplier)
        
        # Calculate SuperTrend Bands
        self.data.df["FinalUB"], self.data.df["FinalLB"] = super_trend_band(
            self.data.df, self.period, self.multiplier
        )

        # Define SuperTrend
        self.supertrend = pd.Series(np.nan, index=self.data.df.index)
        for i in range(self.period, len(self.supertrend)):
            if self.data.Close[i] > self.data.df["FinalUB"][i]:
                self.supertrend[i] = self.data.df["FinalUB"][i]
            else:
                self.supertrend[i] = self.data.df["FinalLB"][i]

        self.supertrend = self.I(self.super_trend, self.supertrend)

    def super_trend(self, supertrend):
        return supertrend

    def next(self):
        if crossover(self.data.Close, self.supertrend):
            if not self.position:
                self.buy()
            else:
                self.position.close()

        elif crossover(self.supertrend, self.data.Close):
            if self.position:
                self.position.close()
