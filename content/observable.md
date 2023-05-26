Title: Observable
Date: 2023-04-10
Category: Javascript
Author: Yoga

| Observable | Promise |
| - | - |
陈述式，直至subscription才会触发 | promise创建之后立即执行 |
支持多值甚至是数据流 | 只能提供单个值 |
能够在执行前或执行中被取消 dispose | 不可以取消 |
多次调用 retry 能够触发多次异步操作 | promise只可以被执行一次，重复调用，promise内部直接返回之前的状态 |
/ | 可使用async,await让多个promise进行同步 |
根据内部操作去判别使用异步还是同步 | promise一定是异步的 |
rxjs: subscribe(), map(), pipe() | then() |

* Observable 创建的异步任务，可以被处理，而且是延时加载的，封装了大量的方法供我们使用以处理复杂的异步任务。
* promise 解决嵌套地狱，解决大量的异步回调所造成的难以调试问题

## Observable 可观察对象

一个可观察对象(Observable)，观察者(Observer)订阅(Subscribe)它，当数据就绪时，之前定义的机制就会分发数据给一直处于等待状态的观察者哨兵。

_用户输入框查询:_

1. 防抖。繁触发搜索，一来浪费服务器资源，二来影响客户端的响应。
2. 防止触发两次。输入的文本没有变化，就不应该重新搜索。
3. 处理返回顺序。服务器的异步返回的顺序是无法保证的。

```ts
// WikipediaService
import { URLSearchParams, Jsonp } from '@angular/http';
import { fromEvent } from 'rxjs';

search (term: string) {
  var search = new URLSearchParams()
  search.set('action', 'opensearch');
  search.set('search', term);
  search.set('format', 'json');
  return this.jsonp             
 .get('http://en.wikipedia.org/w/api.php?callback=JSONP_CALLBACK', { search })              
 .map((response) => response.json()[1]); // 处理返回顺序：对于原先的Response类型的结果，转换成实际的搜索结果的列表，即利用Observable的特性去丢弃上一个未及时返回的结果
}

// AppComponent
var text = document.querySelector('#text');
var inputStream = fromEvent(text, 'keyup') // 为dom元素绑定'keyup'事件, 返回Observable<string>对象
  .debounceTime(400) // 防抖：触发延时是400毫秒
  .pluck('target', 'value') // 取值
  .distinctUntilChanged() // 输入不一致才会触发订阅
  .subscribe(term => this.wikipediaService.search(term)
  .then(items => this.items = items));  

```

## RxJS 响应式扩展 Reactive extensions

ReactiveX来自微软，它是一种针对异步数据流的编程。简单来说，它将一切数据，包括HTTP请求，DOM事件或者普通数据等包装成流的形式，然后用强大丰富的操作符对流进行处理

### 创建型 Operator：创建新 Observable 的独立函数

| 方法 | 作用
| - | -
of(…args) | 可以将普通数据转为可观察序列
fromPromise(promise) | 将Promise转化为Observable
fromEvent(elment, eventName) | 从DOM事件创建序列
ajax(url) | AjaxRequest
create(subscribe) | 一般用于只提供了回调函数的某些功能或者库

```ts
import { of,fromPromise,fromEvent,Observable } from 'rxjs'
import { ajax } from 'rxjs/ajax';

const source = of(1, 2, 3); // 依次发出提供的任意数量的值
const subscribe = source.subscribe(val => console.log(val));

const ob = Observable.fromPromise(somePromise); // Promise转为Observable
const promise = someObservable.toPromise(); // Observable转为Promise，已弃用

const el = document.getElementById('my-element')!;
const mouseMoves = fromEvent<MouseEvent>(el, 'click');

const apiData = ajax('/api/data'); // http

Observable.create((observer) => {})
```

### subscribe 订阅

用于激活可观察的并监听发射的值，ob作为Observable序列必须被“订阅”才能够触发操作

完整的包含下面3个函数的对象被称为observer（观察者），表示的是对序列结果的处理方式

* next: 表示数据正常流动，没有出现异常；
* error: 表示流中出错，可能是运行出错，http报错等等；
* complete: 表示流结束，不再发射新的数据

```ts
ob.subscribe({
  next: d => console.log(d), // 可以有多个next（表示多次发射数据），直到complete或者error
  error: err => console.error(err),
  complete: () => console.log('end of the stream') // 在一个流的生命周期中，error和complete只会触发其中一个
})
```

### pipe 链式调用

pipe方法用于链接可观察的运算符

pipe函数使用闭包返回函数，函数里使用reduce方法把前一个操作的结果作为后一个操作的输入值。

operator1 将接收 observable，对其执行操作并发出 observable。 从 operator1 发出的 observable 被传递给 operator2 作为输入

```ts
observable.pipe(
  operator1(),
  operator2(),
  operator3(),
)
```

### 可管道 Operator: 可以加入到 pipe 链式操作的操作符

| 类别 | 操作
| - | -
组合 | combineLatest, concat, merge, startWith, withLatestFrom, zip
过滤 | filter, take, debounce, debounceTime, distinctUntilChanged
转换 | map, concatMap, mergeMap, scan, switchMap
工具 | tap
multicasting 多播 | share
错误处理 | catchError, retry

* tap：可以理解为窥探，只看不改，返回与源Observable相同的Observable

* map: 对源 observable 的每个值应用投射函数

```ts
const newOb = ob.pipe(
	tap(num=>console.log(num)),
	map(num=>'hello:'+num)
);
newOb.subscribe(data=>console.log(data))
```

先执行管道里的tap和map操作，再把map操作的输出，作为输入去执行subscribe里指定的回调。

* catchError: err流入catch后，catch必须返回一个新的Observable。被catch后的错误流将不会进入observer的error函数

```ts
return this.httpService.get('/api').pipe(
  map(res => res.data),
  catchError(e => {
    return new Promise((r) => r(e.response.data)); // 需返回promise, 不能直接返回error
    throw new HttpException(`position请求错误`, 400); // return 和 throw 二选一
  }),
);
```

* take: 表示只取源发射的前n个数据，取完第n个后关闭源的发射

```ts
//ob作为源会每隔1000ms发射一个递增的数据，即0 -> 1 -> 2
const ob= interval(1000);

ob.take(3)
  .map(n => n * 2)
  .filter(n => n > 0)
  .subscribe(n => console.log(n));
```

* filter: 过滤掉出符合条件的数据

* forkJoin: promise.all 并发请求接口并返回

```ts
const res1 = this.httpService.get('/res1').pipe(
  map(res => res.data),
);
const res2 = this.httpService.get('/res2').pipe(
  map(res => res.data),
);
return forkJoin([res1, res2]).pipe(
  map(res => {
    ...
  }),
);
```

* mergeMap 有顺序依赖的多个请求

```ts
return this.httpService
  .get('/res1')
  .pipe(
    map(res => res.data),
  )
  .pipe(
    mergeMap(res1 => {
      return this.httpService.get('/res2', { params: {} });
    }),
  )
  .pipe(
    map(res2 => res2.data),
  )
```

### await

* lastValueFrom / firstValueFrom 取代 toPromise
```ts
return await lastValueFrom(
  this.httpService
    .post(AuthService.requestUrl, requestData, AuthService.requestConfig)
    .pipe(
      map((response: AxiosResponse) => response.data),
      catchError((e) => {
        throw new HttpException(e.response.data, HttpStatus.UNAUTHORIZED);
      }),
    ),
);
```

https://blog.csdn.net/qq_34035425/article/details/120598759

---

## Promise

promise是在es6标准中的一种用于解决异步编程的解决方案，由于在语言级别上，不同于Java、Python等多线程语言，js是单线程的，所以在node.js中大量使用了异步编程的技术，这样做是为了避免同步阻塞。

Promise对象代表一个异步操作，有三种状态：

* pending（进行中）
* fulfilled（已成功）
* rejected（已失败）

promise的状态只有两种改变情况，且仅改变一次，任何其他操作都无法改变这个状态：

* 由pending转变为resolved
* 由pending转变为rejected

await的一个Promise对象失败或者返回reject，那么整个async程序都会终止，除非使用try…catch捕捉

## 宏任务 VS 微任务

宏任务macrotask： 可每次执行栈执行的代码就是一个宏任务，整体script就是第一个宏任务。

* 主代码块
* setTimeout
* setInterval
* AJAX

微任务microtask：在当前task执行结束后立即执行的任务。

* Promise.then catch finally
* process.nextTick

当异步事件执行完毕后，会将异步的回调加入对应的任务队列中，任务队列分为宏任务和微任务。

微任务和宏任务同时存在则优选执行微任务。
依次执行微任务队列，微队列清空之后，执行宏任务，当宏任务执行过程中再次遇到微任务，则将微任务再次放如微任务队列，如此往复循环，直到所有队列为空

```js
setTimeout(()=>{
    console.log("3")
    Promise.resolve().then(()=>{
        console.log("4")
    })
})
console.log("1")
Promise.resolve().then(()=>{
    console.log("2")
    setTimeout(()=>{
        console.log("5")
    })
})
// 1 2 3 4 5
```

宏任务: setTimeout1, console -> 1, Promise.resolve()

微任务: .then -> 2

宏任务: setTimeout1 -> 3, setTimeout2

微任务: .then -> 4

宏任务: setTimeout2 -> 5
