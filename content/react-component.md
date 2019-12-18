Title: React 组件
Date: 2019-07-06
Category: React
Tags: React, Component
Author: Yoga

## 组件的属性
___


1. **props属性集合：** 保存组件的初始属性数据（大部分原始数据）；
<br> this.props.children数组中会包含本组件实例的所有组件，由React自动填充
<br> this.props.context跨级包含上级组件的数据

2. **state状态集合：** 保存组件的状态数据（用户输入、服务器请求、时间变化）；

3. **render函数：** 主要职责是根据state状态，结合props属性，进行虚拟DOM的构建；render函数内不应该修改组件state，不读写DOM信息，不与浏览器交互（setTimeOut）

4. **setState(data, callback)成员函数：** 页面所有的变化均由状态的变更引发，状态的变更通过调用组件实例的setState函数完成，这个函数合并data到this.state并重新渲染组件，渲染完成后，调用可选的callback回调。


> props与state的区别：props不能被其所在的组件修改，从父组件传进来的属性不会在组件内部更改；state只能在所在组件内部更改，或在外部调用setState函数对状态进行间接修改。

<br>

## 组件的生命周期
___

### 实例化阶段

1.**getDefaultProps**

设置props的默认值，仅调用一次，属性如果没有通过父组件传入的话，返回对象中的相应的属性将合并到this.props·
```javascript
getDefaultProps: function(){
    return {dname:’’};
}
```

2.**getInitialState**

初始化state，仅调用一次，返回的对象会自动合并到this.state上

3.**componentWillMount**

渲染前，仅调用一次，在这个方法内调用setState，render将感知到更新后的state

4.**render**

只能读取props和state，不能更改，只能返回一个ReactElement元素或null或false

5.**componentDidMount**

渲染后，可通过this.getDOMNode获得对应的浏览器DOM元素，可在这个方法里对DOM做进一步修改、进行state数据填充（ajax请求）、继承其他框架（jQuery）。

### 活动阶段
1.**componentWillReceiveProps**

初始化时不调用，是在props传入后渲染之前更新state的最佳时机，旧的props可以通过this.props获取到

```javascript
componentWillReceiveProps: function(nextProps) {
    this.setState({increasing: nextProps.count > this.props.count});
}
```

2.**shouldComponentUpdate**

默认返回true，若确定新的props和state不会更新组件，手动控制组件不更新，返回false，接下来的willUpdate/render/ DidUpdate不执行。

3.**componentWillUpdate**
	
初始化时不调用，不能在该方法中使用setState

4.**render**

5.**componentDidUpdate**
	
初始化时不调用

### 销毁阶段
1.**componentWillUnmount**

在该方法中执行必要的清理（无效的定时器、componentDidMount中创建的DOM元素）

<br>

## 组件事件响应
___

* **事件代理**：React在顶层使用一个全局的事件监听器监听所有事件，在内部维护一个映射表记录事件与组件事件处理函数的对应关系，当某个事件发生时，React根据这个内部映射表将事件分派给指定的事件处理函数。

* **事件自动绑定**：每个事件处理回调函数会自动绑定到组件实例，回调函数中this所指的是组件实例而不是DOM元素。

React支持的事件：

事件类型 | 事件名称
- | -
剪贴板事件 | onCopy / onCut / onPaste 
键盘事件 | onKeyDown / onKeyPress / onKeyUp
焦点事件 | onFocus / onBlur
表单事件 | onChange / onInput / onSubmit
鼠标事件 | onClick / onContextMenu / onDoubleClick / onDrag / onDragEnd / <br> onDragEnter / onDragExit / onDragLeave / onDragOver / <br> onDragStart / onDrop / onMouseDown / onMouseEnter /  <br>  onMouseLeave
触控事件 | onTouchCancel / onTouchEnd / onTouchMove / onTouchStart
用户界面事件 | onScroll
滚轮事件 | onWheel


<br>

## props属性验证
___
React.PropTypes提供各种验证器来验证传入数据的有效性，为了性能考虑只在开发环境下验证。

* 基本类型：React.PropTypes.array / bool / func / number / object / string / node / element

* 指定类型之一：instanceOf(Message) / oneOf([‘News’, ‘Photos‘]) / oneOfType([React.ProtoTypes.string])

* 特定类型的对象：arrayOf(React.PropTypes.number) / objectOf(React.ProtoTypes.number)

* 不可空：React.Prototypes.func.isRequired / React.ProtoTypes.any.isRequired

<br>

## 其他成员
___

```javascript 
var App = React.createClass({​
   //用来定义静态方法，可以在组件类上调用:App.staticMethod()
  statics:{
    staticMethod:function(){}
   }
  //组件调试时显示的组件名
  displayName : ‘APP’,
  //定义在多个组件之间共享的函数代码
  mixins:[]
  render: function(){return <h1>app</h1>}
});
```

<br>

## 设计原则

___

组件应该尽可能的无状态化，只有对用户输入、服务器请求、时间变化等需要作出响应并暂存中间状态时才需要使用state

一个有状态组件(stateful)：封装所有用户的交互逻辑

-> 通过props把状态传给子级 ->

多个无状态组件(stateless)：只负责声明式地渲染数据

> 应放在state中的数据：可能被组件的事件处理器改变并触发用户界面更新的数据。当创建一个状态化的组件时，想象一下表示它的状态最少需要哪些数据，并只把这些数据存入this.state。<br>
不应放在state中的数据:计算所得数据（length）、React组件、基于props的重复数据（在渲染时需要知道它以前的props值时可以把props保存到state）