import ccxt
import pandas as pd
import time
# https://api.binance.com/api/v3/klines?symbol=ETHUSDT&interval=4h&limit=500
# default config


def fetch_ohlcv(exchange, symbol, t_frame, since):
    limit = 500  # Maximum number of data points per call
    ohlcv = []
    while True:
        try:
            new_data = exchange.fetch_ohlcv(symbol, t_frame, since, limit)
            if len(new_data) == 0:
                break
            ohlcv.extend(new_data)
            since = new_data[-1][0] + 1
            time.sleep(exchange.rateLimit / 1000)  # Respect rate limit
        except ccxt.NetworkError as e:
            print(f'Network error: {e}')
            time.sleep(1)
        except ccxt.ExchangeError as e:
            print(f'Exchange error: {e}')
            break
        except Exception as e:
            print(f'Error: {e}')
            break
    return ohlcv



def history_data(exch='binance', symbols=['ETH/USDT'], t_frame='4h', 
                    since='2023-01-01T00:00:00Z', default_type='future', sandbox_mode=True):        
    
    # Initialize exchange
    try:
        exchange = getattr(ccxt, exch)(
            {
                'enableRateLimit': True,
                'options': {
                    'defaultType': default_type,
                }
            }
        )

        if hasattr(exchange, 'set_sandbox_mode'):
            exchange.set_sandbox_mode(sandbox_mode)

    except AttributeError:
        print(f'Exchange "{exch}" not found.')
        quit()

    # Check for OHLCV support
    if not exchange.has["fetchOHLCV"]:
        print(f'{exch} does not support OHLCV data.')
        quit()

    # Load markets
    exchange.load_markets()

    # Define header for DataFrame
    header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
    df_all = pd.DataFrame()

    # Function to fetch OHLCV

    # Fetch data for each symbol
    for symbol in symbols:
        if symbol not in exchange.symbols:
            print(f'Symbol {symbol} not found in {exch}.')
            continue

        print(f'Fetching historical data for {symbol}...')
        since_timestamp = exchange.parse8601(since)
        ohlcv = fetch_ohlcv(exchange, symbol, t_frame, since_timestamp)
        
        if ohlcv:
            symbol_df = pd.DataFrame(ohlcv, columns=header).set_index('Timestamp')
            symbol_df['Symbol'] = symbol
            df_all = pd.concat([df_all, symbol_df])

    # Convert timestamp to datetime
    df_all.index = pd.to_datetime(df_all.index, unit='ms')

    # Save to CSV
    symb = symbols[0].replace('/', '')
    
    filename = f'{symb}_{exch}_fdata.csv'
    df_all.to_csv(filename)
    print(f'{symbols} saved to {filename}')
    return df_all
    
# history_data()