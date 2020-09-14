> 基于内存存储的`非关系型`数据库，支持五种数据结构，并支持`发布与订阅`、`主从复制`、`持久化`等功能。

### Redis数据结构

#### STRING

可以存储`字符串`、`整数`或`浮点数`。

| 命令        | 作用                                                        |
| ----------- | ----------------------------------------------------------- |
| GET         | 获取存储在指定key的值                                       |
| SET         | 设置存储在指定key的值                                       |
| DEL         | 删除存储在指定key的值(任何类型都通用)                       |
| INCR        | 将键存储的值加1                                             |
| DECR        | 将键存储的值减1                                             |
| INCRBY      | 将键存储的值加上整数                                        |
| DECRBY      | 将键存储的值减去整数                                        |
| INCRBYFLOAT | 将键存储的值加上浮点数                                      |
| APPEND      | 将value追加到旧值后，返回追加后值长度                       |
| GETRANGE    | 获取指定闭区间的字符串                                      |
| SETRANGE    | 从某个index开始替换字符串                                   |
| GITBIT      | 将字符串转换为二进制位串，并返回位串中指定index的二进制位值 |
| SETBIT      | 将二进制串中指定index替换为指定的值                         |
| BITCOUNT    | 统计二进制串中指定区间内值为1的数量                         |
| BITOP       | 将多个二进制位串进行位运算并把结果保存在指定key中           |

```shell
$ SET hello world
"OK"
$ GET hello
"world"
# 删除指定key的value，返回删除成功的数量
$ DEL hello
"1"
# 获取key的值不存在返回null
$ GET hello
(niL)
# 将hello追加到旧值后
$ APPEND hello hello
"10"
# 获取字符串[0,4]
$ GETRANGE hello 0 4
"hello"
# 换成hello world
$ SETRANGE 5 world
"10"
```

> Redis中key`大小写敏感`，`GET HELLO` 不同于 `GET hello`。
>
> `keys *`可以查看全部的keys

#### LIST

`LIST`列表结构可以`有序`、`重复`的存储`多个字符串`。类比Java中的`Map<key, List<String>>`结构。

| 命令   | 作用                                   |
| ------ | -------------------------------------- |
| LPUSH  | 将给定的值推入列表的`左端`             |
| RPUSH  | 将给定的值推入列表的`右端`             |
| LRANGE | 获取列表指定范围的所有值               |
| LINDEX | 获取列指定位置上的单个元素             |
| LPOP   | 从列表的`左端`移除一个值，并返回该值   |
| RPOP   | 从列表的`右端`移除一个值，并返回该值   |
| LTRIM  | 对列表进行`修剪`，只保留指定范围的元素 |
| LLEN   | 返回列表的长度                         |

```shell
# 左端推入一个值，并返回该key对应的列表数量
$ LPUSH list hello
"1"
$ RPUSH list world
"2"
$ LINDEX list 0
"hello"
$ LPUSH list say
# 查询列表的全部值
$ LRANGE list 0 -1
1)  "say"
2)  "hello"
3)  "world"
# 移除列表左端值并返回
$ LPOP list
"say"
# 移除列表右端值并返回
$ RPOP list
"world"
```

##### 阻塞式列表操作

| 命令                                     | 作用                                                         |
| ---------------------------------------- | ------------------------------------------------------------ |
| BLPOP [key-name...] timeout              | 1. 从第一个非空列表弹出最`左端`的元素<br>2. 或在timeout秒之内阻塞并等待可弹出元素出现 |
| BRPOP  [key-name...] timeout             | 1. 从第一个非空列表弹出最`右端`的元素<br/>2. 或在timeout秒之内阻塞并等待可弹出元素出现 |
| RPOPLPUSH <source-key>  <dest-key>       | 从source中弹出最右边元素，<br>并推入dest最左端并返回该元素   |
| BRPOPLPUSH<source-key><dest-key> timeout | 相比`RPOPLPUSH`，如果source没有元素<br>那么会阻塞等待timeout |

> 以上四个command常用于`redis队列`。

```shell
# 弹出list最左端的元素(only one)，直到5s后超时
$ BLPOP list 5
 1)  "list"
 2)  "hello"
# 弹出source最右侧元素，推入dest最左侧
$ RPOPLPUSH source dest
null
# 弹出source最右侧元素，推入dest最左侧，阻塞直到timeout
$ BRPOPLPUSH source dest
<空>
```

#### SET

`SET`集合结构可以`无序`、`不重复`的存储`多个字符串`。类比Java中的`Map<key, Set<String>>`结构。

| 命令                    | 作用                                                         |
| ----------------------- | ------------------------------------------------------------ |
| SADD                    | 将给定元素添加到集合中                                       |
| SMEMBERS                | 返回集合包含的所有元素                                       |
| SISMEMBER               | 检查指定元素是否存在集合中                                   |
| SREM                    | 如果给定的元素存在于集合中，那么移除该元素                   |
| `SCARD`                 | 返回集合中元素的数量                                         |
| SRANDMEMBER key [count] | 从集合里面随机返回一个或多个元素，count>0返回不重复，<0则会重复 |
| SPOP                    | 随机的从集合中移除一个元素并返回                             |
| SMOVE                   | 从source中移除元素并添加到dest中，成功为1，否则为0           |

```shell
# 添加元素到指定key的值集合中，返回添加的数量
$ SADD set hello world ya
"3"
# 获取集合中的全部元素
$ SMEMBERS set
1) "world"
2) "ya"
3) "hello"
# 查询hello是否存在key为set的值集合中
$ SISMEMBER set hello
"1"
$ SISMEMBER set hello1
"0"
# 如果hello存在key为set的值集合中，那么移除该元素
$ SREM set hello
"1"
$ SREM set hello
"0"
```

##### 多个集合的处理命令

| 命令                    | 作用                            |
| ----------------------- | ------------------------------- |
| SDIFF <key> [<key>...]  | 多个集合取`差集`                |
| SDIFFSTORE              | 多个集合取差集将结果存入某个key |
| SINTER <key> [<key>...] | 多个集合取`交集`                |
| SINTERSTORE             | 多个集合取交集将结果存入某个key |
| SUNION <key> [<key>...] | 多个集合取`并集`                |
| SUNIONSTORE             | 多个集合取并集将结果存入某个key |

```shell
$ SADD set1 hello
$ SADD set2 world
# 返回set1与set2的差集
$ SDIFF set1 set2
1)  "hello"
# 将差集结果存入res
$ SDIFFSTORE res set1 set2
"1"
# 取交集
$ SINTER set1 set2
<空>
# 取并集
$ SUNION set1 set2
"world"
"hello"
```

#### HASH

`HASH`散列结构可以`无序`、`不重复`的存储多个`字符串或数值`类型的键值对。类比Java中`Map<key, HashMap<v1,v2>>`。

| 命令      | 作用                                   |
| --------- | -------------------------------------- |
| HSET      | 给指定的key关联键值对                  |
| HGET      | 获取指定的key的键值对中`指定键的值`    |
| HGETALL   | 获取指定key关联的全部键值对            |
| HDEL      | 如果键值对中存在指定键，那么移除这个键 |
| HINCRBY   | 将键值对中键的值增加指定数量           |
| HLEN      | 返回`HASH`中键值对数量                 |
| HMGET     | 批量获取一个或多个键的值               |
| HMSET     | 批量的设置一个或多个键的值             |
| `HEXISTS` | 检查指定键是否存在散列中               |
| HKEYS     | 获取散列包含的所有键                   |
| HVALS     | 获取散列包含的所有值                   |
| HGETALL   | 获取散列包含的全部键值对               |

```shell
# 给key为hash的设置键值对，如果键值对中的键存在，那么返回0，否则返回1
$ HSET hash hello world
(integer)1
$ HSET hash hello world
(integer)0
$ HSET hash ni hao
(integer)1
# 获取指定key的键值对中指定键的值
$ HGET hash hello
"world"
# 获取指定key的全部键值对
$ HGETALL hash
"hello"
"world"
"ni"
"hao"
# 若键值对中存在指定键hello和ni，那么移除它们
# 与DEL不同。后者删除全部的值
$ HDEL hash hello ni
(integer)2
$ HGETALL hash
(empty list or set)
```

#### ZSET

`ZSET`结构是`有序`、`不重复`的存储多个键值对。其中有序集合的键被称为`成员(member)`，值被称为`分值(score)`，分值必须为浮点数。`ZSET`是redis中唯一一个既可以根据`成员`访问，也可以根据`分值及分值的排列顺序`来访问元素的结构。

| 命令                  | 行为                                         |
| --------------------- | -------------------------------------------- |
| ZADD key score member | 添加一个带有给定分值的成员添加到有序集合中   |
| `ZRANGE`              | 根据元素在ZSET中所处位置，从ZSET获取多个元素 |
| ZRANGEBYSCORE         | 获取ZSET在给定分值范围内的所有元素           |
| ZREM                  | 如果给定的成员存在ZSET集合，那么移除该成员   |
| ZINCRBY               | 将键值对中指定的键的分数增加指定数值         |
| `ZSOCRE`              | 输出键值对中指定键的分数                     |
| `ZCARD`               | 返回`ZSET`中成员数量                         |
| ZCOUNT                | 返回介于[min,max]之间分值元素的数量          |
| ZRANK                 | 返回元素在`ZSET`的排名                       |

```shell
# 添加元素到ZSET中，如果member存在，会返回0，否则为1
$ ZADD zset 100 first
(integer)1
$ ZADD zset 200 second
(integer)1
# 输出键为second的分数
$ ZSCORE zset second
"200"
# 查询指定index的元素，不包括score
$ ZRANGE zset 0 -1
"first"
"second"
# 查询指定index的元素，包括score
$ ZRANGE zset 0 -1 WITHSCORES
1) "first"
2) "100"
3) "second"
4) "200"
# 获取给定分值范围[0,100]内的从0开始的1个元素
$ ZRANGEBYSCORE zset 0 100 WITHSCORES LIMIT 0 1
1) "first"
2) "100"
# 若成员们存在ZSET，那么移除该成员们
$ ZREM zset first second
(integer) 2
# 将键为first的分数增加101
$ ZINCRBY zset 101 first
"201"
```

##### 有序集合命令

| 命令               | 作用                                                         |
| ------------------ | ------------------------------------------------------------ |
| ZREVRANK           | 返回`ZSET`中member的排名，按照分值从大到小排列               |
| `ZREVRANGE`        | 返回`ZSET`给定范围内的成员，按照分值从大到小排列             |
| `ZRANGEBYSCORE`    | 返回有序集合中分值介于[min,max]的所有成员，按照分值从小到大排列 |
| ZREVRANGEBYSCORE   | 与`ZRANGEBYSCORE`顺序相反，从大到小排列                      |
| ZREMRANGEBYRANK    | 移除`排名`介于[start,stop]之间的所有成员                     |
| `ZREMRANGEBYSCORE` | 移除`分值`介于[min,max]之间的所有成员                        |
| `ZINTERSCORE`      | 对于多个`ZSET`进行`交集`运算                                 |
| `ZUNIONSTORE`      | 对于多个`ZSET`进行`并集`运算                                 |

> `ZSET`默认按照`score升序`排序。

```shell
# 定义如下zset集合
$ ZRANGE zset 0 -1 WITHSCORES	
1)  "n2"
2)  "5"
3)  "n1"
4)  "10"
5)  "n3"
6)  "15"
# 获取n3的排名
$ ZREVRANK zset n3
"0"
# 降序获取范围内元素
$ ZREVRANGE zset 0 -1 WITHSCORES
1)  "n3"
2)  "15"
3)  "n1"
4)  "10"
5)  "n2"
6)  "5"
# 返回分数在[6,10]内，index=0开始的第一个元素
$ ZRANGEBYSCORE zset 6 10 WITHSCORES LIMIT 0 1

# 定义两个ZSET集合
$ ZRANGE zset-1 0 -1 WITHSCORES
1)  "a"
2)  "1"
3)  "b"
4)  "2"
5)  "c"
6)  "3"
$ ZRANGE zset-2 0 -1 WITHSCORES
1)  "d"
2)  "0"
3)  "c"
4)  "1"
5)  "b"
6)  "4"
# 多个`ZSET`进行交集运算,取分值最大的哪个作为新的key中的score
$ ZINTERSTORE zinter 2 zset-1 zset-2 AGGREGATE MAX
"2"
# 多个`ZSET`进行并集运算,取分值综合作为新的key中的score
$ ZUNIONSTORE zunion 2 zset-1 zset-2 AGGREGATE SUM
"4"
```

---

### 发布与订阅

> `发布与订阅(pub/sub)`的特点是`订阅者(subscribe)`负责订阅`频道(channel)`，`发布者(publisher)`负责向频道中发送`二进制字符串`消息。
>
> ![](https://image.leejay.top/image/20200914/PGhhPKDQGtFh.png?imageslim)