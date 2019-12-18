Title: React 特点
Date: 2019-07-06
Category: React
Tags: React, Virtual Dom, Flux
Author: Yoga


### 1. 虚拟Dom

---

浏览器DOM是由HtmlElement元素组成的树，虚拟DOM是有ReactNode节点元素组成的树。每次数据变化React都会扫描整个DOM树，自动计算与上次虚拟DOM的差异变化，然后针对需要变化的部分进行实际的浏览器DOM更新，从而提高性能。

_在文本框中输入任意文本，在禁止文本框，可以发现文本框中原来输入的文本并没有消失，说明React并没有重新渲染input，只是更改了input属性值，这正是react差异对比、局部刷新的特性体现。_

> 虚拟DOM->真实DOM: react-dom <br> 虚拟DOM->移动APP: react-native

将一棵树形结构转换成另一棵树形结构传统最优算法的复杂度是O(n3)。

试探法：通过给子级组件设定唯一的键值，React就能够检测出节点插入、移除和替换，并且借助哈希表使节点移动复杂度变为O(n)。键值只需要在兄弟节点中唯一即可，而不需要是全局唯一的。

虚拟DOM的特殊属性：

* key：可选的唯一标识符。
* ref：用于访问组件对应的实际DOM元素。
* dangerouslySetInnerHTML: 用来直接插入纯HTML文本字符串，避免React的自动转义。

```html
var content = ‘<span>文本内容</span>’;
<div dangerouslySetInnerHTML={{_html: content}}></div>
```

### 2. 组件化
---

从功能角度划分，将UI分解成不同组件，各组件都独立封装，每个组件只关心自身的逻辑。

### 3. 单向数据流
---

单项的数据流动：从父节点到子节点

组件只需要从父节点获取prop渲染即可，如果顶层组件的某个prop改变了，React会递归地向下遍历整棵组件树并重新渲染所有使用这个属性的组件。单项数据流的架构模式Flux，以M层Store为核心，围绕Store设计Action和Dispatcher。

