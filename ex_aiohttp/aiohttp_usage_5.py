# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-15
# @file    : aiohttp_usage_5.py
# @function: 获取响应


import aiohttp
import asyncio


async def main():
    data = {'name': 'johnson', 'age': 25}
    async with aiohttp.ClientSession() as session:
        async with session.post('https://www.httpbin.org/post', data=data) as response:
            print('status:', response.status)  # 状态码
            print('headers:', response.headers)  # 响应头
            print('body:', await response.text())  # 响应体
            print('bytes:', await response.read())  # 响应体（二进制）
            print('json:', await response.json())  # 响应体（json）

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
