Title: 常用内置方法
Date: 2019-01-01
Category: Javascript
Author: Yoga

## Array

* slice

  slice() 方法可提取字符串/数组的某个部分，并以新的字符串/数组返回被提取的部分。

  > stringObject.slice(start,end)

  start：起始坐标，负数从结尾开数

  end：结尾下标，负数从结尾开数，未指定则到底，end < start无效

  返回值：一个新的字符串

* splice

  从数组中添加或删除元素，返回被删除的元素，会改变原始数组

  > arrayObject.splice(index,howmany,element1,.....,elementX)

  index：起始下标

  howmany：删除元素个数，不指定删到底

  element1：要添加的新元素

  返回值：含有被删除元素的数组

* shift 删除并返回第一项

* unshift 添加到第一项返回长度

* pop 删除并返回最后一项

* push 添加到最后返回长度

* concat 拼接数组返回新数组

* reverse 数组返序

* sort 数组排序

* join(separator) 数组合并成字符串，默认‘，’

* indexof 返回下标

* lastIndexof 从后往前找

* findIndex() 方法返回符合条件的数组第一个元素位置。

* forEach

* every 都满足

* some 有一个满足

* filter 返回新数组包含所有满足项

* map 返回新数组包含每个元素处理结果

* reduce

## String

* substring

  返回截取的字符串，不改变原字符串

  > stringObject.substring(start,end)

  start：起始下标

  end：结尾下标, end < start时调换位置，负数时只截取一个字符

* substr

  返回截取的字符串，不改变原字符串

  > stringObject.substr(start,howmany)

  start：起始下标，负数从结尾开数

  howmany：截取几位，负数为空

* split 分割

* replace 替换，默认一次

* length

* indexof/lastIndexof

* charAt

* charCodeAt Unicode编码

* str.match(reg) = reg.exec(str)

* concat

* toLowerCase/toUpperCase

* localeCompare 字符串比较

  ```js
  reportsData.sort((a,b) => a.name.toLowerCase().localeCompare(b.name.toLowerCase()));
  reportsData.sort((a, b) =>
    a.name.toLowerCase() > b.name.toLowerCase() ? 1 : -1,
  );
  ```

* trim 删除前后空格

* replace


## Object

* assign

  将所有可枚举属性的值从一个或多个源对象复制到目标对象。它将返回目标对象。

  > Object.assign(target, ...sources);

  target: 目标对象

  sources: 源对象

  ```js
  const obj = {
    c: 4,
    d: 5
  };
  const object1 = {
    a: 1,
    b: 2,
    c: 3
  };
  const object2 = Object.assign(obj, object1);
  // obj {c: 3, d: 5, a: 1, b: 2}
  // object2 {c: 3, d: 5, a: 1, b: 2}
  // object1 {a: 1, b: 2, c: 3}
  ```