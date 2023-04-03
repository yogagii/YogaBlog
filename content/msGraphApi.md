Title: MS Graph API
Date: 2021-6-4
Category: Cloud
Tags: Microsoft
Author: Yoga

## SharePoint

### Get docSiteId

API | params | response  
- | - | -
GET https://graph.microsoft.com/v1.0/sites/xxx.sharepoint.com:/teams/#siteName# | siteName: string | "sites": [ { "@odata.type": "microsoft.graph.site"} ]

### Get document lists

Get the collection of lists for a site.

API | params | response  
| - | - | -
GET https://graph.microsoft.com/v1.0/sites/#site-id#/lists | docSiteId: string | "lists": [ { "@odata.type": "microsoft.graph.list" }]

### Get document from each list

Returns the metadata for an item in a list.

API | params | response  
| - | - | -
GET https://graph.microsoft.com/v1.0/sites/#site-id#/lists/#list-id#/items/ | docSiteId: string, list.id: string, expand: fields(select) | "items": [ { "@odata.type": "microsoft.graph.baseItem" }]


microsoft.graph.baseItem:

Property name | Type | Description
| - | - | -
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
| - | - | - | -
pageUrl | string | URL that display item in browser | https://xxx.sharepoint.com/:w:/r/teams/#siteName#/_layouts/15/Doc.aspx?sourcedoc=%7B${item.eTag.slice(1, 37)}%7D&file=${encodeURI(item.fields.LinkFilename)}&action=default&mobileredirect=true

---

## Sharepoint API

Step1. 在 portal.azure.com 新建app (App registrations) 并生成client secret

Step2. 在 teams 里 create a team, Apps -> Sharepoint -> Copy link

Step3. Grant permission to your app go to https://[YourSharePointCollectionURL]/_layouts/15/appinv.aspx

![sharepoint api](img/sharepointapi1.png)

### Authentication Token

__POST__ https://accounts.accesscontrol.windows.net/{{tenantId}}/tokens/OAuth/2/

Headers: Content-Type = application/x-www-form-urlencoded

Body:

Key | Value
| - | -
client_id | {{clientId}}@{{tenantId}}
resource | 00000003-0000-0ff1-ce00-000000000000/jnj.sharepoint.com@{{tenantId}}
client_secret | {{secret_value}}
grant_type | client_credentials

```python
import requests, json

token_url = 'https://accounts.accesscontrol.windows.net/%s/tokens/OAuth/2/'%(tenantId)

auth_config={
    'grant_type': 'client_credentials',
    'client_id': '%s@%s'%(clientId, tenantId),
    'client_secret': clientSecret,
    'resource': '00000003-0000-0ff1-ce00-000000000000/xxx.sharepoint.com@%s'%(tenantId)
}

res = requests.post(url=token_url, data=auth_config)
token = json.loads(res.text)['access_token']
```

### Get List by title

__GET__ https://[YourSharePointCollectionURL]/_api/web/lists/GetByTitle('[list name]')/items

Headers: Authorization = Bearer {{token}}

### Get Files by folder

__GET__ https://[YourSharePointCollectionURL]/_api/web/GetFolderByServerRelativeUrl('Shared Documents/General')/Files

Headers: Authorization = Bearer {{token}}

### Get List by title

__GET__ https://[YourSharePointCollectionURL]/_api/web/GetFileByServerRelativeUrl('/teams/{{sitename}}/Shared Documents/General/{{filename}}')/$value

Headers: Authorization = Bearer {{token}}

### Create File

__POST__ https://[YourSharePointCollectionURL]/_api/web/GetFolderByServerRelativeUrl('/teams/{{sitename}}/Shared Documents/General')/Files/Add(url='[FileName]', overwrite=true)

Headers: Authorization = Bearer {{token}}

Body: binary

```python
from io import BytesIO
import csv
from requests.structures import CaseInsensitiveDict

sourcedf = spark.sql(f"select * from <TableName>");

csv_buffer = BytesIO()
data = sourcedf.toPandas()
data.to_csv(csv_buffer, index = False, encoding = "utf_8_sig")
content = csv_buffer.getvalue()

send_url = "https://[YourSharePointCollectionURL]/_api/web/GetFolderByServerRelativeUrl('/teams/{{sitename}}/Shared Documents/General')/Files/Add(url='[FileName]', overwrite=true)"

headers = CaseInsensitiveDict()
headers["Authorization"] = 'Bearer %s'%(token)

res = requests.post(url=send_url, headers=headers, data=content)
```

https://www.c-sharpcorner.com/article/how-to-test-sharepoint-online-rest-apis-using-postman-tool/

https://learn.microsoft.com/zh-cn/sharepoint/dev/sp-add-ins/complete-basic-operations-using-sharepoint-rest-endpoints

