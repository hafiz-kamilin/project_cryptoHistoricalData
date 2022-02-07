#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Mohd Hafizuddin Bin Kamilin"
__version__ = "0.2.1"
__date__ = "24 Jan 2022"

"""
    Sample program to get all trading pair from binance

"""

# use python-binance API to interact with binance
from binance.client import Client

# get all trading pair symbol from binance
def getTradeSymbols(client: str) -> list:

    """
    get trading pair from binance

    usage:
    - getTradeSymbols(client=client, pairing=None)
      - get all available trading pair from binance 

    """

    # Extract trading pairs from exchange information
    info = client.get_all_tickers()
    return list(map(lambda symbol: symbol['symbol'], info))

if __name__ == "__main__":

    # initialize the client class to interact with binance
    # NOTE: no need for an API key for ripping the historical data
    client = Client()

    # get all trade symbols from python
    allTradeSymbols = getTradeSymbols(client=client)
