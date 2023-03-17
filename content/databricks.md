Title: Microsoft Azure Databricks
Date: 2022-11-22
Category: Cloud
Author: Yoga
Tags: Azure, ETL


ETL: Extract, Transform and Load 数据仓库技术

databricks是使用Apache Spark™的原始创建者提供的Databricks统一分析平台。它集成了Spark环境支持Scala、python、R语言进行开发。

adb-xxx.azuredatabricks.net

Workspace -> Users (your own folder) -> 右键import -> .dbc file

-> Create -> Notebook -> Default language: python

jobs -> start cluster

## 调用notebook

```python
%run /_POC_QA_SC_DataCenter/Dayu-connect-to-datalake
```

```python
dbutils.notebook.run("/_POC_QA_SC_DataCenter/Dayu-connect-to-datalake_Func", 60, {"argument": "data"})
```
* 优势：可传参，可调用多个笔记本
* 缺点：启动新作业，变量不存在

## Output

```python
dbutils.notebook.exit(data)
```

ADF 读取output：@activity('Notebook').output

## 文件操作

* dbutils
```python
dbutils.fs.ls("abfss://container@blob.xxx.cn/folder/")
dbutils.fs.rm("abfss://container@blob.xxx.cn/folder/filename", True)
dbutils.fs.mkdirs(TempPath)
dbutils.fs.cp(SapPath+FileName, TempPath)
```
_踩坑：若要跟新表结构，需将存表的文件夹删除_

* 获取文件名
```python
df = spark.read \
  .format("text") \
  .load("abfss://container@blob.xxx.cn/folder/filename_*.txt") \
  .select("*", "_metadata")
display(df)

df.createOrReplaceTempView("df_spark")
df1=spark.sql(f"select distinct _metadata.file_name as filename from (select * from df_spark order by _metadata) a")
for i in range(0,30):
    filename=str(df1.collect()[i][0])
```
_踩坑：xlsx文件也只能用 .format('csv') 不能 .format("com.crealytics.spark.excel")_

* os
```python
import os

os.listdir("/")
```

```
%sh ls /
```

* azure-storage-file-datalake

```
pip install azure-storage-file-datalake
```
```python
import os, uuid, sys
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings

def initialize_storage_account():
    try:  
        global service_client
        credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        service_client = DataLakeServiceClient(account_url=account_url, credential=credential)
    except Exception as e:
        print(e)

def list_directory(container="raw", folder="example_folder"):
    try:
        file_system_client = service_client.get_file_system_client(file_system=container)
        paths = file_system_client.get_paths(path=folder)
        for path in paths:
            print(path.name + '\n')
    except Exception as e:
     print(e)

def create_directory(container="raw", folder="example_folder"):
    file_system_client = service_client.get_file_system_client(file_system=container)
    res = file_system_client.create_directory(folder)

def delete_file(container="raw", file="example_folder/example.xlsx"):
    file_system_client = service_client.get_file_system_client(file_system=container)
    res = file_system_client.delete_file(file)

def delete_directory(container="raw", folder="example_folder"):
    file_system_client = service_client.get_file_system_client(file_system=container)
    res = file_system_client.delete_directory(folder)
```

## 文件读写

* CSV
```python
df_csv=spark.read.format("csv").option("encoding","GBK").load("abfss://container@blob.xxx.cn/folder/filename.csv");
display(df_csv)
# GBK解决中文乱码
```
```python
# CSV不需要header
df_csv.to_csv(<target_file>, index = False, header=False, encoding = 'utf_8_sig')
```
_踩坑：encoding为GBK时，excel里将"创作语言和校对"设置英文首选，会出现中文乱码全是？情况_

* TXT
```python
df_txt=spark.read.format("text").load(sourcefile);
```

```python
df_txt.coalesce(1).write.format("text").save("s3://<bucket>/<folder>/filename")
```
_踩坑：coalesce只会确保产生一个文件，仍会生成以filename命名的文件夹，文件夹下有以part加数字命名的txt文件(以及\_SUCCESS, \_committed, \_started文件)_

```python
# 解决txt文件每一行有引号
df_txt.to_csv(<target_file>, index = False, header=False, sep='\t', quoting=False, quotechar=' ')
```

* Excel
```python
# header必传项, maxRowsInMemory解决文件过大>10mb
df_excel=spark.read.format("com.crealytics.spark.excel").option("header","true").option("maxRowsInMemory", 2000).load(sourcefile);
```
csv是通过spark读的，excel是spark底层hadoop读的，libraries里安装com.crealytics:spark-excel

```python
pip install openpyxl

# excel文件得保留header
df_excel.to_excel(<target_file>, index = False)
```

* JSON
```sql
select * from json.`abfss://container@blob.xxx.cn/folder/filename`
```

```python
df_DateLake=spark.read.format("json").load("abfss://container@blob.xxx.cn/folder/filename.json");
```

* Parquet
```sql
select * from delta.`abfss://container@blob.xxx.cn/folder/filename`
```

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

__DCL__

* blob 存储文件系统的访问权限
```sql
GRANT SELECT, MODIFY ON ANY FILE TO `<user>@<domain-name>` --
```

* schema 访问权限
```sql
SHOW GRANTS ON SCHEMA <SCHEMANAME>

GRANT USAGE, SELECT, CREATE, READ_METADATA, MODIFY ON SCHEMA <SCHEMANAME> TO `<user>@<domain-name>`
```

* table 访问权限
```sql
ALTER TABLE <TABLENAME> OWNER TO `<user>@<domain-name>`
GRANT SELECT, READ_METADATA ON TABLE <TABLENAME> TO `<user>@<domain-name>`

DESCRIBE [EXTENDED] <TABLENAME> --表的基本元数据信息

SHOW GRANTS on TABLE <TABLENAME> --表的权限信息
SHOW GRANTS `<user>@<domain-name>` on TABLE <TABLENAME>
```

__DDL__

* 创建SCHEMA

```sql
CREATE SCHEMA example_schema
LOCATION 'dbfs:/mnt/azrzdbicinmtdpadlsqa/{container}/{example_schema}'
```

* 创建TABLE
```sql
drop table if exists STG.TableName;
create table STG.TableName 
(
`Field1` string,
`Field2` INT,
`InsertTime` timestamp)
USING delta 
LOCATION "abfss://container@blob.xxx.cn/folder/STG/TableName";
```
如果省略 USING，则默认值为 DELTA。

对于除 DELTA 之外的任何 data_source，还必须指定 LOCATION，除非catalog为 hive_metastore。

设置湖地址
```sql
set Address=abfss://container@blob.xxx.cn;
...
LOCATION "${hiveconf:Address}/folder/CSTG/TableName";
```

已创建SCHEMA后不需要Location
```sql
-- 加上comment会更好
CREATE TABLE IF NOT EXISTS example_schema.example_table
(
 col1 STRING COMMENT 'col1_comment'
)
using delta
PARTITIONED BY (insertDate)
```

* 克隆TABLE

> SHALLOW CLONE: 浅表克隆不会将数据文件复制到克隆目标。 表元数据等效于源。 创建这些克隆的成本较低。
</br>DEEP CLONE: 深层克隆还会将源表数据复制到克隆目标。它还会克隆流元数据。

```sql
CREATE OR REPLACE TABLE <SCHEMA>.<TABLENAME> DEEP CLONE <SCHEMA>.<TABLENAME>;
```

__DML__

* Insert Table: CSV/EXCEL (RAW -> STG)

```python
%python
import datetime
ManuPath="abfss://container@blob.xxx.cn/folder/RawZone/MANU/"

def sliceErrorMsg(msg):
    FailReaon = str(msg)
    if FailReaon.find(';') > 0:
        return FailReaon[0:FailReaon.find(';')].replace("'", "`")
    elif FailReaon.find('.') > 0:
        return FailReaon[0:FailReaon.find('.')].replace("'", "`")
    else:
        return FailReaon[0:30].replace("'", "`")

def insertTable(FileName, LandingTableName, TableColumn, ExcelTitle, SaveDay=30, Path=ManuPath):
    try:
        fileFormat = 'csv' if 'csv' in FileName else 'com.crealytics.spark.excel';
        df_DateLake=spark.read.format(fileFormat).option("header","true").load(Path+FileName);
    except:
        spark.sql(f" insert into STG.TableReadLog select '{LandingTableName}',current_date(),now(),'Not found {FileName}',null;");
    else:
        df_DateLake.createOrReplaceTempView("df_spark");
        spark.sql(f"delete from {LandingTableName} where InsertTime<date_sub(now(), {SaveDay})");
        try:
            spark.sql(f"insert into {LandingTableName}({TableColumn}) select {ExcelTitle},now() InsertTime from df_spark;");
        except Exception as FailReaon:
            FailReaon=sliceErrorMsg(FailReaon);
            print(FailReaon);
            spark.sql(f"insert into STG.TableReadLog select '{LandingTableName}',current_date(),now(),'{FailReaon}',null;");
        else:
            spark.sql(f"insert into STG.TableWriteLog select '{LandingTableName}',current_date(),now(),null;");
    
```

* 增量

```sql
INSERT INTO <CSTG_SCHEMA><TABLE> (<columns>, InsertTime)
SELECT <columns>, NOW() FROM <STG_SCHEMA>.<TABLE> WHERE InsertTime>Current_Date();
```

```sql
merge into <CSTG_SCHEMA><TABLE> a
using <STG_SCHEMA>.<TABLE> b
    on a.id=b.id and a.insertDate=b.insertDate -- 同一天内数据更新不会覆盖
when not matched then insert 
(<columns>,insertDate)
values(<columns>)
```

* 容错性增量

```sql
DELETE FROM <CSTG_SCHEMA><TABLE> A WHERE EXISTS (SELECT key FROM <STG_SCHEMA><TABLE> B WHERE A.key=B.key and B.InsertTime>Current_Date());

INSERT INTO <CSTG_SCHEMA><TABLE> (<columns>, InsertTime)
SELECT <columns>, NOW() FROM <STG_SCHEMA>.<TABLE> WHERE InsertTime>Current_Date();
```

* 全量

_有 InsertTime>CurrentDate 时需要判断 IsUpdate_
```python
IsUpdate=spark.sql('select count(1) Num from <STG_SCHEMA>.<TABLE> where InsertTime>=current_date()');
if IsUpdate.collect()[0][0] > 0:
    spark.sql(f'TRUNCATE TABLE <CSTG_SCHEMA><TABLE>;')
    spark.sql(f'INSERT INTO <CSTG_SCHEMA><TABLE> ({columns},InsertTime) SELECT {columns}, now() FROM <STG_SCHEMA>.<TABLE> where InsertTime>Current_Date();')
```

_没有 InsertTime>CurrentDate 不需要 IsUpdate_
```sql
TRUNCATE TABLE <DWD_SCHEMA><TABLE>;

INSERT INTO <DWD_SCHEMA><TABLE> (<columns>)
SELECT <columns> FROM <CSTG_SCHEMA>.<TABLE>;
```

* Insert Table: TXT

法一：
```python
from pyspark.sql.types import *

def insertTxT(FileName, LandingTableName, TableColumn, header=4, SaveDay=30):
    schemalist = [];
    for col in TableColumn: schemalist.append(StructField(col, StringType(), True));
    schema = StructType(schemalist);
    selectColumn = list(filter(not_blank, TableColumn))
    df_DateLake=spark.read.format("csv").option("header","false").option("comment","*").option("encoding","utf-8").option("sep","\t").schema(schema).load(SapPath+FileName).select(selectColumn).toPandas().iloc[header:];
    df_DateLake = spark.createDataFrame(df_DateLake)
    df_DateLake.createOrReplaceTempView("df_spark");
    columns = ','.join(selectColumn)+',InsertTime';
    spark.sql(f"insert into {LandingTableName}({columns}) select *, now() InsertTime from df_spark;");
```

法二：
```python
import pandas

TempPath="dbfs:/FileStore/Temp"
TempFile="/dbfs/FileStore/Temp/"

def insertTxT_Pandas(FileName, LandingTableName, TableColumn,RenameColumn,header=3, SaveDay=30):
    dbutils.fs.rm(TempPath,True)
    dbutils.fs.mkdirs(TempPath)
    dbutils.fs.cp(SapPath+FileName, TempPath)
    df_DateLake=pandas.read_csv(TempFile+FileName, header=header,sep='\t', names=RenameColumn,skipinitialspace=True,skip_blank_lines=True,error_bad_lines=False,dtype=str)
    df_DateLake = spark.createDataFrame(df_DateLake);
    df_DateLake.createOrReplaceTempView("df_spark");
    columns = delInsertTime(TableColumn);
    spark.sql(f"insert into {LandingTableName}({TableColumn}) select {columns}, now() InsertTime from df_spark;");
```

__OPTIMIZE__

优化 Delta Lake 数据的布局，优化数据子集或按列归置数据。

```sql
OPTIMIZE table_name [WHERE predicate]
  [ZORDER BY (col_name1 [, ...] ) ]
```

启用自动优化

```sql
-- 所有新表
set spark.databricks.delta.properties.defaults.autoOptimize.optimizeWrite = true;
set spark.databricks.delta.properties.defaults.autoOptimize.autoCompact = true;
```

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

Table | Desc
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
写入数据库
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

---

```python
# reading the CDL blob storage using scan_read(SCAN package)
from sca_read.loader import helper, getSysttemRelatedTables

display(getSystemRelatedTables(storageaccount="xxx", container="xxx", path="/xx/xx/xx", returnType="pandas_dataframe"))
```

```python
sdf_SAP = spark.sql("""select * from delta.`abfss://xxx@xxx.net`""")

sdf_SAP.display() ## 点击download下载表格
```
underscore variables are related to the pipelining process(sap => L0), don't have any content in it.

```python
# creation of a tempview / caching the data
sdf_SAP.createOrReplaceTempView("SAP_AUFK")
spark.catalog.cacheTable("SAP_AUFK")
# SAP_AUFK can be called in spark.sql
print(sdf_SAP.count())
```

```python
# access a storage account
Storage_account = "xxx"
Container = "xxx"
SAS_Token = dbutils.secrets.get("xxx", "xxx")
configOption = "xxx"
spark.conf.set(configOption, SAS_Token)
fileSystemUrl = "xxx"
dbutils.fs.ls(fileSystemUrl) #list files
```

```python
# display tables, paths, levels
import pandas as pd

def showAllTables():
  l0Tables = dbutils.fs.ls(L0_PATH)
  dfL0 = pd.DataFrame(l0Tables)
```

```python
# print schema
sdf_SAP.select("Record_ID", "DATE_CREATED").where("Record_ID == '1'").printSchema()
```

```python
from pyspark.sql import functions as F
from pyspark.sql.window import window
# group by
windowSpec = Window.partitionBy("Record_ID").orderBy("Record_ID")
# expansion
dfExplode = dfForExplode.withColumn('SEQ_NO', F.row_number().over(windowSpec))
```

```python
import pyspark
from pyspark.sql import functions as F
from pyspark.sql.types import *
# writes the table in sql server and implements the right table schema
def scan_pushDfToSQL(
  df: pyspark.sql.dataframe.DataFrame,
  sqlTable:str,
  database:str,
  sqlserver:str,

sql_table_name = "SIDE_DEPARTMENT_PROJECT_tableName_DEV " # naming conventions
scan_pushDfToSQL(df = sdf_order_issues_inves, sqlTable = sql_table_name, database = "LEIDEN", modeType = "overwrite", verbose = True)
```


### Spark

Spark 是使用 scala 实现的基于内存计算的大数据开源集群计算环境.提供了 java,scala, python,R 等语言的调用接口。

Spark专门用于大数据量下的迭代式计算，将数据一直缓存在内存中,直到计算得到最后的结果,再将结果写入到磁盘,所以多次运算的情况下,Spark 是比较快的。

- Spark SQL: 提供了类 SQL 的查询,返回 Spark-DataFrame 的数据结构(类似 Hive)
- Spark Streaming: 流式计算,主要用于处理线上实时时序数据(类似 storm)
- MLlib: 提供机器学习的各种模型和调优
- GraphX: 提供基于图的算法,如 PageRank

```sql
Select id, result from exams where result > 70 order by result

spark.table("exam").select("id", "result").where("result > 70").orderBy("result")
```

SparkSQL中的三种Join:

* Broadcast Join 小表对大表

将小表的数据分发到每个节点上，供大表使用。executor存储小表的全部数据，牺牲空间，换取shuffle操作大量的耗时。

被广播的表首先被collect到driver段，然后被冗余分发到每个executor上，所以当表比较大时，采用broadcast join会对driver端和executor端造成较大的压力。

基表不能被广播，比如 left outer join 时，只能广播右表

* Shuffle Hash Join

利用key相同必然分区相同的这个原理，先对两张表分别按照join keys进行重分区（shuffle），再对两个表中相对应分区的数据分别进行Hash Join（先将小表分区构造为一张hash表，然后根据大表分区中记录的join keys值拿出来进行匹配）

分区的平均大小不超过spark.sql.autoBroadcastJoinThreshold所配置的值，默认是10M

* Sort Merge Join 大表对大表

将两张表按照join keys进行了重新shuffle，保证join keys值相同的记录会被分在相应的分区。分区后对每个分区内的数据进行排序，排序后再对相应的分区内的记录进行连接

https://blog.csdn.net/hellojoy/article/details/113665938

踩坑：There is not enough memory to build the hash map

_If the estimated size of one of the DataFrames is less than the autoBroadcastJoinThreshold, Spark may use BroadcastHashJoin to perform the join. If the available nodes do not have enough resources to accommodate the broadcast DataFrame, your job fails due to an out of memory error._

In Databricks Runtime 7.0 and above, set the join type to SortMergeJoin with join hints enabled.
```python
# disable broadcast
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)
```

### DataFrame

A DataFrame is a distributed collection of data grouped into named columns

DataFrame是一种表格型数据结构，它含有一组有序的列，每列可以是不同的值。DataFrame的行索引是index，列索引是columns。

```python
data = {
    'state':['Ohio','Ohio','Ohio','Nevada','Nevada'],
    'year':[2000,2001,2002,2001,2002],
}
frame = pd.DataFrame(data)
```

A schema defines the column names and types of a DataFrame

DataFrame transformations are methods that return a new DataFrame and are lazily evaluated

DataFrame actions are methods that trigger computation. An action is needed to trigger the execution of any DataFrame transformations
 
 
```python
df.select("id", "result")
  .where("result > 70")
  .orderBy("result")
  .show()
df.count()
df.collect()
df.show()
```

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
