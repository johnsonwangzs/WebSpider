# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-17
# @file    : demo_webSpider_4_multiproc.py
# @function:


import asyncio
import aiohttp
import multiprocessing
import logging
import json
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_CONNECTION_STRING = 'mongodb://localhost:27017'
MONGO_DB_NAME = 'books'
MONGO_COLLECTION_NAME = 'books_multiproc'

INDEX_URL = 'https://spa5.scrape.center/api/book/?limit=18&offset={offset}'  # 从网页中分析出列表页Ajax接口
DETAIL_URL = 'https://spa5.scrape.center/api/book/{id}'  # 从网页中分析出详情页Ajax接口
PAGE_SIZE = 18  # 每页最多显示数
PAGE_NUMBER = 100  # 总共要爬取的页数
CONCURRENCY = 4  # 并发量
SUB_PAGE = 20  # 每个进程负责页面数

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


async def save_data(data, collection):
    """
    将数据保存到MongoDB
    :param data:
    :return:
    """
    logging.info('saving data %s', data)
    if data:  # 若没有记录则插入，否则覆盖
        return await collection.update_one({
            'id': data.get('id')
        }, {
            '$set': data
        }, upsert=True)


async def scrape_api(url, session, semaphore):
    """
    （通用）页面爬取
    :param url: 要爬取页面的URL
    :return:
    """
    async with semaphore:
        try:
            logging.info('scraping %s', url)
            async with session.get(url, ssl=False) as response:
                return await response.json()
        except aiohttp.ClientError:
            logging.error('error occurred while scraping %s', url, exc_info=True)


async def scrape_index(page, session, semaphore):
    """
    爬取列表页
    :param page: 列表页页码
    :return:
    """
    url = INDEX_URL.format(offset=PAGE_SIZE * (page - 1))
    return await scrape_api(url, session, semaphore)


async def scrape_detail(id, session, semaphore, collection):
    """
    爬取详情页
    :param id: 序号
    :return:
    """
    url = DETAIL_URL.format(id=id)
    data = await scrape_api(url, session, semaphore)
    await save_data(data, collection)


async def main(start_page, session, semaphore, collection):
    """
    主爬取方法
    :param start_page:
    :param session:
    :param semaphore:
    :return:
    """
    # 第一步，爬取列表页
    # 定义用于爬取列表页的所有task组成的列表
    scrape_index_tasks = [asyncio.ensure_future(scrape_index(page, session, semaphore))
                          for page in range(start_page, start_page + SUB_PAGE)]
    results = await asyncio.gather(*scrape_index_tasks)  # 由所有task返回结果组成的列表
    logging.info('results %s', json.dumps(results, ensure_ascii=False, indent=2))

    # 第二步，爬取详情页
    ids = []
    for index_data in results:  # 从列表页爬取结果中提取详情页url所需的id
        if not index_data:
            continue
        for item in index_data.get('results'):
            ids.append(item.get('id'))
    scrape_detail_tasks = [asyncio.ensure_future(scrape_detail(id, session, semaphore, collection)) for id in ids]
    await asyncio.wait(scrape_detail_tasks)  # 也可使用gather方法
    await session.close()


def subprocess(start_page):
    """
    子进程，每个进程下开启线程
    :param start_page: 当前子进程进行爬取的起始页码
    :return:
    """
    client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
    db = client[MONGO_DB_NAME]
    collection = db[MONGO_COLLECTION_NAME]

    session = aiohttp.ClientSession()  # 声明session对象（全局）
    semaphore = asyncio.Semaphore(CONCURRENCY)  # 信号量 用来控制最大并发数量
    asyncio.get_event_loop().run_until_complete(main(start_page, session, semaphore, collection))


if __name__ == '__main__':
    pool = multiprocessing.Pool()
    startPages = range(1, PAGE_NUMBER, SUB_PAGE)
    pool.map(subprocess, startPages)
    pool.close()
    pool.join()
    print('main process ended!')
