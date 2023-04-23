Title: SSO 登录
Date: 2023-04-18
Category: Backend
Tags: nest
Author: Yoga

```
+--------+                               +---------------+
|        |--(A)- Authorization Request ->|   Resource    |
|        |                               |     Owner     |
|        |<-(B)-- Authorization Grant ---|               |
|        |                               +---------------+
|        |
|        |                               +---------------+
|        |--(C)-- Authorization Grant -->| Authorization |
| Client |                               |     Server    |
|        |<-(D)----- Access Token -------|               |
|        |                               +---------------+
|        |
|        |                               +---------------+
|        |--(E)----- Access Token ------>|    Resource   |
|        |                               |     Server    |
|        |<-(F)--- Protected Resource ---|               |
+--------+                               +---------------+
```

### Step1 Get code

[GET] https://fedlogin.xxx.com/as/authorization.oauth2?client_id=xxx&response_type=code&scope=profile&redirect_uri=https://xxx.com/callback

Params:

* client_id: the client ID
* redirect_uri: any redirect URI that has been assigned to the oAuth clientID.
* scope: openid, profile, email. Separate scopes with a space.
* grant_type: 'authorization_code'
* response_type: 'code'


Response:

https://xxx.com/callback?code=XYZCODE4TKNABC

### Step2 Exchange code for token

[POST] https://fedlogin.xxx.com/as/token.oauth2

'Content-Type': 'application/x-www-form-urlencoded'

Body:

* grant_type=authorization_code
* client_id=xxx
* client_secret=xxxxxxx
* redirect_uri=https://xxx.com/callback
* code=(get from previous step)

Response:
* access_token: xxxxxxxxx
* refresh_token: xxx
* token_type: 'Bearer'
* expires_in: 7199

### Step3 Validate token

[POST] https://fedlogin.xxx.com/as/token.oauth2

'Content-Type': 'application/x-www-form-urlencoded'

Body:

* grant_type=urn:pingidentity.com:oauth2:grant_type:validate_bearer
* client_id=xxx
* client_secret=xxxxxxx
* token=(get from step2)
* scope=profile

Response:

* access_token: 
    * username: 邮箱前缀
    * mail: 邮箱
    * givenName: 名
    * cn: wwid
    * sn: 姓
    * title: 职位
* scope: profile
* token_type: 'urn:pingidentity.com:oauth2:validated_token'
* expires_in: 7141
* client_id: xxx

### Step4 Refresh token

[POST] https://fedlogin.xxx.com/as/token.oauth2

'Content-Type': 'application/x-www-form-urlencoded'

Body:

* grant_type=refresh_token
* client_id=xxx
* client_secret=xxxxxxx
* refresh_token=xxx

Response:

* access_token: xxxxxxxxx
* refresh_token: xxx
* token_type: 'Bearer'
* expires_in: 7199

## NestJS

* sso-auth.guard.ts
    * 检查是否是 public 接口，public直接返回 true
    * 检查 session 中是否有 token，若 token 不存在或已过期，返回拼接好的 redirect_uri (step1)
    * 验证 token 是否有效 (step3)
    * token 验证通过，用返回的用户信息中的邮箱去 User表 中查找是否为注册用户
    * 当用户为首次登录，将返回的用户信息更新到 User表
    * 将user_id存入session，给与用户挂钩的接口提供uuid
* app.controller.ts
    * callback 接口获取 code，用 code 换取 token (step2)
    * 将 token 存入session，并添加过期时间 expires_at
* refreshtoken.interceptor.ts
    * 接口请求时刷新 token, 更新 session 中的 expires_at (step4)

```ts
// sso-auth.guard.ts
import {
  Injectable,
  ExecutionContext,
  HttpException,
  HttpStatus,
} from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { IS_PUBLIC_KEY } from 'src/common/decorators/public.decorator';
import { queryString } from 'src/common/utils/common';
import { AuthService } from '../auth.service';

@Injectable()
export class SSOAuthGuard {
  constructor(
    private reflector: Reflector,
    private readonly authService: AuthService,
  ) {}

  async canActivate(context: ExecutionContext) {
    const isPublic = this.reflector.getAllAndOverride<boolean>(IS_PUBLIC_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);
    if (isPublic) {
      return true;
    }
    const request = context.switchToHttp().getRequest();
    const params = {
      client_id: process.env.CLIENT_ID,
      response_type: 'code',
      redirect_uri: process.env.REDIRECT_URI,
      scope: 'profile',
    };
    const token = request.session.token;

    if (!token || token.expires_at < new Date().getTime()) {
      throw new HttpException(
        {
          redirect: `https://fedlogin.xxx.com/as/authorization.oauth2${queryString(
            params,
          )}`,
        },
        HttpStatus.UNAUTHORIZED,
      );
    }
    const { access_token } = token;
    return await this.authService.checkToken(access_token).then((res) => {
      if (res && res.id) {
        request.session.user_id = res.id;
        return true;
      }
      return res;
    });
  }
}
```

## Session

```ts
res
  .setHeader('Set-Cookie', `access_token=${result.access_token}`)
  .status(302).
  redirect('/');
```
重定向到/导致cookie丢失，token不存在再次重定向到sso，死循环

将token存入后端session，正式环境需要用MemoryStore设置过期时间防止内存泄漏

```ts
app.use(
	session ({
		secret: process.env.SESSION_SECRET,
		resave: false,
		saveUninitialized: false,
    store: new MemoryStore({
      checkPeriod: 86400000, // prune expired entries every 24h
    }),
	})
);
```

## Refresh

session中token加入过期时间
```ts
// RefreshTokenInterceptor
if (
  token &&
  token.refresh_token &&
  token.expires_at - 3600000 < new Date().getTime()
) {
  await this.authService
    .refreshToken(token.refresh_token)
    .then((result) => {
      request.session.token = {
        ...result,
        expires_at: new Date().getTime() + result.expires_in * 1000,
      };
    });
}
return next.handle();
```
不加await设置request.session无效

加await会使所有接口速度变慢

加上时间限制，只有当token还有1小时过期时才refresh

后果：不能保证用户不操作2小时token才过期，若最后一次操作刚好在3600s，则1小时后就会过期

## 依赖注入

在依赖注入方面, 从任何模块外部main.js注册的全局拦截器 无法插入依赖项, 因为它们不属于任何模块。
需要从模块(app.module)中设置拦截器

区分环境 法一：
```ts
// app.module.ts
providers: [
  {
    provide: APP_INTERCEPTOR,
    useClass: RefreshTokenInterceptor,
  },
  {
    provide: APP_GUARD,
    useClass: process.env.NODE_ENV ? SSOAuthGuard : LocalAuthGuard,
  },
]
```

坏处：需要创建一个空的 LocalAuthGuard

LocalAuthGuard没有讲user_id存入session，需要在.env中添加一个测试账号
```ts
// user.controller.ts
const user_id = process.env.NODE_ENV
      ? session.user_id
      : process.env.TEST_USER_ID;
return this.userService.findOne(user_id);
```

区分环境 法二：
```ts
// main.ts
if (process.env.NODE_ENV) {
  app.useGlobalGuards(
    new SSOAuthGuard(new Reflector(), new AuthService(new HttpService())),
  );
}
```

坏处：需要传入实例，可能会嵌套很多层
