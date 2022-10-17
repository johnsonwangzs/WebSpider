# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-04
# @file    : getReq_templet_3.py
# @function: 爬取网站二进制数据（图片等）。

import requests

r = requests.get('https://scrape.center/favicon.ico')

print(r.text)  # 乱码
print(r.content)  # bytes类型

# 以二进制格式写入文件
with open('favicon.ico', 'wb') as f:
    f.write(r.content)
