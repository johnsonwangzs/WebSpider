# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-15
# @file    : aiohttp_template_1.py
# @function: aiohttp的用法
"""
aiohttp是一个支持异步请求的库，它和asyncio配合使用，可以方便地实现异步请求操作。
"""

import asyncio
import aiohttp
import time


start = time.time()


async def get(url):
    session = aiohttp.ClientSession()
    response = await session.get(url)  # await关键字：当遇到阻塞式操作时，task被挂起，程序接着去执行其他task
    await response.text()
    await session.close()
    return response


async def request():
    url = 'https://www.httpbin.org/delay/5'
    print('Waiting for', url)
    response = await get(url)
    print('Get response from', url, 'response', response)


tasks = [asyncio.ensure_future(request()) for _ in range(10)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

end = time.time()
print('Cost time:', end - start)
