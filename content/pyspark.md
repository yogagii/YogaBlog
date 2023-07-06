Title: Apache Spark
Date: 2022-01-26
Category: Backend
Author: Yoga

## Spark原理

Spark 是使用 scala 实现的基于内存计算的大数据开源集群计算环境。是UC Berkeley 开源的类Hadoop MapReduce的通用并行框架, 专门用于大数据量下的迭代式计算。提供了 java,scala, python,R 等语言的调用接口。

Spark 在多次运算的情况下是比较快的。因为 Hadoop 在一次 MapReduce 运算之后，会将数据的运算结果从内存写入到磁盘中，第二次运算时再从磁盘中读取数据，2次运算间有多余 IO 消耗；Spark 则是将数据一直缓存在内存中,直到计算得到最后的结果,再将结果写入到磁盘。 

1. 提供 Cache 机制来支持需要反复迭代计算或者多次数据共享,减少数据读取的 IO 开销;
2. 提供了一套支持 DAG 图的分布式并行计算的编程框架,减少多次计算之间中间结果写到 Hdfs 的开销;
3. 使用多线程池模型减少 Task 启动开稍, shuffle 过程中避免不必要的 sort 操作并减少磁盘 IO 操作。

Driver负责运行Application的main()函数并且创建SparkContext，根据shuffle类算子来进行stage的划分，将代码分拆为多个stage，并为每个stage创建一批Task，然后将这些Task分配到各个Executor进程中执行。一个stage的所有Task都执行完毕之后，会在各个节点本地的磁盘文件中写入计算中间结果，然后Driver就会调度运行下一个stage。下一个stage的Task的输入数据就是上一个stage输出的中间结果。

### RDD

Resilent Distributed Datasets弹性分布式数据集，是 Spark 底层的分布式存储的数据结构。数据不只存储在一台机器上，而是分布在多台机器上,实现数据计算的并行化，弹性表明数据丢失时可以进行重建。

RDD 是一种只读的数据块，当你对一个 RDD 进行了操作,那么结果将会是一个新的 RDD，RDD 里面的数据并不是真实的数据，而是一些元数据信息，记录了该 RDD 是通过哪些 Transformation 得到的。在计算机中使用 lineage 来表示这种血缘结构，lineage 形成一个有向无环图 DAG，整个计算过程中将不需要将中间结果落地到 HDFS 进行容错，某个节点出错，则只需要通过 lineage 关系重新计算即可。

RDD操作函数（operation）:

| 类别 | 函数 | 区别
| - | - | -
Transformation | map, filter, groupBy, join, union, reduce, sort, partitionBy | 返回值还是RDD，不会马上提交Spark集群运行
Action | count, collect, take, save, show | 返回值不是RDD，会形成DAG提交Spark集群运行并立即返回结果

Transformation 操作不是马上提交 Spark 集群执行的，在遇到 Transformation 操作时只会记录需要这样的操作，并不会去执行，需要等到有 Action 操作的时候才会真正启动计算过程进行计算。针对每个 Action，Spark 会生成一个 Job，从数据的创建开始，经过 Transformation，结尾是 Action 操作。这些操作对应形成一个有向无环图(DAG)，形成 DAG 的先决条件是最后的函数操作是一个Action。

### shuffle

> shuffle 是划分 DAG 中 stage 的标识，同时影响 Spark 执行速度的关键步骤。shuffle 操作是 spark 中最耗时的操作,应尽量避免不必要的shuffle.

shuffle类算子：

| 类别 | 函数 | 特点
| - | - | -
重分区 | repartition、repartitionAndSortWithinPartitions、coalesce(shuffle=true) | 对所有的分区数据进行随机均匀的打乱，把数据放入下游新的分区内
聚合 | reduceByKey, groupByKey, aggregateByKey, combineByKey | 所有节点上的相同的key移动到同一个节点上
集合/表间交互 | join, cogroup, intersection, subtract, subtractByKey, leftOuterJoin | 将相同join key的数据shuffle到同一个节点上
排序 | sortBy, sortByKey |
去重 | distinct

Transformation 函数分为：
* 窄依赖(narrow dependency)：不发生 shuffle 操作，指子 RDD 的各个分片(partition)不依赖于其他分片，能够独立计算得到结果
* 宽依赖(wide dependency)：会发生 shuffle 操作，指子 RDD 的各个分片会依赖于父RDD 的多个分片，造成父 RDD 的各个分片在集群中重新分片

### 性能优化 - Cache

每次对一个RDD执行一个算子操作时，都会重新从源头处计算一遍，计算出那个RDD来，然后再对这个RDD执行你的算子操作。 -》 对多次使用的RDD进行持久化。

如果程序从头到尾只有一个 Action 操作且子 RDD 只依赖于一个父RDD 的话，就不需要使用 cache 这个机制， RDD 会在内存中一直从头计算到尾,最后才根据你的 Action 操作返回一个值或者保存到相应的磁盘中。需要 cache 的是当存在多个 Action 操作或者依赖于多个 RDD 的时候, 可以在那之前缓存RDD。

原文：https://zhuanlan.zhihu.com/p/34436165

---

## Spark SQL

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

---

A DataFrame is a distributed collection of data grouped into named columns

DataFrame是一种表格型数据结构，它含有一组有序的列，每列可以是不同的值。DataFrame的行索引是index，列索引是columns。

DataFrame transformations are methods that return a new DataFrame and are lazily evaluated

DataFrame actions are methods that trigger computation. An action is needed to trigger the execution of any DataFrame transformations

## PySpark

PySpark is an interface for Apache Spark in Python.

### pyspark.sql.SparkSession

* Create a PySpark DataFrame
```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()

spark.createDataFrame()
```

### pyspark.sql.DataFrame

* Viewing Data
```python
df.show() # collect + truncate转字符串
df.printSchema()
df.columns
df.collect() # 全部
df.take(1) # 第一行
df.tail(1) # 最后一行
df.count()
```

* Selecting Data
```python
df.select(df.c).show() # 选择列
df.select("id", "result")
  .where("result > 70")
  .orderBy("result")
  .show()

df.filter(df.a == 1).show() # 选择行
```

* Grouping Data
```python
df.groupby('color').avg().show()
# groupBy后面跟aggregation function: avg, max, min, mean, sum

def plus_mean(pandas_df):
  return pandas_df.assign(v1=pandas_df.v1 - pandas_df.v1.mean())
# pandas assign: 根据某个列进行计算得到一个新列

df.groupby('color').applyInPandas(plus_mean, schema=df.schema).show()
```

A schema defines the column names and types of a DataFrame

* 创建或替换本地临时视图
```python
df.createOrReplaceTempView("people")
```

* toPandas

```python
# spark 转换为pandas的dataframe
dfp = df.toPandas()
display(dfp)

# pandas的dataframe转化为spark的dataframe
spark_df = sc.createDataFrame(pandas_df)
```

### pyspark.sql.GroupedData

* cogroup
```python
df1.groupby('id').cogroup(df2.groupby('id'))
```

### pyspark.sql.DataFrameWriter
### pyspark.sql.DataFrameReader

* Getting Data in/out

```python
df.write.csv('foo.csv', header=True)
spark.read.csv('foo.csv', header=True).show()
```

* JDBC

```python
spark.read.jdbc(url=url,table= 'Onhand_Inventory',properties = properties)
```

```python
spark.write.jdbc(url, table, mode=None, properties=None)
```

mode：数据更新的模式，append、overwrite、ignore、error（默认，如果数据存在，抛出异常）

不能使用Spark中的jdbc和dataframes进行单个记录更新，只能追加或替换整个表

Using PYODBC to execute query on Azure SQL in Databricks：https://medium.com/@roger_busser/azure-databricks-and-single-row-updates-fe1844a8dbd3

## Pandas

```python
data = {
    'state':['Ohio','Ohio','Ohio','Nevada','Nevada'],
    'year':[2000,2001,2002,2001,2002],
}
frame = pd.DataFrame(data)
```

* pandas.DataFrame.assign 根据某个列进行计算得到一个新列

```python
df.assign(col3=lambda x: x.col1 / 2 + 20)
```

* pandas.merge_asof 匹配最近的键而不是相等的键

```python
def asof_join(l, r):
  return pd.merge_asof(l, r, on='time', by='id')
```

* pandas.DataFrame.to_csv 导出csv

```python
dataframe = pd.DataFrame(dict(
   date=list(pd.date_range('2012-1-1 12:00:00', periods=3, freq='M')),
   country=['KR', 'US', 'JP'],
   code=[1, 2 ,3]), columns=['date', 'country', 'code'])
dataframe.to_csv("test.csv",index=False,sep=',')
```

* pandas.DataFrame.merge

```python
df1.merge(df2, left_on='lkey', right_on='rkey')
```

* pandas.DataFrame.dropna

```python
df.drop('age').collect() # 删除列
df.drop(df.age).collect()

df.select('Age','Gender').dropDuplicates().show() # 去重
```

Drop the rows where at least one element is missing.

```python
df = df.na.drop()  # 删除任何列包含na的行
df.na.drop("any").show() # 任何出现NaN/null就丢弃
df.na.drop("all").show() # 一行都是NaN/null才丢弃
df.na.drop("any",List("age","dt")).show() # 针对特定列出现NaN/null就丢弃改行
df = df.dropna(subset=['col1', 'col2'])  # 删掉col1或col2中任一一列包含na的行
```

* pandas.DataFrame.astype

```python
df.astype({'col1': 'int32'})
df['col1'].astype('float', copy=False)
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
