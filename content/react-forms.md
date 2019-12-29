Title: React 表单
Date: 2019-07-13
Category: React
Tags: React, Form
Author: Yoga

## 事件响应

表单组件（包括所有HTML原生组件）可以通过设置onChange( )回调函数来监听组件变化

`<input> -> value / checked`

`<textarea> -> value`

`<option> -> selected`

**复用**：只写一个事件处理函数且能处理多个事件

1. bind复用

	事件响应函数通过bind的参数识别事件源

```javascript
  // bind方法为事件响应函数增加一个参数
  <input onChange={this.handleChange.bind(this, ‘checked’)} />
  hangdeChange = function(name, event) {
    newState[name] = name == ‘checked’ ? event.target.checked : event.target.value’
  }
```

2. name复用

	React中事件响应函数会自动绑定this

```javascript
	// 要求所有相关的标签都要统一设置name属性
	<input name=‘checked’ onChange={this.handleChange} />
	handleChange: function(event) {
		newState[event.target.name] = event.target.name == ‘checked’ ? event.target.checked : event.target.value;
	}
```

**功能受限的组件**：在input中设置value，元素始终保持value的值，即使用户输入也不会改变

**可控组件**：将input中的valve绑定到state

```html
<input value={this.state.value} />
```

**不可控组件**：

```javascript
var inputValue = React.findDOMNode(this,refs.input).value
```