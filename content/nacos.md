Title: Nacos
Date: 2024-09-09
Category: Backend
Tags: Java
Author: Yoga

Nacos是一个开源的、易于使用的、功能强大的动态服务发现、配置管理和服务管理平台。Nacos的设计目标是实现一个易于使用的、功能强大的动态服务发现、配置和服务管理平台，旨在帮助开发者快速构建云原生应用，解决微服务架构中的服务治理问题，提供服务发现、配置管理等核心功能。

Nacos = Spring Cloud 三大组件（注册中心 Eureka + 服务配置 Config + 服务总线 Bus）


```bash
# 进入nacos容器
kubectl exec -it nacos-xxx  -n dev -- /bin/bash

# 获取临时访问token
curl -X POST '127.0.0.1:8848/nacos/v1/auth/login' -d 'username=xxx&password=xxx'

# 查询配置 (把accessToken换成新的)
curl -X GET '127.0.0.1:8848/nacos/v1/cs/configs?accessToken=xxx&dataId=xxx.yaml&group=DEFAULT_GROUP&tenant=xxx'
```

为了确保依赖于 Nacos的应用程序在 Nacos启动并准备好后才能启动，可以在应用容器中使用 Init Containers

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: my-app
    spec:
      initContainers:
        - name: wait-for-nacos
          image: appropriate/curl
          command: ['sh', '-c', 'until curl -s -o /dev/null -f http://nacos:8848/nacos/#/login; do echo waiting for Nacos; sleep 30; done;']
```
curl: 这是一个用于发送HTTP请求的命令行工具。
* -s: 表示“silent”模式，使命令在运行时不输出任何进度信息或错误信息，因此在命令执行时不会显示任何内容。
* -o /dev/null: 指定输出文件为/dev/null，这意味着所有的响应内容都将被丢弃。如果不想保存响应内容而只是想查看HTTP状态码，该选项非常有用。
* -f: 表示“fail silently”。如果HTTP请求返回4xx或5xx状态码，curl将不会输出内容。而是以非零状态码退出。这使得命令可以用来检测请求是否成功。
