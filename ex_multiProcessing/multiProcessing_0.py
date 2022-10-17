# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-05
# @file    : multiProcessing_0.py
# @function: Python多进程基础。

import multiprocessing


def process(n):
    print("I am process:" + str(n))


if __name__ == '__main__':
    for i in range(5):
        p = multiprocessing.Process(target=process, args=(i,))
        p.start()

    print('CPU number: ' + str(multiprocessing.cpu_count()))  # CPU核数目
    for p in multiprocessing.active_children():  # 当前活跃进程
        print('Child process name: ' + p.name + 'id: ' + str(p.pid))

    print('Process ended.')


