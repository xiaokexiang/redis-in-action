import redis
import time
import logging
from source import load_yaml

# 需求: 文章按照用户投票 + 文章发表的时长计算得分进行排序展示，得分 = 文章得到的票数 * 常量 + 文章发布的时间
# 设计: ZSET time: 文章Id:文章创建时间
#      SET  voted + 文章Id: 用户Id 每篇文章给它投票的用户
#      ZSET score: 文章Id:文章得分(时间+投票)
#      HASH votes: 文章Id:被投票次数

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
prop = load_yaml.get('../properties/env.yaml')
connection = redis.Redis(host=prop['redis']['server'],
                         port=prop['redis']['port'],
                         db=prop['redis']['db'],
                         password=prop['redis']['password'])

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
            logging.info("vote article success!")


def post_article(conn, user_id, title, link):
    # 设置初始值
    conn.setnx('article', 100)
    # 生成文章id，通过incr实现
    article_id = str(conn.incr('article'))
    # 生成文章已投票的key
    voted = 'voted:' + article_id
    # 构建文章已投票表
    conn.sadd(voted, user_id)
    # 设置已投票表过期时间
    conn.expire(voted, ONE_WEEK_SECOND)
    # 批量保存数据，每篇文章就是一个Hash结构
    article = 'article:' + article_id
    now = time.time()
    # hmset() is deprecated
    conn.hset(article, None, None, {'title': title, 'link': link, 'poster': user_id, 'time': now, 'votes': 1})
    # 构建评分排序的ZSET
    conn.zadd('score', {article: now + VOTE_SCORE})
    conn.zadd('time', {article: now})
    logging.info('post article success!')


post_article(connection, 168, 'hello world', 'https://hello.com/hello_world')
article_vote(connection, 169, 'article:101')
