# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-15
# @file    : coroutine_usage_3.py
# @function: 绑定回调

import asyncio
import requests


async def request():
    url = 'https://www.baidu.com'
    status = requests.get(url)
    return status


def callback(task):
    """
    回调函数
    :param task: task对象
    :return:
    """
    print('Status:', task.result())


coroutine = request()
task = asyncio.ensure_future(coroutine)
task.add_done_callback(callback)  # 关联task对象和回调方法。注意这里的参数是函数名callback，而不是callback()
print('Task:', task)

loop = asyncio.get_event_loop()
loop.run_until_complete(task)
print('Task:', task)
