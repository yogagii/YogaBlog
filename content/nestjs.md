Title: NestJS
Date: 2022-01-18
Category: Backend
Tags: nest
Author: Yoga

## Overview

1. Nest深受Angular的影响，借鉴了NG的一些列前端设计思路，特别是其代码结构。让Angular易于开发大型前端的优势也发挥在Node服务器端。
2. 模块化：高度可测试，可扩展，松散耦合且易于维护
3. nestjs直接对接ts类型系统
4. 解析数据库schema，产出swagger，对typeORM的整合的非常不错


## Controllers

控制器的目的是接收应用的特定请求。路由机制控制哪个控制器接收哪些请求。通常，每个控制器有多个路由，不同的路由可以执行不同的操作。

### Response

返回object or array，自动序列化为JSON

返回string，number，boolean，只发送值

```js
findAll(@Res() response){
  response.status(200).send()
})
```

### Request

* @Request(), @Req()：@Res() 只是 @Response() 的别名
* @Param(key?: string)
* @Body(key?: string)
* @Query(key?: string)
