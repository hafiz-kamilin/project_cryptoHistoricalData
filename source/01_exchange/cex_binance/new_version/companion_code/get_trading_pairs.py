# use python-binance API to interact with binance
from binance import Client

def get_trading_pairs(symbol: str, include_leverage: bool) -> list[str]:

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