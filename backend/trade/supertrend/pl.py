import ccxt
import config
from pprint import pprint
exchange_id = "binance"
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class(
    {
        "apiKey": config.BINANCE_API_KEY,
        "secret": config.BINANCE_SECRET_KEY,
        "timeout": 50000,
        "enableRateLimit": True,
        "options": {
            "defaultType": "future",
            'defaultMarginMode': 'isolated',
            'watchBalance': 'margin',
        },
    }
)

def table(values):
    first = values[0]
    keys = list(first.keys()) if isinstance(first, dict) else range(0, len(first))
    widths = [max([len(str(v[k])) for v in values]) for k in keys]
    string = ' | '.join(['{:<' + str(w) + '}' for w in widths])
    return "\n".join([string.format(*[str(v[k]) for k in keys]) for v in values])

sandbox_mode = config.SANDBOX_MODE
exchange.set_sandbox_mode(sandbox_mode)
# balance = exchange.fetch_balance()
# print(balance)


markets = exchange.load_markets()

symbol = 'BTC/USDT'  # YOUR SYMBOL HERE
market = exchange.market(symbol)
# exchange.verbose = True

print('----------------------------------------------------------------------')

# print('Fetching your balance:')
# response = exchange.fetch_balance()
# pprint(response['total'])  # make sure you have enough futures margin...
# pprint(response['info'])  # more details

print('----------------------------------------------------------------------')

# https://binance-docs.github.io/apidocs/futures/en/#position-information-v2-user_data

print('Getting your positions:')
# response = exchange.fapiPrivateV2_get_positionrisk()
# print(table(response))

print('----------------------------------------------------------------------')

# https://binance-docs.github.io/apidocs/futures/en/#change-position-mode-trade

# print('Getting your current position mode (One-way or Hedge Mode):')
# response = exchange.fapiPrivate_get_positionside_dual()
# if response['dualSidePosition']:
#     print('You are in Hedge Mode')
# else:
#     print('You are in One-way Mode')

# print('----------------------------------------------------------------------')


symbol = 'ETHUSDT'  # Replace with your desired futures symbol
# open_orders = exchange.fetch_open_orders(symbol=symbol)
order_id = 1216771770
# order_info = exchange.fetchOrder(order_id, symbol)
order_info = exchange.fetch_my_trades(symbol=symbol, params = {"orderId": order_id})
print("realizedPnl", order_info[0]["info"]["realizedPnl"])
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

