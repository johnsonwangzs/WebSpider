# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-22
# @file    : ex_cookie_1.py
# @function: 基于Session和Cookie的模拟登录，https://login2.scrape.center

import requests
from urllib.parse import urljoin

BASE_URL = 'https://login2.scrape.center/'
LOGIN_URL = urljoin(BASE_URL, '/login')
INDEX_URL = urljoin(BASE_URL, '/page/1')
USERNAME = 'admin'
PASSWORD = 'admin'

session = requests.Session()

# 模拟登录
session.post(LOGIN_URL, data={
    'username': USERNAME,
    'password': PASSWORD
}, allow_redirects=False)  # 禁止requests自动处理重定向

cookies = session.cookies  # 获取第一次登录的cookie
print('Cookies', cookies)

response_index = session.get(INDEX_URL)  # 使第二次请求带上第一次的cookie
print('Response Status', response_index.status_code)
print('Response URL', response_index.url)
