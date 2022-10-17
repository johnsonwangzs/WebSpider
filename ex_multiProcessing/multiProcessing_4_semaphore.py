# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-06
# @file    : multiProcessing_4_semaphore.py
# @function: 队列、信号量（同步和互斥）。生产者与消费者问题。


from multiprocessing import Process, Semaphore, Lock, Queue
import time
from random import random

# 经测试，使用全局的Queue、Semaphore、Lock的话可能会有问题。因此统一到自定义进程类中。


class TestConsumer(Process):
    """
    模拟消费者。
    """
    def __init__(self, buffer: Queue, sema: Semaphore(), lock: Lock()):
        Process.__init__(self)
        self.lock = lock
        self.sema = sema
        self.buffer = buffer

    def run(self):
        """
        当队列内不为空时，可以取出。
        :return:
        """
        while True:
            if not self.buffer.empty():
                self.sema.acquire()  # 获得一个存取信号量
                self.lock.acquire()  # 取得时候，要加锁
                print('Consumer-' + str(self.pid) + ' GET ' + str(self.buffer.get()))
                print('CurQueueSize: ', self.buffer.qsize())
                print('--------')
                self.lock.release()  # 取完，要释放锁
                time.sleep(1)
                self.sema.release()  # 释放一个存取信号量


class TestProducer(Process):
    """
    模拟生产者。
    """
    def __init__(self, buffer: Queue, sema: Semaphore(), lock: Lock()):
        Process.__init__(self)
        self.lock = lock
        self.sema = sema
        self.buffer = buffer

    def run(self):
        """
        当队列不是满的时候，可以放入。
        :return:
        """
        while True:
            if not self.buffer.full():
                self.sema.acquire()
                num = random()
                self.lock.acquire()
                self.buffer.put(num)  # 放入内容
                print('Producer-' + str(self.pid) + ' PUT ' + str(num))
                print('CurQueueSize: ', self.buffer.qsize())
                print('--------')
                self.lock.release()
                time.sleep(1)
                self.sema.release()


if __name__ == '__main__':
    myBuffer = Queue(5)  # 队列即存取空间
    mySema = Semaphore(12)  # 存取操作信号量
    myLock = Lock()  # 操作队列的锁
    for i in range(5):  # 产生生产者
        p = TestProducer(myBuffer, mySema, myLock)
        p.start()
    for i in range(5):  # 产生消费者
        p = TestConsumer(myBuffer, mySema, myLock)
        p.start()
