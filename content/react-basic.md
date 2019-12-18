Title: React 基础
Date: 2019-07-06
Category: React
Tags: React
Author: Yoga

> 使用React只有两个步骤：一是创建虚拟DOM（多层嵌套），二是渲染到浏览器中。我们要做的就是逐级创建出所需要的虚拟DOM树并响应用户的动作来改变虚拟DOM树的组成。


### 1. react.js

---
react.js实现React核心的逻辑，与具体的渲染引擎无关，逐级创建虚拟DOM树

* **React.createElement**

  _参数一是html标签或ReactClass对象，参数二是属性，参数三以后是子元素_

```javascript
var parent = React.createElement(‘ul’, {className:’myClass’}, child1, child2);
```


* **React.DOM**是预先定义好的HTML元素集，相当于预置了第一个参数

  React.createElement(‘ul’) 等价于 React.DOM.ul() 工厂类方法

* **React.createFactory**

  HTML标签的工厂类已经预置，但对于自定义组件而言，首先需要创建一个工厂类

```javascript
var divFactory = React.createFactory(‘div’);
```

* **React.createClass**

  对于自定义的组件类型名，首字母大写且需要预先注册，React通过组件类型名的首字母是否大写来判断是否自定义组件

```javascript
var HelloComponent = React.createClass({
  // render是createClass中唯一必须实现的方法
  render: function() {
    return <h1> Hello world</h1>
  }
});
```
* **React.cloneElement** 
  
  克隆并返回新组件，属性值为原组件与props参数合并

* **React.Children** 

  React.Children.map( ) 每一个实例都调用fn函数

  React.Children.forEach( ) 类似map但是不返回对象

  React.Children.count( ) 返回children中包含的组件总数

  React.Children.only( ) 返回children中仅有的子组件，如果子组件不存在或不唯一则抛出异常

  React.Children.toArray( ) 返回由各子元素组成的数组

### 2. react-dom.js
---

react-dom.js包含了具体的DOM渲染相关逻辑，与浏览器相关，把虚拟DOM树渲染到实际的浏览器DOM节点上。

```javascript
// 将组件挂接到浏览器DOM中
ReactDom.render(HelloComponent, document.getElementById(‘app’));

//获得真实DOM元素
ReactDom.findDOMNode(this.refs.input)
```

