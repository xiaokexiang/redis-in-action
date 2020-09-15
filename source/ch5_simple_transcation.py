import threading
import time

from source import connection

"""
演示无事务情况下三个线程分别加减
"""


def incr_decr_no():
    print(connection.incr('no_tran'))
    time.sleep(.5)
    connection.decr('no_tran')


# 生成三个线程执行加减法
def no_transaction():
    for i in range(3):
        threading.Thread(target=incr_decr_no).start()


def incr_decr():
    # 获取队列
    pipeline = connection.pipeline()
    pipeline.incr('tran')
    time.sleep(1)
    pipeline.decr('tran')
    print(pipeline.execute()[0])


def transaction():
    for i in range(3):
        threading.Thread(target=incr_decr).start()
    time.sleep(.5)


# result: 1 2 3
no_transaction()

# result: 1 1 1
transaction()
