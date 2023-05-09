Title: Docker
Date: 2022-05-04
Category: Programming
Author: Yoga

Docker的三个基本概念:

* Image 镜像
* Container 容器
* Repository 仓库

在第一次部署项目的时候把项目等环境直接放进docker里面，下次要迁移项目到另一台服务器上时，把docker镜像上传到docker仓库上，再另一台服务器直接拉取。

Image是类，Container是镜像的可运行实例，类只有一个，但可以new出千千万万个实例对象。可以使用DockerAPI或CLI创建、启动、停止、移动或删除容器。

Get the app

安装 homebrew: 

```bash
/bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"
```
安装 docker:

```bash
brew install --cask --appdir=/Applications docker
```
打开蓝色小鲸鱼APP：Docker

```bash
docker --version
```

添加 Dockerfile

```bash
git clone https://github.com/docker/getting-started.git

cd getting-started/app
vi Dockerfile
```

```Dockerfile
# syntax=docker/dockerfile:1
   
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN yarn install --production
CMD ["node", "src/index.js"]
EXPOSE 3000
```

创建镜像

```bash
docker build -t getting-started .
```
* -t 镜像名
* . Dockerfile 路径 

创建容器

```bash
docker run -dp 3000:3000 getting-started
```
* -d “detached” mode (in the background)
* -p port mapping 'host’s port 3000':'container’s port 3000'

列出容器

```bash
docker ps
```

停止容器

```bash
docker stop <the-container-id>
```

删除容器

```bash
docker rm <the-container-id>
```

* -f 不用先停止，强制删除容器

上传镜像到 Docker Hub

```bash
docker login -u yogadock
docker image ls

# docker tag SOURCE_IMAGE[:TAG] USER-NAME/TARGET_IMAGE[:TAG]
docker tag getting-started yogadock/getting-started
docker push yogadock/getting-started
```
* 不指定tag默认latest

在虚机上运行新实例

Play with Docker: https://labs.play-with-docker.com/

```bash
docker run -dp 3000:3000 yogadock/getting-started
```

数据卷(volumes)

容器是镜像的实例化。数据如果都在容器中，一旦容器删除，数据就会丢失。

数据卷技术可将容器产生的数据同步到本地，容器之间也可以共享，从而实现容器数据的持久化。

```bash
docker volumn ls # 查看Volumes
docker volume inspect xena-training-volume # 查看某个volumn
docker volume rm xena-training-volume # 删除一个 Volume
docker volume create xena-training-volume # 创建一个Volume
```

---

## Docker 安装phpmyadmin

https://hub.docker.com/_/phpmyadmin

```bash
docker run --name myadmin -d -e PMA_ARBITRARY=1 -p 4000:80 phpmyadmin

docker ps
```

| CONTAINER ID | IMAGE | PORTS | NAMES
| - | - | - | -
0bfccc26fcfe | phpmyadmin | 0.0.0.0:4000 -> 80/tcp | myadmin

```
docker stop 0bfccc26fcfe
docker rm 0bfccc26fcfe
```
nginx
```
location /php/ {
  rewrite "^/php/(.*)$" /$1 break;
  proxy_set_header Host $host;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_set_header X-Forwarded-Proto $scheme;
  proxy_buffering off;
  proxy_pass http://10.216.104.80:4000;
}
```

---

## NestJs

使用 Docker 将NestJs应用容器化

```md
# README.md
# watch docker mode
$ docker-compose up -d ./docker/docker-compose.dev.yml

# production docker mode
$ docker-compose up -d ./docker/docker-compose.yml
```

* Dockerfile：负责导入 Docker 镜像，将它们分为development和production环境，复制我们所有的文件并安装npm依赖项

```ts
// Dockerfile
FROM node:latest // 创建新镜像，使用公共存储库中提供的官方Node.js镜像，并指定版本

WORKDIR /usr/src/app/ // Docker 执行的每个命令(在RUN语句中定义)都将在指定的上下文中执行

COPY package.json ./
RUN npm install

COPY ./ ./

CMD ["npm", "run", "build"]
```

* docker-compose.yml：负责定义我们的容器、应用程序其他服务所需的图像、存储卷、环境变量等

```ts
// docker/docker-compose.yml
version: '3.5'

services:
  pro_server_container:
    build: ../
    ports:
      - 3000:3000
    container_name: 'pro_server_container'
    command: npm run start:prod
    volumes:
      - ../dist:/usr/src/app/dist
```
