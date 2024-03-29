Title: Redux
Date: 2019-08-24
Category: Frontend
Tags: Redux
Author: Yoga

Redux与其他的Flux实现相比更简单，一个Redux应用中Store是唯一的，这样的限定能够使应用中的数据结果集中化，提高了可控性，同时又通过引入Reducer机制巧妙地解决单一Store的限制问题，达到了与使用多个Store同样的效果。

Redux主要由Action、Reducer及Store三部分组成。Action用来表达操作，Reducer根据Action更新state。

Redux vs Flux:

* Redux中只有一个全局Store，Flux里则可以有多个Store。Flux在Store里执行更新逻辑，当Store变化的时候通知Controller view。而Redux将各个Store整合成一个完整的Store，更新逻辑由Reducer处理。

* Redux中可以有多个Reducer，每个Reducer维护整体State中的一部分，多个Reducer合并成一个根Reducer，由其负责维护完整的State，当一个Action被发出，Store会调用Dispatch方法向某个特定的Reducer传递该Action，Reducer接收到Action之后执行更新逻辑，并返回一个新的state，根Reducer收集所有State的更新，再返回一个新的完整的State，然后传递给view。


```js
// get state in effect
const status = yield select(state => state.user.saveLogin.status);

let siteConfig = yield select(state => state.sortConfig);
if (!siteConfig.data.report_type) {
  yield put.resolve({ type: 'sortConfig/request' });
  siteConfig = yield select(state => state.sortConfig);
}
```