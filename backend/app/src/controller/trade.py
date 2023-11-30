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


# (標記價格-price) * leverage * amount --> not closed
# closed:
# for order in open_orders:
#     entry_price = order['price']
#     amount = order['amount']
#     # Fetch current market price
#     ticker = exchange.fetch_ticker(order['symbol'])
#     current_price = ticker['last']
#     # Calculate P&L
#     profit_loss = (current_price - entry_price) * amount
#     print(f"Order {order['id']} P&L: {profit_loss}")
# def calculate_order_profit_loss(order):
#     # Assuming average price is the entry price and 'price' is the exit price
#     entry_price = float(order['average'])  # or order['info']['avgPrice']
#     exit_price = float(order['price'])
#     quantity = float(order['filled'])

#     # P&L Calculation (for a BUY order)
#     if order['side'] == 'buy':
#         profit_loss = (exit_price - entry_price) * quantity
#     # If it's a SELL order, reverse the calculation
#     elif order['side'] == 'sell':
#         profit_loss = (entry_price - exit_price) * quantity
#     else:
#         profit_loss = 0  # Default case

#     return profit_loss

# def calculate_total_profit(orders):
#     total_profit = 0
#     for order in orders:
#         if order['status'] == 'closed':  # Only include closed orders
#             total_profit += calculate_order_profit_loss(order)
#     return total_profit

# orders = [...]  # Your list of order data
# total_profit = calculate_total_profit(orders)
# print("Total Profit:", total_profit)
