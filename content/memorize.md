Title: 高阶函数
Date: 2019-01-01
Category: Javascript
Author: Yoga

> 高阶函数(Higher-order function)：一个函数可以接收另一个函数作为参数。 e.g. map, reduce, filter

### 记忆函数

记忆化（memoization）是一种构建函数的处理过程，能够记住上次计算结果的函数。当函数计算得到结果时，就将该结果按照参数存储起来，当另外一个调用也使用相同的参数，可以直接返回上次存储的结果而不是再计算一遍。

像这样避免既重复又复杂的计算可以显著提高性能。对于动画中的计算、搜索不经常变化的数据或任何耗时的数学计算来说，记忆化这种方式是十分有用的

```js
const memorize = function (fn) {
  const cache = {};
  return function (...args) {
    const _args = JSON.stringify(args)
    if (!cache[_args]) {
      (cache[_args] = fn.apply(fn, args))
    }
    return cache[_args];
  }
}
```

### 斐波那契数列

> 1 1 2 3 5 8 13 21 34

1. 递归法 O(2<sup>n</sup>)

```js
function fibonacci(n) {
  if (n <= 2) {
    return 1;
  } else {
    return fibonacci(n-1) + fibonacci(n-2)
  }
}
```

2. 递归改良法 O(n)

fibonacci = memorize(fibonacci)

```js
var arr = new Array();
function fibonacci(n) {
  if (n <= 2) {
    return 1;
  } else {
    if (!arr[n]) {
      arr[n] = fibonacci(n-1) + fibonacci(n-2);
    }
    return arr[n];
  }
}
```

3. 迭代法 O(n)

```js
function fibonacci(n) {
  var res1 = 1, res2 = 2;
  var sum = res2;
  var i = 3;
  while (i<=n) {
    sum = res1 + res2;
    res1 = res2;
    res2 = sum;
    i ++;
  }
  return sum;
}
```