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