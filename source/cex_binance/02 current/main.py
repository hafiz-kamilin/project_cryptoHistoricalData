#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Mohd Hafizuddin Bin Kamilin"
__version__ = "5.2.1"
__date__ = "26 March 2022"

"""
TODO

1. Add try-except to restart if the download failed
2. Change list to numpy array to save memory
3. Add Aggtrade

"""

# custom libraries
from BinanceHistoricalData.AsyncKlines import AsyncKlines

if __name__ == "__main__":

    # initialize the AsyncKlines class
    createHistoricalKlines = AsyncKlines(
        # trading pair
        symbol="BNBUSDT",
        # klines interval
        interval="1m",
        # start-end datetime (UTC)
        start="2020-1-1 00:00:00",
        end="2022-1-2 00:00:00",
        # include/exclude leveraged trading pair
        include_leverage=False,
        # we can choose either "csv", "pickle" or "feather" to save the klines
        file_format="csv"
    )
