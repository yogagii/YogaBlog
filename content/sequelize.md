Title: Sequelize
Date: 2020-07-25
Category: Backend
Tags: database, sails
Author: Yoga

链接：https://www.jianshu.com/p/4f7353cd5805

Sequelize 是一款基于 Nodejs 功能强大的异步 ORM 框架。
同时支持 PostgreSQL, MySQL, SQLite and MSSQL 多种数据库，很适合作为 Nodejs 后端数据库的存储接口。

_ORM 简单的讲就是对 SQL 查询语句的封装，让我们可以用 OOP 的方式操作数据库，优雅的生成安全、可维护的 SQL 代码。直观上，是一种 Model 和 SQL 的映射关系_

## 安装

```
npm install --save sequelize
```

## 建立连接

```js
const Sequelize = require('sequelize');

// 方法1:单独传递参数
const sequelize = new Sequelize('database', 'root', 'password', {
  host: 'localhost',
  dialect: /* 'mysql' | 'mariadb' | 'postgres' | 'mssql' 之一 */
  operatorsAliases: false,
    dialectOptions: {
        charset: "utf8mb4",
        collate: "utf8mb4_unicode_ci",
        supportBigNumbers: true,
        bigNumberStrings: true
    },

    pool: {
        max: 5,
        min: 0,
        acquire: 30000,
        idle: 10000
    },
    timezone: '+08:00' //东八时区
});

// 方法2: 传递连接 URI
const sequelize = new Sequelize('postgres://user:pass@example.com:5432/dbname');
```

- options.logging: A function that gets executed every time Sequelize would log something.

- options.dialect: The dialect of the database you are connecting to. One of mysql, postgres, sqlite and mssql.

- options.pool: sequelize connection pool configuration
  - max: Maximum number of connection in pool
  - min: Minimum number of connection in pool

验证是否连接成功

```js
sequelize
  .authenticate()
  .then(() => {
    console.log("Success.");
  })
  .catch((err) => {
    console.error("Failed", err);
  });
```

关闭连接

```js
sequelize.close();
```

## 表建模

模型是一个扩展 Sequelize.Model 的类

```js
const Model = Sequelize.Model;
class User extends Model {}
User.init(
  {
    // 属性
    firstName: {
      type: Sequelize.STRING,
      allowNull: false,
    },
    lastName: {
      type: Sequelize.STRING,
      // allowNull 默认为 true
    },
  },
  {
    sequelize,
    modelName: "user",
    // 参数
  }
);
```

Sequelize 在数据库中期望一个名为 users 的表,其中包含 firstName 和 lastName 字段. 默认情况下,表名自动复数。

Sequelize 还默认为每个模型定义了字段id(主键),createdAt和updatedAt。

## 更新表结构
```
npx sails c --dontLift
// 更新表
ExternalResource.sync({alter:true}).then(console.log).catch(console.error)
// 新建表
SummitTrainingContent.sync().then(console.log).catch(console.error)
```