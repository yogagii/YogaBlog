Title: Flux
Date: 2019-08-24
Category: Data
Tags: Flux
Author: Yoga

Facebook提出Flux应用架构解决数据模型处理，Flux是一种思想，跟React本身没有必然联系，基于Flux思想的框架有Redux、Reflux、Flummox等产品。

## 单向数据流：

界面总是基于内部数据模型的一种呈现，但是用于在界面的输入也会回输到内部数据模型上，这是一种数据的双向流动，双向传递流动很难把握，在复杂情况下，有些操作会触发一连串的变化，有些变化还可能是异步的。

为此，Flux引入了单向数据流的思想，当需要插入新的数据或改变原有数据时，数据流完全重新开始。

![Flux](img/flux.png)

Flux中Store的变化由事件Action激发，经由动作分发器Dispatcher派发到存储Store(数据模型)中，并引起Store中数据发生变更，从而影响视图的变化。

![Flux](img/flux2.png)

Action是一个Javascript Plain Object,主要记录对State的操作信息，包含两方面内容：类型(type)和载荷(payload)，type属性是预先定义好的常量标识符，代表特定的action，载荷用于传递具体的数据，action的接收者负责解读和处理这个数据。

```
{
  type: 'ADD_STUDENT',
  name: 'Yoga',
}
```

Dispatcher分发器是Flux应用中的调度枢纽，主要职责是把action分发给Store。Dispatcher维护着一个庞大的需要接受Action的Store回调函数列表，并接受注册。Dispatcher把Action传递给所有登记在册的Store，类似于广播，不是订阅某些Action，而是监听所有Action。

每个Store都会预先在Dispatcher中注册Action响应回调函数，回调函数接受Action作为参数，根据Action type识别Action并调用对应的处理函数。Store中包含应用所有的数据，Store是应用中唯一数据发生变更的地方。

整个view是一个树形嵌套结构，这个嵌套结构的根部是一个特殊的view，成为控制视图Controller View(根组件)，控制视图兼具控制功能，它一方面负责接收Store的广播事件，另一方面也从Store中获取数据（调用其getter函数）。
