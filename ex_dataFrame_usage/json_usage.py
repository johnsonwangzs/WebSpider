# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-08
# @file    : json_usage.py
# @function: json文件存储。
"""
在JavaScript中，一切皆为对象，因此任何支持的数据类型都可以通过json表示（字符串、数字、对象、数组等）。
对象在JavaScript中是指用{}括起来的内容，数据结构是键值对的形式。其中key可以使用整数和字符串表示，value可以是任意类型。
数组在JavaScript中是指用[]括起来的内容，数据结构是索引的形式。它的值可以是任意类型。
json可以由以上两种形式自由组合而成，能够嵌套无限次。
json对象就是Python中列表和字典的嵌套与组合。
"""

import json

# json的数据需要由双引号包围，不可用单引号，否则loads方法会报错
s = '''
[{
    "name": "李白",
    "gender": "male",
    "birthday": "1992-10-18"
}, {
    "name": "Selina",
    "gender": "female",
    "birthday": "1995-10-18"
}]
'''
print(type(s))
data = json.loads(s)  # loads方法将字符串转为json对象
print(data)
print(type(data))

print('=' * 32)

with open('data.json', encoding='utf-8') as f:  # 从文件读取内容，转为json对象
    s = f.read()
    data = json.loads(s)
    print(data)

print('-' * 32)

data = json.load(open('data.json', encoding='utf-8'))
print(data)

print('=' * 32)

data = [{
    "name": "李白",
    "gender": "male",
    "birthday": "1992-10-18"
}, {
    "name": "Selina",
    "gender": "female",
    "birthday": "1995-10-18"
}]
with open('data1.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, indent=2, ensure_ascii=False))  # indent缩进，ensure_ascii用于输出中文字符

print('-'*32)

json.dump(data, open('data2.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

print('='*32)

