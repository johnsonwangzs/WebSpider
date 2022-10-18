# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-17
# @file    : demo_webSpider_5.py
# @function: 爬取豆瓣电影Top250。https://movie.douban.com/top250
"""
【豆瓣top250】
网站列出250个电影，列表页共10页，每页25个电影；从列表页可以得到电影详情页的url。
网站有简单的反爬机制，如果爬虫请求不加伪装，可能会得到返回418状态码。实际上只需设置一下请求头即可。
"""
import re
import pymongo
import requests
import multiprocessing
import logging

INDEX_URL = 'https://movie.douban.com/top250?start={start_num}&filter='  # 列表页url
TOTAL_PAGE = 10  # 列表页总页数
PER_PAGE = 25  # 列表页每页的电影数

# 使用MongoDB保存数据
MONGO_CONNECTION_STRING = 'mongodb://localhost:27017'  # 连接字符串
MONGO_DB_NAME = 'movies'  # 数据库名称
MONGO_COLLECTION_NAME = 'douban_top250'  # 集合名称

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

# 设置请求头，绕开反爬
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 '
                  'Safari/537.36 '
}


def scrape_api(url):
    """
    爬取通用url
    :param url: 目标网页url
    :return:
    """
    logging.info('scraping %s', url)
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.text
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    except requests.RequestException as e:
        logging.error('error occurred while scraping %s', url)


def scrape_index(page):
    """
    爬取某一列表页
    :param page: 页码
    :return:
    """
    url = INDEX_URL.format(start_num=PER_PAGE * (page - 1))
    return scrape_api(url)


def scrape_detail(url):
    """
    爬取某一电影详情页
    :param url: 详情页url
    :return:
    """
    return scrape_api(url)


def save_data(html, collection):
    """
    保存数据到MongoDB
    :param collection: MongoDB集合
    :param html: 数据
    :return:
    """
    movieNamePtn = re.compile('<span property="v:itemreviewed">(.*?)</span>', re.S)
    movieRankPtn = re.compile('<span class="top250-no">(.*?)</span>', re.S)
    movieScorePtn = re.compile('property="v:average">(.*?)</strong>', re.S)
    movieYearPtn = re.compile('<span class="year">\((.*?)\)</span>', re.S)
    movieFrom = re.compile('制片国家/地区.*?</span>(.*?)<br/>', re.S)
    directorPtn = re.compile('rel="v:directedBy">(.*?)</a>', re.S)
    screenwriterPtn = re.compile('编剧.*?<a href=.*?>(.*?)</a>', re.S)
    starringPtn = re.compile('<a href=.*? rel="v:starring">(.*?)</a>', re.S)
    lengthPtn = re.compile('property="v:runtime".*?>(.*?)</span>', re.S)
    imdbPtn = re.compile('IMDb.*?</span>(.*?)<br>', re.S)
    introductionPtn = re.compile('<span class="all hidden">(.*?)</span>', re.S)

    movieName = re.search(movieNamePtn, html).group(1).strip() if re.search(movieNamePtn, html) else None
    movieRank = re.search(movieRankPtn, html).group(1).strip() if re.search(movieRankPtn, html) else None
    movieScore = re.search(movieScorePtn, html).group(1).strip() if re.search(movieScorePtn, html) else None
    movieYear = re.search(movieYearPtn, html).group(1).strip() if re.search(movieYearPtn, html) else None
    movieFrom = [string.strip() for string in re.findall(movieFrom, html)] if re.findall(movieFrom, html) else None
    director = re.search(directorPtn, html).group(1).strip() if re.search(directorPtn, html) else None
    screenwriter = [string.strip() for string in re.findall(screenwriterPtn, html)] \
        if re.findall(screenwriterPtn, html) else None
    starring = [string.strip() for string in re.findall(starringPtn, html)] \
        if re.findall(starringPtn, html) else None
    length = re.search(lengthPtn, html).group(1).strip() if re.search(lengthPtn, html) else None
    imdb = re.search(imdbPtn, html).group(1).strip() if re.search(imdbPtn, html) else None
    introduction = re.search(introductionPtn, html).group(1).strip().replace('\u3000', '').replace(' ', '') \
        .replace('\n', '').replace('<br/>', '') if re.search(introductionPtn, html) else None

    movie_data = {'Movie-Name': movieName,
                  'Movie-Rank': movieRank,
                  'Movie-Score': movieScore,
                  'Movie-Year': movieYear,
                  'Movie-From': movieFrom,
                  'Director': director,
                  'Screenwriter': screenwriter,
                  'Starring': starring,
                  'Length': length,
                  'IMDB': imdb,
                  'Introduction': introduction}

    print(movie_data)
    collection.update_one({
        'name': movie_data['Movie-Name']
    }, {
        '$set': movie_data
    }, upsert=True)


def subproc(page):
    """
    子进程（每一子进程负责一页的爬取）
    :param page: 某一列表页页码
    :return:
    """
    client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
    db = client[MONGO_DB_NAME]
    collection = db[MONGO_COLLECTION_NAME]
    # 爬取列表页
    index_data = scrape_index(page)
    # 从列表页中提取详情页url
    logging.info('got index page: %s', page)
    with open('index_{page}'.format(page=page), 'w', encoding='utf-8') as f:
        f.write(index_data)
    # with open('index_{page}'.format(page=page), 'r', encoding='utf-8') as f:
    #     index_data = f.read()
    pattern = re.compile('<li.*?<div class="item">.*?<div class="hd">.*?<a href="(.*?)" class="">', re.S)
    detail_urls = re.findall(pattern, index_data)
    logging.info('analyzed detail urls in index(page: %s), %s in list', page, len(detail_urls))
    print(detail_urls)
    # 爬取详情页
    for i in range(len(detail_urls)):
        detail_data = scrape_detail(detail_urls[i])
        logging.info('got detail page: %s', detail_urls[i])
        mId = re.search('subject/(.*?)/', detail_urls[i]).group(1)
        # with open('detail_{id}'.format(id=mId), 'w', encoding='utf-8') as f:
        #     f.write(detail_data)
        save_data(detail_data, collection)
        logging.info('detail data for movie: %s saved to database', mId)


if __name__ == '__main__':
    pool = multiprocessing.Pool()
    pages = range(1, TOTAL_PAGE + 1)
    pool.map(subproc, pages)
    pool.close()
    pool.join()
    print('main process ended!')

