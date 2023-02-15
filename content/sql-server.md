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

### STUFF 字符串合并

SQL SERVER 分组group by之后，字符串合并在一起，逗号隔开

```sql
select
  Batchrunid,
  ActivityCode=(stuff((select ',' + ActivityCode from ActivityLogs where Batchrunid=a.Batchrunid and ActivityStatus='Failed' for xml path('') ),1,1,'')) 
from ActivityLogs a 
WHERE a.ActivityStatus='Failed' and a.BatchRunId='pipeline().parameters.BatchRunID'
group by Batchrunid
```

### MIN 字符串排序

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

```sql
--- utc +8小时
select date_format(dateadd(hour,8,current_timestamp()),'y') -- 2023
select date_format(dateadd(hour,8,current_timestamp()),'yMM') -- 202302

select DATEADD(month,-24,CURRENT_DATE()) -- 2年前的今天
```

### 字符串操作

```sql
select substring(string('02月'),1,2) -- substring 字符串截取
```

### 运算符

<>不等于，不包含null的情况
```sql
-- ActivityStatus = 'Success' | 'Failed' | null
select * from ActivityLogs where ActivityStatus <> 'Success' or ActivityStatus is null
```
