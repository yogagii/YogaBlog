Title: React 复合组件
Date: 2019-07-13
Category: React
Tags: React, Component
Author: Yoga

> 组件的原则：职责单一，外在体现可复用性，内在体现分装性

## 组件嵌套
___

法一：在父组件的render函数中直接渲染子组件

法二：对于动态的、数量不固定的子组件需要用到this.props.children

<br>

## 组件参数传递
___

* **动态参数传递**：展开属性（参数名称是变量）

```javascript
  return <Component {...this.props} moreAttr=“value” />
  // 后面的参数会覆盖this.props中的moreAttr
```

* **Underscore**：提供_.omit()来过滤属性

```javascript
// 剩余属性：除checked之外的属性
var {checked, ...other} = this.props;
// 过滤属性
var other = _.omit(this.props, ’checked’); 
```

* **Context特性**：能实现组件树上的数据越级传递

	组件树中上层组件的任意层级的下级组件都能获得上层组件的数据

```javascript
  var Button = React.creatClass({
      // 下级组件必须指定context的数据类型
      contextTypes:{ 
        color: React.PropTypes.string
      }
      render: function( ) {
        return (
          <button style={{background: this.context.color]} ></button>
        );
      }
  })

  var Message = ... <Button>

  var MessageList = React.createClass({
      // 上级组件必须要声明属性
      childContextTypes: {
        color: React.PropTypes.string
      }
      // 上级组件必须声明回调函数
      getChildContext: funtion( ) {
        return {color: ‘purple’};		
      }
  });
```

<br>

## 组件间通信
___

### 子组件向父组件传递信息：

1.**事件回调机制**：父级组件在props中增加一个回调函数，子级组件在恰当时机调用回调函数通知父组件

```javascript
var Parent = React.createClass({
  render: function( ) {
    return (
      <Child onClick={this.onChildClicked} />
    );	
  }
});
var Child = React.createClass({
  handleClick: function( ) {
    this.props.onClick( );
  },
  render: function( ) {
    return (
      <button onClick={this.handleClick} />
    );
  }
});
```

2.**公开组件功能**：子组件对外提供公开方法，公开的方法被调用后返回相应的数据，父组件通过ref属性获得子组件实例的引用

```javascript
var Child = react.creatClass({
  animate: function(){
    // 本组件公开的方法
  }
});
var Parent = react.creatClass({
  handleClick: function() {
    this.refs.items0.animate();
  }
  render: function() {
    return (
      <Child.onClick={this.handleClick.bind(this, i)} ref={‘item’+i} />
    )
  }
});
```
### 没有隶属关系的组件间通信：
	
  在componentDidMount()里订阅事件
	
  在componentWillUnmount()里退订

### mixins

  mixins：复用代码（输出日志，定时器更新界面），混入组件，使其能为多个组件所用

```javascript
// 定时器需创建（ComponentWillMount）和销毁（ComponentWillUmount）
var SetIntervalMixin = {
  componentWillMount: function() {
    this.intervals = [];
  },
  setInterval: function() {
    this.intervals.push(setInterval.apply(null,arguments));
  },
  componentWillUnmount() {
    this.intervals.map(clearInterval);
  }
};
var TickTock = React.creatClass({
  mixins: [SetIntervalMixin],
});
```

> 若重复定义了 componentWillMount, 多个 mixins按声明顺序依次执行componentWillMount，最后执行组件本身。

<br>

## 高阶组件
___

高阶组件：对现有组件的动态包装（redux: connect）

```javascript
function hoc(Comp) {
  return class NewComponent extends Component{
    extendFunc() {} //新增功能
    render() {
      return (
        <Comp {this.props} />
      );
    }
  }
}
const NewComponent = hoc(Comp);
```
将数据展现封装为一个组件，再通过高阶组件附加数据请求。
	