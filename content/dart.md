Title: Dart
Date: 2021-12-24
Category: IOS
Tags: Flutter
Author: Yoga

## 单线程模型

Dart 在单线程中是以消息循环机制来运行的，其中包含两个任务队列

* “微任务队列” microtask queue：（Dart内部）微任务队列优先级高，如果微任务太多，执行时间总和就越久，事件队列任务的延迟也就越久，对于GUI应用来说最直观的表现就是比较卡
* “事件队列” event queue：（外部事件任务）IO、计时器、点击、以及绘制事件

![flutter](img/flutter3.png)

入口函数 main() 执行完后，消息循环机制便启动了。首先会按照先进先出的顺序逐个执行微任务队列中的任务，事件任务执行完毕后程序便会退出，在事件任务执行的过程中也可以插入新的微任务和事件任务

Flutter中，主线程的执行过程一直在循环，永不终止。当某个任务发生异常并没有被捕获时，当前任务的后续代码就不会被执行了，程序并不会退出。

## 变量声明

虽然 Dart 代码是类型安全的，但是由于支持类型推断，大多数变量是不需要显式指定类型的

* var 

Dart 本身是一个强类型语言，任何变量都是有确定类型的，变量一旦赋值，类型便会确定，则不能再改变其类型。

* object

Dart 中所有类型都是Object的子类(包括Function和Null)，所以任何类型的数据都可以赋值给Object声明的对象

Object声明的对象只能使用 Object 的属性与方法

* dynamic

dynamic与Object声明的变量都可以赋值任意对象，且后期可以改变赋值的类型

* final

一个 final 变量只能被设置一次，变量在第一次使用时被初始化，变量类型可以省略

* const

const 变量是一个编译时常量，变量类型可以省略

* 空安全

可空类型要显式（通过在变量后面加一个”!“符号）告诉预处理器它已经不是null了

```dart
int i = 8; //默认为不可空，必须在定义时初始化。
int? j; // 定义为可空类型，对于可空变量，我们在使用前必须判空。
Function? fun;

print(j! * 8);
fun?.call() // 语法糖fun 不为空时则会被调用
```

> 在Dart语言中使用下划线前缀标识符，会强制其变成私有的。

## 函数

```dart
void test(CALLBACK cb){
   print(cb()); 
}

// bool 可省略， 如果没有显式声明返回值类型时会默认当做dynamic处理
bool isNoble(int atomicNumber) { 
  return _nobleGases[atomicNumber] != null;
}

// =>（箭头）语法用于仅包含一条语句的函数
bool isNoble (int atomicNumber)=> true ;

// 函数作为变量
var say = (str){
  print(str);
};

// 函数作为参数传递
void execute(var callback) {
    callback();
}
execute(() => print("xxx"))

// 用[]标记为可选的位置参数
String say(String from, String msg, [String device]) {
  // ... 
}

// 可选的命名参数
void enableFlags({bool bold, bool hidden}) {
  // ... 
}
enableFlags(bold: true, hidden: false);
```

## 异步

### 1. Future

Future与JavaScript中的Promise非常相似，表示一个异步操作的最终完成（或失败）及其结果值的表示。一个Future只会对应一个结果，要么成功，要么失败。

```dart
// 延时任务
Future.delayed(Duration(seconds: 2),(){
   return "hi world!";
}).then((data){
   //执行成功会走到这里  
   print("success");
}).catchError((e){
   //执行失败会走到这里  
   print(e);
}).whenComplete((){
   //无论成功或失败都会走到这里
});
```

只有数组中所有Future都执行成功后，才会触发then的成功回调，只要有一个Future执行失败，就会触发错误回调。(Promise.all)

```dart
Future.wait([
  // 2秒后返回结果  
  Future.delayed(Duration(seconds: 2), () {
    return "hello";
  }),
  // 4秒后返回结果  
  Future.delayed(Duration(seconds: 4), () {
    return " world";
  })
])
```

回调地狱(Callback Hell): 在回调里面套回调

链式调用: Future 的所有API的返回值仍然是一个Future对象，如果在then 中返回的是一个Future的话，该future会执行，执行结束后会触发后面的then回调，这样依次向下，就避免了层层嵌套。

```dart
login("alice","******").then((id){
  	return getUserInfo(id);
}).then((userInfo){
    return saveUserInfo(userInfo);
})
```

async用来表示函数是异步的，定义的函数会返回一个Future对象，可以使用 then 方法添加回调函数。

await 后面是一个Future，表示等待该异步任务完成，异步完成后才会往下走；await必须出现在 async 函数内部。

```dart
task() async {
  try{
    await saveUserInfo(userInfo);
    //执行接下来的操作   
  } catch(e){
    //错误处理   
    print(e);   
  }  
}
```

> 无论是在 JavaScript 还是 Dart 中，async/await 都只是一个语法糖，编译器或解释器最终都会将其转化为一个 Promise（Future）的调用链。

### 2. Stream

Stream 也是用于接收异步事件数据，可以接收多个异步操作的结果（成功或失败）。 也就是说，在执行异步任务时，可以通过多次触发成功或失败事件来传递结果数据或错误异常。

Stream 常用于会多次读取数据的异步任务场景，如网络内容下载、文件读写等。

```dart
Stream.fromFutures([
  // 1秒后返回结果
  Future.delayed(Duration(seconds: 1), () {
    return "hello 1";
  }),
  // 抛出一个异常
  Future.delayed(Duration(seconds: 2),(){
    throw AssertionError("Error");
  }),
  // 3秒后返回结果
  Future.delayed(Duration(seconds: 3), () {
    return "hello 3";
  })
]).listen((data){
   print(data);
}, onError: (e){
   print(e.message);
},onDone: (){

});
```