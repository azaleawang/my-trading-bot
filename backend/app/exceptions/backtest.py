from .commons import NotFound


class BacktestResultNotFound(NotFound):
    DETAIL = "Backtest Result Not found in DB"