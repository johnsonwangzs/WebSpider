# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-05
# @file    : regex.py
# @function: 正则表达式。


import re

# 转义
content = "(百度)www.baidu.com"
result = re.match('\(百度\)www\.baidu\.com', content)
print(result)

html = '''<div id="songs-list">
<h2 class="title">经典老歌</h2>
<p class="introduction">
经典老歌列表
</p>
<ul id="list" class="list-group">
<li data-view="2">一路上有你</li>
<li data-view="7">
<a href="/2.mp3" singer="任贤齐">沧海一声笑</a>
</li>
<li data-view="4" class="active">
<a href="/3.mp3" singer="齐秦">往事随风</a>
</li>
<li data-view="6"><a href="/4.mp3" singer="beyond">光辉岁月</a></li>
<li data-view="5"><a href="/5.mp3" singer="陈慧琳">记事本</a></li>
<li data-view="5">
<a href="/6.mp3" singer="邓丽君">但愿人长久</a>
</li>
</ul>
</div>'''

# 提取class为“active”的li节点中的歌手和歌名
result = re.search('<li.*?active.*?singer="(.*?)">(.*?)</a>', html, re.S)
print(result.group(1), result.group(2))

# 提取第一对歌手和歌名
result = re.search('<li.*?singer="(.*?)">(.*?)</a>', html, re.S)
print(result.group(1), result.group(2))

# 提取所有歌手和歌名
result = re.findall('<li.*?singer="(.*?)">(.*?)</a>', html, re.S)
for each in result:
    print(each, each[0], each[1])
