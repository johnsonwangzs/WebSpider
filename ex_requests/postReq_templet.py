# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-04
# @file    : postReq_templet.py
# @function: post请求。

import requests

# 提交form
data = {
    'name': 'johnson',
    'age': '21'
}
r = requests.post('http://www.httpbin.org/post', data=data)
print(r.text)

print(type(r.status_code), r.status_code)

# 内置状态码查询requests.codes.xxx
exit() if not r.status_code == requests.codes.ok else print('Request Successfully')

# 提交文件
files = {'file': open('favicon.ico', 'rb')}
r = requests.post('https://www.httpbin.org/post', files=files)
print(r.text)