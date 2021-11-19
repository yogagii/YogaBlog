Title: 并发控制
Date: 2021-11-19
Category: Javascript
Author: Yoga

假设有 6 个待办任务要执行，而我们希望限制同时执行的任务个数，即最多只有 2 个任务能同时执行。当 正在执行任务列表 中的任何 1 个任务完成后，程序会自动从 待办任务列表 中获取新的待办任务并把该任务添加到 正在执行任务列表中。

## async-pool

```js
function asyncPool(poolLimit, array, iteratorFn){ ... }
```
* poolLimit（数字类型）：表示限制的并发数；

* array（数组类型）：表示任务数组；

* iteratorFn（函数类型）：表示迭代函数，用于实现对每个任务项进行处理，该函数会返回一个 Promise 对象或异步函数。

使用：
```js
const timeout = i => new Promise(resolve => setTimeout(() => resolve(i), i));
await asyncPool(2, [1000, 5000, 3000, 2000], timeout);
```

实现：
```js
function asyncPool(poolLimit, array, iteratorFn) {
  const ret = []; // 存储所有的异步任务
  const executing = []; // 存储正在执行的异步任务
  for (const item of array) {
    // 调用iteratorFn函数创建异步任务
    const p = Promise.resolve().then(() => iteratorFn(item, array));
    ret.push(p); // 保存新的异步任务
 
    // 当poolLimit值小于或等于总任务个数时，进行并发控制
    if (poolLimit <= array.length) {
      // 当任务完成后，从正在执行的任务数组中移除已完成的任务
      const e = p.then(() => executing.splice(executing.indexOf(e), 1));
      executing.push(e); // 保存正在执行的异步任务
      if (executing.length >= poolLimit) {
        await Promise.race(executing); // 等待较快的任务执行完成
      }
    }
  }
  return Promise.all(ret);
}
```

## async.mapLimit

```js
mapLimit(coll, limit, iteratee, callback opt)
```

* coll(Array / Iterable / object): 要迭代的集合。
* limit(number):	一次异步操作的最大数量。
* iteratee(AsyncFunction):	对于 coll 中的每一个item，迭代执行该异步函数。用(item, callback)调用，callback可选。
* callback([ function ]):	所有iteratee 函数完成后或发生错误时触发的回调函数。用(err, results)调用。results可以是iteratee 函数完成后触发callback时传递的项。

使用：
```js
const async = require('async');

module.exports = async function tableauJob() {
  let concurrencyCount = 0;
  const workbooks = [{
    id: '1',
  }, {
    id: '2'
  }]

  const fetchUrl = async (wk, callback) => {
    concurrencyCount += 1;
    sails.log.info('concurrencyCount: ', concurrencyCount, '，workbook id: ', wk.id);

    const wkObj = { ...wk };
    const permissions = (await TableauService.apiLoader(`workbooks/${wk.id}/permissions`))
      .permissions.granteeCapabilities || [];
    concurrencyCount -= 1;
    wkObj.groups = permissions;
    callback(null, wkObj);
  };

  await async.mapLimit(workbooks, 10, (wk, callback) => {
    fetchUrl(wk, callback);
  }, (err, result) => {
    TableauWorkbook.bulkCreate(result);
  });
}
```

## parallel 

支付宝笔试：
给出一组异步任务方法，和允许同时执行的个数，实现一个方法，用于并发执行异步任务

 当有任务执行完毕后，自动补充任务，始终保持正在执行的任务有 `concurrency` 个

```js
async function parallel(tasks, concurrency) {
  const executing = [];
  const ret = [];
  if (concurrency <= tasks.length) {
    for (let item of tasks) {
      let p;
      p = item.catch((err: any) => ({
        status: 'fail',
        data: err,
      }));
      ret.push(p);
      const e = p.then(() => executing.splice(executing.indexOf(e), 1));
      executing.push(e);
      if (executing.length >= concurrency) {
        await Promise.race(executing);
      }
    }
  }
  const result = {
    resolved: [],
    rejected: [],
  };

  await Promise.all(ret).then((values) => {
    values.forEach((v) => {
      if (v?.status === 'fail') {
        result.rejected.push(v.data);
      } else {
        result.resolved.push(v);
      }
    });
  });
  return result;
}

const tasks = [
  () => Promise.resolve('foo'),
  () => Promise.reject(new Error('ttt')),
];
const { resolved, rejected } = await parallel(tasks, 2);
assert.equal(resolved.length, 1);
assert.equal(rejected.length, 1);
```

* Promise all：只要失败一个就不会走then
* Promise.allSettled()方法返回一个在所有给定的promise都已经fulfilled或rejected后的promise，并带有一个对象数组，每个对象表示对应的promise结果。
