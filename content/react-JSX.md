Title: JSX
Date: 2019-07-06
Category: React
Tags: React, JSX
Author: Yoga

JSX语法转义器会识别嵌入JavaScript代码中的HTML标签，当遇到‘<’标识符就会启动JSX转移过程，遇到‘{’标识符就会当作JavaScript代码进行处理。

引用Babel中负责JSX转义的模块browser.js，并将使用JSX语法描述的js文件类型声明为text/babel

###  1.	三元表达式

```javascript
{this.props.name?this.props.name:’World’}
{this.props.name||’World’}
```

### 2.	注释

{/* 当注释作为独立子节点时需要用大括号包裹起来 */}

### 3.	展开属性
```javascript
component.props.foo = x;  //wrong
```
> 初始化props后，props是不可变的，在整个组件的生命周期中都是只读的

```javascript
var extendProps = {};
extendProps.foo = x;
var component = <Component {…extendProps} />
```

### 4.	自定义HTML属性

在HTML中使用自定义属性，需要给属性名加上data-或aria-前缀
```html
<div data-dd=’xxx’ aria-dd=’xxx’>content</div>
```

