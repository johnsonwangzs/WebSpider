# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-04
# @file    : getReq_templet_2.py
# @function: 使用正则表达式提取网页内容。

import requests
import re

r = requests.get('https://ssr1.scrape.center/')
pattern = re.compile('<h2.*?>(.*?)</h2>', re.S)
titles = re.findall(pattern, r.text)
print(titles)
