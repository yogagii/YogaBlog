Title: React组件
Date: 2019-07-06
Category: React
Tags: React, component
Author: Yoga

## React组件
> props属性集合：保存组件的初始属性数据（大部分原始数据）；
state状态集合：保存组件的状态数据（用户输入、服务器请求、时间变化）；
render函数：主要职责是根据state状态，结合props属性，进行虚拟DOM的构建；render函数内不应该修改组件state，不读写DOM信息，不与浏览器交互（setTimeOut）
setState(data, callback)成员函数：页面所有的变化均由状态的变更引发，状态的变更通过调用组件实例的setState函数完成，这个函数合并data到this.state并重新渲染组件，渲染完成后，调用可选的callback回调。
this.props.children数组中会包含本组件实例的所有组件，由React自动填充
this.props.context跨级包含上级组件的数据
props与state的区别：props不能被其所在的组件修改，从父组件传进来的属性不会在组件内部更改；state只能在所在组件内部更改，或在外部调用setState函数对状态进行间接修改。



### 1. react.js