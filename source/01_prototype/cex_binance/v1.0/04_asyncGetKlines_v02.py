#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Mohd Hafizuddin Bin Kamilin"
__version__ = "0.4.2"
__date__ = "7 Jan 2022"

"""
    + TODO add method to limit the rate under 1200 per minute
    + TODO date range sanity test
    + TODO add write to csv

    # MEMO drop async from the the next code as it will always exceed 1200 rate per minute

"""

# use python-binance API to interact with binance
from binance.helpers import date_to_milliseconds
from binance import Client, AsyncClient
# filler for dummy task to keep the loop moving
from time import sleep
# using concurrent programming design
import asyncio

# refer to python-binance for update/change in supported interval
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

# get the data from binance
class GetAllBinanceData:

    def __init__(self, symbol: str, interval: str, start: str, end: None):

        # initalize the trading pair
        self.trading_pair = self.get_trading_pair(symbol=symbol)
        print("\nTrading pair: " + ', '.join(self.trading_pair) + "\n")
        # pass valid kline interval only (check if the parsed str for kline interval is correct or not)
        self.interval = (interval if interval in SUPPORTED_INTERVAL else None)
        # initialize the start and end time
        self.start = start
        self.end = end
        # initialize the sleep timer for dummy task
        self.timer = 10
        
        # sanity test
        if (self.trading_pair == []) and (self.interval is None):
            raise ValueError("Invalid trading pair and kline interval parsed to the class!") 
        elif (self.trading_pair == []):
            raise ValueError("Invalid trading pair parsed to the class!")
        elif (self.interval is None):
            raise ValueError("Invalid kline interval parsed to the class!")

    # get specific/all trading pair from binance
    def get_trading_pair(client: Client, symbol: str) -> list:

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

    # get kline based on the predefined kline interval
    # task the worker need to do when assigned with their turn
    async def get_historical_klines(self, client: AsyncClient):

        # get klines
        klines = await client.get_historical_klines(
            symbol=self.trading_pair.pop(),
            interval=self.interval,
            start_str=self.start,
            end_str=self.end
        )

        # send somewhere else
        RESULTS.append(klines)

    async def dummy_task(self):

        sleep(10)

    # main async wrapper fucntion
    async def amain(self) -> None:

        client = await AsyncClient.create()

        while self.trading_pair != []:

            await asyncio.gather(
                *(
                    self.get_historical_klines(client) if (
                        (len(self.trading_pair) != 0) and
                        # TODO this shit is not working
                        (int(client.response.headers["x-mbx-used-weight"]) < 1_000)
                    ) else self.dummy_task() for _ in range(len(self.trading_pair))
                )
            )

            await client.close_connection()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(GetAllBinanceData(symbol="usdt", interval="1m", start="2022-1-1 00:00:00", end="2022-2-1 00:00:00").amain())

    print("Result: \n" + str(RESULTS))
    