# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-05
# @file    : multiProcessing_1_customize.py
# @function: 自定义进程类。

import multiprocessing
import time


class MyProcess(multiprocessing.Process):
    """
    自定义进程类，继承Process类，实现run方法即可。
    """
    def __init__(self, loop):
        multiprocessing.Process.__init__(self)
        self.loop = loop

    def run(self):
        for count in range(self.loop):
            time.sleep(1)
            print('Pid: ' + str(self.pid) + ' LoopCount: ' + str(count))  # 进程并行可能导致输出错位


if __name__ == '__main__':
    # 自定义类
    for i in range(2, 5):
        p = MyProcess(i)
        p.start()
    print('Main process ended.')

