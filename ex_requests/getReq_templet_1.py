# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-04
# @file    : getReq_templet_1.py
# @function: 最基本的get请求；设置请求头。

import requests

# 加上数据
data = {
    'name': 'johnson',
    'age': 21
}
r = requests.get('https://www.httpbin.org/get', params=data)
print(r)
print(type(r))
print(r.text)
print(type(r.text))
# 如果返回结果是json格式，可以调用json方法将其转为字典
print(r.json())
print(type(r.json()))

# 修改请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 '
                  'Safari/537.36'
}
r = requests.get('https://www.httpbin.org/get', params=data, headers=headers)
print(r.text)
