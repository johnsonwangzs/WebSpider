# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-04
# @file    : urlParse.py
# @function: 解析/构造url。url标准格式：scheme://netloc/path;params?query#fragment

from urllib.parse import urlparse
from urllib.parse import urlunparse
from urllib.parse import urlencode


def url_parse():
    """
    解析url
    :return:
    """
    res = urlparse('http://www.baidu.com/index.html;user?id=5#comment')
    print(type(res))
    print(res)
    print(res[0], res.scheme)


def url_unparse():
    """
    构造url
    :return:
    """
    # urlunparse接受的参数，其长度必须为6
    data = ['https', 'www.baidu.com', 'index.html', 'user', 'a=6', 'comment']
    print(urlunparse(data))


def url_encode():
    """
    构造GET请求参数
    :return:
    """
    params = {
        'name': 'johnson',
        'age': 21
    }
    base_url = 'https://www.testnet.com?'
    url = base_url + urlencode(params)
    print(url)


url_parse()
print()
url_unparse()
print()
url_encode()
