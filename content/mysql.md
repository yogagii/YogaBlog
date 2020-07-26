Title: MySQL
Date: 2020-07-25
Category: Backend
Tags: mysql, database
Author: Yoga

安装mysql
```
brew install mysql
```

登录mysql
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

