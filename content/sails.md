Title: Sails.js
Date: 2020-07-19
Category: Backend
Tags: sails, nodeJS
Author: Yoga

## 安装

```
npm install -g sails
sails new testProject
sails lift
```
http://localhost:1337/

> 约定优于配置CoC（convention over configuration）—— Ruby on Rails

*就是用事先约定好的规则作为框架来写代码，而不是利用一个中心配置文件。具体例子来说，比如在rails里面，生成一个model和controller，约定好了model默认用名词单数形式，controller默认用名词复数形式。rails框架本身会按照这种约定的形式去寻找相应的文件而不是通过一个配置文件告诉框架说我要把这两个文件关联起来。*

链接：https://www.zhihu.com/question/62960377/answer/360959520

## 资源 Assets

服务器上想让外界存取的静态文档（js、css、图）放在 assets/ 目录，启动应用程序时会被处理并同步到一个隐藏的暂存目录(.tmp/public/)。这个 .tmp/public 文件夹就是 Sails 实际提供的内容，大致等同于 express 的「public」文件夹。

静态中间件是安装在 Sails 路由之后，资源目录有文档与自定义路由冲突，自定义路由会在到达静态中间件前拦截请求。

### 默认任务 Default Tasks

> webpack、grunt都是前端打包的工具。
Grunt是一种能够优化前端的开发流程的工具，而WebPack是一种模块化的解决方案，不过Webpack的优点使得Webpack在很多场景下可以替代Grunt类的工具。

grunt的工作方式是：在一个配置文件中，指明对某些文件进行压缩、组合、检查等任务的具体步骤，然后在运行中输入相应的命令。

Sails 内的 asset pipeline 是一组能增加工程一致性和效率的 Grunt 任务设置。

包含在Sails工程的Grunt任务:

### 禁用Grunt

```
{
  "hooks": {
    "grunt": false
  }
}
```

## 设置 Configuration

* 程序设置

* 指定环境变量或命令行参数

* 改变local或global .sailsrc 文档

* 使用约定位于工程内 config/ 文件夹的模板设置文档

执行时期可通过 sails 全局变数的 sails.config 在应用程序使用合并后的设置。

sails.config 对象的顶层键（例如 sails.config.views）对应在应用程序内特定的设置文档（例如 config/views.js）

新增一个新文档config/foo.js
```js
// 对象会被合并到 `sails.config.blueprints`
module.exports.blueprints = {
  shortcuts: false
};
```