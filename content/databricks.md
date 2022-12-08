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

### 调用notebook

```python
%run /_POC_QA_SC_DataCenter/Dayu-connect-to-datalake
```

```python
dbutils.notebook.run("/_POC_QA_SC_DataCenter/Dayu-connect-to-datalake_Func", 60, {"argument": "data"})
```
* 优势：可传参，可调用多个笔记本
* 缺点：启动新作业，变量不存在

### 文件操作

```python
dbutils.fs.ls("abfss://container@blob.xxx.cn/folder/")
dbutils.fs.rm("abfss://container@blob.xxx.cn/folder/filename", True)
dbutils.fs.mkdirs(TempPath)
dbutils.fs.cp(SapPath+FileName, TempPath)
```
踩坑：若要跟新表结构，需将存表的文件夹删除

### 文件读取

* CSV/TXT
```python
df_DateLake=spark.read.format("csv").option("header","true").option("encoding","utf-8").load("abfss://container@blob.xxx.cn/folder/filename.csv");
display(df_DateLake)
```

* Excel
```python
df_DateLake=spark.read.format("com.crealytics.spark.excel").option("header","true").load("abfss://container@blob.xxx.cn/folder/filename.xlsx");
```

* JSON
```sql
select * from json.`abfss://container@blob.xxx.cn/folder/filename`
```

* Parquet
```sql
select * from delta.`abfss://container@blob.xxx.cn/folder/filename`
```

### Delta Table

__DDL__

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
设置湖地址
```sql
set Address=abfss://container@blob.xxx.cn;
...
LOCATION "${hiveconf:Address}/folder/CSTG/TableName";
```

__DML__

* Insert Table: CSV/EXCEL

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

### SQL

自定义函数
```sql
CREATE OR REPLACE FUNCTION ToDouble(value STRING) RETURNS DOUBLE RETURN double(replace(replace(replace(replace(trim(value),'-',''),'"',''),',',''),'/',''))
```

```python
LandingTable = 'STG.JNJ_Inventory_CN0'
CSTGTable = 'CSTG.JNJ_Inventory_CN0'
TableColumn='WhN, GRDate, PutawayStock'
CleanColumn="WhN, TO_DATE(GRDate,'yyyy/MM/dd') GRDate, ToDouble(PutawayStock) PutawayStock"

spark.sql(f"INSERT INTO {CSTGTable}({TableColumn}) SELECT {CleanColumn}, now() from {LandingTable}");
```

### Data Lake Storage Gen2

SAS Token 共享访问签名是指向一个或多个存储资源的已签名 URI。 该 URI 包括的令牌包含一组特殊查询参数。 该令牌指示客户端可以如何访问资源。 

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

使用 Azure Active Directory (Azure AD) 应用程序服务主体在 Azure 存储帐户中装载数据以进行身份验证。

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

### AWS S3

```python
sc._jsc.hadoopConfiguration().set("fs.s3n.awsAccessKeyId", "xxx")
sc._jsc.hadoopConfiguration().set("fs.s3n.awsSecretAccessKey","xxx")

display(dbutils.fs.ls("s3://<bucketname>/<folder>/"))
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
