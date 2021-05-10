Title: Redis
Date: 2020-07-25
Category: Backend
Tags: database
Author: Yoga

- 用作缓存
- 用作存 cookie,session: 容量小，提升速度; 负载均衡指到其他进程里，

```js
// callback.js
req.session.aadAccessToken = tokenRes.data.access_token
req.session.aadRefreshToken = tokenRes.data.refresh_token
req.session.aadExpiresAt = Date.now() + tokenRes.data.expires_in * 1000

req.session.userId = user.userId;
req.session.uid = user.id;
req.session.role = user.sysRole;

// isLoggedIn.js
if (req.session && req.session.uid && req.session.aadRefreshToken) {
  return proceed()
}

return res.status(401).json({
  message: 'Unauthorized',
  sso_url: `https://login.microsoftonline.com/3ac94b33-9135-4821-9502-eafda6592a35/oauth2/v2.0/authorize?${qs.stringify(
    params
  )}`,
})
```

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

```js
brew services start redis
brew services list
redis-cli ping
redis-cli -h 127.0.0.1
CONFIG SET requirepass "xxxxxx" // 同local.js
AUTH "xxxxxx"
select 4 // db
flushdb // clear database
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
