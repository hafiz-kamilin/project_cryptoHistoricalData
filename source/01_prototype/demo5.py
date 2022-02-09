import asyncio

class Demo:

    def __init__(self, counter):

        self.counter = counter

    async def worker(self):

        a = self.counter - 1
        self.counter = self.counter - 1
        print("Starting work: " + str(a))
        await asyncio.sleep(self.counter)
        print("Work complete: " + str(a))

    async def dummy(self):

        await asyncio.sleep(2)
        print("dummy thicc")

    async def main(self):

        tasks = []
        tasks.append(asyncio.ensure_future(self.dummy()))
        tasks.append(asyncio.ensure_future(self.worker()))
        
        for task in tasks:

            await task

        await self.worker()
        await asyncio.ensure_future(self.worker())

        # while self.counter != 0:

        #     await self.worker()
        #     await asyncio.ensure_future(self.worker())


demo = Demo(counter=5)
asyncio.run(demo.main())
