# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-13
# @file    : demo_webSpider_3.py
# @function: 爬取Ajax网页。以 https://spa1.scrape.center 为例。


import multiprocessing
import requests
import logging
import pymongo

# 设置日志输出级别和输出格式
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

INDEX_URL = 'https://spa1.scrape.center/api/movie/?limit={limit}&offset={offset}'  # 观察得到列表页Ajax接口
LIMIT = 10  # 每页最大显示数
DETAIL_URL = 'https://spa1.scrape.center/api/movie/{id}'  # 观察得到详情页Ajax接口
TOTAL_PAGE = 10

# 使用MongoDB保存数据
MONGO_CONNECTION_STRING = 'mongodb://localhost:27017'  # 连接字符串
MONGO_DB_NAME = 'movies'  # 数据库名称
MONGO_COLLECTION_NAME = 'movies'  # 集合名称


def scrape_api(url):
    """
    通用爬取接口
    :param url: 要爬取的url
    :return:
    """
    logging.info('scraping %s...', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()  # json方法解析响应内容，并将其转化为JSON字符串
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)


def scrape_index(page):
    """
    列表页爬取
    :param page: 第几页
    :return:
    """
    url = INDEX_URL.format(limit=LIMIT, offset=LIMIT * (page - 1))
    return scrape_api(url)


def scrape_detail(id):
    """
    详情页爬取
    :param id: 电影id
    :return:
    """
    url = DETAIL_URL.format(id=id)
    return scrape_api(url)


def save_data(data, collection):
    """
    将数据保存到数据库
    :param data: 数据
    :return:
    """
    # update_one方法：第一个参数为查询条件，第二个参数为要插入（更新）的数据本身
    collection.update_one({
        'name': data.get('name')
    }, {
        '$set': data
    }, upsert=True)  # upsert=True，可以实现存在即更新（且更新时会参照第一个参数中设置的字段，防止出现同名）、不存在即插入的功能


def subprocess(page):
    """
    子进程
    :param page: 某一页面（每个子进程负责一个页面的爬取）
    :return:
    """
    client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
    db = client[MONGO_DB_NAME]
    collection = db[MONGO_COLLECTION_NAME]
    index_data = scrape_index(page)
    for item in index_data.get('results'):
        id = item.get('id')
        detail_data = scrape_detail(id)
        # logging.info('detail data %s', detail_data)
        logging.info('got detail data for id=%s', id)
        save_data(detail_data, collection)
        logging.info('data saved successfully!')


if __name__ == '__main__':
    # 单进程
    # 连接数据库
    # client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
    # db = client[MONGO_DB_NAME]
    # collection = db[MONGO_COLLECTION_NAME]
    # for page in range(1, TOTAL_PAGE + 1):  # 逐页爬取
    #     index_data = scrape_index(page)
    #     for item in index_data.get('results'):
    #         id = item.get('id')
    #         detail_data = scrape_detail(id)
    #         logging.info('detail data %s', detail_data)
    #         save_data(detail_data)
    #         logging.info('data saved successfully!')

    # 多进程
    pool = multiprocessing.Pool()
    pages = range(1, TOTAL_PAGE + 1)
    pool.map(subprocess, pages)
    pool.close()
    pool.join()
    print('main process ended!')

