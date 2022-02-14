# SOURCE: https://stackoverflow.com/a/69452152

import binance
import time

# tqdm not necessary, is only used for showing progress during klines iteration
from tqdm import tqdm

def multiple_klines(quote_currency: str) -> dict:
    klines = {}

    # You don't need API key/secret for this type of requets
    client = binance.Client()

    # Extract trading pairs from exchange information
    exchange_info = client.get_exchange_info()
    symbols = [x['symbol'] for x in exchange_info['symbols']]

    # Filter list
    selected_symbols = list(filter(lambda x: x.endswith(quote_currency), symbols))

    # Iterate over filtered list of trading pairs
    for symbol in tqdm(selected_symbols):
        klines[symbol] = client.get_historical_klines(
            symbol, client.KLINE_INTERVAL_12HOUR,
            "1 Jan, 2021", "18 Sep, 2021"
        )

        # Prevent exceeding rate limit:
        if int(client.response.headers['x-mbx-used-weight-1m']) > 1_000:
            print('Pausing for 30 seconds...')
            time.sleep(30)

    return klines

klines_dict = multiple_klines('USDT')