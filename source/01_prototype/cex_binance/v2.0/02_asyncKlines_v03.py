#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Mohd Hafizuddin Bin Kamilin"
__version__ = "1.2.2"
__date__ = "4 March 2022"

"""
    + improved the async to download multiple trading pairs

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
            3. and get the trading pairs
        
        """

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

        # initialize the active number of concurrent function to fetch the klines
        # NOTE: hard limit for active number of concurrent function to fetch the klines
        #       is set to 10, and the average weight taken for 10 concurrent fetching 
        #       function is around 450-950 for 1m interval;
        #       the max limit allowed by binance is 1200.
        self.concurrent_limit = 10
        # calculate how many minutes in approximately 1 month
        # NOTE: (timestamp for 1 minute) * 60 minutes * 24 hours * 7 days * 4 weeks
        self.timestamp_in_1m = 60000
        self.divisor = self.timestamp_in_1m * 60 * 24 * 7 * 4
        # initialize dictionary to append the aggregated, unprocessed results
        self.raw_results = {}

        # initalize the trading pairs
        self.trading_pairs = self.get_trading_pairs(symbol=symbol, include_leverage=include_leverage)
        # pass valid kline interval only (check if the parsed str for kline interval is correct or not)
        self.interval = (interval if interval in supported_interval else None)
        # initialize the start and end time
        self.start = start
        self.end = end
        # initialize log
        self.logged = logged
        if self.logged is True:
            logging.basicConfig(
                filename="record.log",
                filemode = "w+",
                encoding="utf-8",
                level=logging.DEBUG,
                format="%(levelname)s \n%(message)s"
            )
            # disable logging for the imported library; we want to focus only on the main program
            list_of_logger_to_ignore = list(logging.Logger.manager.loggerDict.keys())
            for logger in list_of_logger_to_ignore:
                logging.getLogger(logger).disabled = True

        # sanity tests
        if (self.trading_pairs == []) and (self.interval is None):
            raise ValueError("Invalid symbol and kline interval parsed to the class!") 
        elif (self.trading_pairs == []):
            raise ValueError("Invalid symbol parsed to the class!")
        elif (self.interval is None):
            raise ValueError("Invalid kline interval parsed to the class!")

        print("\nGet historical klines data from Binance.\n")
        output_str = (
            " Initialization parameters"
            "\n  - Symbol: " + symbol +
            "\n  - Exclude leverage pairs: " + str(include_leverage) +
            "\n  - Total trading pairs: " + str(len(self.trading_pairs)) +
            "\n  - Interval: " + interval +
            "\n  - Start time: " + start +
            "\n  - End time: " + end
        )
        print(output_str)

        # log the parsed/processed parameters
        if self.logged is True:
            logging.info(" Timestamp: " + str(time()))
            logging.info(output_str)
            logging.info(
                " Trading pairs: " + "\n  - " + "\n  - ".join(self.trading_pairs)
            )

    def get_trading_pairs(self, symbol: str, include_leverage: bool) -> list[str]:

        """
            get specific/all trading pairs from binance

            usage:
            1. get_trading_pairs(symbol=None, include_leverage=False)
                = get all available trading pairs (excluding leveraged trading pairs) from binance 
            2. get_trading_pairs(symbol="USDT", include_leverage=False)
                = get all USDT trading pairs (excluding leveraged trading pairs) from binance

        """

        # extract trading pairs information from binance
        info = Client().get_all_tickers()
        # filter the information to get the trading pairs symbols only
        trading_pairs = list(map(lambda pair: pair["symbol"], info))

        # remove leveraged trading pairs (UP/DOWN) from the trading_pairs
        if include_leverage is False:
            to_remove = []
            # find UP/DOWN trading pairs
            for i in range(len(trading_pairs)):
                if ("DOWN" in trading_pairs[i]) is True:
                    # save the element for the DOWN trading pairs we found
                    to_remove.append(trading_pairs[i])
                    # replace the "DOWN" str with "UP" to get the UP trading pairs, and save it
                    to_remove.append(trading_pairs[i].replace("DOWN", "UP"))
            # remove down token
            for element in to_remove:
                trading_pairs.remove(element)

        # if we want trading pairs for specific symbol (e.g., ETH)
        if symbol is not None:
            # play safe; just in case someone forgot to capitalize the whole str
            symbol = symbol.upper()
            # create a list with a trading pairs that has the specific symbol only
            trading_pairs = list(filter(lambda x: x.endswith(symbol), trading_pairs))

        # return the trading pairs
        return trading_pairs

    def time_splitter(self) -> tuple[list[list[int]], list[list[int]]]:

        """
        slice the time according to the divisor and group as chuck 
        NOTE: we need to splice time duration specified by the user into month and
              group it as a chunk of 10 months, to prevent exceeding 1200 request
              weight allowed by binance; 10 months → 10 concurrent fetch call where
              each retrieve 1 month worth of data → 450-950 request weight
        
        """

        def divide_chunks(l):

            """
            divide the splitted time (splitted_start and splitted_end) into a
            nested list
            NOTE: the concurrent function to fetch the klines will read the nested
                  list and fetch the klines based on the defined start/end time

            """
            
            # looping till length l
            for i in range(0, len(l), self.concurrent_limit): 
                yield l[i:i + self.concurrent_limit]

        splitted_start = []
        splitted_end = []

        time_duration = self.end - self.start

        # if the time_duration is larger than the divisor
        if time_duration > self.divisor:

            # find out how many times we can divide the time duration with the divisor and its remainder
            quotient = int(time_duration / self.divisor)
            remainder = time_duration % self.divisor

            for i in range(quotient):

                # append the newly calculated start time to the splitted_start
                if i == 0:
                    splitted_start.append(self.start)
                else:
                    splitted_start.append(self.start + self.timestamp_in_1m)

                # append the newly calculated end time to the splitted_end
                self.start += self.divisor
                splitted_end.append(self.start)

                print(str(splitted_start[i]) + " - " + str(splitted_end[i]))

            # if there is a remainder from the division
            if remainder != 0:

                # append the newly calculated start time to the splitted_start
                splitted_start.append(self.start + self.timestamp_in_1m)

                # append the newly calculated end time to the splitted_end
                self.start += remainder
                splitted_end.append(self.start)

                print(str(splitted_start[-1]) + " - " + str(splitted_end[-1]))

        # if the time_duration is equal or less than the divisor
        else:
            
            # no calculation needed
            splitted_start.append(self.start)
            splitted_end.append(self.end)

        splitted_start = list(divide_chunks(splitted_start))
        splitted_end = list(divide_chunks(splitted_end))

        return splitted_start, splitted_end

    async def get_historical_klines(self, symbol: str, start: str, end: str, sequence: str) -> None:

        """
            fetch the historical klines from binance and save it into a dictionary (self.raw_results)
            NOTE: the data on the dictionary need to be joined and cleaned up!
        
        """

        # fetch the klines for the specified symbol, interval, and timeframe
        klines = await AsyncClient().get_historical_klines(
            symbol=symbol,
            interval=self.interval,
            start_str=start,
            end_str=end
        )

        # log the current total request weight consumed
        if self.logged is True:
            logging.debug(
                "  - Estimated total request weight consumed: " + Client().response.headers["x-mbx-used-weight"]
            )

        # save the fetched klines into the dictionary
        self.raw_results[sequence] = klines

    async def amain(self) -> None:

        splitted_start, splitted_end = self.time_splitter()

        for pair in self.trading_pairs:

            for i in range(len(splitted_start)):

                for j in range(len(splitted_start[i])):

                    client = await AsyncClient.create()

                    await asyncio.gather(
                        *(
                            self.get_historical_klines(
                                symbol=pair,
                                start=splitted_start[i][j],
                                end=splitted_end[i][j],
                                sequence=sequence
                            # the number of running concurrent function follow the self.concurrent_limit
                            ) for sequence in range(self.concurrent_limit)
                        )
                    )

                    await client.close_connection()

    # def save_to_file(self, format: str) -> None:

    #     """
    #     save the downloaded klines from binance as csv/feather/pickle
    #     NOTE: for the sake of simplicity, we call 
    #           self.get_historical_klines() function
    #           in here instead
        
    #     """

    # # specify the column for the klines
    # self.columns = [
    #     "open_time",
    #     "open",
    #     "high",
    #     "low",
    #     "close",
    #     "volume",
    #     "close_time",
    #     "quote_asset_volume",
    #     "number_of_trades",
    #     "taker_buy_base_asset_volume",
    #     "taker_buy_quote_asset_volume",
    #     "ignore"
    # ]


    #     for _ in range(len(self.trading_pairs)):

    #         klines, symbol = self.get_historical_klines()

    #         if (format == "csv"):

    #             # write the column and klines as csv file
    #             with open(symbol + "_" + self.interval + ".csv", "w", newline="") as f:
    #                 write = csv.writer(f)
    #                 write.writerow(self.columns)
    #                 write.writerows(klines)

    #         elif (format == "pickle"):

    #             with open(symbol + "_" + self.interval + ".pickle", "wb") as handle:
    #                 pickle.dump(klines, handle, protocol=pickle.HIGHEST_PROTOCOL)

    #         elif (format == "feather"):

    #             # convert nested list into a dataframe
    #             df = pd.DataFrame(data=klines, columns=self.columns)
    #             # write the dataframe as feather file
    #             df.to_feather(symbol + "_" + self.interval + ".feather", compression="zstd")

if __name__ == "__main__":

    # initialize the BinanceHistoricalKlines class
    createHistoricalKlines = BinanceHistoricalKlines(
        symbol="BTCUSDT",
        interval="1m",
        start="2022-1-1 00:00:00",
        end="2022-3-1 00:00:00",
        include_leverage = False,
        logged=True
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(createHistoricalKlines.amain())
    print("")