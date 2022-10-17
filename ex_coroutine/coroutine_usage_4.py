# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-15
# @file    : coroutine_usage_4.py
# @function: 多任务协程。task列表和wait方法。

import asyncio
import requests


async def request():
    url = 'https://www.baidu.com'
    status = requests.get(url)
    return status


tasks = [asyncio.ensure_future(request()) for _ in range(5)]  # 使用for循环创建一个task列表
print('Tasks:', tasks)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))  # 将task列表传给wait方法，再将其注册到事件循环中，之后会依次执行列表中的task

for task in tasks:
    print('Task result:', task.result())
