import time
import asyncio

# @asyncio.coroutines
async def show(): #برای اینکه توی asyncio دست خودمونه که بگیم برنامه کجا متوقف بشه برای همین ز await استفاده میکنیم تا ارور دریاف نکنیم
    # time.sleep(3)
    await asyncio.sleep(3)
    print('hello worold!')


# print(asyncio.iscoroutinefunction(show))
asyncio.run(show())
