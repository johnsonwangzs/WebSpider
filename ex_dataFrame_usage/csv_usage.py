# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-11
# @file    : csv_usage.py
# @function: csv文件存储。
"""
CSV(Comma-Separated Values). 以纯文本形式存储表格数据。
"""

import csv
import pandas as pd

with open('data.csv', 'w') as csvfile:  # 以csv格式写入文件
    writer = csv.writer(csvfile, delimiter=' ')  # delimiter指定分隔符
    writer.writerow(['id', 'name', 'age'])
    writer.writerow(['10001', 'Mike', 20])
    writer.writerow(['10002', 'Bob', 22])
    writer.writerow(['10003', 'Jordan', 21])

print('-'*32)

with open('data1.csv', 'w') as csvfile:
    fieldnames = ['id', 'name', 'age']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'id': '10001', 'name': 'Mike', 'age': 20})
    writer.writerow({'id': '10002', 'name': 'Bob', 'age': 22})
    writer.writerow({'id': '10003', 'name': 'Jordan', 'age': 21})

print('-'*32)

data = [
    {'id': '10001', 'name': 'Mike', 'age': 20},
    {'id': '10002', 'name': 'Bob', 'age': 22},
    {'id': '10003', 'name': 'Jordan', 'age': 21}
]
df = pd.DataFrame(data)
df.to_csv('data3.csv', index=False)

print('='*32)

with open('data1.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)

print('-'*32)

df = pd.read_csv('data1.csv')
print(df)

print('-'*32)

data = df.values.tolist()
print(data)

