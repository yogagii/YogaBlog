Title: Microsoft Azure Databricks
Date: 2022-11-22
Category: Cloud
Author: Yoga
Tags: Azure, ETL

databricks是使用Apache Spark™的原始创建者提供的Databricks统一分析平台。它集成了Spark环境支持Scala、python、R语言进行开发。

adb-xxx.azuredatabricks.net

## Delta Table

Delta Lake 是经过优化的存储层，它使用基于文件的事务日志扩展了 Parquet 数据文件，可以处理 ACID 事务和可缩放的元数据。Delta Lake 是 Azure Databricks 上所有操作的默认存储格式。 除非另行指定，否则 Azure Databricks 上的所有表都是 Delta 表。

> ACID: 原子性、一致性、隔离性、持久性

Delta Lake 特性：
* 支持ACID事务
* 可扩展的元数据处理
* 统一的流、批处理API接口
* 更新、删除数据，实时读写（读是读当前的最新快照）
* 数据版本控制，根据需要查看历史数据快照，可回滚数据
* 自动处理schema变化，可修改表结构

可以使用 DESCRIBE DETAIL 检索有关 Delta 表的详细信息
```sql
DESCRIBE DETAIL eventsTable
```
返回对表的每次写入的出处信息，包括操作、用户等。 表历史记录会保留 30 天。即使parquet文件被vacuum，历史也会保留。
```sql
DESCRIBE HISTORY eventsTable
```

delta表的schema中，字段名的小写不能相同，delta lake区分大小写，但保存时不敏感，而parquet保存时是大小写敏感的

delta表是一个目录，表的根目录除了表数据外，有一个_delta_log目录，用来存放事务日志；事务日志记录了从最初的delta表开始的所有commit事件，每个commit形成一个json文件，文件名是严格递增的，文件名就是版本号。每10个json合并成一个parquet格式的checkpoint文件，记录之前所有的commit。spark读的时候会自动跳到最新的checkpoint，然后再读之后的json；

当多个用户同时写数据时，都是生成一个新版本的数据文件，用互斥锁来决定顺序，拿到锁的，按顺序生成下一个版本的数据文件，然后释放锁，后来的在之前数据的基础上执行他的commit，生成一个新版本的数据。

truncate table不会释放存储空间：Delta Lake 删除操作后，旧数据文件不会被完全删除，仍保留在磁盘上，但在 Delta Lake 事务日志中记录为“tombstoned”（不再是活动表的一部分）。可以通过time travel回到表的早期版本，如果要删除超过某个时间段的文件，可以使用 VACUUM 以递归方式清空与 Spark 表关联的目录，并删除超过保留期阈值的未提交文件。 默认阈值为 7 天。

```sql
select * from table_name VERSION AS OF 100
-- 回滚
RESTORE [ TABLE ] table_name [ TO ] time_travel_version
```

```sql
-- 清理
VACUUM table_name [RETAIN num HOURS] [DRY RUN]
```
Vacuum 后可在 Storage Explorer 对应表的文件夹下 Folder Statictis 看到 Active blob明显减少，但是当 Storage Account 启用了软删除 Data protection -> Enable soft delete for blobs / containers 时，Total 数量不会减少，在软删除有效期内删除的文件可以在portal上看到并还原，有效期过后会永久删除

Delta lake 优点：
* 实时查询，支持ACID功能，保证了数据流入和查询的隔离性，不会产生脏数据。
* Delta支持数据的删除或更新，数据实时同步 CDC：使用Delta merge功能，启动流作业，实时将上游的数据通过merge更新到Delta Lake中。
* 数据质量控制：借助于Delta Schema校验功能，在数据导入时剔除异常数据，或者对异常数据做进一步处理。

Delta lake 缺点：
* 更新操作很重，更新一条数据和更新一批数据的成本可能是一样的，所以不适合一条条的更新数据
* 更新数据的方式是新增文件，会造成文件数量过多，需要清理历史版本的数据
* 乐观锁的并发能力较差，更适合写少读多的场景

_踩坑：用 ADF 将.parquet文件存储到sql server时，delta table格式会保留下全部数据文件，将需要转存sql server的表（dm和dim，需要update的表不行）改为 USING parquet，parquet 表可每次truncate后全量更新，需保证字段格式严格按照ddl中定义的格式._

只有 Delta lake table支持的语句：
* DELETE FROM
* UPDATE
* MERGE INTO
* CLONE
* CACHE
* COPY INTO
* DESCRIBE HISTORY
* VACUUM
* RESTORE

## Delta Live Table 增量实时表

```sql
CREATE OR REFRESH STREAMING LIVE TABLE customers_silver
AS SELECT * FROM STREAM(LIVE.customers_bronze)
```
当为管道触发更新时，流式处理表或视图仅处理自上次更新以来到达的新数据。 增量实时表运行时会自动跟踪已处理的数据。

## SQL

* 自定义变量
```sql
SET delDate=current_date();
set tableList = ('TABLE1', 'TABLE2');

delete from <TABLE> where insertDate=${hiveconf:delDate} and tablename in ${hiveconf:tableList};
```

* 日期
    * date_part 提取部分日期
    * date_add 返回在 startDate 之后的日期 numDays
    * date_sub 返回在 startDate 之前的日期 numDays
    * dayofmonth 返回这个月的第几天
```sql
SET DayL1M=date_sub(getDate(), dayofmonth(getdate())); -- 上个月末 20230531
SET DayL5M=date_sub(${hiveconf:DayL1M}, 155); -- 6*31 半年前
SET DataMonth=date_part('YEAR', ${hiveconf:DayL1M})*100+date_part('MONTHS', ${hiveconf:DayL1M}); -- 上个月 202305
SET DataMonthL6=date_part('YEAR', ${hiveconf:DayL5M})*100+date_part('MONTHS', ${hiveconf:DayL5M}); -- 6个月前 202212
```

* 自定义函数
```sql
CREATE OR REPLACE FUNCTION ToDouble(value STRING) RETURNS DOUBLE RETURN double(replace(replace(replace(replace(trim(value),'-',''),'"',''),',',''),'/',''))
```

```python
LandingTable = 'STG.Inventory_CN'
CSTGTable = 'CSTG.Inventory_CN'
TableColumn='WhN, GRDate, PutawayStock'
CleanColumn="WhN, TO_DATE(GRDate,'yyyy/MM/dd') GRDate, ToDouble(PutawayStock) PutawayStock"

spark.sql(f"INSERT INTO {CSTGTable}({TableColumn}) SELECT {CleanColumn}, now() from {LandingTable}");
```

* MERGE INTO

```sql
with {tablename} as (SELECT EXPLODE(data) data FROM json.`{jsonAddress}{Pre_Tablename}{tablename}`)

merge into <schema>.Test a
using {tablename} b on (a.id=b.id)  
when matched then update 
  set name = b.name
when not matched then insert 
  (id, name) values (b.id, b.name);
```

* Range join optimization 范围联接优化

适用范围：
1. 在区间范围内
2. 数据类型：numeric，date (days)，timestamp (second)
3. INNER JOIN / LEFT OUTER JOIN / RIGHT OUTER JOIN
4. Have a bin size tuning parameter 箱大小: 建议将箱大小设置为值间隔的典型预期长度

```sql
--- Point in interval range join
SELECT *
FROM points JOIN ranges ON points.p BETWEEN ranges.start and ranges.end;

--- Interval overlap range join
SELECT *
FROM r1 JOIN r2 ON r1.start < r2.end AND r2.start < r1.end;
```
Enable range join using a range join hint

```sql
SELECT /*+ RANGE_JOIN(ranges, 10) */ *
FROM points JOIN ranges ON points.p >= ranges.start AND points.p < ranges.end;
```

* INFORMATION_SCHEMA 

The INFORMATION_SCHEMA is a SQL standard based schema, provided in every catalog created on Unity Catalog.

| Table | Desc
| - | -
CATALOGS | Describes catalogs.
TABLES | Describes tables and views defined within the catalog.
COLUMNS | Describes columns of tables and views in the catalog.


https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/sql-ref-information-schema

```sql
SELECT table_owner FROM information_schema.tables WHERE table_schema = 'information_schema' AND table_name = 'columns';

SELECT ordinal_position, column_name, data_type FROM information_schema.tables
```

_踩坑: AnalysisException: [UC_NOT_ENABLED] Unity Catalog is not enabled on this cluster._

## Data Lake Storage Gen2

如果在 ADLS Gen2 上配置防火墙，必须配置网络设置以允许 Azure Databricks 工作区连接到 ADLS Gen2

SAS Token: 共享访问签名是指向一个或多个存储资源的已签名 URI。 该 URI 包括的令牌包含一组特殊查询参数。 该令牌指示客户端可以如何访问资源。 

```python
def connectToDatalake(blob, token):
    spark.conf.set("fs.azure.account.auth.type.%s.dfs.core.chinacloudapi.cn"%(blob), "SAS")
    spark.conf.set("fs.azure.sas.token.provider.type.%s.dfs.core.chinacloudapi.cn"%(blob), "org.apache.hadoop.fs.azurebfs.sas.FixedSASTokenProvider")
    spark.conf.set("fs.azure.sas.fixed.token.%s.dfs.core.chinacloudapi.cn"%(blob), token)
    
def importExcelConfig(blob, token):
    spark._jsc.hadoopConfiguration().set("fs.azure.account.auth.type.%s.dfs.core.chinacloudapi.cn"%(blob), "SAS")
    spark._jsc.hadoopConfiguration().set("fs.azure.sas.token.provider.type.%s.dfs.core.chinacloudapi.cn"%(blob), "org.apache.hadoop.fs.azurebfs.sas.FixedSASTokenProvider")
    spark._jsc.hadoopConfiguration().set("fs.azure.sas.fixed.token.%s.dfs.core.chinacloudapi.cn"%(blob), token)
```

OAuth: 使用 Azure Active Directory (Azure AD) 应用程序服务主体在 Azure 存储帐户中装载数据以进行身份验证。

```python
configs = {"fs.azure.account.auth.type": "OAuth",
          "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
          "fs.azure.account.oauth2.client.id": "<application-id>",
          "fs.azure.account.oauth2.client.secret": "<service-credential-key-name>",
          "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/<directory-id>/oauth2/token"}

dbutils.fs.mount(
  source = "abfss://<container-name>@<storage-account-name>.dfs.core.windows.net/",
  mount_point = "/mnt/<mount-name>",
  extra_configs = configs)
```

Azure Key Vault: 将 client secret 保存到 Azure Key Vault

https://learn.microsoft.com/zh-cn/azure/databricks/getting-started/connect-to-azure-storage

To reference the client secret stored in an Azure Key Vault, you can create a secret scope backed by Azure Key Vault in Azure Databricks. https://<databricks-instance>#secrets/createScope

```python
configs = {"fs.azure.account.auth.type": "OAuth",
          "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
          "fs.azure.account.oauth2.client.id": "<application-id>",
          "fs.azure.account.oauth2.client.secret": dbutils.secrets.get(scope="<scope-name>",key="<service-credential-key-name>"),
          "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/<directory-id>/oauth2/token"}

dbutils.fs.mount(
  source = "abfss://<container-name>@<storage-account-name>.dfs.core.chinacloudapi.cn/",
  mount_point = "/mnt/<mount-name>",
  extra_configs = configs)
```

```python
service_credential = dbutils.secrets.get(scope="<scope>",key="<service-credential-key>")

spark.conf.set("fs.azure.account.auth.type.<storage-account>.dfs.core.chinacloudapi.cn", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.<storage-account>.dfs.core.chinacloudapi.cn", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id.<storage-account>.dfs.core.chinacloudapi.cn", "<application-id>")
spark.conf.set("fs.azure.account.oauth2.client.secret.<storage-account>.dfs.core.chinacloudapi.cn", service_credential)
spark.conf.set("fs.azure.account.oauth2.client.endpoint.<storage-account>.dfs.core.chinacloudapi.cn", "https://login.microsoftonline.com/<directory-id>/oauth2/token")
```

mount之后可以创建Schema，然后在schema中建的table数据都会存入湖中

```sql
CREATE SCHEMA ads_jointown
LOCATION '/mnt/<mount-name>'
```

## AWS S3

```python
sc._jsc.hadoopConfiguration().set("fs.s3n.awsAccessKeyId", "xxx")
sc._jsc.hadoopConfiguration().set("fs.s3n.awsSecretAccessKey","xxx")

display(dbutils.fs.ls("s3://<bucketname>/<folder>/"))
```

ADF不支持用S3作为Sink，只能通过Databricks将数据写入S3

```python
pip install boto3
```

```python
import boto3
from boto3.session import Session
from botocore.exceptions import ClientError

session = Session(access_key, secret_key)
s3_client = session.client('s3')

def list_object(bucketName):
    file_list = []
    response = s3_client.list_objects_v2(Bucket=bucketName)
    file_desc = response['Contents']
    for f in file_desc:
        print('file_name: {}, file_size: {}'.format(f['Key'], f['Size']))
        file_list.append(f['Key'])
    return file_list

def write_file(file_name, bucket, content):
    try:
        response = s3_client.put_object(Body=content, Key=file_name, Bucket=bucket)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def delete_file(file_name, bucket):
    try:
        response = s3_client.delete_object(Key=file_name, Bucket=bucket)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def copy_file(file_name, bucket, source_file):
    try:
        response = s3_client.copy_object(Key=file_name, Bucket=bucket, CopySource={
            'Bucket': bucket,
            'Key': source_file
        })
    except ClientError as e:
        logging.error(e)
        return False
    return True
```

```python
def copy_folder(bucket, sourcefolder, targetfolder, deleteSource=True):
    file_list = list_object(bucket, sourcefolder)
    for obj in file_list:
        filename = targetfolder+obj[len(sourcefolder):]
        copy_file(filename, bucket, obj)
        if deleteSource and len(obj) - len(sourcefolder) > 1:
            delete_file(obj, bucket)
```

```python
from io import BytesIO

def create_csv(sourcedf, filename, target_bucket):
    csv_buffer = BytesIO()
    data = sourcedf.toPandas()
    data.to_csv(csv_buffer, index = False, encoding = 'utf_8_sig')
    content = csv_buffer.getvalue()
    write_file(filename, target_bucket, content)
```

## SQL SERVER

* JDBC

读取数据库

```python
jdbcHostname = 'xxx'
jdbcPort = '1433'
jdbcDatabase = 'xxx'
properties = {
"user" : 'xxx',
"password" : 'xxx' }
url = "jdbc:sqlserver://{0}:{1};database={2}".format(jdbcHostname,jdbcPort,jdbcDatabase)
display(spark.read.jdbc(url=url,table='xxx',properties = properties))
```
```python
config_table = (spark.read
  .format("jdbc")
  .option("url", url)
  .option("dbtable", 'xxx')
  .option("user", properties['user'])
  .option("password", properties['password'])
  .load()
)
display(config_table)
```

创建表

```python
from pyspark.sql.types import *

schema = StructType([
  StructField("TableName", StringType(), nullable = False),
  StructField("SQLFlag", IntegerType(), nullable = False),
])

configList = [
    ['DIM_Calendar', 1],
]

config_df = spark.createDataFrame(configList, schema)
config_df.show()
```
_踩坑：StructField无法创建自增字段_

```sql
SET jdbcURL=`xxx`

CREATE OR REPLACE TABLE <Schema_Name>.<Table_Name>
  USING JDBC
OPTIONS (
  url "${hiveconf:jdbcURL}",
  dbtable 'xxx',
  user 'xxx',
  password 'xxx'
) AS
SELECT * FROM df_spark
```
> 这样创建的表 location在sql server，不在湖中，湖里不会有对应的文件夹

---

## Cluster 集群

Cluster type:

* All-purpose cluster: can be shared by multiple users and are best for performing ad-hoc analysis, data exploration, or development. 

* Job cluster:  Job clusters terminate when your job ends, reducing resource usage and cost. Once you’ve completed implementing your processing and are ready to operationalize your code, switch to running it on a job cluster.

_踩坑：ADF 调用notebook 报错：Failure starting repl. Try detaching and re-attaching the notebook. 此类问题一般发生的原因为Driver node size不足/处于繁忙状态来不及处理请求。_

1. 在ADF activity侧加上了自动重试 retry 次数。（当cmd1成功，cmd2失败，重生会导致cmd1反复执行，所以 DML 增量数据若要加retry 需要先 delete 插入数据，全量数据truncate不回重复）
2. 建议对于生产job任务采用Job cluster，而不是all purpose cluster。 Job cluster有更好的资源隔离，即用即删，成本也更便宜。但是job cluster背后要足量ip，ip不足会导致job直接挂掉无法修复，一般是有1024网段的databricks采用。

_踩坑：IpykernelUtils are causing the conflict and holding the python process. It is since 11.3 which has introduced Ipykernel shells_

当存在在一个interactive cluster上同时跑多个并行notebooks的情况，IpykernelUtils 会引起冲突并且holding python process, 进而出现无法启动python kernel的错误。

在cluster添加如下spark configuration：
    "spark.databricks.python.defaultPythonRepl pythonshell"

_踩坑：Caused by: org.apache.hadoop.fs.PathIOException: `/[schemaName]/[tableName]/\_SUCCESS': Input/output error: Parallel access to the create path detected. Failing request to honor single writer semantics_

限制Spark往HDFS写出数据时生成_SUCCESS文件 （未验证）
    
```sql
set mapreduce.fileoutputcommitter.marksuccessfuljobs=false
```

## Library

_踩坑：Library installation failed due to infra fault_

* 工作区库 workspace-libraries

工作区库充当本地存储库，工作区中的所有用户均可使用共享文件夹中的工作区库，而某个用户文件夹中的工作区库仅该用户可用。

可以从工作区库中创建群集安装库，先在群集上安装工作区库，然后才能将其用于笔记本或作业。

先从公共存储库（PyPI 或 Maven）安装需要的库 create library -> PyPI 将 Python Whl 下载到本地

再上传下载的包到DBFS create library -> Upload -> Python Whl

* 集群库 cluster-libraries

群集库可供群集上运行的所有笔记本使用

安装已上传到工作区的工作区库：Install new -> Workspace

https://learn.microsoft.com/zh-cn/azure/databricks/libraries/workspace-libraries

---

## Diagnostic setting

Azure portal -> Databricks -> Monitoring -> Diagnostic settings

workspace的监控日志，比如谁生成/删除一个token


## Unity Catalog 数据治理组件

功能：
* 治理所有数据资产：数仓，库表，数据湖，文件，机器学习模型，dashboard, notebook
* 数据血缘
* 安全策略
* ABAC权限管理，表级、列级权限控制（WIP）
* 数据审计，数据共享

Hierarchy of primary data objects flows 主要数据对象的层次结构:
* Metastore 元存储：元数据的顶级容器，用于管理对数据资产的访问的权限，用户可以查看分配了USAGE数据权限的所有目录。
* Catalog 目录
* Schema 架构/数据库
* Table 表/视图
