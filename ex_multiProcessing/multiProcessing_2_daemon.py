# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-05
# @file    : multiProcessing_2_daemon.py
# @function: daemon和join的用法。
#            daemon:默认值为False。如果值为True，代表被操作的进程为后台运行的守护进程，且该进程无法创建新的进程。当该进程的父进程终止后，该进
#            程也随之终止。
#            join()可以阻塞当前进程，使其等待子进程结束后再继续执行。


from multiprocessing import Process
import time


class MyProcess(Process):
    def __init__(self, loop):
        Process.__init__(self)
        self.loop = loop

    def run(self):
        for count in range(self.loop):
            time.sleep(1)
            print('Pid: ' + str(self.pid) + ' LoopCount: ' + str(count))


if __name__ == '__main__':
    for i in range(2, 5):
        p = MyProcess(i)
        p.daemon = True
        p.start()
        p.join()

    # daemon=True且无join()，主进程一旦结束，则子进程立即终止
    p = MyProcess(5)
    p.daemon = True
    p.start()

    # daemon=False，主进程结束后子进程不受影响
    p = MyProcess(6)
    p.start()

    print('Main process ended!')
