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

A nestjs template that contains basic functions (typeorm, task, email, unit test): 
https://github.com/yogagii/nest_startup

```
$ npm i -g @nestjs/cli
$ nest new project-name
```

## Controllers 控制器

控制器的目的是接收应用的特定请求。路由机制控制哪个控制器接收哪些请求。通常，每个控制器有多个路由，不同的路由可以执行不同的操作。

> $ nest g controller cats

__Request:__

* @All() 用于处理所有 HTTP 请求方法的处理程序
* @Get()
* @Post()
* @Put()
* @Patch()
* @Delete()
* @Options()
* @Header('Cache-Control', 'none') 指定自定义响应头
* @Redirect('https://nestjs.com', 301) 重定向

Param decorators:
* @Request(), @Req()：@Req() 只是 @Request() 的别名
* @Param(key?: string)
* @Body(key?: string)
* @Query(key?: string)

```js
import { Controller, Get, Req, Param } from '@nestjs/common';
@Get(':id')
findOne(@Param() params): string { //@Param('id') id
  return `This action returns a #${params.id} cat`;
}

@Post()
async create(@Body() createCatDto: CreateCatDto) {
  return 'This action adds a new cat';
}
```

DTO（数据传输对象）模式。DTO是一个对象，它定义了如何通过网络发送数据。

```ts
export class CreateCatDto {
  readonly name: string;
  readonly age: number;
  readonly breed: string;
}
```

__Response:__

返回object or array，自动序列化为JSON

返回string，number，boolean，只发送值

```js
import { Response } from 'express';

findAll(@Res() response){
  response.status(200).send()
})
```
* @Response()，@Res()必须通过调用 response 对象（res.json(…) 或 res.send(…)）发出某种响应，否则 HTTP 服务器将挂起。

* @HttpCode() 响应的状态码总是默认为 200，除了 POST 请求（默认响应状态码为 201）

异步
```js
async findAll(): Promise<any[]> {
  return [];
}
```

## Providers 提供者

Provider 只是一个用 @Injectable() 装饰器注释的类。

> $ nest g service cats

__依赖注入__

Nest 将 catsService 通过创建并返回一个实例来解析 CatsService，解析此依赖关系并将其传递给控制器的构造函数，实现数据共享

```ts
constructor(private readonly catsService: CatsService) {}
```

Provider 通常具有与应用程序生命周期同步的生命周期（“作用域”）。在启动应用程序时，必须解析每个依赖项，因此必须实例化每个提供程序。同样，当应用程序关闭时，每个 provider 都将被销毁。

```ts
import { Injectable, Inject } from '@nestjs/common';

@Injectable() // 类装饰器：基于构造函数的注入
export class HttpService<T> {
  @Inject('HTTP_OPTIONS') // 属性装饰器：基于属性的注入
  private readonly httpClient: T;
}
```

```ts
// app.module.ts
@Module({
  controllers: [CatsController], // 服务的使用者
  providers: [CatsService], // 服务的提供者
})
```

## Modules 模块

模块是具有 @Module() 装饰器的类。 @Module() 装饰器提供了元数据，Nest 用它来组织应用程序结构。

每个 Nest 应用程序至少有一个模块，即根模块。根模块是 Nest 开始安排应用程序树的地方，根模块可能是应用程序中唯一的模块.

```ts
// app.module.ts
@Module({
  controllers: [AppController, CatsController],
  providers: [AppService, CatsService],
})
export class AppModule {}
```

> $ nest g module cats

```ts
// cats.module.ts
// @Global() // 全局模块，不需要在 imports 数组中导入
@Module({
  controllers: [CatsController],
  providers: [CatsService],
  // exports: [CatsService], // 每个导入CatsModule的模块都可以访问CatsService，共享相同的CatsService实例
})
export class CatsModule {}

// app.module.ts
@Module({
  imports: [CatsModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
```

## Middleware 中间件

Nest 中间件等价于 express 中间件

* 对请求和响应对象进行更改。
* 调用堆栈中的下一个中间件函数。
* 如果当前的中间件函数没有结束请求-响应周期, 它必须调用 next() 将控制传递给下一个中间件函数。否则, 请求将被挂起。

```ts
// app.module.ts
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer.apply(LoggerMiddleware)
    .exclude(
      { path: 'cats', method: RequestMethod.GET },
      'cats/(.*)',
    )
    .forRoutes(CatsController);
  }
}
```

forRoutes() 可接受一个字符串、多个字符串、对象、一个控制器类甚至多个控制器类(逗号分隔)。

```ts
// main.ts
app.use(logger); // 绑定到每个注册路由
```

## Exception filters 异常过滤器

```ts
import { ForbiddenException } from '@nestjs/common';

@Get()
async findAll() {
  throw new ForbiddenException(); // 内置异常
  throw new HttpException('Forbidden', HttpStatus.FORBIDDEN); // 基础异常类
  throw new HttpException({
    status: HttpStatus.FORBIDDEN,  // 403
    error: 'This is a custom message',
  }, HttpStatus.FORBIDDEN);
}
```
绑定过滤器
```ts
@UseFilters(new HttpExceptionFilter())  // 实例
@UseFilters(HttpExceptionFilter) // 类
```
> 尽可能使用类而不是实例。由于 Nest 可以轻松地在整个模块中重复使用同一类的实例，因此可以减少内存使用。

```ts
// main.ts
app.useGlobalFilters(new HttpExceptionFilter()); // 全局范围的过滤器
```

## Pipes 管道

管道有两个类型:

* 转换：管道将输入数据转换为所需的数据输出
* 验证：对输入数据进行验证，如果验证成功继续传递; 验证失败则抛出异常;

Nest 自带八个开箱即用的管道:

* ValidationPipe
* ParseIntPipe
* ParseBoolPipe
* ParseArrayPipe
* ParseUUIDPipe
* DefaultValuePipe
* ParseEnumPipe
* ParseFloatPipe

```ts
@Post()
@UsePipes(ValidationPipe)
async create(@Body() createCatDto: CreateCatDto) {
  this.catsService.create(createCatDto);
}
```

## Guards 守卫

守卫的责任：授权 -- 根据运行时出现的某些条件（例如权限，角色，访问控制列表等）来确定给定的请求是否由路由处理程序处理。

在 Express 中通常由中间件处理授权、验证身份。中间件不知道调用 next() 函数后会执行哪个处理程序。然而守卫可以访问 ExecutionContext 实例，因此确切地知道接下来要执行什么。

> 守卫在每个中间件之后执行，但在任何拦截器或管道之前执行。

每个守卫必须实现一个canActivate()函数。此函数应该返回一个布尔值，指示是否允许当前请求。

```ts
@Controller('cats')
@UseGuards(RolesGuard)
export class CatsController {
  @Post()
  @Roles('admin')
  create(@Body() createCatDto: CreateCatDto) {
    this.catsService.create(createCatDto);
  }
}
```
Nest提供了通过 @SetMetadata() 装饰器将定制元数据附加到路由处理程序的能力。
```ts
@SetMetadata('roles', ['admin'])
```

## Task Scheduling 定时任务

* 计时工作(cron job)

```ts
@Cron('45 * * * * *') // 该方法每分钟执行一次，在第 45 秒执行。
handleCron() {
  this.logger.debug('Called when the current second is 45');
}
```

```bash
* * * * * *
| | | | | |
| | | | | day of week
| | | | month
| | | day of month
| | hour
| minute
second (optional)
```

stop()-停止一个按调度运行的任务

start()-重启一个停止的任务

setTime(time:CronTime)-停止一个任务，为它设置一个新的时间，然后再启动它

lastDate()-返回一个表示工作最后执行日期的字符串

```ts
const job = this.schedulerRegistry.getCronJob('notifications');

job.stop();
console.log(job.lastDate());
```

* 间隔（Interval）
```ts
@Interval(10000)
handleInterval() {
  this.logger.debug('Called every 10 seconds');
}
```

* 延时任务（Timeout）
```ts
@Timeout(5000)
handleTimeout() {
  this.logger.debug('Called once after 5 seconds');
}
```

## Test 测试

Nest 提供Jest和SuperTest开箱即用的集成。

https://github.com/yogagii/bst_data

__Unit test__:

* xxx.controller.spec.ts: 模拟service的方法，测试controller是否调用service方法
* xxx.service.spec.ts: 模拟Repository方法，不连接数据库，mock假数据，验证业务逻辑

__e2e测试__:

* app.e2e-spec.ts: 模拟app module，连接测试数据库，验证各路由

踩坑：需在beforeAll中createTestingModule，beforeEach中import AppModule会导致数据库重复连接（AlreadyHasActiveConnectionError）

## Event 监听事件

使用 try catch 无法处理异步代码块内出现的异常

```js
// 异常捕获成功
try {
  throw new Error('error');
} catch(e) {
  console.log('异常捕获');
}

// 异常捕获失败
try {
  setTimeout(() => {
    throw new Error('error');
  })
} catch(e) {
  console.log('异常捕获');
}
```

使用event方式来处理异常

```bash
npm i --save @nestjs/event-emitter
```

事件监听
```ts
import { Injectable } from '@nestjs/common';
import { OnEvent } from '@nestjs/event-emitter';

@Injectable()
export class UpdateStatusListener {
  constructor(private readonly mdmService: MdmService) {}

  @OnEvent('updateStatus.sendFormFailed')
  handleOrderCreatedEvent(event) {
    console.log('sendFormFailed: ', event);
  }
}
```

```ts
@Module({
  providers: [UpdateStatusListener],
})
```

事件触发
```ts
import { EventEmitter2 } from '@nestjs/event-emitter';
@Injectable()
export class EmailService {
  constructor(
    private eventEmitter: EventEmitter2,
  ) {}

  async sendEmailCode() {
    try {
      await this.mailerService.sendMail(sendMailOptions);
    } catch (error) {
      this.eventEmitter.emit('updateStatus.sendFormFailed', {
        event_id: courseData.event_id,
      });
    }
  }
}
```