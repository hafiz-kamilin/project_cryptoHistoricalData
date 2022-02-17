# use python-binance API to interact with binance
from binance.client import Client

client = Client()
client.get_exchange_info()
print(client.response.headers["x-mbx-used-weight"])
print(client.response.headers["x-mbx-used-weight"])
print(client.response.headers["x-mbx-used-weight"])