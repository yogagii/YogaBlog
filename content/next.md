Title: Next.js
Date: 2022-08-31
Category: React
Tags: Next
Author: Yoga

## nextjs12.x 集成 less

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

## 注册全局变量

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

## window

踩坑：window is not defined

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

## Layout & Route

在 Next.js 中，一个 page 就是一个从 .js、jsx、.ts 或 .tsx 文件导出的 React 组件 ，这些文件存放在 pages 目录下。每个 page 都使用其文件名作为路由。

```ts
// _app.tsx
import type { AppProps } from "next/app";
import Layout from "@/components/Layout";
import "../config";

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <Layout>
      <Component {...pageProps} />
    </Layout>
  );
}

export default MyApp;
```

```ts
// components/Layout/index.tsx
import Head from "next/head";
import "antd/dist/antd.css";
import Menu from "@/components/Menu";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <Head>
        <title>Carto Dashboard</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Menu />
      <div>{children}</div>
    </>
  );
}
```

```ts
// components/Menu/index.tsx
const routeMap = {
  chart: "/",
  operation: "/operation",
};

const SideMenu = () => {
  const onClick = (e: any) => {
    Router.push(routeMap[e.key as keyof typeof routeMap]);
  };

  const items = [
    { key: "chart", icon: <AreaChartOutlined /> },
    { key: "operation", icon: <ExceptionOutlined /> },
  ];

  return (
    <Menu
      onClick={onClick}
      style={{ width: 60 }}
      items={items}
    />
  );
};

export default SideMenu;
```