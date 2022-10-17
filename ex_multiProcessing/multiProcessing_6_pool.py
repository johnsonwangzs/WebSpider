# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-06
# @file    : multiProcessing_6_pool.py
# @function: 进程池。用于管理大量进程。


from multiprocessing import Lock, Pool
import time


def function(index):
    print('Start process: ', index)
    time.sleep(3)
    print('End process', index)


if __name__ == '__main__':
    pool = Pool(processes=3)  # 初始化一个Pool，指定进程数。（如果不指定，那么会自动根据CPU内核来分配进程数）
    for i in range(4):
        # pool.apply_async(function, (i,))  # 非阻塞
        pool.apply(function, (i, ))  # 阻塞

    print("Started processes")
    pool.close()  # 关闭pool，使其不再接受新的任务
    pool.join()  # 主进程阻塞，等待子进程的退出
    print("Subprocess done.")
