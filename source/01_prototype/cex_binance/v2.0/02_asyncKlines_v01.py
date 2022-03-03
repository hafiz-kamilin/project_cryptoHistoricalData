#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Mohd Hafizuddin Bin Kamilin"
__version__ = "1.2.1"
__date__ = "3 March 2022"

"""
    + add logging feature
    + add async fetch historical klines

"""

# use python-binance API to interact with binance
from binance import Client, AsyncClient
# to get the current time in timestamp
from time import time
# data processing and saving as feather
import pandas as pd
# using concurrent programming design
import asyncio
# for logging and debuging purpose
import logging
# data saving as pickle
import pickle
# data saving as csv
import csv

class BinanceHistoricalKlines:

    def __init__(self, symbol: str, interval: str, start: str, end: None, include_leverage: bool, logged: bool) -> None:

        """
            1. initialize the parameters to get the klines,
            2. check if the parameters is valid, 
            3. and get the trading pair
        
        """

        # get specific/all trading pair from binance
        def get_trading_pair(symbol: str, include_leverage: bool) -> list[str]:

            """
                get trading pair from binance

                usage:
                1. get_trading_pair(symbol=None, include_leverage=False)
                   = get all available trading pair (excluding leveraged trading pair) from binance 
                2. get_trading_pair(symbol="USDT", include_leverage=False)
                   = get all USDT trading pair (excluding leveraged trading pair) from binance

            """

            # extract trading pairs information from binance
            info = Client().get_all_tickers()
            # filter the information to get the trading pair symbols only
            trading_pair = list(map(lambda pair: pair["symbol"], info))

            # remove leveraged trading pair (UP/DOWN) from the trading_pair
            if include_leverage is False:
                to_remove = []
                # find UP/DOWN trading pair
                for i in range(len(trading_pair)):
                    if ("DOWN" in trading_pair[i]) is True:
                        # save the element for the DOWN trading pair we found
                        to_remove.append(trading_pair[i])
                        # replace the "DOWN" str with "UP" to get the UP trading pair, and save it
                        to_remove.append(trading_pair[i].replace("DOWN", "UP"))
                # remove down token
                for element in to_remove:
                    trading_pair.remove(element)

            # if we want trading pair for specific symbol (e.g., ETH)
            if symbol is not None:
                # play safe; just in case someone forgot to capitalize the whole str
                symbol = symbol.upper()
                # create a list with a trading pairs that has the specific symbol only
                trading_pair = list(filter(lambda x: x.endswith(symbol), trading_pair))

            # return the trading pair
            return trading_pair

        # NOTE: refer to python-binance for update/change in supported interval
        supported_interval = {
            "1m",
            "3m",
            "5m",
            "30m",
            "1h",
            "2h",
            "4h",
            "6h",
            "8h",
            "12h",
            "1d",
            "3d",
            "1w",
            "1M"
        }
        # specify the column for the klines
        self.columns = [
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "number_of_trades",
            "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume",
            "ignore"
        ]

        # initalize the trading pair
        self.trading_pair = get_trading_pair(symbol=symbol, include_leverage=include_leverage)
        # pass valid kline interval only (check if the parsed str for kline interval is correct or not)
        self.interval = (interval if interval in supported_interval else None)
        # initialize the start and end time
        self.start = start
        self.end = end
        # initialize log
        self.logged = logged
        if self.logged is True:
            logging.basicConfig(filename='record.log', encoding='utf-8', level=logging.DEBUG, format='%(levelname)s \n%(message)s')

        # sanity test
        if (self.trading_pair == []) and (self.interval is None):
            raise ValueError("Invalid trading pair and kline interval parsed to the class!") 
        elif (self.trading_pair == []):
            raise ValueError("Invalid trading pair parsed to the class!")
        elif (self.interval is None):
            raise ValueError("Invalid kline interval parsed to the class!")

        print("\nGet historical klines data from Binance.\n")
        output_str = (
            " Initialization parameters"
            "\n  - Symbol: " + symbol +
            "\n  - Exclude leverage pair: " + str(include_leverage) +
            "\n  - Total trading pair: " + str(len(self.trading_pair)) +
            "\n  - Interval: " + interval +
            "\n  - Start time: " + start +
            "\n  - End time: " + end
        )
        print(output_str)

        # logging
        if self.logged is True:
            logging.info(" Timestamp: " + str(time()))
            logging.info(output_str)
            logging.info(
                " Trading pair: " + "\n  - " + "\n  - ".join(self.trading_pair)
            )

    async def get_historical_klines(self, symbol: str, start: str, end: str, tag: str, client: AsyncClient) -> tuple[list, str]:

        """
            get the historical klines from the binance and return as tuple,
            
            which contain
            1. nested list (klines) 
            2. identifier to know on which sequence we should append the result (tag)
        
        """

        # get kline based on the predefined kline interval
        klines = await client.get_historical_klines(
            symbol=symbol,
            interval=self.interval,
            start_str=start,
            end_str=end
        )

        return klines, tag

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
                with open(symbol + "_" + self.interval + ".csv", "w", newline="") as f:
                    write = csv.writer(f)
                    write.writerow(self.columns)
                    write.writerows(klines)

            elif (format == "pickle"):

                with open(symbol + "_" + self.interval + ".pickle", "wb") as handle:
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
        end="2022-2-1 00:00:00",
        include_leverage = False,
        logged=True
    )

    # store the klines data as file
    createHistoricalKlines.save_to_file("feather")