#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Mohd Hafizuddin Bin Kamilin"
__version__ = "0.0.3"
__date__ = "23 May 2022"

"""
    Sample program to get custom kline/ohlc(v) interval data from binance

    + refactoring code structure into a function
    + added function to get all trade symbols

"""

# use python-binance API to interact with binance
from binance.exceptions import BinanceAPIException
from binance.client import Client
# and csv to write the kline data
import csv

# get all trade symbol from binance
def allTradeSymbols(client):

    info = client.get_all_tickers()
    symbols = list(map(lambda symbol: symbol['symbol'], info))

    return symbols

# get kline from binance
def getBinanceKline(client, symbol, interval):

    # all supported kline interval on binance
    # NOTE: the interval are hard coded
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
    chosenInterval = interval
    # sorted the list to ensure the sequence matched with the klineInterval's dict key sequence
    chosenInterval.sort()

    # specify the column for the csv file
    columns = [
        'open_time', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume',
        'ignore'
    ]

    try:

        # for every available kline interval
        for i in range(len(klineInterval)):

            if i == chosenInterval[0]:

                # remove the interval from the list of pending interval to do
                chosenInterval.pop(0)

                # get kline based on the chosen kline interval
                klines = client.get_historical_klines(symbol, klineInterval[i], "1 Jan, 2021")

                with open(klineInterval[i] + '.csv', 'w', newline='') as f:
                    write = csv.writer(f)
                    write.writerow(columns)
                    write.writerows(klines)

    # catch exception and get the error message
    except BinanceAPIException as e:

        print(e.status_code)
        print(e.message)


if __name__ == "__main__":

    # initialize the client class to interact with binance
    # NOTE: no need for an API key for ripping the historical data
    client = Client()

    # get all trade symbols
    symbols = allTradeSymbols(client=client)

    # specify the symbol for kline as btc//usdt
    symbol = 'BTCUSDT'
    # get 1h, 1d, 1M of kline interval
    interval = [5, 11, 14]

    # get all kline intervals and save it as csv
    getBinanceKline(client, symbol, interval)
