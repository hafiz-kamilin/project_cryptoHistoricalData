#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Mohd Hafizuddin Bin Kamilin"
__version__ = "0.0.2"
__date__ = "25 May 2022"

"""
    Sample program to get custom trading pair and timerange from binance via async

    + add get_trading_pair()

"""

# use python-binance API to interact with binance
from binance import Client, AsyncClient
# using concurrent programming design
import asyncio

RESULTS = []

# get the data from binance
class GetAllBinanceData:

    def __init__(self, symbol: str, workers_num: int = 10):

        # initalize the trading pair we want
        self.trading_pair = self.get_trading_pair(symbol=symbol)

        print("\nTrading pair: " + ', '.join(self.trading_pair) + "\n")

        # initialize the number of worker (hard coded)
        self.workers_num: int = workers_num
        # set the max number of worker in queue is 10
        self.task_q: asyncio.Queue = asyncio.Queue(maxsize=10)

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
            # filter the trading pair that has the specific symbol we want and return
            return list(filter(lambda x: x.endswith(symbol), trading_pair))

        else:
            # return all trade trading pair available in binance
            return trading_pair

    # distribute the trading pairs to the workers
    async def assign_trading_pair_to_worker(self):

        # assign each of the trading pair to the worker?
        for i in self.trading_pair:
            await self.task_q.put(i)

        # NOTE: wtf is this?
        for i in range(self.workers_num):
            await self.task_q.put(None)

    # get kline based on the predefined kline interval
    # task the worker need to do when assigned with their turn
    async def get_historical_klines(self, client: AsyncClient):

        while True:

            # wait for the trading pair to be assigned to the worker
            trading_pair = await self.task_q.get()

            # stop when there is no more trading pair to parse
            if trading_pair is None:
                break

            # get klines based on the predefined interval
            klines = await client.get_historical_klines(
                symbol=trading_pair,
                interval=AsyncClient.KLINE_INTERVAL_1MINUTE,
                start_str="2022-1-23 10:00:00",
                end_str="2022-1-23 10:01:00"
            )

            # send somewhere else
            RESULTS.append(klines)

    # main async wrapper fucntion
    async def amain(self) -> None:

        client = await AsyncClient.create()

        await asyncio.gather(
            self.assign_trading_pair_to_worker(),
            *[self.get_historical_klines(client) for _ in range(self.workers_num)]
        )

        await client.close_connection()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(GetAllBinanceData(symbol="usdc").amain())

    print("Result: \n" + str(RESULTS))
    