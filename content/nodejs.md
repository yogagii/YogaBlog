Title: nodeJS
Date: 2020-08-03
Category: Backend
Tags: nodeJS
Author: Yoga

Nginx 比 Apache 高并发的原因

Nginx 负载均衡调度算法
负载均衡之轮询算法

Apache 多进程（多线程）

Nginx 单进程（单线程）

```js
new promise(console.log(3)) // 这一轮最后执行
setTimeout(console.log(2)) // 下一轮执行
console.log(1)
// 1 3 2
```

path.resolve()指向根目录

```js
export const App
// import { App } from app.js

export default App
// import App from app.js

Module.exports = {}
// import * as Moment from "moment"

Module.exports = {
  _default: this
}
// import * as React from 'react';
// import React from 'react';
```

## buffer 缓冲器

```js
new ArrayBuffer([1, 2, 3])
```

TypedArray 有类型的数组

- Uint8Array
- Uint16Array
- Uint32Array

如果要把 blob 文件转化为二进制的数据的话，要先把 blob 转化为 arraybuffer，然后再使用 typedArray 就可以直接编辑二进制数据了

```js
var ab = new ArrayBuffer(32)
var iA = new Int8Array(ab)
iA[0] = 97
var blob = new Blob([iA], { type: 'application/octet-binary' })
var fr = new FileReader()
fr.addEventListener('load', function (ev) {
  var abb = ev.target.result
  var iAA = new Int8Array(abb)
  console.log(iAA)
})
//把blob文件转化为arraybuffer；
fr.readAsArrayBuffer(blob)
```

```js
const { Buffer } = require('Buffer');
const buf = Buffer.from('abcd', 'utf8'); // <Buffer 61 62 63 64>
const buf = Buffer.from([1, 2, 3, 4]); // <Buffer 01 02 03 04>
const buf = Buffer.from([1, 2, 3, 257]); // <Buffer 01 02 03 01> 257 % 256
const buf = Buffer.from([1, 2, 3, 257, 23]); // <Buffer 01 02 03 01 17> 16进制
const buf = Buffer.from([1, 2, 3, 257, 0xff]); // <Buffer 01 02 03 01 ff> 16进制

buf.buffer // ArrayBuffer {[uint8Contents]: <63 6f 6e ...>, byteLength: 8192}
buf.byteOffset // 152 从第152位开始为实际数据
buf.byteLength // 5

const buf1 = Buffer.from(buf)
buf[0] = 9 // buf1[0] = 1 复制
const buf2 = Buffer.from(buf.buffer, buf.byteOffset, buf.byteLength)
buf[0] = 9 // buf2[0] = 9 引用
buf2.compare(buf) // 0 相同 1 大于 -1 小于
```

```js
const buf = Buffer.alloc(2) // <Buffer 00 00>
buf.fill('a') // <Buffer 61 61>
buf.writeUInt16BE(2) // <Buffer 00 02> 大端字节序
buf.writeUInt16LE(2) // <Buffer 02 00> 小端字节序
```