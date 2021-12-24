Title: Mocha
Date: 2020-08-24
Category: Backend
Tags: Unit test
Author: Yoga

### 单元测试 Unit Testing

单元测试是检测一小段代码的良好实践，典型的单元测试是测试独立的function，要保证这个测试是单独孤立的。如果你写的测试用了外部的资源，比如网络或者数据库，它就不是一个单元测试。

### 集成测试 Integration Testing

集成测试想要测试的是这个系统的各个部分在一起合作的如何－将各个代码块集成在一起。当你需要验证两个不同的系统是否在一起正常的通信和正常运转，比如你的应用程序和数据库是否集成正确，运转正常，这个时候就需要集成测试了。结果是，当验证集成测试结果时，你通过写数据库连接语句检查数据库状态是否正常而顺便做了数据库连接测试。

https://blog.csdn.net/aajx90520/article/details/101658973

sails-disk still is a database: so it's prone to "corruption from outside" during the course of tests. On top of that this makes testing actually slow. It's not really a unit test if the entire app has to be started first, with sails lift. Unit tests should not spin up server or hit databases


lifecycle.test.js

```js
const MockAdaper = require();

before(function(done) {
  this.timeout(50000) // 设置超时时间

  if (err) {
    return done(err) // 服务启动失败
  }

  global.httpMock = new MockAdaper(axios); // 模拟获取数据

  // 创建模拟用户
  const user1 = {
    userId = 'user1'
  }
  await User.create(user1);
  // ORM自带功能：模拟数据库，内存里的数据库
  // new Sequelize('sqlite::memory')
}

after(){
  sails.lower(done) //停止服务
}
```

不带 raylight 99999

带 raylight 返回包括 keyworkds，但限制 50 条

覆盖率
```
"scripts": {
  "test": "npm run custom-tests && echo 'Done.'",
  "cov": "nyc mocha test/lifecycle.test.js test/**/*.test.js",
  "custom-tests": "mocha test/lifecycle.test.js test/**/*.test.js"
}
```

autocomplete.test.js
```js
const supertest = require('supertest')

describe('search.autocomplete', () => {
  describe('#autocomplete()', () => {
    it('responds with json', (done) => {
      supertest(sails.hooks.http.app)
        .get('/search/autocomplete?deviceMobile=false&q=detail')
        .set('Cookie', [authedUserCookie])
        .expect('Content-Type', /json/)
        .expect(200)
        .expect(({ body }) => {
          if (!body.sap || !body.workbooks || !body.trainings) {
            throw new Error('format error.')
          }
        })
        .end(done)
    })
  })
})
```
## sinon
```js
const supertest = require('supertest');
const sinon = require('sinon');

describe('external-resource.list', () => {
  before(async () => {
    await ExternalResource.create({
      user: global.user.id,
      title: 'resource1',
      link: 'https://www.baidu.com',
      attachment: {
        url: 'sitePublicFiles/public/jsonconfig/6faf8565-ceb9-4cd8-a3c7-6f4bcf465aa4/u%3D3720661285%2C1522818110%26fm%3D26%26gp%3D0.jpg',
        moved: true,
        filename: 'u=3720661285,1522818110&fm=26&gp=0.jpg',
      },
      description: 'description',
      role: ['COE'],
      position: ['PVP'],
      region: ['AP'],
      sector: ['CONS'],
    });
  });

  describe('#list()', () => {
    it('responds with json', (done) => {
      sinon.stub(sails.helpers, 'arrayContains').returns(true);
      supertest(sails.hooks.http.app)
        .get('/external-resource/list')
        .set('Cookie', [authedUserCookie])
        .expect('Content-Type', /json/)
        .expect(200)
        .expect(({ body }) => {
          if (!body.list || !body.pagination) {
            throw new Error('format error.');
          }
          if (body.list.find((item) => !item.tags)) {
            throw new Error('return data without tags');
          }
          if (!body.list[0].tags.region || !body.list[0].tags.sector) {
            throw new Error('missing tags');
          }
        })
        .end(done);
    });
  });
});
```