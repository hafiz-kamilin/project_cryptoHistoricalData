# SOURCE: https://stackoverflow.com/a/70081987

import asyncio
from binance import AsyncClient

RESULTS = []  # let's store all results here


class GetAllBinanceData:
    def __init__(self, workers_num: int = 10):
        self.workers_num: int = workers_num
        self.task_q: asyncio.Queue = asyncio.Queue(maxsize=10)

    async def get_symbols_from_somewhere(self):
        """Get symbols and distribute them among workers"""
        # imagine the symbols are from some file
        symbols = ["BNBBTC", "ETHBTC", "NEOBTC"]
        for i in symbols:
            await self.task_q.put(i)

        for i in range(self.workers_num):
            await self.task_q.put(None)

    async def get_historical_klines(self, client: AsyncClient):
        """Get data and print it"""
        while True:
            symbol = await self.task_q.get()
            if symbol is None:
                break
            klines = await client.get_historical_klines(
                symbol=symbol,
                interval=AsyncClient.KLINE_INTERVAL_1MINUTE,
                start_str="2021-11-23 10:00:00",
                end_str="2021-11-23 10:01:00"
            )
            print(klines)  # just print
            RESULTS.append(klines)  # send somewhere else

    async def amain(self) -> None:
        """Main async wrapper fucntion"""
        client = await AsyncClient.create()
        await asyncio.gather(
            self.get_symbols_from_somewhere(),
            *[self.get_historical_klines(client) for _ in range(self.workers_num)]
        )

        await client.close_connection()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(GetAllBinanceData().amain())
    print("*" * 100)
    print(RESULTS)