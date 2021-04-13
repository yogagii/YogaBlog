Title: Sails.js
Date: 2020-07-19
Category: Backend
Tags: sails, nodeJS
Author: Yoga

sails.js 是类似于 Ruby on Rails 的开发平台，可以快速整合数据库资源，非常适合网站和 API 服务的构建

类似框架：

- ExpressJS
- Koa.js
- Egg.js

链接：https://www.bilibili.com/video/BV19p411Z7rJ?from=search&seid=13206583137553736240

## 安装

```
npm show sails
npm install -g sails@0.12.14 // @+版本号

sails new testProject
cd testProject
sails lift
```

http://localhost:1337/


> 约定优于配置 CoC（convention over configuration）—— Ruby on Rails

_就是用事先约定好的规则作为框架来写代码，而不是利用一个中心配置文件。具体例子来说，比如在 rails 里面，生成一个 model 和 controller，约定好了 model 默认用名词单数形式，controller 默认用名词复数形式。rails 框架本身会按照这种约定的形式去寻找相应的文件而不是通过一个配置文件告诉框架说我要把这两个文件关联起来。_

链接：https://www.zhihu.com/question/62960377/answer/360959520

在我们开发 sails 应用程序时，如果每一次修改源代码后都要通过【sails lift】命令重新启动服务的话会非常的麻烦，那么通过 nodemon 工具的话，我们就可以非常简单地完成自动启动服务。

http://nodemon.io/

```
"scripts": {
  "debug": "node debug app.js",
  "start": "nodemon app.js"
},
```

---

## 结构

- api: 后台处理程序
  - controllers：控制器，映射路由 URL
  - hooks: 系统功能调用和改变
  - models: 数据库实体模型，和数据库表一一映射
  - policies: 访问策略（权限判断，session 认证）
  - responses: 自定义回应
  - services: 定制全局服务类（静态服务类，全局函数，邮件服务）
- assets: 网站静态文件根目录
- config: 系统设置文件集
  - env
    - production.js 生产环境设置
  - global.js 全局变量
  - route.js 手动配置路由
  - policies.js 权限配置
  - session.js
  - view.js 默认布局设定
  - blueprints 蓝图
  - security (CSRF)
- tasks: 打包工具
  - pipeline.js 编译顺序
- views: 网页模版
- app.js: 应用程序启动入口
- .sailsrc: 设置

---

## 资源 Assets

服务器上想让外界存取的静态文档（js、css、图）放在 assets/ 目录，启动应用程序时会被处理并同步到一个隐藏的暂存目录(.tmp/public/)。这个 .tmp/public 文件夹就是 Sails 实际提供的内容，大致等同于 express 的「public」文件夹。

静态中间件是安装在 Sails 路由之后，资源目录有文档与自定义路由冲突，自定义路由会在到达静态中间件前拦截请求。

### 默认任务 Default Tasks

> webpack、grunt 都是前端打包的工具。
> Grunt 是一种能够优化前端的开发流程的工具，而 WebPack 是一种模块化的解决方案，不过 Webpack 的优点使得 Webpack 在很多场景下可以替代 Grunt 类的工具。

grunt 的工作方式是：在一个配置文件中，指明对某些文件进行压缩、组合、检查等任务的具体步骤，然后在运行中输入相应的命令。

Sails 内的 asset pipeline 是一组能增加工程一致性和效率的 Grunt 任务设置。

包含在 Sails 工程的 Grunt 任务:

### 禁用 Grunt

```
{
  "hooks": {
    "grunt": false
  }
}
```

---

## 设置 Configuration

- 程序设置

- 指定环境变量或命令行参数

- 改变 local 或 global .sailsrc 文档

```js
sails = require('sails');
rc = require('sails/accessible/rc’);

sails.lift(rc('sails'));
```

rc: 检索通过环境变量设置的配置

With the exception of NODE_ENV and PORT, configuration set via environment variables will not automatically apply to apps started using .lift(), nor will options set in .sailsrc files. If you wish to use those configuration values, you can retrieve them via require('sails/accessible/rc')('sails') and pass them in as the first argument to .lift().

- 使用约定位于工程内 config/ 文件夹的模板设置文档

执行时期可通过 sails 全局变数的 sails.config 在应用程序使用合并后的设置。

sails.config 对象的顶层键（例如 sails.config.views）对应在应用程序内特定的设置文档（例如 config/views.js）

```js
// 新增一个新文档config/foo.js
// 对象会被合并到 `sails.config.blueprints`
module.exports.blueprints = {
  shortcuts: false,
}
```

---

## 控制器 Controllers

MVC 中的 C，负责响应请求，包含项目的大部分业务逻辑。

### Actions

控制器由一组称为 Action 的函数组成, action 可以绑定 routes，这样当客户机请求路由时，将执行绑定方法以执行某些业务逻辑并生成响应。

GET /hello route in your application could be bound to a method like:

```js
function (req, res) {
  return res.send("Hi there!");
}
```

### Generating controllers

> $ sails generate controller <controller name> [action names separated by spaces...]
<br/> $ sails generate controller comment create destroy tag like

控制器在 api/Controllers/文件夹中定义，Pascal 命名法（UserController.js）

文件内部定义了一个 object
{
action names: corresponding action methods.
}

```js
// api/controllers/SayController.js
module.exports = {
  hi: function (req, res) {
    return res.send('Hi there!')
  },
  bye: function (req, res) {
    return res.redirect('http://www.sayonara.com')
  },
}
// config/routes.js
module.exports.routes = {
  'GET /say/hi': { action: 'say/hi' },
}
```

```js
// api/controllers/say/hi.js
module.exports = async function hi(req, res) {
  res.ok() // 200
}
/// config/routes.js
module.exports.routes = {
  'GET /say/hi': { action: 'say/hi' },
}
```

There are two main types of routes in Sails:

- automatic (or "implicit"隐性的).

自带路由/say/hi 和 /say/bye

- custom (or "explicit"显性的)

在/config/routes 里手动配置

```js
// [HTTP method (optionally)] [address]: [target]
module.exports.routes = {
  'get /signup': { view: 'conversion/signup' },
  'POST /make/a/sandwich': 'SandwichController.makeIt', // trigger the makeIt() action in api/controllers/SandwichController.js
  '/logout': 'AuthController.logout', // bind all request methods
  'GET /page2': [{ policy: 'accessLog' }, { controller: 'test', action: 'page2' }],
}
```

### Express

req 请求对象, res 响应对象, next 应用程序请求

如果当前的中间件函数没有结束请求 - 响应周期，则必须调用 next()以将控制传递给下一个中间件函数。否则，请求将被挂起。

```js
app.get('/', function (req, res, next) {
  next()
})
```

_Sails 缺少参数 next，所以 Sails controller actions should always be the last stop in the request chain--that is, they should always result in either a response or an error._

### "Thin" Controllers

- Write a custom model method 封装
- Write a service as a function 服务
- extract it into a node module 模块

---

## 蓝图 Blueprint API

Blueprints are Sails’s way of quickly generating API routes and actions based on your application design.

> \$ sails generate api User

生成文件

- api/controllers/UserController.js
- api/models/User.js

```js
attributes: {
  username: {
    type: 'string'
  },
  address: {
    type: 'string'
  }
}
```

**Blueprint routes**

If you create a User.js model file in your project, then with blueprints enabled you will be able to immediately visit /user/create?name=joe to create a user, and visit /user to see an array of your app's users.

**Blueprint actions**

- find
- findOne
- create
- update
- destroy
- populate
- add
- remove
- replace

To override a RESTful blueprint route for a single model, simply create an action in the relevant controller file (or a standalone action in the relevant folder) with the appropriate name: find, findOne, create, update, destroy, populate, add or remove.

| Route            | Action                 |
| ---------------- | ---------------------- |
| GET /user        | UserController.find    |
| GET /user/:id    | UserController.findOne |
| POST /user       | UserController.create  |
| PATCH /user/:id  | UserController.update  |
| DELETE /user/:id | UserController.destroy |

```js
// config/blueprints.js
actions: true, // expose implicit routes 将控制器里的方法自动映射成URL
rest: false, // expose RESTful routes 将增删改查全部暴露给用户
shortcuts: false, // CRUD "shortcut" routes to GET requests
```

```js
// actions没开启时可手动增加路由
module.exports.routes = {
  'GET /foo/go': 'UserController.find',
}
```

### Security

If CSRF protection is enabled, you'll need to provide or disable a CSRF token for POST/PUT/DELETE actions, otherwise you will get a 403 Forbidden response.

When CSRF protection is enabled in your Sails app, all non-GET requests to the server must be accompanied by a special "CSRF token", which can be included as either the '\_csrf' parameter or the 'X-CSRF-Token' header.

```js
// config/security.js
csrf: false
```

---

## 回应 Responses

```js
foo: function(req, res) {
   res.ok() // 200
   res.forbidden() // 403
   res.notFound() // 404
   res.serverError() // 500
}
```

- normalized 标准化的 (错误代码是一致的)
- abstracted 被分离的 (有考虑到生产环境与开发环境的日志记录)
- content-negotiated 内容协商的(JSON)

```js
foo: function(req, res) {
   if (!req.param('id')) {
     res.badRequest('Sorry, you need to tell us the ID of the FOO you want!');
   }
}
```

任何储存在 /api/responses 文件夹的 .js 脚本可通过在控制器内呼叫 res.[responseName] 来执行。例如，可以通过呼叫 res.serverError(errors) 来执行 /api/responses/serverError.js

### 默认回应 Default responses

- res.serverError(errors)
- res.badRequest(validationErrors, redirectTo)
- res.notFound()
- res.forbidden(message)

### 自定义回应 Custom Response

要加入你自己的自定义回应方法，只需新增与方法名称相同的文档到 /api/responses

To add your own custom response method, simply add a file to /api/responses with the same name as the method you would like to create.

---

## 部署 Deployment

所有生产环境设置都储存在 config/env/production.js

```js
cors: {
  allRoutes: false, //关闭全路由的跨域存取
  origin: 'http://foobar.com,https://owlhoot.com', //允许存取的域名
  credentials: true, //需要cookies验证
},
csrf: true
```

在生产环境中，使用 forever start app.js --prod 或 pm2 start app.js -x -- --prod 启动服务器，这和 sails lift --prod 所做的事相同，但是当服务器崩溃时，它会自动重新启动。

---

## Views

- 403.ejs
- 404.ejs
- 500.ejs
- pages
  - homepage.ejs:网站主页
- layouts
  - layout.ejs:网页公共布局

pages 中的内容会被渲染到 layout 中的<%- body %>

---

## Policies

为访问的 URL 绑定存取日志功能。

```js
// api/policies/accessLog.js
module.exports = function (req, res, next) {
  console.info(req.method, req.path)
  return next()
}
```

```js
// config/policies.js
module.exports.policies = {
  '*': ['is-logged-in', 'accesslog'], // 排在前面的先执行
}
```
