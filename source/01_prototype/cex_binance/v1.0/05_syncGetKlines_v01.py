#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Mohd Hafizuddin Bin Kamilin"
__version__ = "0.5.1"
__date__ = "10 Feb 2022"

# use python-binance API to interact with binance
from typing import Tuple
from binance.client import Client
# and csv to write the kline data
import csv

# NOTE: refer to python-binance for update/change in supported interval
SUPPORTED_INTERVAL = {
    '1m',
    '3m',
    '5m',
    '30m',
    '1h',
    '2h',
    '4h',
    '6h',
    '8h',
    '12h',
    '1d',
    '3d',
    '1w',
    '1M'
}
# store the result
RESULTS = []

class BinanceHistoricalKlines:

    def __init__(self, symbol: str, interval: str, start: str, end: None):

        # initalize the trading pair
        self.trading_pair = self.get_trading_pair(symbol=symbol)
        print("\nTrading pair: " + ', '.join(self.trading_pair))
        # pass valid kline interval only (check if the parsed str for kline interval is correct or not)
        self.interval = (interval if interval in SUPPORTED_INTERVAL else None)
        # initialize the start and end time
        self.start = start
        self.end = end

        # sanity test
        if (self.trading_pair == []) and (self.interval is None):
            raise ValueError("Invalid trading pair and kline interval parsed to the class!") 
        elif (self.trading_pair == []):
            raise ValueError("Invalid trading pair parsed to the class!")
        elif (self.interval is None):
            raise ValueError("Invalid kline interval parsed to the class!")

    # get specific/all trading pair from binance
    def get_trading_pair(self, symbol: str) -> list[str]:

        """
        get trading pair from binance

        usage:
        1. get_trading_pair(pairing=None)
        - get all available trading pair from binance 
        2. get_trading_pair(pairing="USDT")
        - get all USDT trading pair from binance

        """

        # extract trading pairs information from binance
        info = Client().get_all_tickers()
        # filter the information to get the trading pair symbols only
        trading_pair = list(map(lambda pair: pair['symbol'], info))

        # if we want trading pair for specific symbol (e.g., ETH)
        if symbol is not None:
            # play safe; just in case someone forgot to capitalize the whole str
            symbol = symbol.upper()
            # return trading pair that has the specific symbol
            return list(filter(lambda x: x.endswith(symbol), trading_pair))
        else:
            # return all trade trading pair
            return trading_pair

    def get_binance_historical_klines(self) -> Tuple[list, str]:

        symbol = self.trading_pair.pop()

        # get klines
        klines = Client().get_historical_klines(
            symbol=symbol,
            interval=self.interval,
            start_str=self.start,
            end_str=self.end
        )

        return klines, symbol

    def save_to_csv(self) -> None:

        # specify the column for the csv file
        columns = [
            'open_time', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume',
            'ignore'
        ]

        klines, symbol = self.get_binance_historical_klines()

        with open(symbol + '.csv', 'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(columns)
            write.writerows(klines)

if __name__ == "__main__":

    createHistoricalKlines = BinanceHistoricalKlines(
        symbol="BNBUSDT",
        interval="1m",
        start="2022-1-23 10:00:00",
        end="2022-1-23 10:01:00"
    )

    createHistoricalKlines.save_to_csv()