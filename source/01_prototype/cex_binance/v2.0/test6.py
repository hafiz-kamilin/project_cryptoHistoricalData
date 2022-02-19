from binance import Client, AsyncClient
from time import sleep
import asyncio

class GetAllBinanceData:

    def __init__(self):

        self.weight = 0
        self.count = 0

    async def test_call(self, client: AsyncClient):


        # get kline based on the predefined kline interval
        klines = await client.get_historical_klines(
            symbol="BNBUSDT",
            interval="1m",
            start_str="2021-1-1 0:00:00",
            end_str="2021-1-3 00:00:00"
        )

        self.weight = int(Client().response.headers["x-mbx-used-weight"])
        print("Weight" + str(self.weight))
        self.count += 1
        print("Count" + str(self.count))

        # client.response.headers["x-mbx-used-weight"]

    async def amain(self) -> None:

        client = await AsyncClient.create()

        await asyncio.gather(
            *(
                self.test_call(client) if (self.weight < 10) else None for _ in range(10)
            )
        )

        await client.close_connection()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(GetAllBinanceData().amain())
    