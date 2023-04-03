Title: Microsoft Azure Adminstrator
Date: 2022-04-13
Category: Cloud
Tags: Azure
Author: Yoga

## Azure Active Directory

用户和组身份：身份验证 + 访问授权

https://portal.azure.com/

https://portal.azure.com/#blade/Microsoft_AAD_IAM/LicensesMenuBlade/Overview

新建并切换域名：

Azure Active Directory -> Manage tenants -> create

创建用户：

Users -> New User

User Test 1: Aa123456

Bob: Caqu2794

Alice: myPassword1234

创建组：

Groups -> New Group -> 添加用户

Devices -> Device Settings -> 指定用户

Join Type: Azure AD joined / register

Azure DNS: 不能实现域名注册，只提供域名解析服务

---

## Authentication and Authorization
The basic steps required to use the OAuth 2.0 authorization code grant flow to get an access token from the Microsoft identity platform endpoint are:

1. Register your app with Azure AD.
2. Get authorization.
3. Get an access token.
4. Call Microsoft Graph with the access token.
5. Use a refresh token to get a new access token.

To configure an app to use the OAuth 2.0 authorization code grant flow, you'll need to save the following values when registering the app:

1. The Application (client) ID assigned by the app registration portal.
2. A Client (application) Secret
3. A Redirect URI (or reply URL) for your app to receive responses from Azure AD.

The first step to getting an access token for OAuth 2.0 flow is to redirect the user to the Microsoft identity platform /authorize endpoint. Azure AD will sign the user in and ensure their consent for the permissions your app requests. In the authorization code grant flow, after consent is obtained, Azure AD will return an authorization_code to your app that it can use at the Microsoft identity platform /token endpoint for an access token.

SailsJS

* route：路由
* policies: 每个接口前先调 isLoggedIn
* local: 放cliendId, secret, credentical
* IsLoggedIn: 检查session里是否有token
* callback：sso回调
* check：给前端返回userInfo和permission
* azuerTokenRefresher: 用户一直操作则刷新token过期时间

### grant_type: authorization_code

```js
// callback.js
const tokenReq = {
  client_id: sails.config.custom.azureAD.clientId,
  scope: sails.config.custom.azureAD.scope,
  code: req.query.code,
  redirect_uri: sails.config.custom.azureAD.redirectUri,
  grant_type: 'authorization_code',
  client_secret: sails.config.custom.azureAD.clientSecret,
}

const tokenRes = await axios.post(
  'https://login.microsoftonline.com/xxx.onmicrosoft.com/oauth2/v2.0/token',
  qs.stringify(tokenReq),
  {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  }
)

req.session.aadAccessToken = tokenRes.data.access_token
req.session.aadRefreshToken = tokenRes.data.refresh_token
req.session.aadExpiresAt = Date.now() + tokenRes.data.expires_in * 1000

const infoRes = await axios.get('https://graph.microsoft.com/v1.0/me/', {
  headers: {
    Authorization: `Bearer ${tokenRes.data.access_token}`,
  },
  params: {
    $select: fields.join(),
  },
})
```

```js
// isLoggedIn.js
module.exports = async function isLoggedIn(req, res, proceed) {
  if (req.session && req.session.uid && req.session.aadRefreshToken) {
    return proceed()
  }

  const params = {
    client_id: sails.config.custom.azureAD.clientId,
    response_type: 'code',
    redirect_uri: sails.config.custom.azureAD.redirectUri,
    response_mode: 'query',
    scope: sails.config.custom.azureAD.scope,
    state: req.headers.referer,
  }
  return res.status(401).json({
    message: 'Unauthorized',
    sso_url: `https://login.microsoftonline.com/#########/oauth2/v2.0/authorize?${qs.stringify(
      params
    )}`,
  })
}
```

### grant_type: client_credentials

```js
const tokenEndpoint = 'https://login.microsoftonline.com/#########/oauth2/v2.0/token'

const tokenReq = {
  client_id: sails.config.custom.azureAD.clientId,
  scope: 'https://graph.microsoft.com/.default',
  client_secret: sails.config.custom.azureAD.clientSecret,
  grant_type: 'client_credentials',
}

async function retriveToken() {
  const tokenRes = await axios.post(tokenEndpoint, qs.stringify(tokenReq), {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  })
  token = tokenRes.data.access_token
  setTimeout(retriveToken, 3300 * 1000)
}
```

### grant_type: refresh_token

```js
// azureTokenRefresher.js
module.exports = async function isLoggedIn(req, res, next) {
  if (req.session && typeof req.session.aadExpiresAt === 'number' && req.session.aadExpiresAt < Date.now() + 300000) {
    // Refresh the AD access token if it expires in 300s
    const tokenReq = {
      client_id: sails.config.custom.azureAD.clientId,
      scope: sails.config.custom.azureAD.scope,
      refresh_token: req.session.aadRefreshToken,
      redirect_uri: sails.config.custom.azureAD.redirectUri,
      grant_type: 'refresh_token',
      client_secret: sails.config.custom.azureAD.clientSecret,
    }
    const tokenRes = await axios.post(
      'https://login.microsoftonline.com/xxx.onmicrosoft.com/oauth2/v2.0/token',
      qs.stringify(tokenReq),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    )

    req.session.aadAccessToken = tokenRes.data.access_token
    req.session.aadExpiresAt = Date.now() + tokenRes.data.expires_in * 1000
  }
  return next()
}
```

---

## NestJS + Passport

auth/guards/aad-auth.guard.ts
```ts
import { Injectable } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';

@Injectable()
export class AADAuthGuard extends AuthGuard('aad') {}
```

auth/strategies/aad.strategy.ts
```ts
import { OIDCStrategy } from 'passport-azure-ad';
import { PassportStrategy } from '@nestjs/passport';
import { Injectable } from '@nestjs/common';

@Injectable()
export class AADStrategy extends PassportStrategy(OIDCStrategy, 'aad') {
  constructor() {
    super(
      {
        identityMetadata:
          'https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration',
        clientID: <ClientID>,
        clientSecret: <ClientSecret>,
        responseType: 'id_token',
        responseMode: 'form_post',
        issuer: null,
        audience: null,
        loggingLevel: 'info',
        passReqToCallback: true,
        validateIssuer: false,
        allowHttpForRedirectUrl: true,
        redirectUrl: <RedirectURL>,
      },
      (iss, sub, profile, accessToken, refreshToken, done) => {},
    );
  }

  async validate(payload: any) {
    return payload;
  }
}
```

https://www.npmjs.com/package/passport-azure-ad
