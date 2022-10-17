# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-05
# @file    : getReq_templet.py
# @function: get请求；Client对象；HTTP/2.0支持。

import httpx

# 基本get请求
response = httpx.get('https://www.httpbin.org/get')
print(response.status_code)
print(response.headers)
print(response.text)
print('--------')

# Client对象写法
url = 'https://www.httpbin.org/headers'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 '
                  'Safari/537.36'
}
with httpx.Client(headers=headers) as Client:
    response = Client.get(url)
    print(response.text)
    print(response.json()['headers']['User-Agent'])
print('--------')

# 请求http/2.0网站
client = httpx.Client(http2=True)  # 需要首先设置http2参数，开启对http/2.0的支持
response = client.get('https://spa16.scrape.center')
print(response.text)
