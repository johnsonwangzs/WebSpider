# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-15
# @file    : coroutine_usage_1.py
# @function: 协程对象
"""
引入asyncio库后，可以使用async定义方法，该方法在调用时不会立即被执行，而是返回一个协程对象。
event_loop是事件循环，相当于一个无限循环，可以把一些函数注册到这个事件循环上，当满足发生条件的时候，就调用相应的处理方法。
"""


import asyncio


async def execute(x):
    """
    使用async关键字定义一个方法，该方法无法直接执行，而是一个协程对象。
    必须将此方法注册到时间循环中才可执行。
    :param x:
    :return:
    """
    print('number:', x)


coroutine = execute(1)  # 创建一个协程对象
print('Coroutine:', coroutine)
print('After calling execute')

loop = asyncio.get_event_loop()  # 创建一个事件循环
loop.run_until_complete(coroutine)  # 将协程对象注册到事件循环中，然后启动
"""
实际上，将coroutine传递给run_until_complete方法时，coroutine被封装成了一个task对象
task是对协程对象的进一步封装，比协程对象多了运行状态，例如running和finished等，可以利用这些状态获取协程对象的执行情况
"""
print('After calling loop')
