from .commons import NotFound, DetailedHTTPException


class BacktestResultNotFound(NotFound):
    DETAIL = "Backtest Result Not found in DB"
    
class SQSError(DetailedHTTPException):
    DETAIL = "SQS Error occrued"