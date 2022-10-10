Title: ES6 新特性
Date: 2019-01-01
Category: Javascript
Author: Yoga

## ES6

## 1.箭头函数

```js
//es5
var fun = function () {};
//es6
var fn = () => {};
```

- 箭头函数不需要 function 关键字来创建函数，更适用于那些本来需要匿名函数的地方。

- 函数的 this 依赖于函数调用（window），箭头函数没有自己的 this，arguments，super 或 new.target。

```js
// function
function Person() {
  var that = this;
  that.age = 0;

  setInterval(function growUp() {
    // 回调引用的是`that`变量, 其值是预期的对象.
    that.age++;
  }, 1000);
}

// arrow function
function Person() {
  this.age = 0;

  setInterval(() => {
    this.age++; // |this| 正确地指向 p 实例
  }, 1000);
}
```

通过 call() 或 apply() 方法调用箭头函数时，只能传递参数（不能绑定 this），他们的第一个参数会被忽略。

- 当函数体只有一个 `return` 语句时，可以省略 `return` 关键字和花括号

- yield 关键字通常不能在箭头函数中使用。因此，箭头函数不能用作函数生成器。

## 2.剩余参数/不定参数 Rest Parameters

剩余参数允许将一个不定数量的参数表示为一个数组

```js
function(a, b, ...theArgs) {
  // ...
}
```

如果函数的最后一个命名参数以...为前缀，则它将成为一个由剩余参数组成的真数组，theArgs 将收集该函数的第三个参数和所有后续参数

剩余参数可以被解构 f(...[a, b, c])

arguments 对象不是一个真正的数组，而剩余参数是真正的 Array 实例

_伪数组：1.arguments, 2.getElementsByTagName 3.childNodes_

```js
Array.prototype.slice.call(arguments);
Array.from(arguments);
```

## 3.展开运算符/拓展参数 Spread syntax

传递数组作为参数

```js
function myFunction(x, y, z) {}
let args = [0, 1, 2];

//es5
myFunction.apply(null, args);
//es6
myFunction(...args);
```

## 4.默认参数 Functions Default

在没有值或 undefined 被传入时使用默认形参。

```js
function test(num = 1) {
  console.log(num, typeof num);
}

test(); // 1 'number'
test(undefined); // 1 'number'
test(""); // '' 'string'
```

## 10.Set

数组去重

```js
// input [false, true, undefined, null, NaN, 0, 1, {}, {}, 'a', 'a', NaN]
// output [false, true, undefined, null, NaN, 0, 1, {}, {}, 'a']
Array.prototype.uniq = function () {
  return [...new Set(this)];
};
```

---

## ES2021

Promise.race() 承诺列表中寻找第一个履行或拒绝的承诺；

Promise.any() 是从承诺列表中查找第一个履行的承诺。

判断是否存在缓存，缓存中有数据直接返回，缓存中无数据 -> 从数据库获取。

缺点：1. 缓存数据不更新，2.不能并发

Promise.race 在cacheGet中reject导致拒绝，无法返回数据库获得数据，Promise.any 在cacheGet中reject不影响，会返回数据库数据

优势：1. 用缓存数据直接相应接口，解决504，同时读取数据库更新缓存，保证接口每次获得最新数据，2. 读缓存和度数据库可并发

```ts
async cacheGet(key: any): Promise<any> {
    return new Promise((resolve, reject) => {
      this.cacheManager.get(key, (error, result: any) => {
        if (result) {
          resolve(JSON.parse(result));
        }
        reject(error);
      });
    });
  }
```

```ts
const [examlist, userlist]: [Pagination<ExamDto>, Pagination<UserDto>] =
  await Promise.all([
    Promise.any([
      this.examsService.getBehaviorList(),
      this.cacheService.cacheGet("examlist"),
    ]),
    Promise.any([
      this.usersService.getUserList(),
      this.cacheService.cacheGet("userlist"),
    ]),
  ]);
```
tsconfig.json
```json
{
  "compilerOptions": {
    "target": "es2021",
  }
}
```