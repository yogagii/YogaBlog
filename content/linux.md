Title: Linux 服务器配置
Date: 2022-04-21
Category: Programming
Author: Yoga

## 安装node

1. 到 node 官网

http://nodejs.cn/download/

https://registry.npmmirror.com/binary.html?path=node/ 

去下载一个 linux 可用的 node 版本

2. 传输到服务器 /home/jyu36 并解压

```bash
xz -d node-v14.18.2-linux-x64.tar.xz
tar -xvf node-v14.18.2-linux-x64.tar
```

3. 软连接 (不确定是否必须)

ln -s /home/nodejs/node-v14.18.2-linux-x64/bin/npm /usr/local/bin
ln -s /home/nodejs/node-v14.18.2-linux-x64/bin/node /usr/local/bin

4. 配置环境变量

```bash
vi /etc/profile

export NODEJS_HOME=/home/v-jyu36/node-v14.18.2-linux-x64
export PATH=$PATH:$NODEJS_HOME/bin

source /etc/profile
```

## 安装git

```
yum -y install git 
git --version
```

## 安装pm2

```
npm install pm2 -g
```

## 操作

* 删除单行
```
dd
```

* 删除全部
```
dG
```

* 快速定位
```
/正则匹配
```