import ccxt
import os

exchange_id = "binance"
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class(
    {
        "apiKey": os.getenv("BINANCE_API_KEY"),
        "secret": os.getenv("BINANCE_SECRET_KEY"),
        "timeout": 50000,
        "enableRateLimit": True,
        "options": {
            "defaultType": "future",
            "defaultMarginMode": "isolated",
            "watchBalance": "margin",
        },
    }
)
sandbox_mode = os.getenv("SANDBOX_MODE")
exchange.set_sandbox_mode(sandbox_mode)


def get_order_realizedPnl(order_id: int = 1216771770, symbol: str = "ETHUSDT"):
    order_info = exchange.fetch_my_trades(symbol=symbol, params={"orderId": order_id})
    if not order_info:
        return None
    return order_info[0]["info"]["realizedPnl"]