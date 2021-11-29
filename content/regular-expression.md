Title: Regular Expression
Date: 2020-12-14
Category: Javascript
Tags: Regexp
Author: Yoga

* *：>= 0次。例如，zo 能匹配 "z" 以及 "zoo"。 等价于{0,}。

* +：>= 1次。例如，'zo+' 能匹配 "zo" 以及 "zoo"，但不能匹配 "z"。+ 等价于 {1,}。

```js
// 连续重复字符
/(.)\1+/g
```

* ?：0次或1次

* {n} n次

* {n,} >= n次

* \d 数字

* \D 非数字

* \w 包括下划线的任何单词字符

* \W 非单词字符

* g全局

* i不分大小写

* m多行

url最后一个params
```js
const url = 'xx.xx.xx/xx/aa/bb/cc';
url.match(/([^\/]*)\/*$/)[1]; // 'cc'
```

VScode搜索正则匹配

![rx](img/rx1.png)

![rx](img/rx2.png)
