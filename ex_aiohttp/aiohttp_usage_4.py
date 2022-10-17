# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-15
# @file    : aiohttp_usage_4.py
# @function: post请求

import aiohttp
import asyncio


async def main():
    data = {'name': 'johnson', 'age': 25}
    async with aiohttp.ClientSession() as session:
        # post表单提交   Content-Type为application/x-www-form-urlencoded
        async with session.post('https://httpbin.org/post', data=data) as response:
            print(await response.text())

        # post json数据提交  Content-Type为application/json
        # async with session.post('https://httpbin.org/post', json=data) as response:
        #     print(await response.text())


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
