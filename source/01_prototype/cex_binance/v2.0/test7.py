from binance import Client, AsyncClient
from time import sleep
import asyncio
import csv

class GetAllBinanceData:

    def __init__(self):

        self.weight = 0
        self.count = 0
        self.symbols = [
            "BTCUSDT", 
            "ETHUSDT", 
            "BNBUSDT", 
            "BCCUSDT", 
            "NEOUSDT", 
            "LTCUSDT", 
            "QTUMUSDT", 
            "ADAUSDT", 
            "XRPUSDT", 
            "EOSUSDT"
        ]

    async def test_call(self, weight, client: AsyncClient):

        if weight < 10:

            symbol = self.symbols.pop()

            # get kline based on the predefined kline interval
            klines = await client.get_historical_klines(
                symbol=symbol,
                interval="1m",
                start_str="2021-1-1 0:00:00",
                end_str="2021-1-7 00:00:00"
            )

            with open(symbol + '.csv', 'w', newline='') as f:
                write = csv.writer(f)
                write.writerows(klines)

            self.weight = int(Client().response.headers["x-mbx-used-weight"])
            print("Weight " + str(self.weight))
            self.count += 1
            print("Count " + str(self.count))

        else:

            pass

    async def amain(self) -> None:

        client = await AsyncClient.create()

        await asyncio.gather(
            *(
                self.test_call(self.weight, client) for _ in range(10)
            )
        )

        await client.close_connection()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(GetAllBinanceData().amain())
    