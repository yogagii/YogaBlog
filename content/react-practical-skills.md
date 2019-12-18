Title: React 实用技巧
Date: 2019-08-03
Category: React
Tags: React, Ref, AJAX, className.js, Immutable.js
Author: Yoga

### 绑定未提供的事件
___

在componentDidMount中获取对应的真实DOM元素绑定事件
```javascript
componentDidMount: function() {
  window.addEventListener('resize',this.onWindowResize);
}
componentWillUnmount: function() {
  window.removeEventListener('resize', this.onWindowResize);
}
```

<br>

### AJAX加载数据
___

最好在componentDidMount函数中加载数据，加载成功后调用setState来触发渲染更新界面

当请求到达之前可能已更换页面或移除组件，此时setState会报错：setState on an unmounted component

1.通过this.isMounted()来检测组件的状态是否已经mounted（ES6已废除）

```javascript
componentDidMount: function() {
  //AJAX
  $.get(this.props.source, function(result) { 
    if (this.isMounted()) {
      this.setState({});
    }
  }.bind(this));
}
```
2.在组件卸载之前取消未完成的请求

```javascript
componentDidMount: function() {
  this.serverRequest = $.get(...);
}
componentWillUnmount: function() {
  this.serverRequest.abort();
}
```

<br>

### ref属性
___

ref字符串

```javascript
<input ref="theInput" />
//获得真实DOM
this.refs.theInput.getDOMNode().focus();
```
ref回调函数(回调函数会在组件被挂载后立刻执行)

```javascript
<input ref={(compInstance) => this.theInput = compInstance}>
this.theInput.focus();
```
> 对于stateless function来说，引用不会被加载，因为无状态组件被没有对应的实例

<br>

### className.js
___

根据isBgRed状态切换不同class项的效果

```javascript
if (isBgRed) {
  classString = 'bg-red';
} else {
  classString = 'bg-green';
}
```

className工具

```javascript
import classNames from 'classnames';
classSting = classNames({ 'bg-red': isBgRed, 'bg-green': !isBgRed });

classNames('foo', 'boo'); //"foo boo"
classNames({ 'foo': true }); //"foo"
classNames({ foo: true }, { boo: true }); //"foo boo"
classNames({ foo: true, boo: true }); //"foo boo"
let buttonType = 'primary';
classNames({ [`btn-${buttonType}`]: true }); //ES6

//多类名去重
var classNames = require('classnames/dedupe');
```

<br>

### Immutable.js
___


**持久化数据结构**：对Immutable数据对象的任何修改、添加、删除操作都会返回一个新的Immutable对象，同时原对象不变。

**结构共享**：如果对象树中只有一个节点发生了变化，则只修改受到影响的父节点对它的引用，其他节点与原对象共享，避免深拷贝。

```javascript
import Immutable from 'immutable';
var imtArray = Immutable.fromJS([1, { 2, 3 }]);
var imtList = Immutable.List([1, 2]);
var imtMap = Immutable.Map({ a: 1 });
```


