#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Mohd Hafizuddin Bin Kamilin"
__version__ = "5.0.0"
__date__ = "7 March 2022"

# to interact with binance-api via concurrent klines fetch
import asyncio

# custom libraries
from BinanceHistoricalData.AsyncKlines import AsyncKlines

if __name__ == "__main__":

    # initialize the AsyncKlines class
    createHistoricalKlines = AsyncKlines(
        # trading pair
        symbol="BNBUSDT",
        # klines interval
        interval="5m",
        # start-end datetime (UTC)
        start="2021-1-1 00:00:00",
        end="2021-1-1 00:05:00",
        # include/exclude leveraged trading pair
        include_leverage = False,
        # we can choose either "csv", "pickle" or "feather" to save the klines
        file_format = "csv",
        # option to enable/disable logging
        logged=True
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(createHistoricalKlines.amain())