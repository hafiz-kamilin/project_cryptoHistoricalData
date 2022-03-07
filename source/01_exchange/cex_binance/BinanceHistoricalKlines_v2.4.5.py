#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Mohd Hafizuddin Bin Kamilin"
__version__ = "2.5.4"
__date__ = "13 Feb 2022"

"""
    1. Created a synchronous historical klines downloader for Binance CEX.
    2. Feature
       a) Get all/specific trading pairs
       b) Download the klines for specific trading pairs with custom interval
       c) Save the klines as csv/pickle/feather
       d) 10 simultaneous async download for the trading pair
    3. TODO
       a) Async download
       b) Aggtrade download

"""

# use python-binance API to interact with binance
from binance.client import Client
# data processing and saving as feather
import pandas as pd
# data saving as pickle
import pickle
# # data saving as csv
import csv

class BinanceHistoricalKlines:

    def __init__(self, symbol: str, interval: str, start: str, end: None) -> None:

        """
            1. initialize the parameters to get the klines,
            2. check if the parameters is valid, 
            3. and get the trading pair
        
        """

        # get specific/all trading pair from binance
        def get_trading_pair(symbol: str) -> list[str]:

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
            'open_time',
            'open',
            'high',
            'low',
            'close',
            'volume',
            'close_time',
            'quote_asset_volume',
            'number_of_trades',
            'taker_buy_base_asset_volume',
            'taker_buy_quote_asset_volume',
            'ignore'
        ]

         # initalize the trading pair
        self.trading_pair = get_trading_pair(symbol=symbol)
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

    def get_historical_klines(self) -> tuple[list, str]:

        """
            get the historical klines from the binance and return as tuple,
            which contain
            
            1. nested list (klines) 
            2. str (trading symbol)
        
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

    def save_to_file(self, format: str) -> None:

        """
        save the downloaded klines from binance as csv/feather/pickle
        NOTE: for the sake of simplicity, we call 
              self.get_historical_klines() function
              in here instead
        
        """

        for _ in range(len(self.trading_pair)):

            klines, symbol = self.get_historical_klines()

            if (format == "csv"):

                # write the column and klines as csv file
                with open(symbol + "_" + self.interval + ".csv", 'w', newline='') as f:
                    write = csv.writer(f)
                    write.writerow(self.columns)
                    write.writerows(klines)

            elif (format == "pickle"):

                with open(symbol + "_" + self.interval + ".pickle", 'wb') as handle:
                    pickle.dump(klines, handle, protocol=pickle.HIGHEST_PROTOCOL)

            elif (format == "feather"):

                # convert nested list into a dataframe
                df = pd.DataFrame(data=klines, columns=self.columns)
                # write the dataframe as feather file
                df.to_feather(symbol + "_" + self.interval + ".feather", compression="zstd")

if __name__ == "__main__":

    # initialize the BinanceHistoricalKlines class
    createHistoricalKlines = BinanceHistoricalKlines(
        symbol="ust",
        interval="1m",
        start="2022-1-1 00:00:00",
        end="2022-2-1 00:00:00"
    )

    # store the klines data as file
    createHistoricalKlines.save_to_file("feather")