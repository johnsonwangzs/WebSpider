# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-22
# @file    : ex_jwt.py
# @function: 基于JWT的模拟登录， https://login3.scrape.center

import requests
from urllib.parse import urljoin

BASE_URL = 'https://login3.scrape.center/'
LOGIN_URL = urljoin(BASE_URL, '/api/login')
INDEX_URL = urljoin(BASE_URL, '/api/book')
USERNAME = 'admin'
PASSWORD = 'admin'

response_login = requests.post(LOGIN_URL, json={
    'username': USERNAME,
    'password': PASSWORD
})
data = response_login.json()
print('Response JSON', data)
jwt = data.get('token')
print('JWT', jwt)

headers = {
    'Authorization': f'jwt {jwt}'
}
response_index = requests.get(INDEX_URL, params={
    'limit': 18,
    'offset': 0
}, headers=headers)
print('Response Status', response_index.status_code)
print('Response URL', response_index.url)
print('Response Data', response_index.json())
