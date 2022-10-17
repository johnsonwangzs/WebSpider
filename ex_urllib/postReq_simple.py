# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-04
# @file    : postReq_simple.py
# @function: 构造简单的post请求。包括请求头（header），提交数据（form）。

from urllib import request, parse

url = 'https://www.httpbin.org/post'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 '
                  'Safari/537.36',
    'Host': 'www.httpbin.org'
}

formDict = {'name': 'johnson'}
data = bytes(parse.urlencode(formDict), encoding='utf-8')

req = request.Request(url=url, data=data, headers=headers, method='POST')
response = request.urlopen(req)

print(response.read().decode('utf-8'))
