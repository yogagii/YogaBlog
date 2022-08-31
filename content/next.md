Title: Next.js
Date: 2022-08-31
Category: React
Tags: Next
Author: Yoga

nextjs12.x 集成 less

1）安装依赖

```bash
npm install next-plugin-antd-less
npm install classnames
npm install less-loader
```

2）在next.config.js中加配置

```ts
const withAntdLess = require('next-plugin-antd-less');

const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
};

module.exports = withAntdLess(nextConfig);
```

3) 文件名 xx.module.less
```ts
// index.tsx
import styles from "./menu.module.less";
```