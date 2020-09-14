"""
redis实现对数据行的缓存
包括何时将指定的数据行存入redis & 数据行每隔多少秒更新缓存
"""
import json
import time

from source import connection

QUIT = False


def schedule_to_cache(conn, row_id, delay):
    # 添加delay表
    conn.zadd('delay', {row_id: delay})
    # 添加调度表，score为时间戳
    conn.zadd('schedule', {row_id: time.time()})


"""
守护进程，结合延时判断是否需要缓存数据行
"""


def cache_rows(conn):
    while not QUIT:
        # 获取schedule表第一个元素及score(时间)
        next_value = conn.zrange('schedule', 0, 0, withscores=True)
        now = time.time()
        # 判断schedule下个值的时间是否超过now时间,超过说明还未到执行时机
        if not next_value or next_value[0][1] > now:
            time.sleep(0.5)
            continue
        row_id = next_value[0][0]
        # 获取延时
        delay = conn.zscore('delay', row_id)
        if delay <= 0:
            conn.zrem('delay', row_id)
            conn.zrem('schedule', row_id)
            conn.delete('inv' + row_id)
        # 模拟要保存缓存行数据
        row = {'row_id': '123'}
        conn.zadd('schedule', row_id, now + delay)
        # 保存为json格式
        conn.set('inv' + row_id, json.dumps(row))


schedule_to_cache(connection, "171", 0)
# cache_rows(connection)
