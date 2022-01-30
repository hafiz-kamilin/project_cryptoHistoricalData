#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Mohd Hafizuddin Bin Kamilin"
__version__ = "0.0.1"
__date__ = "24 May 2022"

"""
    Sample program to get specific or all trading pair from binance

"""

# use python-binance API to interact with binance
from binance.client import Client

# get specific/all trading pair symbol from binance
def getTradeSymbols(client: str, pairing: str) -> list:

    """
    get trading pair from binance

    usage:
    1. getTradeSymbols(client=client, pairing=None)
       - get all available trading pair from binance 
    2. getTradeSymbols(client=client, pairing="USDT")
       - get all USDT trading pair from binance

    """

    # Extract trading pairs from exchange information
    info = client.get_all_tickers()
    symbols = list(map(lambda symbol: symbol['symbol'], info))

    if pairing is not None:

        # play safe; just in case someone forgot to capitalize the whole str
        pairing = pairing.upper()
        # filter specific trade symbol pairing in binance and return
        return list(filter(lambda x: x.endswith(pairing), symbols))

    else:

        # return all trade symbols available in binance
        return symbols

if __name__ == "__main__":

    # initialize the client class to interact with binance
    # NOTE: no need for an API key for ripping the historical data
    client = Client()

    # get all trade symbols from python
    allTradeSymbols = getTradeSymbols(client=client, pairing=None)
    usdtTradeSymbols = getTradeSymbols(client=client, pairing='usdt')
