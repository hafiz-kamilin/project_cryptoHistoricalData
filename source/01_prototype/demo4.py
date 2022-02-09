import asyncio
 
async def worker():
    print("Starting work")
    await asyncio.sleep(5)
    print("Work complete")
 
async def other_worker():
    print("Starting other worker")
    await asyncio.sleep(2)
    print("Other worker complete")
 
async def third_worker():
    print("Starting third worker")
    await asyncio.sleep(1)
    print("Third worker complete")
 
async def main():
    print("Starting workers")
    tasks = []
    tasks.append(asyncio.ensure_future(worker()))
    tasks.append(asyncio.ensure_future(other_worker()))
 
    print("First two workers added to the event loop.")
    for task in tasks:
        await task
 
    print("Adding third worker to the event loop.")
    await third_worker()
    # in this case, this is the same thing
    await asyncio.ensure_future(third_worker())
 
asyncio.run(main())