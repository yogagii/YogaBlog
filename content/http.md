Title: HTTP
Date: 2020-10-09
Category: Javascript
Tags: Http
Author: Yoga

web socket需要把http设为1.1
只握手一次

location{
  proxy_http_version: 1,1;
  proxy_set_header Upgrade $http_upgrade;
  proxy_set_header Connection "upgrade"; // 升级到最新版本 Status code 101
  proxy_set_header Host $host; // 暴露被反向代理隐藏的host
}

## iframe

![http](img/http.jpeg)
