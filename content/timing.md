Title: Timing
Date: 2021-10-26
Category: Analytics
Tags: DevTools
Author: Yoga

* Resource Scheduling
    * Queueing: __队列__ -- 请求排队的时间。浏览器是有线程限制的，发请求也不能所有的请求同时发送，会将请求加入队列中（Chrome的最大并发连接数是6）。如果说同一时间，发起的同一域名的请求超过了6个，这时候就需要排队了。
* Connection Start
    * Stalled:  __阻塞__ -- 浏览器得到要发出这个请求的指令，到请求可以发出的等待时间，一般是代理协商、以及等待可复用的TCP连接释放的时间，不包括DNS查询、建立TCP连接等时间等
    * Proxy nengotiation
    * DNS Lookup: __DNS查找__ -- 请求某域名下的资源，浏览器需要先通过DNS解析器得到该域名服务器的IP地址
    * Initial connection: __建立TCP连接__ -- 客户端从发请求开始到TCP握手结束这一段，包括DNS查询+Proxy时间+TCP握手时间
    * SSL: __安全套阶层__ -- 加密数据，https 是安全套接字层超文本传输协议，就是在HTTP的基础上加入了SSL协议，SSL依靠证书来验证服务器的身份，并为浏览器和服务器之间的通信加密。
* Request/Reponse
    * Request sent:  __发送请求__ -- 请求第一个字节发出前到最后一个字节发出后的时间，也就是上传时间
    * Waiting(TTFB): __首字节时间__ -- 请求发出后，到收到响应的第一个字节所花费的时间(Time To First Byte)
    * Content Download: __内容下载__ -- 收到响应的第一个字节，到接受完最后一个字节的时间，就是下载时间

## Stalled优化：

浏览器对同一个主机域名的并发连接数有限制，因此如果当前的连接数已经超过上限，那么其余请求就会被阻塞，等待新的可用连接；此外脚本也会阻塞其他组件的下载；

前端Dashboard页面展示的图表数据最好是提前统计好，然后放到缓存里面，避免统计时间比较长的ajax请求太多阻塞其他请求。

将资源合理分布到多台主机上，可以提高并发数，但是增加并行下载数量也会增大开销，这取决于带宽和CPU速度，过多的并行下载会降低性能；

脚本置于页面底部；

Stalled时间过长是网络问题导致的，有可能是本地网络不好，有可能是服务器网络不好，也有可能是中间链路的网络节点故障（防火墙、网关、VPN等等）。走内网IP访问不存在此问题，在内网做本地DNS，在公司通过域名访问则直接解析到内网IP。

## DNS优化：

在DNS查找完成之前，浏览器不能从主机名那里下载到任何东西。DNS查询的时间，当本地DNS缓存没有的时候，这个时间可能是有一段长度的，但是比如你一旦在host中设置了DNS，或者第二次访问，由于浏览器的DNS缓存还在，这个时间就为0了。

利用DNS缓存（设置TTL时间）

利用Connection:keep-alive特性建立持久连接，可以在当前连接上进行多个请求，无需再进行域名解析；

## Request sent优化：

减少HTTP请求，可以使用CSS Sprites、内联图片、合并脚本和样式表等；

对不常变化的组件添加长久的Expires头（相当于设置久远的过期时间），在后续的页面浏览中可以避免不必要的HTTP请求；

## Waiting优化：

发送请求完毕到接收请求开始的时间；通常是耗费时间最长的。从发送请求到收到服务器响应的第一字节之间的时间，受到线路、服务器距离等因素的影响。

网页重定向越多，TTFB越高，所以要减少重定向

使用CDN，将用户的访问指向距离最近的工作正常的缓存服务器上，由缓存服务器直接响应用户请求，提高响应速度；

## Content Download优化：

通过条件Get请求，对比If-Modified-Since和Last-Modified时间，确定是否使用缓存中的组件，服务器会返回“304 Not Modified”状态码，减小响应的大小；

移除重复脚本，精简和压缩代码，如借助自动化构建工具grunt、gulp等；

压缩响应内容，服务器端启用gzip压缩，可以减少下载时间；

原文链接：https://blog.csdn.net/lhz_333/article/details/93544313
