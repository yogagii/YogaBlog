Title: XENA
Date: 2020-08-21
Category: Analytics
Tags: Docker
Author: Yoga

```
git clone https://github.com/docker/getting-started.git

cd getting-started
docker build -t docker101tutorial

docker run -d -p 80:80 \ —name docker-tutorial docker101tutorial

docker tag docker101tutorial yogadock/docker101tutorial
docker push yogadock/docker101tutorial

```

## XENA

username: TST-ITS-SCMStudent17

password: Scm$tudent17a

```js
docker ps
docker volumn ls
docker volume rm 文件名和
docker volume create xena-training-volume
docker volume inspect xena-training-volume

docker login jnj.artifactrepo.jnj.com
// username
// password
docker pull jnj.artifactrepo.jnj.com/xena/xena-training-toolbox
docker run -itd --name=xena-training-toolbox --mount source=xena-training-volume,target=/root/xena jnj.artifactrepo.jnj.com/xena/xena-training-toolbox
Copy to clipboard

// open docker extension screen
ll
// /root/xena 
kubectl
git config --global user.email "TST-ITS-SCMStudent#@its.jnj.com"
git config --global user.name student#
git clone https://sourcecode.jnj.com/scm/asx-ncnl/student#.git
```

JPM Application Development Pipeline

![docker](img/jpm.png)

