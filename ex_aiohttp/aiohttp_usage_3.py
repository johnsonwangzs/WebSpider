# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-15
# @file    : aiohttp_usage_3.py
# @function: aiohttp的其他请求类型


import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        # async with session.post('https://httpbin.org/post', data=b'data') as response:
        # async with session.put('https://httpbin.org/put', data=b'data') as response:
        # async with session.delete('https://httpbin.org/delete') as response:
        async with session.head('https://httpbin.org/get') as response:
            print(await response.text())


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
