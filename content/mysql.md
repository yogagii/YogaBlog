Title: MySQL
Date: 2020-07-25
Category: Backend
Tags: sql
Author: Yoga

安装 mysql

```
brew install mysql
```

启动 mysql

```
service mysqld start
```

登录 mysql

```sql
mysql -u root -p
mysql -u root -p --ssl
mysql -u root -p --ssl-mode-required
```

退出 mysql

```sql
exit
```

* DDL 数据定义语言（无法回滚）：create，drop，alter，truncat，rename
* DML 数据操作语言（可以回滚）：insert，update，delete，select

创建数据库

```sql
CREATE DATABASE <数据库名>;
```

查看当前的数据库

```sql
show databases;
```

创建数据库

```sql
create database <数据库名>;
```

删除数据库

```sql
drop database <数据库名>;
```

选择数据库

```sql
use <数据库名>;
```

创建新用户

```sql
CREATE USER 'tester'@'localhost' IDENTIFIED BY '123';
SHOW GRANTS for 'tester'@'localhost';
GRANT ALL ON *.* TO 'tester'@'localhost' WITH GRANT OPTION;
flush privileges;
```

删除用户

```sql
DROP USER 'tester'@'localhost';
```

检查端口号

```sql
show global variables like 'port'; -- 默认 3306
```

导入表sql

```sql
source /Users/yoga/code/xxx.sql
```

导出表

```sql
-- need FILE privilege: GRANT FILE ON *.* TO 'username'@'hostname';
SELECT *
INTO OUTFILE '/path/to/your/outputfile.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
FROM table_name;
```
```bash
mysqldump -u username -p --tab=/path/to/your/directory your_database your_table_name
mysqldump -u username -p --no-data database table_name > /path/to/your/outputfile.sql
```

创建数据表

```sql
CREATE TABLE table_name (column_name column_type);
mysql> CREATE TABLE runoob_tbl(
   -> runoob_id INT NOT NULL AUTO_INCREMENT,
   -> runoob_title VARCHAR(100) NOT NULL,
   -> runoob_author VARCHAR(40) NOT NULL,
   -> submission_date DATE,
   -> PRIMARY KEY ( runoob_id )
   -> )ENGINE=InnoDB DEFAULT CHARSET=utf8;
-- ENGINE 设置存储引擎，CHARSET 设置编码。
```

显示当前数据库的表单

```sql
show tables
```

显示表结构

```sql
desc <表名>
```

显示表字段

```sql
SHOW COLUMNS FROM table_name;
```

显示建表语句

```sql
SHOW CREATE TABLE table_name;
```

删除数据表

```sql
DROP TABLE table_name; --将删除表的结构被依赖的约束(constrain)，触发器(trigger)，索引(index)
truncate TABLE table_name; --只删除数据不删除表的结构
```

插入数据

```sql
INSERT INTO table_name ( field1, field2,...fieldN )
                       VALUES
                       ( value1, value2,...valueN );
mysql> INSERT INTO runoob_tbl
    -> (runoob_title, runoob_author, submission_date)
    -> VALUES
    -> ("学习 PHP", "菜鸟教程", NOW());
```

查询数据

```sql
SELECT column_name,column_name
FROM table_name
[WHERE Clause]
[LIMIT N][ OFFSET M]
-- LIMIT 返回的记录数
-- OFFSET 开始查询的数据偏移量, 默认为0
```
mssql不支持limit，mysql支持

更新表

```sql
ALTER TABLE `CustomViews` ADD `prompts` JSON;
ALTER TABLE fpa.CustomViews DROP COLUMN prompts;
```
更新数据

```sql
UPDATE table_name SET field1=new-value1, field2=new-value2
[WHERE Clause]
```

DELETE 语句

```sql
DELETE FROM table_name [WHERE Clause]
```

LIKE 子句 (string has somevalue) / ILIKE 不区分大小写

```sql
SELECT field1, field2,...fieldN
FROM table_name
WHERE field1 LIKE condition1 [AND [OR]] filed2 = 'somevalue'

-- runoob_tbl 表中获取 runoob_author 字段中以 COM 为结尾
mysql> SELECT * from runoob_tbl  WHERE runoob_author LIKE '%COM';
```

LEFT JOIN 

```sql
SELECT e.project_id FROM (
  bc_wr_user_exam as e
  LEFT JOIN bc_r_user_task as t on t.project_id = e.project_id
)
```
LEFT JOIN 左连接：两表关联，左表全部保留，右表关联不上用null表示。

RIGHT JOIN 右连接：右表全部保留，左表关联不上的用null表示。

INNER JOIN 内连接：两表关联，保留两表中交集的记录。

左表独有：两表关联，查询左表独有的数据。
```sql
select * from t1 left join t2 on t1.id = t2.id where t2.id is null;
```

右表独有：两表关联，查询右表独有的数据

```sql
select * from t1 right join t2 on t1.id = t2.id where t1.id is null;
```

FULL JOIN 全连接：两表关联，查询它们的所有记录。MySQl 不支持 FULL JOIN，通过UNION来实现：
```sql
SELECT * FROM a LEFT JOIN b ON a.name = b.name 
UNION
SELECT * FROM a RIGHT JOIN b ON a.name = b.name;
```

UNION 操作符 (new set)

```sql
-- 排除重复
SELECT country FROM Websites
UNION
SELECT country FROM apps
ORDER BY country;

-- 保留重复
SELECT country FROM Websites
UNION ALL
SELECT country FROM apps
ORDER BY country;
```

排序

```sql
mysql> SELECT * from runoob_tbl ORDER BY submission_date ASC;
mysql> SELECT * from runoob_tbl ORDER BY submission_date DESC;
```

分组

```sql
SELECT column_name, function(column_name)
FROM table_name
WHERE column_name operator value
GROUP BY column_name;

-- 在分组统计数据基础上再进行相同的统计（SUM,AVG,COUNT…）
SELECT name, SUM(singin) as singin_count FROM  employee_tbl GROUP BY name WITH ROLLUP;
```

正则表达式

```sql
-- 查找name字段中以'st'为开头的所有数据
SELECT name FROM person_tbl WHERE name REGEXP '^st';
```

展开数组

```sql
SELECT EXPLODE(DATA) data FROM table_name
```

返回参数中的第一个非空表达式

```sql
select COALESCE(CnName, EnName) from table_name
```

自定义变量
```sql
set @key=value
set @key:=value
select @key:=value
```

自定义函数
```sql
Create function 函数名(参数)
Returns 返回值数据类型
as
begin
SQL 语句(必须有return变量或值)
End
```

子查询部分(subquery factoring)：将需要频繁执行的SQL片段加个别名放到全局中
```sql
with A as (
  select * from user
)

select * from A, customer where customer.userid = user.id
```

### 存储过程(Stored Procedure)：一组为了完成特定功能的SQL 语句

* 当对数据库进行复杂操作时，可将此复杂操作用存储过程封装起来与数据库提供的事务处理结合一起使用
* 存储过程只在创造时进行编译，以后每次执行存储过程都不需再重新编译，而一般SQL语句每执行一次就编译一次,所以使用存储过程可提高数据库执行速度，效率要比T-SQL语句高
* 存储过程有助于减少应用程序和数据库服务器之间的流量，因为应用程序不必发送多个冗长的 SQL 语句，而只用发送存储过程的名称和参数

```sql
-- 创建过程 --
mysql> DELIMITER //
mysql> create procedure mypro(in a int, in b int, out sum int)
     > begin
     > set sum = a + b; -- 这个封号不能漏 --
     > end //

-- 调用过程 -- call 用来调用过程，@s 是用来接收过程输出参数的变量。
call mypro(1,2,@s);
-- 输出结果 --
select @s;
```
踩坑：服务器处理 SQL 语句默认是以分号作为语句结束标志的。然而在创建存储过程时，存储过程体可能包含有多条 SQL 语句，服务器在处理时会以遇到的第一个分号作为整个程序的结束符。通常使用 DELIMITER 命令将结束命令修改为其他字符，创建完成后再改回来。
```sql
mysql > DELIMITER ;
```

流程控制语句

* if
* case
* while
* repeat
* loop
```sql
create procedure mypro2(in num int)
begin
if num<0 then -- 条件开始
select '负数';
elseif num=0 then
select '不是正数也不是负数';
else
select '正数';
end if;-- 条件结束
end;

-- 调用过程
call mypro2(-1);
```
存储过程管理
```sql
-- 显示存储过程
SHOW PROCEDURE STATUS;
-- 显示特定数据库的存储过程，代码如下所示
SHOW PROCEDURE status where db = 'schooldb';
-- ：显示特定模式的存储过程，要求显示名称中包含“my”的存储过程，代码如下所示
SHOW PROCEDURE status where name like '%my%';
-- 显示存储过程源码
SHOW CREATE PROCEDURE mypro1;
-- 删除存储过程
drop PROCEDURE mypro1;
```

原文链接：https://blog.csdn.net/scj0725/article/details/114625180

| Procedure | Function
| - | -
作为PL/SQL语句执行 | 作为一个表达式执行
在 COMMAND 命令窗口中，使用 EXECUTE 命令执行过程 | 借用 select 语句来执行
不可在 DDL 和 SELECT 语句中调用过程 | 可在 DDL 和 SELECT 语句中调用函数
在头部不能包含RETURN语句 | 在头部必须包含RETURN语句
可以通过output参数返回值，可返回多个值 | 必须返回一个single值
可以有一个不包括值的返回语句 | 必须至少包含一个RETURN语句

### 事务 Transaction

事务就是由单独单元的一个或多个sql语句组成，在这个单元中，每个sql语句都是相互依赖的。

事务是一个整体，里面的内容要么都执行成功，要么都不成功。不可能存在部分执行成功而部分执行不成功的情况。如果某条sql语句一旦执行失败或者产生错误，那么整个单元将会回滚(返回最初状态)到事务开始之前的状态。

事务的四个特性(ACID):
* 原子性（Atomicity）：指事务是一个不可分割的最小工作单位，事务中的操作只有都发生和都不发生两种情况
* 一致性（Consistency）：事务必须使数据库从一个一致状态变换到另外一个一致状态，不存在中间状态。
* 隔离性（Isolation）：多个事务之间相互隔离的，并发执行的各个事务之间不能互相干扰。
* 持久性（Durability）：一个事务一旦提交成功，它对数据库中数据的改变将是永久性的，接下来的其他操作或故障不应对其有任何影响。

```sql
start transaction; -- 开始事务
-- do something
commit; -- 提交事务
```

> 事务 VS 存储过程：存储过程中可以有事务，事务中也可以有多个存储过程；存储过程方便了功能块的进行，事务保证了功能执行的完整性；事务是保存在项目里的，存储过程是保存在数据库里的。

---

2020.9.10

查询缓存：缓存相同查询语句的结果

```
SHOW ENGINES
```

Mysql 常用存储引擎：

- InnoDB
- MyISAM

Charset 字符集：

- utf8 (utf8mb3 一个字符最多三个字节，emoji 是 4 字节编码)
- utf8mb4 (完整)

```sql
SET character_set_client='utf8mb4' -- 数据库接收到的
SET character_set_connection='utf8mb4' -- 当前连接
SET character_set_results='utf8mb4' -- 返回给客户端的
```

## B+树

每个键都是一个叶节点，每张表不会超过 3-4 层

一级索引里存的是完整记录，二级索引只存了部分字段

对两个字段做联合索引时，只存了这两个字段和主键

回表：根据主键索引 id 查询很快，能拿到完整数据，根据二级索引 name 查询只能拿到 name 和 id


```sql
SELECT * FROM fpa.test WHERE NAME = 'aaa'
SELECT * FROM fpa.test WHERE NAME LIKE = 'aaa%' -- 模糊匹配: 以aaa开头的字符串
```

联合索引：最左匹配原则

idx_a_b_c

```sql
SELECT * FROM fpa.test WHERE a = 'xxx' AND b = 'yyy'
SELECT * FROM fpa.test WHERE b = 'xxx' AND c = 'yyy' -- 用不到联合索引
SELECT * FROM fpa.test WHERE a = 'xxx' OR b = 'yyy' -- a和b两个索引都用不到
```

范围索引

联表查询

```sql
const query = {
  order: [['updatedAt', 'createdAt']],
  include: [user] -- 必须有外键才能联表查询 foreignKey: 'user'
}
```

## 优化

- 建立合理的索引（避免回表）
- 写合理的查询语句 (select a,b 不要select *，尽量少做连表查询）
- 分表和分库 （根据功能模块，把有业务关联的数据分库）

```sql
-- set announcement unread
UPDATE fpa.`Notifications` SET isUnread=1 WHERE USER='9ca53fc1-5644-4bf4-bc6e-d598218c8af2' AND TYPE='comment'
SELECT * FROM fpa.`Notifications` WHERE USER='9ca53fc1-5644-4bf4-bc6e-d598218c8af2' AND TYPE='comment'

-- add sap permission
INSERT INTO fpa.`Permissions` (resource, USER, TYPE, createdAt, updatedAt) VALUES('SAP', '9ca53fc1-5644-4bf4-bc6e-d598218c8af2', 'GENERAL', NOW(), NOW())
DELETE FROM fpa.`Permissions` where user='9ca53fc1-5644-4bf4-bc6e-d598218c8af2' AND resource='SAP'
SELECT * FROM fpa.`Permissions` where user='9ca53fc1-5644-4bf4-bc6e-d598218c8af2'

-- select external resource
SELECT count(*) AS `count` FROM `ExternalResources` AS `ExternalResource` WHERE (JSON_CONTAINS(`position`, JSON_ARRAY('PVP')) = 1 AND JSON_CONTAINS(`role`, JSON_ARRAY('IT')) = 1 AND JSON_CONTAINS(`region`, JSON_ARRAY('AP')) = 1 AND JSON_CONTAINS(`sector`, JSON_ARRAY('ALLSECTORS')) = 1);

-- update
UPDATE fpa.`ViewsCountRecords` SET TYPE = 'SAP'

-- delete user
delete from fpa.users where userId="wfang9"
DELETE FROM fpa.Permissions WHERE `user`='c8a5d877-2a18-4bff-8070-b5a4d5d033a3'
```