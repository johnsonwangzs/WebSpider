# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-04
# @file    : postReq_advanced.py
# @function: 更高级的post请求构造方法——处理基本的身份认证。

from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener
from urllib.error import URLError

usr = 'admin'
pwd = 'admin'
url = 'https://ssr3.scrape.center'

p = HTTPPasswordMgrWithDefaultRealm()
p.add_password(None, url, usr, pwd)

# 建立用于处理验证的Handler类
authHandler = HTTPBasicAuthHandler(p)

# 构建Opener
opener = build_opener(authHandler)

try:
    res = opener.open(url)
    html = res.read().decode('utf-8')
    print(html)
except URLError as e:
    print(e.reason)
