Title: Nginx
Date: 2020-08-03
Category: Backend
Tags: Nginx
Author: Yoga

Nginx就是性能非常好的反向代理服务器，用来做负载均衡。

### 安装

下载  [https://nginx.org/download/nginx-1.14.2.tar.gz](https://nginx.org/download/nginx-1.14.2.tar.gz) 

上传nginx-1.14.2.tar.gz到目标服务器

tar -zxf ***.tar.gz 解压缩

确认gcc是否安装，若否先yum -y install gcc  gcc-c++ kernel-devel

安装完成后进入nginx目录 ./configure --with-http_ssl_module

make && make install

安装成功， 进入/usr/local/nginx/sbin/

执行./nginx启动

软连接 ln -s /usr/local/nginx/sbin/nginx /usr/sbin/nginx

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

### SSL 证书

_踩坑：Nginx 配置完后，只能打开http开头的域名，因为缺少SSL证书_

HTTP 协议以明文方式发送内容，不提供任何方式的数据加密，如果攻击者截取了Web浏览器和网站服务器之间的传输报文，就可以直接读懂其中的信息

HTTPS 经由 HTTP 进行通信，但利用 SSL/TLS 来加密数据包。HTTPS 开发的主要目的，是提供对网站服务器的身份认证，保护交换数据的隐私与完整性。

在nginx的conf目录下新建一个cert目录，并将两个证书文件上传到cert目录下

```bash
listen 443 ssl; # managed by Certbot
ssl_certificate "/etc/letsencrypt/live/xxx.cer";
ssl_certificate_key "/etc/letsencrypt/live/xxx.key";
ssl_session_cache shared:SSL:1m;
ssl_session_timeout  10m;
ssl_ciphers PROFILE=SYSTEM;
ssl_prefer_server_ciphers on;
```

_踩坑：[emerg] the "ssl" parameter requires ngx_http_ssl_module. Nginx 缺少 http_ssl_module 模块_

切换到源码包：cd /home/usr/nginx-1.14.2/

./configure --with-http_ssl_module

make (不要make install，否则会覆盖安装)

备份原有已安装好的nginx：cp /usr/local/nginx/sbin/nginx /usr/local/nginx/sbin/nginx.bak

停止nginx运行：nginx -s stop

将刚刚编译好的nginx覆盖掉原有的nginx：cp ./objs/nginx /usr/local/nginx/sbin/nginx

启动nginx：nginx

nginx -V 查看是否已成功加入
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