Title: Kubernetes
Date: 2024-04-16
Category: Programming
Tags: CI/CD
Author: Yoga

## Kubernetes

Azure Cli
```bash
# list available clouds
az cloud list --output table
 
# China Azure
az cloud set --name AzureChinaCloud

# 登录
az login --service-principal --tenant xxx -u xxx -p xxx

# 访问 aks
az aks get-credentials --resource-group xxx --name xxx
```

kubectl 是操作 k8s 集群的命令行工具， 可在 k8s 集群的 master 节点执行
```bash
# 获取所有部署的 service
kubectl get services --all-namespaces
kubectl get pods --all-namespaces

# logs
kubectl logs --tail=100 -n dev pod-xxxxx
kubectl logs -n dev pod-xxxxx | grep -C 10 "your_search_string" #上下行数
kubectl logs pod-xxxxx | grep -A <num_lines> "your_search_string" #下行数

# check the pod docker image tag version, every release there is a new version tagged on bitbucket
kubectl describe pod pod-xxxxx -n qa

kubectl --namespace=dev exec -it pod-xxxxx -- ls -al  
kubectl --namespace=dev exec -it pod-xxxxx-- ls -al /mnt/secrets
kubectl --namespace=dev exec -it pod-xxxxx -- cat /mnt/secrets/AZURE-PASSWORD
```

## Helm

Helm 可以理解为 Kubernetes 的包管理工具，可以方便地发现、共享和使用为Kubernetes构建的应用。

* Chart：Helm应用(package)，包括该应用的所有Kubernetes manifest模版
* Repository：Helm package存储仓库
* Release：chart的部署实例，每个chart可以部署一个或多个release

Helm把Kubernetes资源(比如deployments、services或 ingress等) 打包到一个chart中，而chart被保存到chart仓库。通过chart仓库可用来存储和分享chart。Helm使发布可配置，支持发布应用配置的版本管理，简化了Kubernetes部署应用的版本控制、打包、发布、删除、更新等操作。

Helm 采用客户端/服务器架构

* 客户端 Helm CLI 是一个命令行工具，负责管理charts、reprepository和release
* 服务端 tiller 接收来自 helm 客户端的请求，并把相关资源的操作发送到Kubernetes，负责管理（安装、查询、升级或删除等）和跟踪Kubernetes资源。release的相关信息保存在kubernetes的ConfigMap中。

### Template

在部署kubernetes的时候，会使用kubectl apply -f的命令定义Deployment、Service、ConfigMap等对象

Helm帮助我们管理kubenetes的yaml对象文件，借助go的template语法，将kubernetes对象模板化，并允许自己定义填充模板的值，做到一套模板多个发布，并支持版本管理。

* kind: Deployment

Deployment是一种控制器，用于管理Pod的部署。Deployment确保了在指定的策略下，应用的多个副本可以持续运行，并且如果有任何容器崩溃，Deployment会替换它。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Values.adminAuthorization.name }}
  annotations:
  labels:
    chart: "{{ .Chart.Name }}-{{ .Chart.Version }}"
    app: {{ .Values.adminAuthorization.name }}
    env: {{ .Values.env }}
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  replicas: {{ .Values.adminAuthorization.replicas }} # 副本数量
```

* kind: ConfigMap

ConfigMap是一种API对象，用于存储不包含敏感信息的配置信息，可以用作环境变量、命令行参数、配置文件等。

* kind: Service

kuberntes中四层的负载均衡调度机制，Ingress借助service的服务发现机制实现集群中Pod资源的动态感知

* kind: Ingress
对外暴露服务，实现http，域名，URI，证书等请求方式，配置规则，Controller控制器通过service服务发现机制动态实现后端Pod路由转发规则的实现

* kind: CronJob

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: job-1
spec:
  schedule: "*/5 * * * *"
  concurrencyPolicy: Forbid
```

### Package Stage

In order to package the helm chart the root project directory must contain a _scm_helm directory with a Chart.yaml file inside of it.

```yaml
# manifest.yaml
package:
  enabled: true
  type: helm
  lint: true
  chartExtraRepos:
    - name: #repo name
      url: #repo url
      credentialsId: #credentialsId, if needed, to access the helm repo 
  versionFileUpdates:
    - type: yaml
      file: _scm_helm/Chart.yaml
      path: version
```

### Publish Stage

In order to publish a helm chart it must first be packaged using the packageHelmChart function and stashed to the project stash. 

```yaml
publish:
  type: helm
  publicChart: false
  chartRepo: #artifactory repository (team key for the repo for the chart to be published to)
```

### Deploy Stage

Deploys a published Helm chart to a Kubernetes cluster.

```yaml
deploy:
  enabled: false
  type: helm
  name: #name of helm release
  helmUpgradeAdditionalArgs: #helm upgrade command additional args
  atomic: true
  kubernetesConfig: # configuration for connecting to kubernetes
    type: aks
    region: #clusterRegion
    credentialsId: #VPCx api user credentials
    name: #cluster name
```
