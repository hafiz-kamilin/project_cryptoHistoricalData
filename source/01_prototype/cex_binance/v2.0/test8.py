#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Mohd Hafizuddin Bin Kamilin"
__version__ = "0.1.1"
__date__ = "23 Jan 2022"

"""
    Sample program to get a '1 minute' kline/ohlc(v) data from binance

"""

# use python-binance API to interact with binance
# and csv to write the kline data
from binance.client import Client
import csv

# initialize the client class to interact with binance
# NOTE: no need for an API key for ripping the historical data
client = Client()

# specify the symbol for kline as btc//usdt
SYMBOL = 'BTCUSDT'
# specify the column for the csv file
columns = [
    'open_time', 'open', 'high', 'low', 'close', 'volume',
    'close_time', 'quote_asset_volume', 'number_of_trades',
    'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume',
    'ignore'
]

# get kline in 1 minute interval
klines = client.get_historical_klines(
    symbol=SYMBOL,
    interval="1m",
    start_str="2021-1-1 00:00:00",
    end_str="2021-1-1 00:00:00"
)

with open('1m.csv', 'w', newline='') as f:
    write = csv.writer(f)
    write.writerow(columns)
    write.writerows(klines)
