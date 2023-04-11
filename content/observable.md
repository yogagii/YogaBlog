Title: Observable
Date: 2023-04-10
Category: Javascript
Author: Yoga

Observable | Promise
| - | - |
/ | promise解决了嵌套地狱的问题
陈述式，直至subscription才会触发 | promise创建之后立即执行
支持多值甚至是数据流 | 只能提供单个值
能够在执行前或执行中被取消 dispose | 不可以取消
多次调用 retry 能够触发多次异步操作 | promise只可以被执行一次，重复调用，promise内部直接返回之前的状态
/ | 可使用async,await让多个promise进行同步
根据内部操作去判别使用异步还是同步 | promise一定是异步的
subscribe(), map(), pipe() | then()

### Observable 可观察对象，

一个可观察对象(Observable)，观察者(Observer)订阅(Subscribe)它，当数据就绪时，之前定义的机制就会分发数据给一直处于等待状态的观察者哨兵。

## Promise

promise是在es6标准中的一种用于解决异步编程的解决方案，由于在语言级别上，不同于Java、Python等多线程语言，js是单线程的，所以在node.js中大量使用了异步编程的技术，这样做是为了避免同步阻塞。

Promise对象代表一个异步操作，有三种状态：
* pending（进行中）
* fulfilled（已成功）
* rejected（已失败）

promise的状态只有两种改变情况，且仅改变一次：由pending转变为resolved，由pending转变为rejected，任何其他操作都无法改变这个状态

await的一个Promise对象失败或者返回reject，那么整个async程序都会终止，除非使用try…catch捕捉

宏任务macrotask： 可每次执行栈执行的代码就是一个宏任务，整体script就是第一个宏任务。

* 主代码块
* setTimeout
* setInterval

微任务microtask：在当前task执行结束后立即执行的任务。
* Promise
* process.nextTick

对于某个宏任务，如果其中有微任务和宏任务，则分别加到对应的队列中，然后该宏任务中所有的微任务执行完毕再执行宏任务队列中的下一个宏任务。

在node中，会先将所有宏任务中的的同步任务执行完毕，宏任务中所有的微任务执行完毕再执行宏任务队列中的下一个宏任务。
