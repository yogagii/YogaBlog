Title: Microsoft Azure Databricks ETL
Date: 2022-11-22
Category: Cloud
Author: Yoga
Tags: Azure, ETL


ETL: Extract, Transform and Load 数据仓库技术

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

## Input & Output

```python
dbutils.widgets.get("argument1")
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

## 数据处理

### DCL

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

### DDL

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

### DML

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

* 版本容错性增量

    相同版本号全量覆盖，不同版本号增量

    解决 增量 和 容错性增量 无法删除错误上传的数据问题

```sql
DELETE FROM <CSTG_SCHEMA><TABLE> A
WHERE EXISTS (SELECT B.YearMonth 
              FROM <STG_SCHEMA><TABLE> B
              WHERE  B.YearMonth=A.YearMonth  AND InsertTime>Current_Date());

insert into <CSTG_SCHEMA><TABLE> (<columns>, InsertTime)
select distinct -- 测试期间防止多次stg抽数据 所以添加distinct
      <columns>,now()
FROM <STG_SCHEMA>.<TABLE> WHERE InsertTime>Current_Date();
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

### OPTIMIZE

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
