Title: Local Environment
Date: 2021-04-13
Category: Backend
Tags: Local
Author: Yoga

local.js:

```js
/**
* Local environment settings
*
this file to specify configuration settings for use while developing
* the app on your personal system.
*
* For more information, check out:
* https://sailsjs.com/docs/concepts/configuration/the-local-js-file
*/

module.exports = {
  // Any configuration settings may be overridden below, whether it's built-in Sails
  // options or custom configuration specifically for your app (e.g. Stripe, Mailgun, etc.)
  custom: {
    mailEnable: true,
    approvalDebugMode: true,
    frontendUrl: "http://localhost:8000",
    frontHost: "https://dev.fpa.jnj.com",
    host: "http://localhost:8443",
  },
  datastores: {
    default: {
      adapter: "sails-mysql",
      host: "localhost",
      port: 3306,
      user: "root",
      password: "root",
      database: "fpa",
    },
  },
  security: {
    cors: {
      allowOrigins: [
        "http://localhost:8000",
        "https://localhost:8000",
        "http://localhost:3000",
        "https://dev.fpa.jnj.com",
      ],
      allowRequestHeaders: "content-type,cache-control,pragma",
      allowResponseHeaders: "Location,Content-Type",
    },
  },
  port: 8443,
  http: {
    trustProxy: true,
  },
  session: {
    adapter: "@sailshq/connect-redis",
    pass: "XXXXXXXXXX",
    db: 5,
  },
  ssl: {
    disableCertificateValidation: true,
  },
};
```

## SSL

Error: unable to get local issuer certificate:

法一：

```js
async apiLoader(endpoint, forceUpdate = false) {
    try {
      const token = await this.getToken();
      const { data } = await axios.get(endpoint, {
        headers: {
          'X-SAP-LogonToken': token,
          Accept: 'application/json',
        },
        // httpsAgent
        httpsAgent: new https.Agent({ keepAlive: true, rejectUnauthorized: false }),
        baseURL: `${sails.config.custom.sap.endpoint}/biprws`,
        forceUpdate,
      });
      return data;
    } catch (error) {
      sails.log(`Api error: ${endpoint} ${error}`);
      if (error.message.includes('401')) {
        this.getNewToken();
      }
      throw error;
    }
  },
```

法二：
```js
// local.js
module.exports = {
  ssl: {
    disableCertificateValidation: true,
  },
}
```
