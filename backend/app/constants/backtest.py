
BACKTEST_RESULT_EXAMPLE = {
    "info": {
        "name": "MaRsi",
        "symbols": ["BTC/USDT"],
        "t_frame": "4h",
        "since": "2023-01-01T00:00:00Z",
        "default_type": "future",
        "params": {"rsi_window": 20},
        "s3_url": "https://my-trading-bot.s3.ap-northeast-1.amazonaws.com/backtest/strategy/",
        "user_id": 1
    },
    "result": '{\n    "Start": "2023-01-01 00:00:00",\n    "End": "2023-11-28 08:00:00",\n    "Duration": "331 days 08:00:00",\n    "Exposure Time [%]": 82.08223311957752,\n    "Equity Final [$]": 1355324.8288,\n    "Equity Peak [$]": 1517576.6848,\n    "Return [%]": 35.532482879999996,\n    "Buy & Hold Return [%]": 124.00617171900525,\n    "Return (Ann.) [%]": 39.69092387742143,\n    "Volatility (Ann.) [%]": 57.32197021057216,\n    "Sharpe Ratio": 0.6924207896486616,\n    "Sortino Ratio": 1.6752137367792543,\n    "Calmar Ratio": 1.8197071583421327,\n    "Max. Drawdown [%]": -21.811709480542106,\n    "Avg. Drawdown [%]": -3.649393432304394,\n    "Max. Drawdown Duration": "137 days 13:00:00",\n    "Avg. Drawdown Duration": "8 days 05:00:00",\n    "# Trades": 2,\n    "Win Rate [%]": 50.0,\n    "Best Trade [%]": 36.58727154426143,\n    "Worst Trade [%]": -0.763650456607301,\n    "Max. Trade Duration": "270 days 20:00:00",\n    "Avg. Trade Duration": "135 days 23:00:00",\n    "Profit Factor": NaN,\n    "Expectancy [%]": 17.911810543827063,\n    "SQN": 0.9453312864480757,\n    "_strategy": "MaRsi(params=)",\n    "plot": "backtest/result/MaRsi_BTC-USDT_1h_20231128-082333.html"\n}',
}