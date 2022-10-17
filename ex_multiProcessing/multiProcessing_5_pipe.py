# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-06
# @file    : multiProcessing_5_pipe.py
# @function: 管道。一个进程从Pipe一端输入对象，然后被Pipe另一端的进程接收，单向管道只允许管道一端的进程输入，而双向管道则允许从两端输入。


from multiprocessing import Process, Pipe


class PartyA(Process):
    def __init__(self, pipe: Pipe()):
        Process.__init__(self)
        self.pipe = pipe

    def run(self):
        self.pipe.send('Party-A msg.')
        print('Party-A received:', self.pipe.recv())


class PartyB(Process):
    def __init__(self, pipe: Pipe()):
        Process.__init__(self)
        self.pipe = pipe

    def run(self):
        print('Party-B received:', self.pipe.recv())
        self.pipe.send('Party-B msg.')


if __name__ == '__main__':
    pipe = Pipe(duplex=True)  # 双向为True，单向为False
    a = PartyA(pipe[0])
    b = PartyB(pipe[1])
    a.daemon = b.daemon = True
    a.start()
    b.start()
    a.join()
    b.join()
    print('Main process ended!')