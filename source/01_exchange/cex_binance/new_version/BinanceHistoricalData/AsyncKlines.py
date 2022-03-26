#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Mohd Hafizuddin Bin Kamilin"
__version__ = "5.2.1"
__date__ = "26 March 2022"

# use python-binance API to interact with binance
from binance import Client, AsyncClient
# to get the current datetime
from datetime import datetime
# to interact with binance-api via concurrent klines fetch
import asyncio
# for logging and debuging purpose
import logging
# measure the time taken to fetch the klines
import time

# custom libraries
from BinanceHistoricalData.companion_code.get_trading_pairs import get_trading_pairs
from BinanceHistoricalData.companion_code.time_splitter import time_splitter
from BinanceHistoricalData.companion_code.save_to_file import save_to_file

class AsyncKlines:

    def __init__(self, symbol: str, interval: str, start: str, end: None, include_leverage: bool, file_format: str, logged: bool) -> None:

        fetch_klines = self.FetchKlines(
            # trading pair
            symbol=symbol,
            # klines interval
            interval=interval,
            # start-end datetime (UTC)
            start=start,
            end=end,
            # include/exclude leveraged trading pair
            include_leverage=include_leverage,
            # we can choose either "csv", "pickle" or "feather" to save the klines
            file_format=file_format,
            # option to enable/disable logging
            logged=logged
        )

        loop = asyncio.get_event_loop()
        loop.run_until_complete(fetch_klines.amain())

    class FetchKlines:

        def __init__(self, symbol: str, interval: str, start: str, end: None, include_leverage: bool, file_format: str, logged: bool) -> None:

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
            self.converted_interval = {
                "1m": 1 * 60,
                "3m": 3 * 60,
                "5m": 5 * 60,
                "30m": 30 * 60,
                "1h": 60 * 60,
                "2h": 2 * 60 * 60,
                "4h": 4 * 60 * 60,
                "6h": 6 * 60 * 60,
                "8h": 8 * 60 * 60,
                "12h": 12 * 60 * 60,
                "1d": 24 * 60 * 60,
                "3d": 3 * 24 * 60 * 60,
                "1w": 7 * 24 * 60 * 60,
                "1M": 4 * 7 * 24 * 60 * 60
            }

            # 1 day     86,400 s  →  86,400 timestamp  →  86,400,000 binance's timestamp
            # 1 hour    3,600 s   →  3,600 timestamp   →  3,600,000 binance's timestamp
            # 1 minute  60 s      →  60 timestamp      →  60,000 binance's timestamp

            timestamp_in_1m = 60
            # NOTE: (timestamp for 1 minute) * 60 minutes * 24 hours * 7 days * 4 weeks * 10 months
            #       based on the previous finding, we can only fetch 1 month worth of data via 10 concurrent running fetch function.
            #       thus, we will only fetch max 10 months of data with 10~20 maximum of concurrent running fetch function
            self.duration_limit = timestamp_in_1m * 60 * 24 * 7 * 4 * 10
            # set how many concurrent fetching function to run
            self.concurrent_limit = 10

            # initialize dictionary to append the aggregated, unprocessed results
            self.aggregated_result = {}

            # initalize the trading pairs
            self.trading_pairs = get_trading_pairs(symbol=symbol, include_leverage=include_leverage)
            # pass valid kline interval only (check if the parsed str for kline interval is correct or not)
            self.interval = (interval if interval in supported_interval else None)
            # initialize the start and end time
            self.start = start
            self.end = end
            # initialize the file format chosen to save the klines
            self.file_format = file_format

            # initialize log
            self.logged = logged
            if self.logged is True:
                logging.basicConfig(
                    filename="record_historicalKlines.log",
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

            # display the fetching parameters to the user
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
                logging.info(" Timestamp: " + str(datetime.now()))
                logging.info(output_str)
                logging.info(
                    " Trading pairs: " + "\n  - " + "\n  - ".join(self.trading_pairs)
                )

        async def get_historical_klines(self, symbol: str, start: str, end: str, sequence: int) -> None:

            """
                fetch the historical klines from binance and save it into a dictionary (self.aggregated_result)
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
            request_weight = Client().response.headers["x-mbx-used-weight"]
            if self.logged is True:
                # binance's max total request weight is 1200
                if int(request_weight) <= 1200:
                    logging.debug(
                        "  - Estimated request weight consumed: " + request_weight
                    )
                    print("  - Current requests weight: " + request_weight)
                else:
                    logging.warning(
                        "  - Exceeded 1200 request weight limit: " + request_weight
                    )
                    print("  - Exceeded requests weight: " + request_weight)
            
            # save the fetched klines into the dictionary
            self.aggregated_result[sequence] = klines

        async def amain(self) -> None:

            # get the splitted time duration to fetch the klines
            splitted_start, splitted_end, delay = time_splitter(
                start=self.start,
                end=self.end,
                interval_value = self.converted_interval[self.interval],
                duration_limit=self.duration_limit,
                concurrent_limit=self.concurrent_limit
            )
            # initialize async client
            client = await AsyncClient.create()

            # get the klines for each of the trading pairs, one by one
            for pair in self.trading_pairs:

                if self.logged is True:
                    logging.debug(
                        "  - Trading pair: " + pair
                    )
                print("\n Retrieving klines for " + pair)
                
                # store the fetched klines
                rearranged_klines = []
                # record the initial time
                start_time = time.time()

                # get the number of segment
                segment = len(splitted_start)

                # for each chunk of time duration
                for i in range(segment):

                    print_log = "  - Fetch segment " + str(i + 1) + " (" + str(segment) + ") with " + str(len(splitted_start[i])) + " concurrent"
                    print(print_log)
                    if self.logged is True:
                        logging.info(
                            print_log
                        )

                    # gather concurrent function to fetch the klines
                    await asyncio.gather(
                        *(
                            self.get_historical_klines(
                                symbol=pair,
                                start=splitted_start[i][j],
                                end=splitted_end[i][j],
                                # use sequence as a dictionary key to know how to arrange the klines
                                sequence=j
                            ) for j in range(len(splitted_end[i]))
                        )
                    )

                    await client.close_connection()

                    # rearrange the dictionary into a list
                    # NOTE: arrange in ascending order based on the aggregated_result's key
                    for k in range(len(self.aggregated_result)):
                        for l in range(len(self.aggregated_result[k])):
                            rearranged_klines.append(self.aggregated_result[k][l])

                    self.aggregated_result = {}

                    # if the timerange is really huge, add 10 s delay before fetching again to prevent exceeding the weight limit
                    if (delay is True) and (i < segment - 1):
                        time.sleep(10)
                        print("  - Wait: 10 s")
                        if self.logged is True:
                            logging.info(
                                "  - Wait: 10 s"
                            )

                # measure the time taken to fetch a single trading pair
                end_time = time.time() - start_time
                print_log = "  - Time taken: " + str(end_time) + " s"
                print(print_log)
                if self.logged is True:
                    logging.info(
                        print_log
                    )

                if rearranged_klines != []:
                    # write the fetched klines into the file
                    print("  - Writing " + pair + " klines to file...")
                    save_to_file(
                        file_format=self.file_format,
                        pair=pair,
                        start=self.start,
                        end=self.end,
                        interval=self.interval,
                        rearranged_klines=rearranged_klines
                    )
                    if self.logged is True:
                        logging.info(
                            "  - Save the fetched klines to file"
                        )
                else:
                    print("  - No klines data found...")
                    if self.logged is True:
                        logging.info(
                            "  - No klines data to fetch"
                        )
        
            print("\nCompleted\n")
