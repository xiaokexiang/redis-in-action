> 基于内存存储的`非关系型`数据库，支持五种数据结构，并支持`发布与订阅`、`主从复制`、`持久化`等功能。

### Redis数据结构

#### STRING

可以存储`字符串`、`整数`或`浮点数`。

| 命令 | 作用                                  |
| ---- | ------------------------------------- |
| GET  | 获取存储在指定key的值                 |
| SET  | 设置存储在指定key的值                 |
| DEL  | 删除存储在指定key的值(任何类型都通用) |

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
```

> Redis中key`大小写敏感`，`GET HELLO` 不同于 `GET hello`。

#### LIST

`LIST`列表结构可以`有序`、`重复`的存储`多个字符串`。类比Java中的`Map<key, List<String>>`结构。

| 命令   | 作用                                 |
| ------ | ------------------------------------ |
| LPUSH  | 将给定的值推入列表的`左端`           |
| RPUSH  | 将给定的值推入列表的`右端`           |
| LRANGE | 获取列表指定范围的所有值             |
| LINDEX | 获取列指定位置上的单个元素           |
| LPOP   | 从列表的`左端`弹出一个值，并返回该值 |
| RPOP   | 从列表的`右端`弹出一个值，并返回该值 |

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

#### SET

`SET`集合结构可以`无序`、`不重复`的存储`多个字符串`。类比Java中的`Map<key, Set<String>>`结构。

| 命令      | 作用                                       |
| --------- | ------------------------------------------ |
| sadd      | 将给定元素添加到集合中                     |
| SMEMBERS  | 返回集合包含的所有元素                     |
| SISMEMBER | 检查指定元素是否存在集合中                 |
| SREM      | 如果给定的元素存在于集合中，那么移除该元素 |

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

#### HASH

`HASH`散列结构可以`无序`、`不重复`的存储多个`字符串或数值`类型的键值对。类比Java中`Map<key, HashMap<v1,v2>>`。

| 命令    | 作用                                   |
| ------- | -------------------------------------- |
| HSET    | 给指定的key关联键值对                  |
| HGET    | 获取指定的key的键值对中`指定键的值`    |
| HGETALL | 获取指定key关联的全部键值对            |
| HDEL    | 如果键值对中存在指定键，那么移除这个键 |
| HINCRBY | 将键值对中键的值增加指定数量           |

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

| 命令          | 行为                                         |      |
| ------------- | -------------------------------------------- | ---- |
| ZADD          | 添加一个带有给定分值的成员添加到有序集合中   |      |
| ZRANGE        | 根据元素在ZSET中所处位置，从ZSET获取多个元素 |      |
| ZRANGEBYSCORE | 获取ZSET在给定分值范围内的所有元素           |      |
| ZREM          | 如果给定的成员存在ZSET集合，那么移除该成员   |      |
| ZINCRBY       | 将键值对中指定的键的分数增加指定数值         |      |
| ZSOCRE        | 输出键值对中指定键的分数                     |      |

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

