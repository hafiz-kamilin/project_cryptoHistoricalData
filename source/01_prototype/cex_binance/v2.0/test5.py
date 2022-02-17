from binance import Client, AsyncClient
from time import sleep
import asyncio

class GetAllBinanceData:

    def __init__(self):

        self.weight = 0
        self.count = 0

    def test_call(self):

        self.weight = int(Client().response.headers["x-mbx-used-weight"])
        print("Weight" + str(self.weight))
        self.count += 1
        print("Count" + str(self.count))

        # client.response.headers["x-mbx-used-weight"]

    async def amain(self) -> None:

        client = await AsyncClient.create()

        await asyncio.gather(
            self.test_call() if (self.weight < 10) else None for _ in range(10)
        )

        await client.close_connection()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(GetAllBinanceData().amain())
    