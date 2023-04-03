Title: Nginx
Date: 2020-08-03
Category: Backend
Tags: Nginx
Author: Yoga

Nginx就是性能非常好的反向代理服务器，用来做负载均衡。

### 启动

踩坑：Redirecting to /bin/systemctl start nginx.service Failed to start nginx.service: Unit not found.

在 /etc/init.d/下创建名为nginx的启动脚本即可

设置执行权限：chmod +x /etc/init.d/nginx

注册成服务：chkconfig -add nginx

设置开机启动：chkconfig nginx on

Linux上开机自动启动Nginx: 在/etc/rc.local文件中加一行 nginx

启动：nginx 或 service nginx start

踩坑：nginx: [error] invalid PID number “” in “/run/nginx.pid”

nginx -c /etc/nginx/nginx.conf # 找到 nginx.conf 路径

nginx -s reload

### 查看Ngnix配置
```bash
sudo su -
ps -aux | grep nginx
# root xxx 0.0  0.0 xxx xxx ? Ss Mar19 0:00 nginx: master process /usr/sbin/nginx

/usr/sbin/nginx -t
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok

cat /etc/nginx/nginx.conf
# include /etc/nginx/default.d/*.conf;
# include /etc/nginx/default.d/*.conf;

cat /etc/nginx/conf.d/swift.conf
```

```bash
# 测试
nginx -t
# 重启
service nginx restart
nginx -s reload
```

### nginx.conf

后端

pm2 start npm --name iqvia-data-3007 -- run start:prod
```
location /iqvia/ {
    rewrite "^/iqvia/(.*)$" /$1 break;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_pass http://xx.xx.xx.39:3007;
}
```

前端 build
```
server {
    server_name hr_hackathon.xxx.com;
    root /usr/share/nginx/fpa_share_doc/dist;
    location / {
      try_files $uri $uri/ /index.html;
    }
  }
```
指向index

npm run build:prod
```
# 0042 (42 -> 39)
location /iqvia-email {
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_buffering off;
    proxy_pass http://xx.xx.xx.39;
}
# 0039 (nginx在42，资源在39)
location /iqvia-email/ {
    alias   /var/www/iqvia_email/build/;
    index index.html;
}

# 0080 (80资源在本机)
location /iqvia-email/ {
    alias   /var/www/iqvia_email/build/;
    index index.html;
    try_files $uri /iqvia-email/index.html;
}
```
指向端口

```bash
next build
next start -p 3008
pm2 start npm --name carto-dashboard-3008 -- run start
```
```ts
// next.config.ts
module.exports = {
  basePath: '/carto-dashboard',
};
```
```
location /carto-dashboard {
  proxy_set_header Host $host;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_set_header X-Forwarded-Proto $scheme;
  proxy_pass http://xx.xx.xx.80:3008;
}
```
前端 单页
```
server {
  server_name project_organization.xxx.com;
  root /root/www/project_organization;
  index dateBar.html;
}
```
静态资源

```
location /static {
    alias   /var/www/static;
}
```

___

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