import asyncio as asyncio

async def task1():
    for i in range(5):
        print("Task 1 - step", i)
        await asyncio.sleep(1)
        
async def task2():
    for i in range(5):
        print("Task 2 - setp", i)
        await asyncio.sleep(1)
        

async def main():
    t1 = asyncio.create_task(task1())
    t2 = asyncio.create_task(task2())
    
    await t1
    await t2
    
asyncio.run(main())