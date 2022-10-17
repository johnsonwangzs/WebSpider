# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-15
# @file    : coroutine_usage_2.py
# @function: task对象
"""
task是任务，是对协程对象的进一步封装，包含协程对象的各个状态。
"""

import asyncio


async def execute(x):
    print('number:', x)
    return x


coroutine1 = execute(1)
print('Coroutine:', coroutine1)
print('After calling execute')

loop1 = asyncio.get_event_loop()
task1 = loop1.create_task(coroutine1)  # create_task方法将协程对象转化为task对象，此时task对象处于pending状态
print('Task:', task1)

loop1.run_until_complete(task1)  # run_until_complete方法将task对象添加到事件循环中执行，此后task对象处于finished状态
print('Task:', task1)
print('After calling loop')

print('='*32)

# 或者使用ensure_future方法，是定义task对象的另一种方式
coroutine2 = execute(1)
print('Coroutine:', coroutine2)
print('After calling execute')
task2 = asyncio.ensure_future(coroutine2)
print('Task1:', task2)
loop2 = asyncio.get_event_loop()
loop2.run_until_complete(task2)
print('Task1:', task2)
print('After calling loop')
