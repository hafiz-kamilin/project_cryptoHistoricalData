#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Mohd Hafizuddin Bin Kamilin"
__version__ = "0.0.1"
__date__ = "24 May 2022"

"""
    Sample program to get predefined trading pair and timerange from binance via async

"""

# use python-binance API to interact with binance
from binance import AsyncClient
# using concurrent programming design
import asyncio

RESULTS = []  # let's store all results here

# get the data from binance
class GetAllBinanceData:

    def __init__(self, workers_num: int = 10):

        # initialize the number of worker (hard coded)
        self.workers_num: int = workers_num
        # set the max number of worker in queue is 10
        self.task_q: asyncio.Queue = asyncio.Queue(maxsize=10)

    # get symbols and distribute them among workers
    async def get_symbols_from_somewhere(self):

        # predefined symbols
        symbols = ["BNBBTC", "ETHBTC", "NEOBTC"]

        # assign each of the symbol to the worker?
        for i in symbols:
            await self.task_q.put(i)
        # NOTE: wtf is this?
        for i in range(self.workers_num):
            await self.task_q.put(None)

    # get kline based on the predefined kline interval
    # task the worker need to do when assigned with their turn
    async def get_historical_klines(self, client: AsyncClient):

        while True:

            # wait for the task assigned to the worker
            symbol = await self.task_q.get()

            # stop when there is no more symbol to parse
            if symbol is None:
                break

            # get kline based on the predefined kline interval
            klines = await client.get_historical_klines(
                symbol=symbol,
                interval=AsyncClient.KLINE_INTERVAL_1MINUTE,
                start_str="2021-11-23 10:00:00",
                end_str="2021-11-23 10:01:00"
            )

            print(klines)  # just print
            RESULTS.append(klines)  # send somewhere else

    # main async wrapper fucntion
    async def amain(self) -> None:

        client = await AsyncClient.create()

        await asyncio.gather(
            self.get_symbols_from_somewhere(),
            *[self.get_historical_klines(client) for _ in range(self.workers_num)]
        )

        await client.close_connection()


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(GetAllBinanceData().amain())