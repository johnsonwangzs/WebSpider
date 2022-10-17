# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-04
# @file    : getCookie.py
# @function:

import requests

r = requests.get('https://www.baidu.com')
print(r.cookies)
print(r.cookies.items())

for key, value in r.cookies.items():
    print(key + '=' + value)

headers = {
    'Cookie': '_octo=GH1.1.2095199455.1664883350; _device_id=4ee2f0aff7bbfb39d3382f1176939c6c; has_recent_activity=1; '
              'color_mode={"color_mode":"auto","light_theme":{"name":"light","color_mode":"light"},"dark_theme":{'
              '"name":"dark","color_mode":"dark"}}; preferred_color_mode=light; tz=Asia/Shanghai; logged_in=no; '
              '_gh_sess=GFUdH3umG9LfLnZ8vTnvbySe1wwmAyKBGIxXrcRAOGgC5Ho8uyYwpKVmR76Vt0d'
              '/b7BNeDcNpuROq8oFQE8l7ro7GwQzFFtkfnpJnm22f3t2CFSenj0ruVvZ5EBKbwbFbAhtA3egChHfC85ElwNsOl2whT+9aQLi104Yq'
              '+A1HyrtUHwyGBagclc3uAqQzGzAkBDX7kOfM6IltYG69dQ2NeW0FrjUmLmvYuOPBAZcpgutpSraiwxyvUxOK'
              '+lGRBBAJa6HrIQvjld9fuQ5bWStpQ==--8hwY7fySf/dRPrLe--d1p69SqTa+W0KR58OKX8uQ== '
}
r = requests.get('https://github.com/', headers=headers)
print(r.text)
