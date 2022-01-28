Title: SCAN -- Supply Chain ANalytics
Date: 2022-01-20
Category: Project
Author: Yoga

## SCAN

SCAN stands for Supply Chain ANalytics. SCAN is an analytics program within Janssen Supply Chain. Our aim is to accelerate value delivery by providing analytics as a service. 

* Capability building (data and analytics training)
* Democratized data
* Dashboarding & visualisation support
* Advanced analytics

## Data Democratization 数据民主化

Data democratization is the ability for information in a digital format to be accessible to Subject Matter Expert in JSC and data analysts/scientists.

Data Democratization brings data to the digital stack for each type of profile

授予员工访问数据的权限，确保信息易于查找、检索和理解。使决策权掌握在员工手中，并为员工提供一些他们所需的信息以辅助他们优化工作。

## EDW 企业数据仓库

The primary function of the Enterprise Data Warehouse, is to provide a centralized data store of J&J enterprise-level data.

## CDL 

The Common Data Layer (CDL) is a repository that centralizes the Supply Chain Data.This common layer can support all digital solutions across the business. The CDL ingests and publishes near real-time data from supply chain systems globally. The Level 0 layer of the CDL is a direct reflection of the data as it is stored in the upstream source systems.

CDL defined Databricks as the tool to use for data consumption. A secure access to CDL is given via an Azure Active Directory (AD) credential passthrough. The access is of type read-only, preventing L2 teams to write/modify any content in CDL L0 and L1. The access is direct to CDL Production environment, even during the development in downstream DEV & QA systems. 

## Databricks

databricks是使用Apache Spark™的原始创建者提供的Databricks统一分析平台。它集成了Spark环境支持Scala、python、R语言进行开发。

Databricks is a powerful, Spark-based platform that enables users to process, manage, and visualize massive volumes of data. Founded by the original creators of Apache Spark, Databricks has embedded and optimized Spark as part of a larger platform designed for not only data processing, but also data science, machine learning, and business analytics. Using Databricks, users can ingest data, build data pipelines, run them in production, and automate these processes for reliability and scale. 

Databricks Proof of Concept (extended to Proof of Value) was first mooted by Janssen APAC Data Science team to re-evaluate Data Science workbench tool, as pro-code alternative to existing Low Code Data Science workbench tool - Dataiku, as well as end-to-end ML Ops solution suite covering products like Feature Store and ML Flow.

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
 
## ABAP

Advanced Business Application Programming高级商务应用编程，ABAP主要用作SAP的编程。

---

## Microsoft Azure Databricks

adb-xxx.azuredatabricks.net

Workspace -> Users (your own folder) -> 右键import -> .dbc file

-> Create -> Notebook -> Default language: python

jobs -> start cluster

Extract, Transform and Load
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
