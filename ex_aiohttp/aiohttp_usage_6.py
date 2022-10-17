# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-15
# @file    : aiohttp_usage_6.py
# @function: 并发限制


import asyncio
import aiohttp

CONCURRENCY = 5  # 爬取的最大并发量为5
URL = 'https://www.baidu.com'

semaphore = asyncio.Semaphore(CONCURRENCY)  # 创建一个信号量
session = None


async def scrape_api():
    async with semaphore:  # 使用async with语句将信号量semaphore作为上下文对象
        print('scraping', URL)
        async with session.get(URL) as response:
            await asyncio.sleep(1)
            print(response.status)
            return await response.text()


async def main():
    global session
    session = aiohttp.ClientSession()
    scrape_index_tasks = [asyncio.ensure_future(scrape_api()) for _ in range(10000)]  # 声明10000个task
    await asyncio.gather(*scrape_index_tasks)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
