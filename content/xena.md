Title: XENA
Date: 2020-09-22
Category: Programming
Author: Yoga

username: Student17

password: xxx

```js
docker ps
docker volumn ls
docker volume rm 文件名和
docker volume create xena-training-volume
docker volume inspect xena-training-volume

docker login xxx.artifactrepo.xxx.com
// username
// password
docker pull xxx.artifactrepo.xxx.com/xena/xena-training-toolbox
docker run -itd --name=xena-training-toolbox --mount source=xena-training-volume,target=/root/xena xxx.artifactrepo.xxx.com/xena/xena-training-toolbox
Copy to clipboard

// open docker extension screen
ll
// /root/xena 
kubectl
git config --global user.email "Student17@its.xxx.com"
git config --global user.name student17
git clone https://sourcecode.xxx.com/scm/asx-ncnl/student17.git
```

JPM Application Development Pipeline

![docker](img/jpm.png)

---

## Jenkins

Jenkinsfile tells Jenkins to use the Jenkins Pipeline Manager Global Shared Library and also tells it to check manifest-sources.yaml file for the location of pipeline manifests that declare the logic of CI/CD jobs.

* Jenkinsfile

```groovy
#!/bin/groovy
@Library('jpm_shared_lib@1.x') _  // imports the latest stable version of JPM
import org.xxx.*
def args = [:]
args.debug = true
args.manifestSourcesFile = 'manifest-sources.yaml' // // tells JPM where to find job configuration
args.environmentMappingFile = 'environment-mapping.yaml'
new stdPipeline().execute(args) // invoke the JPM Standard Pipeline
```

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

## JFrog

JFrog Artifactory 作为 Docker Hub 的拉入式缓存。通过在 JFrog Artifactory 上本地缓存 Docker 映像,对该图像的所有请求首先来自缓存,而不是直接来自 Docker Hub，减少了外部流量。
