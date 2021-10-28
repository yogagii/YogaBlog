Title: 闭包
Date: 2021-10-22
Category: Javascript
Tags: Javascript
Author: Yoga

> 闭包：有权访问另一个函数作用域内变量的函数

C++中函数中的局部变量仅在函数函数执行期间可用，执行完毕不能访问

JS函数以及创建的词法环境形成闭包，环境包含闭包创建时所能访问的所有局部变量

闭包有3个特性：
1. 函数嵌套函数
2. 函数内部可以引用函数外部的参数和变量
3. 参数和变量不会被垃圾回收机制回收

```js
function A () {
  var n = 0;
  this.B = function () {
    n++;
    console.log(n);
  }
}
var a = new A();
a.B() // 1
a.B() // 2
```
```js
function A () {
  var n = 0;
  function B () {
    n++;
    console.log(n);
  }
  return B;
}
var a = A();
a() // 1
a() // 2
```
n是执行A函数时创建的B函数实例的引用

B实例仍可访问到n不回收

```js
function fn() {
  var num = 3
  return function() {
    var n = 0;
    console.log(++n);
    console.log(++num);
  }
} 
var fn1 = fn();
fn1(); // 1 4
fn1(); // 1 5
```
匿名函数内部引用着fn里的变量num，所以变量num无法被销毁，而变量n是每次被调用时新创建的，所以每次fn1执行完后它就把属于自己的变量连同自己一起销毁，于是乎最后就剩下孤零零的num

https://blog.csdn.net/weixin_43558749/article/details/90905723