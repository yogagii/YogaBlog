Title: Express
Date: 2019-04-01
Category: Frontend
Tags: Express
Author: Riz

```ts
import * as express from 'express';
```

```js
# .babel es6 => es5 X 
# default => import 
import express from 'express';
```

```jsx
const Com = () => {
    return (<div></div>)
} 

export default Com;
```

正常用Js
```
import Com from './Com'
import * as React from 'react'
default => X
```

但使用Ts拿不到，因为Ts的协议更加规范


```ts
import * as express from 'express';
import * as bodyParser from 'body-parser';
import * as request from 'request';

// dont modify this entry file
// when you need to add middleware, please add it to manager/middleware.ts

const app = express();

// Use body parser middleware to handle post body data
//app.use(bodyParser);

app.get('/', (req, res: express.Response) => {
  const id = req.query.id;
  // 
  request('http://www.baidu.com', (err, body, qRes) => {
    console.log(qRes);
    res.end(qRes);
  });
});

// slot for the shell to create
// req request content
// res response action
app.get('/req', (req, res) => {
  console.log(req);

  const retMsg = { value: 'hello world' };
  res.end(JSON.stringify(retMsg));
});

// start
app.listen(8811, () => {
  console.log('Open the server');
});

```


```json
{
  "name": "express-example",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "start": "ts-node-dev index",
    "prod": "ts-node index",
    "create": "ts-node ./bin/create",
    "test": ""
  },
  "author": "",
  "license": "ISC",
  "dependencies": {
    "@types/express": "^4.17.3",
    "@types/node": "^13.9.1",
    "body-parser": "^1.19.0",
    "chalk": "^3.0.0",
    "cookie-parser": "^1.4.4",
    "express": "^4.17.1",
    "moment": "^2.24.0",
    "multer": "^1.4.2",
    "request": "^2.88.2",
    "ts-node": "^8.6.2"
  },
  "devDependencies": {
    "eslint": "^5.4.0",
    "eslint-config-umi": "^1.4.0",
    "eslint-plugin-flowtype": "^2.50.0",
    "eslint-plugin-import": "^2.14.0",
    "eslint-plugin-jsx-a11y": "^5.1.1",
    "eslint-plugin-react": "^7.11.1",
    "nodemon": "^2.0.2",
    "prettier": "^1.19.1",
    "ts-node-dev": "^1.0.0-pre.44",
    "typescript": "^3.8.3"
  },
  "lint-staged": {
    "*.{js,jsx}": [
      "eslint --fix",
      "git add"
    ]
  }
}

```

Book: 深入PHP：面向对象、模式与实践