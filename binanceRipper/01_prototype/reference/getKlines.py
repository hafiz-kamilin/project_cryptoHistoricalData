# SOURCE: https://stackoverflow.com/questions/68260770/binance-api-store-kline-candlestick-data-to-csv-file

from binance.client import Client
import csv

client = Client()

SYMBOL = 'BTCUSDT'

columns = [
    'open_time', 'open', 'high', 'low', 'close', 'volume',
    'close_time', 'quote_asset_volume', 'number_of_trades',
    'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume',
    'ignore'
]

klines = client.get_historical_klines(SYMBOL, Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2021")

with open('1week.csv', 'w', newline='') as f:
    write = csv.writer(f)
    write.writerow(columns)
    write.writerows(klines)
