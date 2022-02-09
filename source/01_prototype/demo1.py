#!/usr/bin/env python3
# countasync.py

import asyncio

async def count(i: int):
    print("One " + str(i))
    await asyncio.sleep(1)
    print("Two " + str(i))

async def main():
    await asyncio.gather(
        *(count(i) for i in range(3))
    )

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
