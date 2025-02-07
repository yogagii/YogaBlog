Title: Azure Blob Storage
Date: 2024-03-29
Category: Cloud
Tags: Azure
Author: Yoga

1. list file

```js
/* eslint-disable no-undef */
const { ContainerClient } = require("@azure/storage-blob");

const azure = {
  blobContainer: "xxx",
  storageAccount: "xxx",
  sasDomain: "blob.core.xxx.cn",
  containerName: "xxx",
  sasToken: "sp=xxx",
};

const getStorageDetails = () => {
  return {
    containerName: azure.blobContainer,
    storageAccount: azure.storageAccount,
    sasToken: azure.sasToken,
    sasDomain: azure.sasDomain,
    sasUrl: `https://${azure.storageAccount}.${azure.sasDomain}/${azure.containerName}?${azure.sasToken}`,
  };
};

const listContainer = async (path = "ManualFile/") => {
  const { sasUrl } = getStorageDetails();
  const containerClient = new ContainerClient(sasUrl);
  for await (const blob of containerClient.listBlobsFlat()) {
    if (blob.name.startsWith(path)) {
      console.log(`Blob ${blob.name}`);
    }
  }
};

listContainer();
```

2. upload file

```js
const { ContainerClient } = require("@azure/storage-blob");
const crypto = require("crypto");
const fs = require("fs");

const TEST_LOCATION = "/test/";
const FILE_NAME = `test0328.csv`;
const TEST_DATA_CONTENT = fs.readFileSync("./test.csv", "utf-8");

const makeMD5 = (content) => {
  const buffer = Buffer.from(content);
  const md5 = crypto.createHash("md5").update(content).digest("hex");
  return md5;
};

async function getBlockBlobClientByFileName(fileName) {
  const { sasUrl } = getStorageDetails();
  const containerClient = new ContainerClient(sasUrl);
  return containerClient.getBlockBlobClient(`${TEST_LOCATION}${fileName}`);
}

const uploadFileToAzureStorageBlob = async (file) => {
const md5string = makeMD5(TEST_DATA_CONTENT);
const buffer = Buffer.from(md5string, "hex");


const blockBlobClient = await getBlockBlobClientByFileName(file.name);
const uploadDataResponse = await blockBlobClient.uploadData(file.data, {
  blobHTTPHeaders: {
    blobContentMD5: buffer,
  },
});
};

uploadFileToAzureStorageBlob({
  name: FILE_NAME,
  data: Buffer.from(TEST_DATA_CONTENT),
});
```

3. download file

```js
const downloadFile = async (file) => {
  const blockBlobClient = await getBlockBlobClientByFileName(file.name);
  const downloadResponse = await blockBlobClient.downloadToFile('./test0315.csv');
};

downloadFile({
	name: FILE_NAME
})
```

4. image url

```js
const blockBlobClient = await getBlockBlobClientByFileName(fileName);
const downloadBlockBlobResponse = await blockBlobClient.download(0);
const content = downloadBlockBlobResponse.readableStreamBody;

response.setHeader("Content-Type", "image/jpg");
content.pipe(response);
```

https://learn.microsoft.com/zh-cn/azure/storage/blobs/storage-blob-upload-typescript

5. redirect url

如果直接在接口里返回视频资源，整个视频文件的内容会被加载到内存中可能会导致内存占用过高，可以选择通过HTTP响应重定向用户到Blob文件的URL，直接从blob中流式传输给客户端

```js
interface ExtendedRequestOptions extends RequestOptions {
	rejectUnauthorized?: boolean;
}

export async function downloadRequestHandler(
	request: Request,
	response: Response,
	next: NextFunction
) {
	const { destination, filename } = request.params;
	const fileType = request.params.fileType as FileType;
	const encodedFilename = encodeURIComponent(fileWithExtensionName);
	const splits = fileWithExtensionName.split(".");
	const contentType = getContentType(fileType, splits.pop());

	const { azure } = await getConfig();
	const { sasToken, sasDomain, blobContainer, storageAccount } = azure.cpBlob;
	const azureHost = `https://${storageAccount}.privatelink.${sasDomain}`;

	const targetPath = `/${blobContainer}/${destination}/${fileType}/${encodeURIComponent(
		encodedFilename
	)}?${sasToken}`;

	proxy(azureHost, {
		proxyReqPathResolver: () => targetPath,
		proxyReqOptDecorator: function (proxyReqOpts: ExtendedRequestOptions) {
			proxyReqOpts.rejectUnauthorized = false;
			if (proxyReqOpts.headers) {
				delete proxyReqOpts.headers["authorization"];
			}
			return proxyReqOpts;
		},
		userResHeaderDecorator: (headers) => {
			headers["content-type"] = contentType;
			return headers;
		},
	})(request, response, next);
}
```

---

### Monut blob

Linux 挂载步骤如下：

1. sudo su -
2. rpm -Uvh https://packages.microsoft.com/config/rhel/8/packages-microsoft-prod.rpm
    
    报错：rpm: unknown option
    `wget https://packages.microsoft.com/config/rhel/8/packages-microsoft-prod.rpm`
    `rpm -Uvh packages-microsoft-prod.rpm`
    
3. yum install blobfuse2
4. blobfuse2 --version
5. cd /app
    切回到自己权限再挂载，否则无法查看挂载后的文件夹
6. mkdir landing-blob
7. vi blobfuse-landing-blob.yaml
8. blobfuse2 mount ./mnt/landing-blob --config-file=./blobfuse-landing-blob-qa.yaml --disable-writeback-cache=true
    
    有缓存的情况下，相同文件名在blob里更新后vm上不会更新
    
9. 验证文件同步

使用blobfuse2将Azure Blob挂载到VM上时，VM重启后挂载确实可能会失效。这是因为blobfuse2的挂载通常是临时的，并不会在系统重启后自动重新挂载。采取以下几种方法来保持挂载的持久性：

1. **使用fstab文件**：你可以将blobfuse2的挂载信息添加到Linux系统的`/etc/fstab`文件中，这样在每次启动时，系统会自动尝试挂载指定的存储。
2. **使用启动脚本**：创建一个启动脚本来自动挂载blobfuse2，并将该脚本添加到系统的启动过程中。这样，每次VM启动时，都会自动执行挂载操作。

---

### Proxy

> https://${storageAccount}.privatelink.${sasDomain}/${blobContainer}/${destination}/${fileType}/${encodeURIComponent(encodedFilename)}

```js
const { azure } = await getConfig();
const { sasToken, sasDomain, blobContainer, storageAccount } = azure.cpBlob;
const azureHost = `https://${storageAccount}.privatelink.${sasDomain}`;

const targetPath = `/${blobContainer}/${destination}/${fileType}/${encodeURIComponent(
  encodedFilename
)}?${sasToken}`;

proxy(azureHost, {
  proxyReqPathResolver: () => targetPath,
  proxyReqOptDecorator: function (proxyReqOpts: ExtendedRequestOptions) {
    proxyReqOpts.rejectUnauthorized = false;
    if (proxyReqOpts.headers) {
      delete proxyReqOpts.headers["authorization"];
    }

    return proxyReqOpts;
  },
})(request, response, next);
```
下载图片
```bash
curl --request GET --url 'https://xxx.privatelink.blob.core.xxx.cn/blob/xxx/test.jpg?sasToken'  -k --output /home/test.jpg
```

```java
String blobUrl = blobClient.getBlobUrl();
// https://<your-account-name>.blob.core.windows.net/<your-container-name>/<your-blob-name>
// SAS 令牌访问 Blob
String sasToken = "?sv=<your-sas-token>";
String fullBlobUrl = blobUrl + sasToken;
```
