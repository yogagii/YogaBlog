Title: SQL Server
Date: 2023-02-07
Category: Backend
Tags: sql
Author: Yoga

### 系统表 sysobjects

* 获取系统表 sysobjects: 在数据库内创建的每个对象（约束、默认值、日志、规则、存储过程等）在表中占一行。
```sql
select * from sys.objects 
```

* 获取表结构 syscolumns: 每个表和视图中的每列在表中占一行，存储过程中的每个参数在表中也占一行。

```sql
select * from sys.columns --- 用object_id过滤
```
* 获取存储过程: 

```sql
select a.name,a.[type],b.[definition] from sys.all_objects a,sys.sql_modules b
where a.is_ms_shipped=0 and a.object_id = b.object_id and a.[type] in ('P','V','AF')
order by a.[name] asc
```

### 锁

```sql
WITH NOLOCK -- 无锁, 只能用于select，可能读取到未完成事务

WITH HOLDLOCK -- 保持锁

WITH UPDLOCK -- 更新锁

WITH TABLOCKX -- 强制使用独占表级锁，这个锁在事务期间阻止任何其他事务使用这个表
```

INSERT、 UPDATE 或DELETE 命令时，SQL Server 会自动使用独占锁。

更新锁(UPDLOCK)优点：

* 允许读取数据（不阻塞其它事务）并在以后更新数据，同时确保自从上次读取数据后数据没有被更改。
* 当我们用UPDLOCK来读取记录时可以对取到的记录加上更新锁，从而加上锁的记录在其它的线程中是不能更改的只能等本线程的事务结束后才能更改

```sql
SELECT Qty FROM myTable WITH (UPDLOCK) WHERE Id in (1,2,3)
```

### Procedure 存储过程
```sql
create procedure Proc_Student
@Proc_Son int
as
select * from Student where Sno = @Proc_Son

exec Proc_Stu
```

### 局部变量

* 全局变量是由系统定义的，在整个SQL Server实例内都能访问到的变量，以@@作为第一个字符，用户只能访问，不可以赋值
* *局部变量由用户定义，生命周期只在一个批处理有效，局部变量以@作为第一个字符，由用户自己定义和赋值

```sql
DECLARE @i NVARCHAR(20)
SET @i=1
PRINT @i
```

### for xml path 多行合并

将查询结果集以XML形式展现，将多行的结果，展示在同一行。PATH模式：通过简单的XPath语法来允许用户自定义嵌套的XML结构、元素、属性值。

```sql
select ','+name from <table> FOR xml path('') 
```

SQL SERVER 分组group by之后，字符串合并在一起，逗号隔开

```sql
select
  Batchrunid,
  ActivityCode=(stuff((select ',' + ActivityCode from ActivityLogs where Batchrunid=a.Batchrunid and ActivityStatus='Failed' for xml path('') ),1,1,'')) 
from ActivityLogs a 
WHERE a.ActivityStatus='Failed' and a.BatchRunId='pipeline().parameters.BatchRunID'
group by Batchrunid
```

### 聚合函数

* SUM
* COUNT
* AVG
* MAX
* MIN 字符串排序

```sql
WITH ListPrice AS (
  select
    MaterialCode,
    CONCAT(
      SalesOrg,
      '-',
      Currency,
      '-',
      ValuePricingUOM
    ) XH
  FROM ListPrice
),
SELECT
  MIN(XH) XH,
  split(MIN(XH), '-') [0] SalesOrg,
  split(MIN(XH), '-') [1] Currency,
  split(MIN(XH), '-') [2] ValuePricingUOM
FROM
  ListPrice
GROUP BY
  MaterialCode
```

### CASE 条件

```sql
SELECT
  CASE
    WHEN Currency = 'CNY' THEN ValuePricingUOM
    ELSE ExchangeRate * ValuePricingUOM
  END PriceCNY,
FROM
  ListPrice
```

### date 日期

* current_date
* current_timestamp
* now

```sql
select current_date(); -- 2023-02-24
select current_timestamp(); -- 2023-02-24T06:43:26.124+0000
select now(); -- 2023-02-24T06:43:37.100+0000

select date('2023-03-17') -- 2022-03-17
select timestamp('2023-03-17') -- 2022-03-17T00:00:00.000+0000
select timestamp(concat(substring(insertDate,1,4),'-',substring(insertDate,5,2),'-',substring(insertDate,7,2))) -- insertDate='20230410'  2023-04-10T00:00:00.000+0000
```

* dateadd
```sql
select current_date()-weekday(current_date())-7; -- 上周一
select year(current_date())*100+month(current_date()); -- 202302

select DATEADD(month,-24,CURRENT_DATE()) -- 2年前的今天
```

* date_format
```sql
--- utc +8小时
select date_format(dateadd(hour,8,current_timestamp()),'y') -- 2023
select date_format(dateadd(hour,8,current_timestamp()),'yMM') -- 202302
```

### 字符串操作
* substring 字符串截取
```sql
select substring(string('02月'),1,2) -- 02
```

* STUFF (source_string, start, length, change_string) 字符串替换

```sql
select stuff('02月',1,1,'') -- 2月
```

* concat 字符串拼接, 忽略NULL
```sql
select concat(NUll, 'HaHa') -- 'HaHa'
select NULL+'HaHa' -- NULL
```
* CONCAT_WS(separator,input_string1,input_string2) 用分隔符拼接多个字符串, 忽略NULL
```sql
select concat(',', 'A', NUll, 'B') -- 'A,B'
select concat_ws(',',collect_set(filename)) totalname from <table>
```

* TRIM 删除前后空格
```sql
select TRIM(' A ') -- 'A'
```

* rlike 正则匹配
```sql
select * from df_manu where filename rlike 'Actual_sales_2[01][0-9][0-9][0-9][0-9].xlsx'
-- Actual_sales_202303.xlsx
```

* 大小写
```sql
select LOWER('yoga') -- yoga
select UPPER('yoga') -- YOGA
select INITCAP('yoga') -- Yoga
```

### 运算符

* <>不等于，不包含null的情况
```sql
-- ActivityStatus = 'Success' | 'Failed' | null
select * from ActivityLogs where ActivityStatus <> 'Success' or ActivityStatus is null
```

* ISNULL(p1, p2) p1为null返回p2，否则返回p1
```sql
select isnull(TableName,'')+Remark -- 解决其中一个字段为空的情况，等效于concat
```

* IN (一般比OR操作符清单执行更快)
```sql
select * from <TABLE> where id in (1001, 1002); -- id=1001 or id=1002
```

### 集合操作

* UNION (DISTINCT)：并集 (去重 大小写敏感)
* UNION ALL：并集

query1 UNION (ALL) query2
```sql
select 'a' A union select 'a' A -- a
select 'a' A union select 'b' A -- a, b

select 'a' A union all select 'a' A -- a, a
```

* INTERSECT (DISTINCT)：交集 (去重 大小写敏感)
* INTERSECT ALL：交集

query1 INTERSECT query2
```sql
select 'a' A intersect select 'a' A -- a
select 'a' A intersect select 'b' A -- null
```

### WHERE VS HAVING

* Where 是一个约束声明，使用Where来约束来之数据库的数据，Where是在结果返回之前起作用的，作用在group by子句和having子句之前，Where中不能使用聚合函数。
* Having 是一个过滤声明，是在查询返回结果集以后对查询结果进行的过滤操作，在聚合后对组记录进行筛选，在Having中可以使用聚合函数。

查找重复行
```sql
select COUNT(*) as RepNum, MaterialCode from <TABLE> group by MaterialCode Having COUNT(*)>1;
```

### ORDER BY

```sql
order by qty -- 会逐位比较数字 100 < 20 < 30 

-- 解决方式
order by qty*1
order by int(qty)
order by len(qty) desc -- 可以同时找出正负最大的数
```
