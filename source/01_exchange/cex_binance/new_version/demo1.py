# get klines

from binance.client import Client
import csv

client = Client()

columns = [
    'open_time', 'open', 'high', 'low', 'close', 'volume',
    'close_time', 'quote_asset_volume', 'number_of_trades',
    'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume',
    'ignore'
]

klines = client.get_historical_klines("LUNAUST", '1m', "2022-1-1 00:00:00", "2022-3-1 00:00:00")

with open('1m.csv', 'w', newline='') as f:
    write = csv.writer(f)
    write.writerow(columns)
    write.writerows(klines)
