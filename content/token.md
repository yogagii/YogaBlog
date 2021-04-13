Title: Token
Date: 2021-04-13
Category: Backend
Tags: Token
Author: Yoga

## Version1:

```js
const { EventEmitter } = require('events');

let globalToken;
const emitter = new EventEmitter();

async getToken() {
  if (!globalToken) {
    globalToken = 'pending';
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = 0;
    const { data } = await axios.post(
      'logon/long',
      sails.config.custom.sap.auth,
      {
        baseURL: `${sails.config.custom.sap.endpoint}/biprws`,
      },
    );
    globalToken = data.logonToken;
    emitter.emit('token', globalToken);
    setTimeout(() => {
      globalToken = undefined;
    }, 1000 * 60);
  } else if (globalToken === 'pending') {
    await new Promise((res, rej) => {
      emitter.on('token', res);
      setTimeout(() => {
        rej();
      }, 3000);
    });
  }

  return globalToken;
},
```

## Version2:

```js
// let globalToken;
const authCache = {
  token: '',
  expiresAt: 0,
  updatePromise: null,
};

async getToken() {
  if (authCache.expiresAt < Date.now()) {
    authCache.expiresAt = Date.now() + 30 * 1000; // Avoid concurrency
    authCache.updatePromise = axios
      .post(
        'logon/long',
        sails.config.custom.sap.auth,
        {
          baseURL: `${sails.config.custom.sap.endpoint}/biprws`,
        },
      )
      .then((res) => {
        authCache.expiresAt = Date.now() + 50 * 60 * 1000;
        authCache.token = res.data.logonToken;
        authCache.updatePromise = null;
        fs.writeFile(
          path.join(process.cwd(), './sap_token'),
          authCache.token,
          (err) => {
            if (err) {
              sails.log.error(err);
            }
          },
        );
      })
      .catch(() => {
        authCache.expiresAt = 0;
      });
  }
  await authCache.updatePromise;
  return authCache.token;
},
```

## Version3: Redis

多实例只会有一个 Redis

```js
const redis = require('redis');
const { promisify } = require('util');

const redisClient = redis.createClient({
  db: sails.config.session.db,
  password: sails.config.session.pass,
  port: sails.config.session.port,
  host: sails.config.session.host,
})
const getRedisAsync = promisify(redisClient.get).bind(redisClient)

module.exports = {
  async getNewToken() {
    sails.log.info('Get new sap token')
    const newtoken = await axios
      .post('logon/long', sails.config.custom.sap.auth, {
        baseURL: `${sails.config.custom.sap.endpoint}/biprws`,
      })
      .then((res) => {
        redisClient.psetex('sapToken', 60 * 60 * 1000, res.data.logonToken)
        return res.data.logonToken
      })
      .catch((error) => {
        sails.log.error('Fetch sap token error: ', error)
      })
    return newtoken
  },

  async getToken() {
    let token = ''
    try {
      const val = await getRedisAsync('sapToken')
      if (!val) {
        throw Error('No Such Key')
      }
      redisClient.psetex('sapToken', 60 * 60 * 1000, val)
      token = val
    } catch (err) {
      token = await this.getNewToken()
    }
    return token
  },

  async apiLoader(endpoint, forceUpdate = false) {
    try {
      const token = await this.getToken()
      const { data } = await axios.get(endpoint, {
        headers: {
          'X-SAP-LogonToken': token,
          Accept: 'application/json',
        },
        baseURL: `${sails.config.custom.sap.endpoint}/biprws`,
        forceUpdate,
      })
      return data
    } catch (error) {
      sails.log(`Api error: ${endpoint} ${error}`)
      if (error.message.includes('401')) {
        this.getNewToken()
      }
      throw error
    }
  },
}
```

promise版
```js
return new Promise((resolve) => {
  redisClient.get('sapToken', async (err, val) => {
    console.log('redisClient sapToken: ', err, val);
    if (err || !val) {
      console.log('get newtoken');
      await axios
        .post(
          'logon/long',
          sails.config.custom.sap.auth,
          {
            baseURL: `${sails.config.custom.sap.endpoint}/biprws`,
          },
        )
        .then((res) => {
          console.log('newtoken: ', res.data);
          redisClient.psetex('sapToken', 60 * 60 * 1000, res.data.logonToken);
          resolve(res.data.logonToken);
        })
        .catch((error) => {
          sails.log.error('Fetch sap token error: ', error);
        });
    } else if (typeof val === 'string') {
      await redisClient.ttl('sapToken', (e, t) => {
        console.log('token rest time: ', e, t);
      });
      redisClient.psetex('sapToken', 60 * 60 * 1000, val);
      resolve(val);
    }
  });
});
```
