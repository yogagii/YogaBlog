Title: MS Graph API
Date: 2021-6-4
Category: Backend
Tags: Microsoft
Author: Yoga

## Token

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
  'https://login.microsoftonline.com/jnj.onmicrosoft.com/oauth2/v2.0/token',
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

### grant_type: client_credentials

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
      'https://login.microsoftonline.com/jnj.onmicrosoft.com/oauth2/v2.0/token',
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

## SharePoint

### Get docSiteId

API | params | response  
- | - | -
GET https://graph.microsoft.com/v1.0/sites/jnj.sharepoint.com:/teams/#siteName# | siteName: string | "sites": [ { "@odata.type": "microsoft.graph.site"} ]

### Get document lists

Get the collection of lists for a site.

API | params | response  
- | - | -
GET https://graph.microsoft.com/v1.0/sites/#site-id#/lists | docSiteId: string | "lists": [ { "@odata.type": "microsoft.graph.list" }]

### Get document from each list

Returns the metadata for an item in a list.

API | params | response  
- | - | -
GET https://graph.microsoft.com/v1.0/sites/#site-id#/lists/#list-id#/items/ | docSiteId: string, list.id: string, expand: fields(select) | "items": [ { "@odata.type": "microsoft.graph.baseItem" }]


microsoft.graph.baseItem:

Property name | Type | Description
- | - | -
id | string | The unique identifier of the item. Read-only.
createdBy | identitySet | Identity of the creator of this item. Read-only.
createdDateTime | DateTimeOffset | The date and time the item was created. Read-only.
eTag | string | ETag for the item. Read-only.
lastModifiedBy | identitySet | Identity of the last modifier of this item. Read-only.
lastModifiedDateTime | DateTimeOffset | The date and time the item was last modified. Read-only.
parentReference | itemReference | Parent information, if the item has a parent. Read-write.
webUrl | string (url) | URL that displays the item in the browser. Read-only.

additional item:

Property name | Type | Description | Value
- | - | - | -
pageUrl | string | URL that display item in browser | https://jnj.sharepoint.com/:w:/r/teams/#siteName#/_layouts/15/Doc.aspx?sourcedoc=%7B${item.eTag.slice(1, 37)}%7D&file=${encodeURI(item.fields.LinkFilename)}&action=default&mobileredirect=true



