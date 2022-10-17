# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-04
# @file    : getCookie.py
# @function: 获取网站的cookie。

import http.cookiejar
import urllib.request

cookie = http.cookiejar.CookieJar()

# 构建处理cookie的Handler
handler = urllib.request.HTTPCookieProcessor(cookie)

opener = urllib.request.build_opener(handler)
response = opener.open('https://www.baidu.com')

for item in cookie:
    print(item.name + "=" + item.value)
