# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-06
# @file    : logging_usage.py
# @function: logging日志库的使用。


import logging


# 打印日志级别
def test_logging():
    """
    默认情况下日志打印只显示大于等于 WARNING 级别的日志。
    通过 logging.basicConfig() 可以设置 root 的日志级别，和日志输出格式。
    :return:
    """
    logging.basicConfig(level=logging.DEBUG)  # Logging.basicConfig() 需要在开头就设置，在中间设置并无作用
    # logging.basicConfig(filename='./example.log', level=logging.DEBUG)  # 将日志信息记录到文件
    logging.debug('Python debug')
    logging.info('Python info')
    logging.warning('Python warning')
    logging.error('Python Error')
    logging.critical('Python critical')
    logging.log(2, 'test')


def test_logging_time():
    """
    显示日志记录时间。
    :return:
    """
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.warning('is when this event was logged.')


def test_logging_level():
    """
    更改显示消息的格式。
    :return:
    """
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.debug('Python message format Debug')
    logging.info('Python message format Info')
    logging.warning('Python message format Warning')


# test_logging()
# test_logging_time()
test_logging_level()
