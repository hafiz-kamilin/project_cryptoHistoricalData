# get aggtrades

# source 1: https://python-binance.readthedocs.io/en/latest/binance.html?highlight=aggregate_trade_iter#binance.client.Client.aggregate_trade_iter
# source 2: https://python-binance.readthedocs.io/en/latest/binance.html?highlight=aggregate_trade_iter#binance.client.AsyncClient.aggregate_trade_iter

from binance.client import Client

client = Client()

aggtrades = client.aggregate_trade_iter(
    symbol="ETHBTC",
    start_str="2022-01-01 07:00:00"
)

aggtrades = list(aggtrades)

print(Client().response.headers["x-mbx-used-weight"])
print(aggtrades)
