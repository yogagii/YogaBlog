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

### 3.Azure Data Lake Storage Gen2

Authentication type: System Assigned Managed Identy

赋予的是创建者的个人权限

Authentication type: Service Principal

URL: https://[accountname].dfs.core.chinacloudapi.cn

Tenant: [Tenant ID]

Service principal ID: [Client ID]

Service principal key: ###

Azure cloud type: Azure China 踩坑：选Data Factory's cloud type会导致删文件失败

Test connection: To file path: [container] SP如果只到container的权限to linked services是不通的

### 4.Sharepoint

_踩坑：ADF不能连接跨 tenant 的 Sharepoint，Global 的 Sharepoint 和 IC 的 ADF 肯定不通_

解决方式：

1. 申请VM，在VM上安装Azure Storage Explorer, 用Filetransfer直接入湖
2. 将手工数据放在S3，用ADF copydata 从S3入湖
3. 将手动数据放在Sharepoint, 用ADF 调 Sharepoint API 入湖 (Graph API: Not Granted)

Sharepoint API 见 https://yogagii.github.io/ms-graph-api.html

---

## Activities 

## Move & transform 
### >>> Copy data

### AWS S3 -> Azure Data Lake Storage

Source: 
* Linked service: DelimitedText
* File Path: [bucketname]/RowZone/MANU 踩坑：多层路径写在一起，自己用/分开
* Recursively: 勾选的话当文件夹为空会报错

Sink:
* Linked service: DelimitedText

踩坑: s3中不能有.DS_Store, ~$MATERIAL_MASTER.xlsx这种隐藏文件

### Azure Data Lake Storage -> SQL Server

Source: 
* Linked service: Parquet
* File Path type: Wildcard file path
(Wildcard paths: [container]/[filepath]/*.snappy.parquet)
* Recursively: true

Sink:
* Linked service: Azure SQL Database (Table: @dataset().SQLTableName)
* Write behavior: Insert
* Bulk insert table lock: Yes
* Table option: Auto create table
* Pre-copy script: @{concat('drop table if exists ',item().TableName)} 更新失败不会回滚

_踩坑: ErrorCode=ParquetNotSupportedTypeGeneric,'Type=Microsoft.DataTransfer.Common.Shared.HybridDeliveryException,Message=Parquet file contained column 'txn', which is of a non-primitive, unsupported type.,Source=Microsoft.DataTransfer.Richfile.ParquetTransferPlugin,'_

加上 *.snappy.parquet 而不是 *.parquet，_delta_log/里包含checkpoint.parquet files

### Rest Resource -> 

Source:
* Linked Service: REST
* Dataset properties: v_url = concat(variables('v_url'), item(), concat('?agentId=',pipeline().parameters.v_agentId,'&agentName=',pipeline().parameters.v_agentName),'&stockDate=',formatDateTime(adddays(addhours(utcnow(),8),-1),'yyyy-MM-dd'))

_踩坑：默认UTC时间，需addhours(utcnow(),8)转成北京时间_

### HTTP -> Azure Data Lake Storage

用 HTTP 调取 Sharepoint 接口，将sharepoint文件入湖

Source:
* Linked Service: HTTP
* format: Binary
* Base URL: @{concat('https://xxx.sharepoint.com/teams/XXXTeam/_api/web/GetFileByServerRelativeUrl(''/teams/XXXTeam/Shared Documents/General/',linkedService().filename,''')/$value')
}
* Request method: GET
* Additional headers: Authorization: @{concat('Bearer ', activity('getToken').output.access_token)}

Sink:
* Linked Service: Azure Data Lake Storage Gen2
* format: Binary

用Binary可以保留原始文件格式，亲测csv，excel，pdf，png均能成功

## General

### >>> Web
Get Token
* URL: https://xxx/oauth2/token
* Method: POST
* Body: grant_type=client_credentials&client_id=xxx&client_secret=xxx
* Headers: Content-Type application/x-www-form-urlencoded

### >>> Lookup

* Source dataset: Azure SQL Database
* Dataset properties: SQLTableName = [Table_Name]
* Use query: Query
* Query: @concat('SELECT * FROM [Table_Name] where JobFlag=',pipeline().parameters.v_jobflag)
* First row only: False (默认勾选)

当query中原本就有'时需要两个'

@concat('select Batchrunid, ActivityCode=(stuff((select '','' + ActivityCode from ActivityLogs where Batchrunid=a.Batchrunid and ActivityStatus=''Failed'' for xml path('''') ),1,1,'''')) from ActivityLogs a WHERE a.BatchRunId=''',pipeline().parameters.BatchRunID,''' group by Batchrunid')

### >>> Stored procedure

提前在sql server创建好存储过程

* Linked Service: Azure SQL Database
* Stored procedure name: [Procedure_Name]
* Stored procedure parameters

## Iteration & conditionals

### >>> ForEach

在sql server中创建config table，遍历所有表执行worker

* Items: @activity('LookupConfigTable').output.value

_踩坑：ForEach 中调用 notebook 报错：java.lang.Exception: Unable to start python kernel for ReplId-6ab47-72d45-cb368-d, kernel exited with exit code 1. Another app is currently holding the xtables lock. Perhaps you want to use the -w option?_

* Sequential: 勾选后顺序执行

## Databricks

### >>> Notebook

* Notebook path
* Base parameters: 设置传入参数 "argument1": "value"

```python
dbutils.widgets.get("argument1") # value
```

_踩坑：ADF 调用notebook 报错：java.lang.Exception: Unable to start python kernel for ReplId-xxx, kernel exited with exit code 1. Another app is currently holding the xtables lock. Perhaps you want to use the -w option?_

解决方案：
1. 多个grandpa错开时间执行
2. 在ForEach 上Settings里勾选 Sequential 顺序执行，不并发
3. 调用 Notebook 时加上retry次数，Notebook 里需加上delete语句防止数据重复
4. Notebook 执行IPTABLES配置（未验证）

```python
%sh
IPTABLES="/sbin/iptables"
IPTABLES_WAIT="-w 20"
```

5. 微软建议：Cluster增加配置 "spark.databricks.python.defaultPythonRepl pythonshell" 

---

## 向 Microsoft Teams 发送通知

https://learn.microsoft.com/zh-cn/azure/data-factory/how-to-send-notifications-to-teams?tabs=data-factory

### Incoming Webhook

Microsoft Teams -> Apps -> Incoming Webhook -> Add a team -> Set up a connector -> 保存 Webhook URL 

### >>> Set variable

* Name: MsgCard
* Value: 

```json
{
    "@type": "MessageCard",
    "@context": "http://schema.org/extensions",
    "themeColor": "0076D7",
    "summary": "ADF Pipeline Fail Alert message​​​​",
    "sections": [
        {
            "activityTitle": "@{concat('【',pipeline().parameters.Status,'】【',pipeline().globalParameters.Environment,'】 ',pipeline().parameters.GrandpaName,' has executed ',pipeline().parameters.Status)}​​​​",
            "facts": [
                {
                    "name": "Environment:",
                    "value": "@{pipeline().globalParameters.Environment}"
                },
                {
                    "name": "Data Factory name:",
                    "value": "@{pipeline().DataFactory}"
                },
                {
                    "name": "Grandpa name:",
                    "value": "@{pipeline().parameters.GrandpaName}"
                },					
                {
                    "name": "Batch RunID:",
                    "value": "@{pipeline().parameters.BatchRunID}"
                }
            ],
            "markdown": true
        }
    ],
    "potentialAction": [
        {
            "@type": "OpenUri",
            "name": "View pipeline run",
            "targets": [
                {
                    "os": "default",
                    "uri": "@{concat('https://adf.azure.cn/monitoring/pipelineruns/',pipeline().parameters.BatchRunID,'?factory=/subscriptions/',pipeline().globalParameters.ADFSubscription,'/resourceGroups/',pipeline().globalParameters.ADFResourceGroup,'/providers/Microsoft.DataFactory/factories/',pipeline().DataFactory)}"
                }
            ]
        }
    ]
}
```
### >>> Web

* URL: @pipeline().globalParameters.TeamsWebhookUrl
* Method: POST
* Body: @json(variables('MsgCard'))

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
