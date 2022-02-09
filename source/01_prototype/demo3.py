import asyncio
from binance import AsyncClient
from time import sleep

api_key = '<api_key>'
api_secret = '<api_secret>'

async def main():
    client = await AsyncClient.create(api_key, api_secret)

    _ = await client.get_exchange_info()

    for _ in range(10):

        print(client.response.headers['x-mbx-used-weight'])
        sleep(1)


    await client.close_connection()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())