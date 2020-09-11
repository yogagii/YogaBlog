Title: Mocha
Date: 2020-08-24
Category: Backend
Tags: Unit test
Author: Yoga

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
