Title: Nginx
Date: 2020-08-03
Category: Backend
Tags: Nginx
Author: Yoga

Nginx就是性能非常好的反向代理服务器，用来做负载均衡。


查看Ngnix配置
```
sudo su -
ps -aux | grep nginx
cat /usr/local/nginx/conf/nginx.conf

// 测试
nginx -t
// 重启
service nginx restart
```

nginx.conf
```
// build
server {
    server_name hr_hackathon.jujadc.com;
    root /usr/share/nginx/fpa_share_doc/dist;
    location / {
      try_files $uri $uri/ /index.html;
    }
  }
// 单页
server {
  server_name project_organization.jujadc.com;
  root /root/www/project_organization;
  index dateBar.html;
}
```


Nginx 比 Apache 高并发的原因

Nginx 负载均衡调度算法
负载均衡之轮询算法

Apache 多进程（多线程）

Nginx 单进程（单线程）

web socket需要把http设为1.1
只握手一次

```js
location{
  proxy_http_version: 1,1;
  proxy_set_header Upgrade $http_upgrade;
  proxy_set_header Connection "upgrade"; // 升级到最新版本 Status code 101
  proxy_set_header Host $host; // 暴露被反向代理隐藏的host
}
```