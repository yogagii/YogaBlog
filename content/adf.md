Title: Microsoft Azure Data Factory
Date: 2022-11-22
Category: Cloud
Author: Yoga
Tags: Azure, ETL

## DAYU

### 申请资源

* ADF PaaS Service
* IR
* Azure SQL Server
* Key Vault
* AWS S3
* Azure Date Lake Storage

## Linked Service

### 1.Amazon S3

Authentication type: Access Key

Access Key ID: ###

Secret access key: ###

### 2.Azure Blob Storage

Authentication type: SAS URI

SAS URL: https://xxx.blob.core.chinacloudapi.cn/containername

SAS token: sv=2020-02-10&st=2022-10-11###

## Pipelines

### AWS S3 -> Azure Data Lake Storage

Source: 
* Linked service: DelimitedText
* File Path: <bucketname>/RowZone/MANU 踩坑：多层路径写在一起，自己用/分开

Sink:
* Linked service: DelimitedText

踩坑: s3中不能有.DS_Store, ~$MATERIAL_MASTER.xlsx这种隐藏文件

---

## IPRO

### Sharepoint -> Azure Data Lake Storage

https://docs.microsoft.com/en-us/azure/data-factory/connector-sharepoint-online-list?tabs=data-factory#prerequisites

1. 创建 app registration，storage account
2. sharepoint 授权 app
3. Datafactory 创建sharepoint连接器
4. Datafactory 创建pipeline: getToken -> copy data

### Azure Data Lake Storage -> Azure Databricks

https://docs.microsoft.com/zh-cn/azure/storage/blobs/data-lake-storage-use-databricks-spark

1. 创建 storage account, app registration, databricks cluster
2. 在 containers 里上传csv
3. 在databricks 中挂载(mount) csv

### Azure SQL Database 1 -> Azure Data Lake Storage -> Azure SQL Database 2

1. 创建 SQL database
2. Datafactory 创建pipeline: copy data (db1 -> storage) -> Notebook(databricks) -> copy data (storage -> db2)
