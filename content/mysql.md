Title: MySQL
Date: 2020-07-25
Category: Backend
Tags: mysql, database
Author: Yoga

安装 mysql

```
brew install mysql
```

登录 mysql

```
mysql -u root -p
```

退出 mysql

```
exit
```

创建数据库

```
CREATE DATABASE <数据库名>;
```

查看当前的数据库

```
show databases;
```

删除数据库

```
drop database <数据库名>;
```

选择数据库

```
use <数据库名>;
```

创建数据表

```
CREATE TABLE table_name (column_name column_type);
mysql> CREATE TABLE runoob_tbl(
   -> runoob_id INT NOT NULL AUTO_INCREMENT,
   -> runoob_title VARCHAR(100) NOT NULL,
   -> runoob_author VARCHAR(40) NOT NULL,
   -> submission_date DATE,
   -> PRIMARY KEY ( runoob_id )
   -> )ENGINE=InnoDB DEFAULT CHARSET=utf8;
// ENGINE 设置存储引擎，CHARSET 设置编码。
```

显示当前数据库的表单

```
show tables
```

删除数据表

```
DROP TABLE table_name;
```

插入数据

```
INSERT INTO table_name ( field1, field2,...fieldN )
                       VALUES
                       ( value1, value2,...valueN );
mysql> INSERT INTO runoob_tbl
    -> (runoob_title, runoob_author, submission_date)
    -> VALUES
    -> ("学习 PHP", "菜鸟教程", NOW());
```

查询数据

```
SELECT column_name,column_name
FROM table_name
[WHERE Clause]
[LIMIT N][ OFFSET M]
// LIMIT 返回的记录数
// OFFSET 开始查询的数据偏移量, 默认为0
```

更新数据

```
UPDATE table_name SET field1=new-value1, field2=new-value2
[WHERE Clause]
```

DELETE 语句

```
DELETE FROM table_name [WHERE Clause]
```

LIKE 子句 (string has somevalue)

```
SELECT field1, field2,...fieldN
FROM table_name
WHERE field1 LIKE condition1 [AND [OR]] filed2 = 'somevalue'

// runoob_tbl 表中获取 runoob_author 字段中以 COM 为结尾
mysql> SELECT * from runoob_tbl  WHERE runoob_author LIKE '%COM';
```

UNION 操作符 (new set)

```
// 排除重复
SELECT country FROM Websites
UNION
SELECT country FROM apps
ORDER BY country;

// 保留重复
SELECT country FROM Websites
UNION ALL
SELECT country FROM apps
ORDER BY country;
```

排序

```
mysql> SELECT * from runoob_tbl ORDER BY submission_date ASC;
mysql> SELECT * from runoob_tbl ORDER BY submission_date DESC;
```

分组

```
SELECT column_name, function(column_name)
FROM table_name
WHERE column_name operator value
GROUP BY column_name;

//在分组统计数据基础上再进行相同的统计（SUM,AVG,COUNT…）
SELECT name, SUM(singin) as singin_count FROM  employee_tbl GROUP BY name WITH ROLLUP;
```

正则表达式

```
// 查找name字段中以'st'为开头的所有数据
SELECT name FROM person_tbl WHERE name REGEXP '^st';
```

2020.9.10

查询缓存：缓存相同查询语句的结果

```sql
SHOW ENGINES
```

Mysql 常用存储引擎：

- InnoDB
- MyISAM

Charset 字符集：

- utf8 (utf8mb3 一个字符最多三个字节，emoji 是 4 字节编码)
- utf8mb4 (完整)

```sql
SET character_set_client='utf8mb4' // 数据库接收到的
SET character_set_connection='utf8mb4' // 当前连接
SET character_set_results='utf8mb4' // 返回给客户端的
```

## B+树

每个键都是一个叶节点，每张表不会超过 3-4 层

一级索引里存的是完整记录，二级索引只存了部分字段

对两个字段做联合索引时，只存了这两个字段和主键

回表：根据主键索引 id 查询很快，能拿到完整数据，根据二级索引 name 查询只能拿到 name 和 id


```sql
SELECT * FROM fpa.test WHERE NAME = 'aaa'
SELECT * FROM fpa.test WHERE NAME LIKE = 'aaa%' // 模糊匹配: 以aaa开头的字符串
```

联合索引：最左匹配原则

idx_a_b_c

```sql
SELECT * FROM fpa.test WHERE a = 'xxx' AND b = 'yyy'
SELECT * FROM fpa.test WHERE b = 'xxx' AND c = 'yyy' // 用不到联合索引
SELECT * FROM fpa.test WHERE a = 'xxx' OR b = 'yyy' // a和b两个索引都用不到
```

范围索引

联表查询

```sql
const query = {
  order: [['updatedAt', 'createdAt']],
  include: [user] // 必须有外键才能联表查询 foreignKey: 'user'
}
```

## 优化

- 建立合理的索引（避免回表）
- 写合理的查询语句 (select a,b 不要select *，尽量少做连表查询）
- 分表和分库 （根据功能模块，把有业务关联的数据分库）

```sql
// set announcement unread
UPDATE fpa.`Notifications` SET isUnread=1 WHERE USER='9ca53fc1-5644-4bf4-bc6e-d598218c8af2' AND TYPE='comment'
SELECT * FROM fpa.`Notifications` WHERE USER='9ca53fc1-5644-4bf4-bc6e-d598218c8af2' AND TYPE='comment'

// add sap permission
INSERT INTO fpa.`Permissions` (resource, USER, TYPE, createdAt, updatedAt) VALUES('SAP', '9ca53fc1-5644-4bf4-bc6e-d598218c8af2', 'GENERAL', NOW(), NOW())
DELETE FROM fpa.`Permissions` where user='9ca53fc1-5644-4bf4-bc6e-d598218c8af2' AND resource='SAP'
SELECT * FROM fpa.`Permissions` where user='9ca53fc1-5644-4bf4-bc6e-d598218c8af2'

// select external resource
SELECT count(*) AS `count` FROM `ExternalResources` AS `ExternalResource` WHERE (JSON_CONTAINS(`position`, JSON_ARRAY('PVP')) = 1 AND JSON_CONTAINS(`role`, JSON_ARRAY('IT')) = 1 AND JSON_CONTAINS(`region`, JSON_ARRAY('AP')) = 1 AND JSON_CONTAINS(`sector`, JSON_ARRAY('ALLSECTORS')) = 1);

// update
UPDATE fpa.`ViewsCountRecords` SET TYPE = 'SAP'

// delete user
delete from fpa.users where userId="wfang9"
DELETE FROM fpa.Permissions WHERE `user`='c8a5d877-2a18-4bff-8070-b5a4d5d033a3'
```