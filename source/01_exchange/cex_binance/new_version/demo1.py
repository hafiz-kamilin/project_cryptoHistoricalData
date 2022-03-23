# get klines

from binance.client import Client
from time import time
import csv

client = Client()

columns = [
    'open_time', 'open', 'high', 'low', 'close', 'volume',
    'close_time', 'quote_asset_volume', 'number_of_trades',
    'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume',
    'ignore'
]

time_start = time()
klines = client.get_historical_klines("BNBUSDT", '5m', "2021-1-1 00:00:00", "2021-1-1 00:05:00")
print("  - Time taken: " + str(time() - time_start) + " s")
with open('1m.csv', 'w', newline='') as f:
    write = csv.writer(f)
    write.writerow(columns)
    write.writerows(klines)
