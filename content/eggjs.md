Title: Egg.js
Date: 2020-12-31
Category: Backend
Tags: egg, nodeJS
Author: Yoga

https://eggjs.org/zh-cn/intro/index.html

Sails 是和 Egg 一样奉行『约定优于配置』的框架，扩展性也非常好。但是相比 Egg，Sails 支持 Blueprint REST API、WaterLine 这样可扩展的 ORM、前端集成、WebSocket 等。而 Egg 不直接提供功能，只是集成各种功能插件(egg-blueprint，egg-waterline)。

Egg 继承于 Koa


Sails 使用 Express 的静态中间件来提供你的资源。你可以在 /config/http.js 设置这个中间件。与 koa2 中间件不同的是，express中间件一个接一个的顺序执行, 通常会将 response 响应写在最后一个中间件中

Koa 的中间件和 Express 不同，Koa 选择了洋葱圈模型。

![koa](img/koa.png)

## 基础对象:

从 Koa 继承而来的 4 个对象（Application, Context, Request, Response) 

框架扩展的一些对象（Controller, Service, Helper, Config, Logger）