import redis
import time
import logging

# 需求: 文章按照用户投票 + 文章发表的时长计算得分进行排序展示，得分 = 文章得到的票数 * 常量 + 文章发布的时间
# 设计: ZSET time: 文章Id:文章创建时间
#      SET  voted + 文章Id: 用户Id 每篇文章给它投票的用户
#      ZSET score: 文章Id:文章得分(时间+投票)
#      HASH votes: 文章Id:被投票次数

# 用于判断文章发布时间是否超过一周，超过不能投票
ONE_WEEK_SECOND = 7 * 86400
# 按照一天需要200票计算得出常量
VOTE_SCORE = float(86400 / 200)


def article_vote(conn, user_id, article):
    # 当前时间与文章创建时间差
    offset = time.time() - ONE_WEEK_SECOND
    create_time = conn.zscore('time', article)
    # 文章不存在或超过一周时间不能投票
    if create_time is None or offset > create_time:
        logging.error('User has voted or time over one week or article is None')
        return
    else:
        # 获取文章id
        article_id = article.partition(':')[-1]
        # 准备投票,下面三步需要保证原子性
        if conn.sadd('voted:' + article_id, user_id):
            # 至此说明用户是第一次投票，给文章加分，
            conn.zincrby('score', VOTE_SCORE, article)
            # 将记录文章的投票次数加1
            conn.hincrby(article, 'votes', 1)


connection = redis.Redis(host='10.192.30.215', port=6379, db=2, password='dpp123456+_)')
article_vote(connection, 1, 'article:1')
