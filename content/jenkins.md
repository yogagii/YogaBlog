Title: Jenkins部署
Date: 2020-04-30
Category: Programming
Tags: Jenkins, AWS
Author: Yoga

Repository URL: https://sourcecode.jnj.com/scm/asx-nbbg/fpa_mobile.git

Branch Specifier: */develop

Build Triggers: 轮询 SCM

Build: 执行shell
```
npm i
npm install aws-sdk &
export NODE_OPTIONS=--max_old_space_size=4096
npm run build-dev
aws s3 rm s3://jnj-fpa-dev/mobileFrontend/m --recursive --only-show-errors
aws s3 cp dist s3://jnj-fpa-dev/mobileFrontend/m --recursive --sse --only-show-errors
```

Umi配置:

```javascript
export default {
  define: {
    'process.env.backendUrl': 'https://api.fpa.jnj.com',
  },
  base: '/m/index.html#/',
  publicPath: '/m/',
};
```
![UMI](img/umi1.png)