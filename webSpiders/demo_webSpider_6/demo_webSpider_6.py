# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-20
# @file    : demo_webSpider_6.py
# @function: 利用Selenium爬取 https://spa2.scrape.center 。
import json

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import urljoin
from os import makedirs
from os.path import exists
import logging

RESULT_DIR = 'results'
exists(RESULT_DIR) or makedirs(RESULT_DIR)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

BASE_URL = 'https://spa2.scrape.center'
INDEX_URL = 'https://spa2.scrape.center/page/{page}'
TIME_OUT = 10
TOTAL_PAGE = 10

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 设置无头模式
browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, TIME_OUT)


def save_data(data):
    """
    将数据保存为本地JSON格式
    :param data:
    :return:
    """
    name = data.get('name')
    data_path = f'{RESULT_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


def scrape_page(url, condition, locator):
    """
    （通用）爬取
    :param url: 要爬取的url
    :param condition: 页面加载成功的判断条件（ec中的一项）
    :param locator: 定位器（一个元组，通过配置查询条件和参数来获取一个或多个节点）
    :return:
    """
    logging.info('scraping %s', url)
    try:
        browser.get(url)
        wait.until(condition(locator))
    except TimeoutException:
        logging.error('error occurred while scraping %s', url, exc_info=True)


def scrape_index(page):
    """
    列表页爬取
    :param page: 页码
    :return:
    """
    url = INDEX_URL.format(page=page)
    # 条件为所有节点都加载出来
    scrape_page(url,
                condition=ec.visibility_of_all_elements_located,
                locator=(By.CSS_SELECTOR, '#index .item'))


def parse_index():
    """
    解析列表页，得到详情页url
    :return:
    """
    elements = browser.find_elements(By.CSS_SELECTOR, '#index .item .name')
    for element in elements:
        href = element.get_attribute('href')
        yield urljoin(BASE_URL, href)


def scrape_detail(url):
    """
    爬取详情页
    :param url: 详情页url
    :return:
    """
    # 判断页面加载成功的条件：电影名称加载出来
    scrape_page(url,
                condition=ec.visibility_of_element_located,
                locator=(By.TAG_NAME, 'h2'))


def parse_detail():
    """
    解析详情页
    :return:
    """
    url = browser.current_url
    name = browser.find_element(By.TAG_NAME, 'h2').text
    categories = [element.text for element in browser.find_elements(By.CSS_SELECTOR, '.categories button span')]
    cover = browser.find_element(By.CSS_SELECTOR, '.cover').get_attribute('src')
    score = browser.find_element(By.CLASS_NAME, 'score').text
    drama = browser.find_element(By.CSS_SELECTOR, '.drama p').text
    return {
        'url': url,
        'name': name,
        'categories': categories,
        'cover': cover,
        'score': score,
        'drama': drama
    }


def main():
    try:
        for page in range(1, TOTAL_PAGE + 1):
            scrape_index(page)
            detail_urls = parse_index()
            # logging.info('details urls %s', list(detail_urls))
            for detail_url in list(detail_urls):
                logging.info('get detail url %s', detail_url)
                scrape_detail(detail_url)
                detail_data = parse_detail()
                save_data(detail_data)
                logging.info('detail data %s', detail_data)
    finally:
        browser.close()


if __name__ == '__main__':
    main()
