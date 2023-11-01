Title: Redis
Date: 2020-07-25
Category: Backend
Tags: database
Author: Yoga

- 用作缓存
- 用作存 cookie,session: 容量小，提升速度; 负载均衡指到其他进程里，

cookie 的过期时间和 redis 保持一致

```js
// local.js
session: {
  adapter: '@sailshq/connect-redis',
  pass: 'XXXXXXXXXXXXX',
  db: 5,
},
```

清缓存

```js
async function flushCacheWithDomain(domain) {
  if (!domain) {
    throw new Error('need domain.')
  }
  function innerScan(cursor) {
    return new Promise((resolve, reject) => {
      redisClient.scan(cursor, 'MATCH', `*${domain}*`, 'COUNT', '100', (err, res) => {
        if (err) {
          reject(err)
        }
        const [newCursor, keys] = res
        Promise.all(keys.map((key) => redisClient.del(key)))
          .then(() => {
            sails.log.info(`del ${keys.length} keys.`)
            if (newCursor === '0' || newCursor === 0) {
              resolve(1)
            } else {
              resolve(innerScan(newCursor))
            }
          })
          .catch(reject)
      })
    })
  }

  await innerScan('0')
}
```

## 本地启动

1. MAC

```bash
brew install redis
```

* start redis foreground
```bash
redis-server
```
  stop: Ctrl-C.

* start redis background
```bash
brew services start redis
brew services list
brew services stop redis # stop
```

* redis-cli
```bash
redis-cli ping
redis-cli -h 127.0.0.1 # 默认 port 6379
CONFIG SET requirepass "xxxxxx" # 同local.js
AUTH "xxxxxx"
select 4 # db
flushdb # clear database
KEYS * # get all keys
get sapToken # get certain key
ttl sapToken # get expire time
PSETEX sapToken 1500000 "xxx" # set
del sapToken # delete
shutdown # shutdown
```

2. LINUX

* 安装

```bash
wget https://download.redis.io/releases/redis-6.2.6.tar.gz # 下载
tar xzf redis-6.2.6.tar.gz # 解压
mv redis-6.2.6 /usr/local/redis # 移动
cd /usr/local/redis # 进入安装目录
yum -y install gcc automake autoconf libtool make # 安装gcc
make MALLOC=libc # 编译（指定分配器为libc）
make install PREFIX=/usr/local/redis # 安装
```

* 启动

vi redis.conf

/daemonize (查找daemonize)

daemonize no 改为 daemonize yes

```bash
./bin/redis-server redis.conf # 启动
ps -ef | grep redis # 查看进程
netstat -pan | grep 6379 # 查看端口

./bin/redis-cli
set test hello
get test
```

https://baijiahao.baidu.com/s?id=1722728002073366376&wfr=spider&for=pc

* 环境变量

vim ~/.bash_profile
```
export REDIS_HOME=/usr/local/redis
PATH=$PATH:$HOME/bin:$REDIS_HOME/bin
```
source ~/.bash_profile

* 远程连接

vi redis.conf
```bash
# bind 127.0.0.1 -::1 # 127.0.0.1只允许本机访问，加上#会变成0.0.0.0
protected-mode no  # yes 以守护进程方式启动 -> no 以配置文件方式启动
```
本地连接远程redis：redis-cli -h 10.49.xxx.xxx (不需要加端口号默认6379)

3. docker

```bash
docker run --restart=always -p 6379:6379 --name myredis -d redis:7.0.12
```

* 指定redis.conf 以及挂载data的目录

新建data文件夹 /var/docker/redis/data

下载 http://download.redis.io/redis-stable/redis.conf
放在目录 /var/docker/redis/redis.conf

```bash
docker run \
-p 6379:6379 \
--name vredis \
-v /var/docker/redis/redis.conf:/etc/redis/redis.conf \
-v /var/docker/redis/data:/data \
--restart=always \
-d redis:7.0.12 redis-server /etc/redis/redis.conf # -d 后台运行
```

* 进入容器

```bash
docker exec -it <CONTAINER_ID> bash # 以交互方式进入容器
redis-cli
ctrl+c # 退出 redis
exit # 退出 docker
```

## Redis 读写

```js
const redis = require('redis');
const { promisify } = require('util');

const redisClient = redis.createClient({
  db: sails.config.session.db,
  password: sails.config.session.pass,
  port: sails.config.session.port,
  host: sails.config.session.host,
});
const getRedisAsync = promisify(redisClient.get).bind(redisClient);

redisClient.psetex(sapTokenKey, 25 * 60 * 1000, val);

extoken = await getRedisAsync(sapTokenKey);
```

## 启用 Redis 密钥空间通知

```js
CONFIG SET notify-keyspace-events Ex

// client 1
redis-cli -h xxx-dev-rep-group-1-001.ugvuyh.0001.use1.cache.amazonaws.com
setex name 10 yoga

// client 2
redis-cli -h xxx-dev-rep-group-1-001.ugvuyh.0001.use1.cache.amazonaws.com --csv psubscribe '*'
// Reading messages... (press Ctrl-C to quit)
// "psubscribe","*",1
// "pmessage","*","__keyevent@0__:expired","name"
```

```js
const SubscribeExpired = () => {
  const sub = redis.createClient({
    db: sails.config.session.db,
    password: sails.config.session.pass,
    port: sails.config.session.port,
    host: sails.config.session.host,
  });
  const expiredSubKey = `__keyevent@${sails.config.session.db}__:expired`;
  sub.psubscribe(expiredSubKey, () => {
    sub.on('pmessage', async (pattern, channel, message) => {
      ...
    });
  });
};
// 只在instance1上注册事件
if (process.env.NODE_APP_INSTANCE === '0' || !process.env.NODE_APP_INSTANCE) {
  redisClient.send_command('config', ['set', 'notify-keyspace-events', 'Ex'], SubscribeExpired);
}
```

## 数据类型

### list 链表

lpush 生产者 （秒杀：前 100 名下单， redis 承受并发能力强）

rpop 消费者

### 哈希 map

通过 key 取到值， key 为任意字符串，快速定位到

### Redis Sets 集合

### Redis Sorted sets 有序集合

### Bitmap

活跃用户，快速查阅用户登录状态

## Redis 部署

### 单机

主从：一个 master 多个 slave

哨兵：master 挂了自动把某个 slav 变成 master

集群

### Redis 缓存击穿，穿透，雪崩

击穿：热点数据某一时刻到期了，大量数据一瞬间进入 db

穿透：故意访问不存在的数据

雪崩：一大批数据同一时间过期
