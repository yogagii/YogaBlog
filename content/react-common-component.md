Title: React 常用组件
Date: 2019-08-03
Category: React
Tags: React, Component
Author: Yoga

### 按钮组件

* 样式：允许使用者自行定义并作为属性传入，若不传需提供默认样式

* 事件：将自定义的事件处理函数作为属性传入，事件触发时该函数被调用

### 分页组件

* 数据：pageSize, pageNum, pages, offset, total, col_name, direction

* 事件：onFirst首页, onLast尾页 (-> disabled: true), onPrev上一页, OnNext下一页, onFresh刷新, onChange

### 树形组件

由于树形结构的级数可变，需要用递归的方式才能实现树形组件的定义

### Modal对话框

弹出Modal时在当前页面先覆盖一个遮罩层（z-index值超大），在之上显示Modal

关闭Modal：先卸载React组件 -- ReactDOM.unmountComponentAtNode(this._overlay),再删除div -- this._portalContainerNode.removeChild(this._overlay)
