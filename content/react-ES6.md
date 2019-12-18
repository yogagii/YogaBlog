Title: React in ES6
Date: 2019-08-17
Category: React
Tags: React, ES6
Author: Yoga

### 导出

```javascript
React.DOM.a({
  onClick:this._download.bind(this, 'CSV'),
  href: 'data.csv'
}, 'Export CSV');
```

### 展开运算符

```javascript
var attr = {
  href: 'http://example.org',
  target: '_blank',
};
return <a {...attr}>Hello</a> //忽略不存在在a中的属性
```

### 浅拷贝

```
var attribs = object.assign({}, this.props);
```

### 模块化
 引入 import React from 'react'

 导出 export default Logo

 类 class Logo extends React.Component{}

### 构建

* 转译JS: $babel --presents react,es2015 js\source -d js\build

  Babel转移JSX, 也支持转移最新Js (Bible中负责JSX转译的模块browserify.js)

  使用JSX语法的JS文件：type="text/babel"，变量需要花括号，循环体也需要花括号

* 打包JS: $browserify js\build\app.js -o bundle.js

* 拼合CSS: type css\components\*.css\* >bundle.css 

scripts/build.sh

watch "sh script/build.sh" js/source css 监听改变自动运行构建