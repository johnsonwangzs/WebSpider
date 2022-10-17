# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-05
# @file    : multiProcessing_3_lock.py
# @function: 进程锁（互斥访问资源）。可以解决multiProcessing_3中的输出错位问题。


from multiprocessing import Process, Lock


class MyProcess(Process):
    def __init__(self, loop, lock):
        Process.__init__(self)
        self.loop = loop
        self.lock = lock

    def run(self):
        for count in range(self.loop):
            self.lock.acquire()
            print('Pid: ' + str(self.pid) + ' LoopCount: ' + str(count))
            self.lock.release()


if __name__ == '__main__':
    pLock = Lock()
    for i in range(50, 60):  # 效果可能不明显，可多试几次，或调大参数
        p = MyProcess(i, pLock)
        p.start()








