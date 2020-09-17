import time

"""
模拟实现使用redis实现登陆存储token相关的逻辑
"""


# login -> token:user_info
def check_token(conn, token):
    return conn.hget('login', token)


"""
新增/更新token & 记录用户的商品浏览数据
"""


def update_token(conn, token, user, item=None):
    timestamp = time.time()
    # 登陆token & 用户
    conn.hset('login', token, user)
    # 最近登陆时间
    conn.zadd('recent', {token: timestamp})
    if item:
        # 如果用户浏览商品，记录下来
        conn.zadd('viewed' + token, {item: timestamp})
        # 移除旧的记录，只保留用户最近浏览的25个商品
        conn.zremrangebyrank('viewed' + token, 0, -26)


"""
限制会话数，定时清除
"""

QUIT = False
limit = 10000000


def clean_session(conn):
    while not QUIT:
        # 返回此key的指数量
        size = conn.zcard('recent')
        # 判断是否超过指定数量
        if size < limit:
            time.sleep(1)
            continue
        # 计算需要删除的会话index，超过100就按照100来删除
        end_index = min(size - limit, 100)
        # 获取需要删除的用户tokens
        tokens = conn.zrange('recent', 0, end_index - 1)
        session_key = []
        for token in tokens:
            # 填充需要清除的用户浏览商品表
            session_key.append('viewed' + token)
            # 填充购物车表
            session_key.append('cart' + token)
        # 批量删除用户浏览表
        conn.delete(*session_key)
        # 清空登陆已用户表
        conn.hdel('login', *tokens)
        # 清空最近登陆时间表
        conn.zrem('recent', *tokens)


"""
使用redis实现购物车功能
token 和 购物车进行绑定
"""


def add_to_cart(conn, token, item, count):
    # 如果商品数量为0，那么删除
    if count <= 0:
        conn.hrem('cart' + token)
    # 修改对应的商品数量
    else:
        conn.hset('cart' + token, item, count)
