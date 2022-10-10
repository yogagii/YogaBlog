Title: Next.js
Date: 2022-08-31
Category: React
Tags: Next
Author: Yoga

### nextjs12.x 集成 less

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

### 注册全局变量

config.ts
```ts
const globalAny: any = global;

globalAny.Theme = {
  primaryColor: "#E88570",
  secondaryColor: "#BE46D8",
};

export {};
```

index.d.ts
```ts
declare module '*.js'
declare module '*.less'
declare module '*.jpg'
declare module '*.svg'
declare const Theme: {
  primaryColor: string;
  secondaryColor: string;
};
```

_app.tsx
```tsx
import type { AppProps } from "next/app";
import "../config";

function MyApp({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}

export default MyApp;
```

使用：Theme.primaryColor

### window

next.js是服务器渲染，运行在node上的，并不是浏览器上的；

所以使用生命周期componentDidMount，在页面渲染到浏览器后，才能找到window

```ts
const [isDeskTop, setDeskTop] = useState(true);

useEffect(() => {
  setDeskTop(!(window?.innerWidth <= 576));
}, []);
```

引入外部模块

```ts
const jsPDF = (await import('./jspdf.debug')).default;
var pdf = new jsPDF("", "pt", "a4");
```