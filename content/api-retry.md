Title: 错误重试和指数退避
Date: 2021-08-19
Category: Javascript
Tags: AWS
Author: Ron, Adarsh

### Introduction

网络上的大量组件 (例如 DNS 服务器、交换机、负载均衡器等) 都可能在某个指定请求生命周期中的任一环节出现问题。在联网环境中，处理这些错误回应的常规技术是在客户应用程序中实施重试。此技术可以提高应用程序的可靠性和降低开发人员的操作成本。

Although Vital backend is a highly available system running on the highly available AWS infra, there are third-party API integrations that are upstream. These dependencies might not be highly available. This means there may be instances when the backend API would fail. This can happen due to variety of issues ranging from network issues to upstream downtime. To handle such situations, it is of grave importance for Vital to have a well-crafted retry logic that can ensure the application itself is highly available for the end user.

### Design Considerations

Before having a retry logic in place it is important to align with the following facts:

4XX status codes are meant for the client-side errors. This means retries aren't supposed to be done on such HTTP statuses. If the client retries, then it will only aggravate the problems(unnecessary load on server/gateway).

客户端错误 (4xx) 表示您需要对请求本身进行修改，纠正该问题，然后再重试。

5XX status codes indicate an issue on the server side. Retry can be done with caution.
If a retry is done on 5XX status code, then the client can adopt an Exponential Back-off strategy for retrying.

Exponential Back-off strategy employs a progressively delayed retry mechanism. For example, retry after 1 second, retry after 2 seconds, retry after 4 seconds, retry after 8 seconds, etc.

指数退避的原理是对于连续错误响应，重试等待间隔越来越长。您应该实施最长延迟间隔和最大重试次数。最长延迟间隔和最大重试次数不一定是固定值，并且应当根据正在执行的操作和其他本地因素（例如网络延迟）进行设置。

To further improve the strategy, we can have a upper limit for the retry. This can be either a time limit(like 250 milliseconds) or a count(like 10). This now makes the strategy, a Truncated Exponential Back-off Strategy.

Another important consideration is to make sure the APIs we are retrying is actually safe to retry. This is because the previous request might have partially failed but may have induced the expected side-effect as well. If retrying causes an unwanted re-running of the side-effect, then it has to be avoided.

Another consideration is that although exponential back-off strategy is good, in the worst-case scenario of tons of client requests failing and causing retries, the backend will get a burst of load causing much worse situation. To avoid this a random delay can be added for each back-off retry. This randomness is called the Jitter.

大多数指数回退算法会利用抖动 (随机延迟) 来防止连续的冲突。由于在这些情况下您并未尝试避免此类冲突，因此无需使用此随机数字。但是，如果使用并发客户端，抖动可帮助您更快地成功执行请求。

Truncated Exponential Back-off strategy is a standard error-handling strategy for networked applications. This can be used for requests that return 429, 408 and 5XX status codes.

This strategy can be defined as - Wait Interval = Minimum((Base * 2^n) + Random Interval, Maximum Back-off Time)

### Implementation

The default connection timeout value for API calls in Vital is set to 60 seconds. For SAP reports this is set to 120 seconds.

The retry mechanism can take this timeout value into consideration when designing the Truncated Exponential Back-off strategy. The HTTP status code for this would be 408.

For a status code of 5XX or 429, we can have a retry delay of Minimum((1000* 2^n) + Math.floor(Math.random() * 1000) + 1, 15000) milliseconds with a max retry attempt of 3.

For a status code of 408, we can have a retry delay of 1 second with max retry attempt of 1.

## fetch-retry

https://www.npmjs.com/package/fetch-retry

The default behavior of fetch-retry is to wait a fixed amount of time between attempts, but it is also possible to customize this by passing a function as the retryDelay option. The function is supplied three arguments: attempt (starting at 0), error (in case of a network error), and response. It must return a number indicating the delay.

```js
var originalFetch = require('isomorphic-fetch');
var fetch = require('fetch-retry')(originalFetch, {
    retries: 5,
    retryDelay: 800
  });

fetch(url, {
    retryDelay: function(attempt, error, response) {
      return Math.pow(2, attempt) * 1000; // 1000, 2000, 4000
    }
  }).then(function(response) {
    return response.json();
  }).then(function(json) {
    // do something with the result
    console.log(json);
  });
```
