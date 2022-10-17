# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-15
# @file    : aiohttp_usage_2.py
# @function: URL参数的设置

import aiohttp
import asyncio


async def main():
    params = {'name': 'johnson', 'age': 25}
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.httpbin.org/get', params=params) as response:
            print(await response.text())


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
