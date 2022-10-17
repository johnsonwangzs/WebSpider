# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-04
# @file    : setSession.py
# @function: 利用session维持会话。使用Session操作，相当于一个浏览器的两个标签页，不使用Session相当于两个浏览器。

import requests

s = requests.Session()
s.get('https://www.httpbin.org/cookies/set/number/1234')
r = s.get('https://www.httpbin.org/cookies')
print(r.text)
