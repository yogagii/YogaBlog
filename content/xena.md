Title: XENA
Date: 2020-09-22
Category: Programming
Author: Yoga

JPM Application Development Pipeline

> Checkout -> Manifest Load -> Setup --> Unit Test -> Lint -> Static Analysis -> Package -> Publish -> Deploy -> Integration Test -> Regression Test

## Jenkins Pipeline

### 1. Creating JPM Pipeline Job

This can be done **manually** or **automatically** via Automation Pipelines integration hook

* Jenkinsfile

Jenkinsfile tells Jenkins to use the Jenkins Pipeline Manager Global Shared Library and also tells it to check manifest-sources.yaml file for the location of pipeline manifests that declare the logic of CI/CD jobs.

* manifest.yaml

```yaml
version: "1.0"
sources:
  - name: common
    location:
      locationType: project
      file: manifest.yaml
    manifest:
      type: simple
      path: common
      required: true
  - name: environment
    location:
      locationType: project
      file: manifest.yaml
    manifest:
      type: by-environment
      path: environments
      required: true
```

### 2. Job Manifest Environments

* environment-mapping.yaml

```yaml
- branchNamePattern: '(feature|bugfix|hotfix)/.*'
  environment: 'PREDEV'
- branchNamePattern: 'develop'
  environment: 'DEV'
```

branchName 来源于Jenkins job中 Branches to build
### 3. Unit Tests & Lint

npm run test

npm run lint

```yaml
unitTest:
  enabled: true
lint:
  enabled: true
```

### 4. Static Code Analysis

SonarQube increases productivity by enabling development teams to detect duplication and redundancy of code allowing to optimize the code complexity, maintenance time and cost.

```yaml
staticAnalysis:
  enabled: true
  type: multi
  stages:
    sonar:
      type: sonar
      enabled: true
```

### 5. Package

```yaml
package:
  enabled: false
  name: dist/xxx-app
  type: zip
  dir: project
  exclude:
    - Jenkinsfile
    - manifest.yaml
    - manifest-sources.yaml
    - environment-mapping.yaml
  include:
    - dist/**
    - node_modules/**
    - package.json
  versionPackageName: false
  versionFileUpdates:
    - type: node-package
```

## JFrog

JFrog Artifactory 作为 Docker Hub 的拉入式缓存。通过在 JFrog Artifactory 上本地缓存 Docker 映像,对该图像的所有请求首先来自缓存,而不是直接来自 Docker Hub，减少了外部流量。

### 5. Build Docker Image and Publish to Artifactory

```yaml
publish:
  enabled: true
  type: multi
  stages:
    Docker:
      enabled: true
      type: docker
      credsList:
        - registry: https://.artifactrepo.xxx.com
          credentialsId: xxx
```

* _scm_container/<docker_image_name>/container.yaml

pull images directly from the internet and upload them to artifactory in the repo

```yaml
name: <docker_image_name>
tagStrategies:
  dev:
    branches:
      - feature/.*
      - bugfix/.*
      - hotfix/.*
      - develop
      - master
    tags:
      - <tagStrategies>
build: true
artifactoryRepository: xxx
overrideImageSource: true
```

* _scm_container/<docker_image_name>/Dockerfile

build images from a Dockerfile 

```Dockerfile
FROM node:18

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./ # 锁定包版本号，加快安装速度
RUN npm install

COPY ./ ./

CMD ["npm", "run", "build"]
```

### 6. JFrog Xray

JFrog Xray is an enterprise approved tool for scanning of the software artifacts effectively enhancing artifact security and OSS license compliance.

```yaml
buildAnalysis:
  enabled: true
```
### 7. Pull Docker Images From Artifactory

```bash
docker login <account_id>.artifactrepo.xxx.com
 
# You will be prompted with the following
Username: <service_account_username>
Password: <service_account_password>
```

~/.docker/config.json

```json
{
  "auths": {
    "<docker_image_name>": {
      "auth": "<USERNAME>:<PASSWORD> (converted to base 64)",
      "email": "xxx"
    },
    "<docker_image_name>": {}
  },
  "credsStore": "desktop"
}
```

```bash
docker pull <account_id>.artifactrepo.xxx.com/<image_name>:<image_tag>

docker pull xxx.artifactrepo.xxx.com/xena/xena-training-toolbox
docker run -itd --name=xena-training-toolbox --mount source=xena-training-volume,target=/root/xena xxx.artifactrepo.xxx.com/xena/xena-training-toolbox
```

### 8. Deployment to Linux virtual machine via SSH

ssh - which sets up an ssh-agent that uses an ssh key to authenticate with the remote service.

* step1. 本机生成私钥+公钥：

  ssh-keygen -t rsa

  _没有rsa时生成的私钥格式为`-----BEGIN OPENSSH PRIVATE KEY-----` (踩坑：jenkins 2.263 版本在检验密钥时还不支持这种格式)
  加上rsa的私钥格式为`-----BEGIN RSA PRIVATE KEY-----`_
  
  查看本机私钥：cat ~/.ssh/id_rsa

  查看本机公钥：cat ~/.ssh/id_rsa.pub

  ssh-copy-id [user]@[server]

2. 把公钥放到服务器服务器：
    
  cat /home/[user]/.ssh/authorized_keys 确定文件中有公钥
  
  本机：ssh [user]@[server] 若不用输入密码则成功
    
3. 把私钥放到Jenkins
    
  Manage Jenkins → Configure System → SSH remote hosts:
  
  Hostname: 10.xx.xx.xx
  
  Port: 22
  
  Credentials: ADD → Jenkins
  
  Kind: SSH Username with private key
  
  Username: [user]
  
  Private Key：粘贴私钥，需带上Begin和End
  
  Check connection: Successfull connection
  
  Manage Jenkins → Manage Credentials → 复制credentialsId

```yaml
deploy:
  type: ssh
  script: |
      #!/bin/bash
      set -x
      set -e
      mkdir -p unpack
      unzip -d unpack dist/xxx-app.zip
      scp -o StrictHostKeyChecking=no \
      -r unpack/* \
      ${manifest.deploy.userName}@${manifest.deploy.serverName}:${manifest.deploy.applicationDir}
```

ssh 只能连上user，连不上root，打包后的文件只能放在 /home/user，软连接到 /var/www

```json
// package.json
"start:qa": "node dist/main",
```
pm2 start npm --name project-name --watch -- run start:qa 

--watch 只要当前目录下有任意文件发生改变，PM2都会尝试重启进程。
