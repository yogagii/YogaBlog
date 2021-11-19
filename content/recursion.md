Title: 递归
Date: 2021-11-19
Category: Javascript
Author: Yoga

## 斐波那契数列

```js
function fibonacci(n) {
  if (n <= 2) {
    return 1;
  } else {
    return fibonacci(n-1) + fibonacci(n-2)
  }
}
```

## 字符串全排列

重新排列一个字符串，使得每个相邻字符都不同，列出所有情况

* 枚举采用全排列
* 过滤相邻重复，正则表达式var re = /(.)\1+/g;

```js
// 全排列，result.length = s.length阶乘
var perm = function (s: string) {
  var result = [];
  if (s.length <= 1) {
    return [s];
  } else {
    for (var i = 0; i < s.length; i++) {
      var c = s[i];
      var newStr = s.slice(0, i) + s.slice(i + 1, s.length);
      var l = perm(newStr);

      for (var j = 0; j < l.length; j++) {
        var tmp = c + l[j];
        result.push(tmp);
      }
    }
  }
  return result;
};

// 删除重复字符串
const delectDuplicateArr = (arr: Array<string[]>) => {
  const result = [];
  const s = new Set();
  arr.forEach((a: string[]) => {
    if (!s.has(JSON.stringify(a))) {
      s.add(JSON.stringify(a));
      result.push(a);
    }
  });
  return result;
};

function reorganize(str: string): string[] {
  // write your code here ...
  const allArr = perm(str);
  const re = /(.)\1+/g;
  const result = allArr.filter((val) => !val.match(re));
  return delectDuplicateArr(result);
}

// input 'aabb'
// output ['abab', 'baba']
```

## 爬楼梯

假如楼梯有 n 个台阶，每次可以走 1 个或 2 个台阶，请问走完这 n 个台阶有几种走法

```js
function climbStairs(n) {
  if (n == 1) return 1
  if (n == 2) return 2
  return climbStairs(n - 1) + climbStairs(n - 2)
}
```

## 深拷贝

```js
function clone(o) {
  var temp = {}
  for (var key in o) {
    if (typeof o[key] == 'object') {
      temp[key] = clone(o[key])
    } else {
      temp[key] = o[key]
    }
  }
  return temp
}
```

链接：https://juejin.cn/post/6844904014207795214