from binance.client import Client

client = Client()
a = client.response.headers._store["x-mbx-used-weight"][1]
print(client.response.headers)