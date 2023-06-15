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

## 安装 Docker

* MAC

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
* LINUX

yum install -y yum-utils device-mapper-persistent-data lvm2

yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

yum install -y docker-ce docker-ce-cli [containerd.io](http://containerd.io/)

systemctl start docker --add-host=host.docker.internal:host-gateway

docker -v

---

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

* RUN: 在容器中运行指令的命令。
* CMD: 启动容器时运行指定的命令，Dockerfile 中可以有多个 CMD 指令，但只有最后一个生效，如果 docker run 后面指定有参数，该参数将会替换 CMD 的参数。

创建镜像

```bash
docker build -t getting-started .
```
* -t 镜像名
* . Dockerfile 路径 

列出镜像

```bash
docker image ls
```

删除镜像

```bash
docker rmi <image-id>
```

创建容器

```bash
docker run -dp 3000:3000 getting-started
```
* -d “detached” mode (in the background)
* -p port mapping 'host’s port 3000':'container’s port 3000'

列出容器

```bash
docker ps # 运行中的容器
docker ps -a 
```

停止容器

```bash
docker stop <the-container-id>
```

重启容器

```bash
docker start <the-container-id> # 包含容器文件系统挂载的操作
docker restart <the-container-id> # 不包含容器文件系统的卸载与挂载操作
```
_更新.env文件后得删除容器重建，docker restart/start无用_

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

查看日志

```bash
docker logs <container-id> -f
```

* -f, --follow 实时输出日志，最后一行为当前时间戳的日志

显示容器根目录

```bash
docker exec -it <container-id> ls
```

插件

```bash
docker plugin ls
docker plugin stop <plugin-id>
```
_docker: Error response from daemon: authorization denied by plugin openpolicyagent/opa-docker-authz-v2:0.4: request rejected by administrative policy._

配置

```bash
docker info
docker info | grep Dir
du -hs /var/lib/docker/
df -h /var/lib/docker/

docker system df # 占用的空间
docker system prune # 清理没用的空间
```

### volume mount 数据卷

容器是镜像的实例化。数据如果都在容器中，一旦容器删除，数据就会丢失。

数据卷技术可将容器产生的数据同步到本地，容器之间也可以共享，从而实现容器数据的持久化。

```bash
docker volume ls # 查看Volumes
docker volume inspect todo-db # 查看某个volumn
docker volume rm todo-db # 删除一个 Volume
docker volume create todo-db # 创建一个Volume
```

```bash
docker run -dp 3000:3000 --mount type=volume,src=todo-db,target=/etc/todos getting-started
```

### bind mount

将宿主机中的文件、目录mount到容器上。其上的数据可以被宿主机读写，可以被mount它的所有容器读写。

bind mount the current directory from the host into the /app directory in the container
```bash
docker run -dp 3000:3000 \
  -w /app --mount type=bind,src="$(pwd)",target=/app \
  node:18-alpine \
  sh -c "yarn install && yarn run dev"
```

* -w sets the “working directory” or the current directory that the command will run from

nodemon 是一种工具，可在检测到目录中的文件更改时动重新启动应用程序
```json
// package.json
"scripts": {
  "dev": "nodemon src/index.js"
},
```

### network

```bash
docker network create todo-app
docker network ls
docker network rm todo-app
```

Start a MySQL container and attach it to the network.
```bash
docker run -d \
  --network todo-app --network-alias mysql \
  -v todo-mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=secret \
  -e MYSQL_DATABASE=todos \
  mysql:8.0
```

connect to the database
```bash
docker exec -it <mysql-container-id> mysql -u root -p

# 等价于
docker exec -it <mysql-container-id> bin/bash 
mysql -u root -p
```

Connect app to MySQL
```bash
docker run -dp 3000:3000 \
  -w /app -v "$(pwd):/app" \
  --network todo-app \
  -e MYSQL_HOST=mysql \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD=secret \
  -e MYSQL_DB=todos \
  node:18-alpine \
  sh -c "yarn install && yarn run dev"
```
删除network, database, todo-app都不会使数据丢失

### Docker Compose

Docker Compose is a tool that was developed to help define and share multi-container applications. With Compose, we can create a YAML file to define the services and with a single command, can spin everything up or tear it all down.

管理多个容器的，定义启动顺序的，合理编排，方便管理

docker-compose.yml
```yaml
services:
  app:
    image: node:18-alpine
    command: sh -c "yarn install && yarn run dev"
    ports:
      - 3000:3000
    working_dir: /app
    volumes:
      - ./:/app
    environment:
      MYSQL_HOST: mysql
      MYSQL_USER: root
      MYSQL_PASSWORD: secret
      MYSQL_DB: todos

  mysql:
    image: mysql:8.0
    volumes:
      - todo-mysql-data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: todos

volumes:
  todo-mysql-data:
```
By default, Docker Compose automatically creates a network specifically for the application stack (which is why we didn’t define one in the compose file).

```bash
docker compose up -d
docker compose down # 默认不会删除volume
docker compose down --volumes
```

## .dockerignore

In this case, the node_modules folder should be omitted in the second COPY step because otherwise, it would possibly overwrite files which were created by the command in the RUN step. 
```
node_modules
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

根目录下添加Dockerfile和docker-compose.yml

* Dockerfile：负责导入 Docker 镜像，将它们分为development和production环境，复制我们所有的文件并安装npm依赖项

```ts
// Dockerfile
FROM node:latest // 创建新镜像，使用公共存储库中提供的官方Node.js镜像，并指定版本

WORKDIR /usr/src/app/ // Docker 执行的每个命令(在RUN语句中定义)都将在指定的上下文中执行

COPY package.json ./
COPY package-lock.json ./ // 锁定版本
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
    build: ./
    env_file:
      - .env // 环境变量
    environment:
      DATABASE_UI_HOST: host.docker.internal // 替换localhost
    ports:
      - 3000:3000
    container_name: 'pro_server_container'
    command: npm run start:qa
    volumes:
      - ./dist:/usr/src/app/dist
```
host.docker.internal 是mac和windows的参数，linux环境需在起container时增加--add-host=host.docker.internal:host-gateway

* package.json node dist/main 改用nodemon 执行

```json
{
	"scripts" : {
		"start:qa": "nodemon dist/main",
		"start:prod": "NODE_ENV=production nodemon dist/main",
	},
	"dependencies": {
		"nodemon": "^2.0.20"
	}
}
```
运行 docker compose up -d

取代了pm2 start —watch 意味着不用装node

---

## Watchtower

Watchtower 是一个可以实现自动化更新 Docker 基础镜像与容器的实用工具。它监视正在运行的容器以及相关的镜像，当检测到 reg­istry 中的镜像与本地的镜像有差异时，它会拉取最新镜像并使用最初部署时相同的参数重新启动相应的容器。

```bash
docker run -d \
    --name watchtower \
    --restart unless-stopped \
    -v /var/run/docker.sock:/var/run/docker.sock \
    containrrr/watchtower -c
```
* -s 默认每 5 分钟执行一次 "0 2 * * * *"
* -c 自动清除旧镜像

If pulling images from private Docker registries, supply registry authentication credentials with the environment variables REPO_USER and REPO_PASS or by mounting the host's docker config file into the container 

vi $HOME/.docker/config.json
```json
{
	"auths": {
		"<docker_image_name>": {
      "auth": "<USERNAME>:<PASSWORD> (converted to base 64)",
      "email": "xxx"
    },
	},
	"credsStore": "desktop"
}
```
```bash
docker run -d \
  --name watchtower \
  -v $HOME/.docker/config.json:/config.json \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower -c \
  --interval 300
```
