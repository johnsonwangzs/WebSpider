# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-06
# @file    : demo_webSpider_1.py
# @function: 爬取网站 https://ssr.scrape.center 的所有内容。
#            需要爬取的页面有两类，一类是电影列表页（TOTAL_PAGE指定页数），一类是电影详情页。


import requests
import logging
import re
from urllib.parse import urljoin
import json
from os import makedirs
from os.path import exists
import multiprocessing

# 设置日志输出级别和输出格式
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

# 设置要爬取的网站URL及爬取的页面数（若网站有分页）
BASE_URL = 'https://ssr1.scrape.center'
TOTAL_PAGE = 10

# 设置保存路径
RESULT_DIR = 'results'
exists(RESULT_DIR) or makedirs(RESULT_DIR)


def scrape_page(url):
    """
    使用requests模块实现页面（通用）爬取。
    :param url:
    :return:
    """
    logging.info('scraping %s...', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        logging.error('get invalid status code %s while scraping %s',
                      response.status_code, url)
    except requests.RequestException:
        # 将logging库中的error方法里的exc_info参数设置为True，可以打印出Traceback错误堆栈信息
        logging.error('error occurred while scraping %s', url, exc_info=True)


def scrape_index(page):
    """
    列表页的爬取。
    :param page: 页码。
    :return:
    """
    index_url = f'{BASE_URL}/page/{page}'  # f-String
    return scrape_page(index_url)


def parse_index(html):
    """
    生成器。解析列表页。
    根据html源码构建正则表达式，解析列表页，并得到每部电影的详情页URL。
    :param html: 获取的列表页源码
    :return:
    """
    pattern = re.compile('<a.*?href="(.*?)".*?class="name">')  # 提取标题超链接href属性
    items = re.findall(pattern, html)  # 提取列表页的所有href值
    if not items:
        return []
    for item in items:  # 通过for循环可以遍历生成器
        detail_url = urljoin(BASE_URL, item)  # 拼接为完整的详情页URL
        logging.info('get detail url %s', detail_url)
        yield detail_url


def scrape_detail(url):
    """
    详情页的爬取。
    :param url: 详情页的URL
    :return:
    """
    return scrape_page(url)


def parse_detail(html):
    """
    生成器。解析详情页。
    根据html源码构建正则表达式，解析详情页，并得到每部电影的详情页URL。
    :param html: 获取的列表页源码
    :return:
    """
    # 封面图片
    cover_pattern = re.compile('class="item.*?<img.*?src="(.*?)".*?class="cover">', re.S)  # 使用re.S标志符处理换行
    # 电影名称
    name_pattern = re.compile('<h2.*?>(.*?)</h2>')
    # 电影种类
    categories_pattern = re.compile('<button.*?category.*?<span>(.*?)</span>.*?</button>', re.S)
    # 上映时间
    published_at_pattern = re.compile('(\d{4}-\d{2}-\d{2})\s?上映')
    # 剧情简介
    drama_pattern = re.compile('<div.*?drama.*?>.*?<p.*?>(.*?)</p>', re.S)
    # 评分
    score_pattern = re.compile('<p.*?score.*?>(.*?)</p>', re.S)

    cover = re.search(cover_pattern, html).group(1).strip() if re.search(cover_pattern, html) else None
    name = re.search(name_pattern, html).group(1).strip() if re.search(name_pattern, html) else None
    categories = re.findall(categories_pattern, html) if re.findall(categories_pattern, html) else []
    published_at = re.search(published_at_pattern, html).group(1) if re.search(published_at_pattern, html) else None
    drama = re.search(drama_pattern, html).group(1).strip() if re.search(drama_pattern, html) else None
    score = float(re.search(score_pattern, html).group(1).strip()) if re.search(score_pattern, html) else None

    return {
        'cover': cover,
        'name': name,
        'categories': categories,
        'published_at': published_at,
        'drama': drama,
        'score': score
    }


def save_data(data):
    """
    （按电影名称）存储数据。
    :param data: 待存储的数据
    :return:
    """
    name = data.get('name')
    data_path = f'{RESULT_DIR}/{name}.json'
    # json.dump(): 将python对象转换为字符串并且写入文件。
    # ensure_ascii: 默认输出ASCLL码，如果把这个该成False，就可以输出中文。
    # indent: 参数根据数据格式缩进显示，读起来更加清晰。
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)  # 也可以写为with open() as fp的形式


def subprocess(page):
    """
    子进程。
    :param page: 某一页面
    :return:
    """
    index_html = scrape_index(page)
    detail_urls = parse_index(index_html)
    for detail_url in list(detail_urls):
        detail_html = scrape_detail(detail_url)
        data = parse_detail(detail_html)
        logging.info('get detail data %s', data)
        logging.info('saving data to json data...')
        save_data(data)
        logging.info('data saved successfully!')


if __name__ == '__main__':
    # 单进程
    # for page in range(1, TOTAL_PAGE + 1):
    #     index_html = scrape_index(page)
    #     detail_urls = parse_index(index_html)  # 产生一个生成器对象
    #     # logging.info('detail urls %s', list(detail_urls))  # list()将生成器yield返回的结果存储成列表的形式
    #
    #     for detail_url in list(detail_urls):
    #         detail_html = scrape_detail(detail_url)
    #         data = parse_detail(detail_html)
    #         logging.info('get detail data %s', data)
    #         logging.info('saving data to json file...')
    #         save_data(data)
    #         logging.info('data saved successfully!')

    # 多进程
    pool = multiprocessing.Pool()  # 创建进程池
    pages = range(1, TOTAL_PAGE + 1)
    pool.map(subprocess, pages)  # 把每个页面都作为一个进程
    pool.close()  # 进程池不再加入新锦成
    pool.join()  # 阻塞主进程，等待进程池中的子进程执行完毕

    print('main process ended!')
