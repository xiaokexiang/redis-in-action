"""
使用redis的PUBLISH/SUBSCRIBE实现发布/订阅模式
"""
import threading
import time

from source import connection

"""
传入频道序列号&消息用于发布消息
"""


def publish():
    # 用于连接时长
    time.sleep(2)
    for i in [1, 2, 3, 4, 5, 6]:
        connection.publish('channel', i)


def subscribe(conn):
    # 启动线程发送消息
    threading.Thread(target=publish, args=()).start()
    # 获取发布/订阅对象
    pub_sub = conn.pubsub()
    # 订阅频道,一开始会出现确认信息：{'type': 'subscribe', 'pattern': None, 'channel': b'channel', 'data': 1}
    pub_sub.subscribe('channel')
    count = 0
    for item in pub_sub.listen():
        # {'type': 'message', 'pattern': None, 'channel': b'channel', 'data': b'1'}
        print(item)
        count += 1
        if count == 5:
            # 取消订阅也会出现信息：{'type': 'unsubscribe', 'pattern': None, 'channel': b'channel', 'data': 0}
            pub_sub.unsubscribe('channel')


subscribe(connection)
