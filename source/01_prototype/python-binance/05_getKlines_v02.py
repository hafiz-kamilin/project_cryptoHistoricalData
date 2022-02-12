#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Mohd Hafizuddin Bin Kamilin"
__version__ = "0.5.2"
__date__ = "12 Feb 2022"

# use python-binance API to interact with binance
from binance.client import Client
# provides runtime support for type hints
from typing import Tuple
# data processing with panda
import pandas as pd
# and csv to write the kline data
import csv

class BinanceHistoricalKlines:

    def __init__(self, symbol: str, interval: str, start: str, end: None) -> None:

        """
            initializing the variables and check if the parsed variables to class
            passed the sanity test
        
        """

        # NOTE: refer to python-binance for update/change in supported interval
        supported_interval = {
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
        # specify the column for the klines
        self.columns = [
            'open_time', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume',
            'ignore'
        ]


        # initalize the trading pair
        self.trading_pair = self.get_trading_pair(symbol=symbol)
        print("\nTrading pair: " + ', '.join(self.trading_pair))
        # pass valid kline interval only (check if the parsed str for kline interval is correct or not)
        self.interval = (interval if interval in supported_interval else None)
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

    # get the historical klines from binance
    def get_binance_historical_klines(self) -> Tuple[list, str]:

        """
            get the historical klines from the self. parameters and return as tuple,
            which contain nested list (klines) and str (trading symbol)
        
        """

        # remove the trading pair to be processed from the queue
        symbol = self.trading_pair.pop()

        # get klines
        klines = Client().get_historical_klines(
            symbol=symbol,
            interval=self.interval,
            start_str=self.start,
            end_str=self.end
        )

        return klines, symbol

    # save the klines as csv
    def save_to_csv(self) -> None:

        klines, symbol = self.get_binance_historical_klines()

        # write the column and klines as csv file
        with open(symbol + '.csv', 'w', newline='') as f:
            write = csv.writer(f)
            write.writerow(self.columns)
            write.writerows(klines)

    # save the klines as feather
    def save_to_feather(self) -> None:

        klines, symbol = self.get_binance_historical_klines()

        # convert nested list into a dataframe
        df = pd.DataFrame(data=klines, columns=self.columns)
        # write the dataframe as feather file
        df.to_feather(symbol + ".feather")

if __name__ == "__main__":

    createHistoricalKlines = BinanceHistoricalKlines(
        symbol="BNBUSDT",
        interval="1m",
        start="2022-1-1 00:00:00",
        end="2022-1-31 00:00:00"
    )

    createHistoricalKlines.save_to_feather()
    createHistoricalKlines.save_to_csv()