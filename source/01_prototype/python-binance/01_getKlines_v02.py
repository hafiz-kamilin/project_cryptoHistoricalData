#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Mohd Hafizuddin Bin Kamilin"
__version__ = "0.0.2"
__date__ = "23 May 2022"

"""
    Sample program to get custom kline/ohlc(v) interval data from binance

    + added catch exception
    + add a dictionary of applicable kline interval
    + add ability to choose which kline interval to use

"""

# use python-binance API to interact with binance
from binance.exceptions import BinanceAPIException
from binance.client import Client
# and csv to write the kline data
import csv

# initialize the client class to interact with binance
# NOTE: no need for an API key for ripping the historical data
client = Client()

# specify the symbol for kline as btc//usdt
SYMBOL = 'BTCUSDT'

# all supported kline interval on binance
klineInterval = {
    0 : Client.KLINE_INTERVAL_1MINUTE,
    1 : Client.KLINE_INTERVAL_3MINUTE,
    2 : Client.KLINE_INTERVAL_5MINUTE,
    3 : Client.KLINE_INTERVAL_15MINUTE,
    4 : Client.KLINE_INTERVAL_30MINUTE,
    5 : Client.KLINE_INTERVAL_1HOUR,
    6 : Client.KLINE_INTERVAL_2HOUR,
    7 : Client.KLINE_INTERVAL_4HOUR,
    8 : Client.KLINE_INTERVAL_6HOUR,
    9 : Client.KLINE_INTERVAL_8HOUR,
    10 : Client.KLINE_INTERVAL_12HOUR,
    11 : Client.KLINE_INTERVAL_1DAY,
    12 : Client.KLINE_INTERVAL_3DAY,
    13 : Client.KLINE_INTERVAL_1WEEK,
    14 : Client.KLINE_INTERVAL_1MONTH,
}
# chosen kline interval to get from binance historical data
# get 1h, 1d, 1M interval
chosenInterval = [5, 11, 14]
# sorted the list to ensure the sequence matched with the klineInterval's dict key
chosenInterval.sort()

# specify the column for the csv file
columns = [
    'open_time', 'open', 'high', 'low', 'close', 'volume',
    'close_time', 'quote_asset_volume', 'number_of_trades',
    'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume',
    'ignore'
]

try:

    i = 0
    # as long there is interval left to be parsed
    while len(chosenInterval) != 0:

        if i == chosenInterval[0]:

            # remove the interval from the list of pending interval to do
            chosenInterval.pop(0)

            # get kline based on the chosen kline interval
            klines = client.get_historical_klines(SYMBOL, klineInterval[i], "1 Jan, 2021")

            with open(klineInterval[i] + '.csv', 'w', newline='') as f:
                write = csv.writer(f)
                write.writerow(columns)
                write.writerows(klines)
        
        i += 1

# catch exception and get the error message
except BinanceAPIException as e:

    print(e.status_code)
    print(e.message)
