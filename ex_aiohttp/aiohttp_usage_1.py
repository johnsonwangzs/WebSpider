# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-15
# @file    : aiohttp_usage_1.py
# @function: aiohttp库的用法。
"""
aiohttp是一个基于asyncio的异步http网络模块，既提供了服务端，又提供了客户端。
用服务端可以搭建支持异步处理的服务器；用客户端可以发起异步的网络请求（requests库则是同步的）
"""

import aiohttp
import asyncio


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text(), response.status


async def main():
    async with aiohttp.ClientSession() as session:
        html, status = await fetch(session, 'https://wangzs.net')
        print(f'html: {html[:200]}...')
        print(f'status: {status}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
