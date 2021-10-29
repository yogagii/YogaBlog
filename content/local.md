Title: Local Environment
Date: 2021-04-13
Category: Backend
Author: Yoga

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
