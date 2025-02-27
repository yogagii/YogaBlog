Title: Kubernetes
Date: 2024-04-16
Category: Programming
Tags: CI/CD
Author: Yoga

## Kubernetes

### Docker VS K8S

* Docker是一个轻量级的容器化平台，它允许开发人员将应用程序和其依赖项打包为可移植的容器镜像，并在不同的环境中进行部署。Docker采用单机模式，适用于部署和管理单个主机上的容器。它提供了容器的构建、运行和管理功能，并使得应用程序的部署变得简单和可靠。
* 对于复杂的应用程序，可能需要使用编排工具（如 Docker Compose、Kubernetes）来管理多个容器的部署、协作和扩展。Kubernetes是一个分布式的容器编排工具，适合构建、管理和调度多个容器的集群。它可以管理数千个容器，并提供高自动扩展、负载平衡和故障恢复的功能。

### 核心概念

* Pod：K8S 最小的部署单元，是一组容器的集合。每个 Pod 都由一个特殊的根容器 Pause 容器，以及一个或多个紧密相关的用户业务容器组成。

* Pause 容器作为 Pod 的根容器，以它的状态代表整个容器组的状态。K8S 为每个 Pod 都分配了唯一的 IP 地址，称之为 Pod IP。Pod 里的多个业务容器共享 Pause 容器的IP，共享 Pause 容器挂载的 Volume。

* Label：标签，附加到某个资源上，用于关联对象、查询和筛选。一个 Label 是一个 key=value 的键值对，K8S 通过 Label Selector（标签选择器）来查询和筛选拥有某些 Label 的资源对象

* ReplicaSet（RC）：用来确保预期的 Pod 副本数量，如果有过多的 Pod 副本在运行，系统就会停掉一些 Pod，否则系统就会再自动创建一些 Pod

* Service：定义了一个服务的访问入口，创建 Service 时，K8S会自动为它分配一个全局唯一的虚拟 IP 地址，即 Cluster IP。服务发现就是通过 Service 的 Name 和 Service 的 ClusterIP 地址做一个 DNS 域名映射来解决的

* Namespace：命名空间，Namespace 多用于实现多租户的资源隔离，Namespace 通过将集群内部的资源对象“分配”到不同的Namespace中，形成逻辑上分组的不同项目、小组或用户组

### kubectl

kubectl 是操作 k8s 集群的命令行工具， 可在 k8s 集群的 master 节点执行

mac 安装
```bash
brew install kubectl
kubectl version --client
```

### 容器探针

默认情况下Kubernetes只是检查Pod容器是否正常运行，容器的主进程崩溃，Kubelet将重启容器，但即使进程没有崩溃，有时应用程序运行也会出错，比如访问Web服务器时显示500内部错误，此时http进程依旧运行，重启容器可能是最直接有效的办法。

* liveness probe 存活探针: 检查容器是否还在运行，如果探测失败, 就根据Pod重启策略，判断是否要重启容器
* readiness probe 就绪探针: 保证只有准备好了请求的Pod才能接收客户端请求，如果检查失败，Kubernetes会将该Pod从服务代理的分发后端去除，不再分发请求给该Pod

需要一个判断应用是否正常运行的接口：/healthcheck

### AKS

Azure Kubernetes 服务 (AKS) 是一种托管 Kubernetes 服务

```bash
# login service account
az login --service-principal --tenant xxx -u xxx -p xxx

# 访问 aks
az aks get-credentials --resource-group xxx --name xxx
```

配置kubeconfig
```bash
# 添加 Context
kubectl config set-context prod --cluster=xxx --namespace=default --user=xxx --kubeconfig=$HOME/.kube/kube-prod.config
# 查看 kubeconfig 文件信息
kubectl config view --kubeconfig=$HOME/.kube/kube-prod.config
kubectl config get-contexts --kubeconfig=$HOME/.kube/kube-prod.config 
# 切换 Context
kubectl config use-context prod  --kubeconfig=$HOME/.kube/kube-prod.config
# 查看当前 Context
kubectl config current-context
kubectl config view
# 列出所有 Context 
kubectl config get-contexts
```

https://learn.microsoft.com/zh-cn/azure/aks/learn/quick-kubernetes-deploy-cli

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
Debug

```bash
# 显示资源使用情况：
kubectl top nodes
kubectl top pods --all-namespaces
kubectl get pods --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,CPU_REQUESTS:.spec.containers[*].resources.requests.cpu,CPU_LIMITS:.spec.containers[*].resources.limits.cpu,MEMORY_REQUESTS:.spec.containers[*].resources.requests.memory,MEMORY_LIMITS:.spec.containers[*].resources.limits.memory,AGE:.status.startTime'

kubectl get pods -o wide -n dev
```

Azure Kubernetes Service status is Red, as the total CPU limits is reaching the maximum of a node.

**排查 AKS 群集中 CPU 使用率过高**

https://learn.microsoft.com/zh-cn/troubleshoot/azure/azure-kubernetes/availability-performance/identify-high-cpu-consuming-containers-aks?tabs=command-line#step-2-review-best-practices-to-avoid-high-cpu-usage

Your service will be not stable if the pods are running in system node, since there will have periodic scanning to increase the workload on system node.

service pod 不应该挂载到 system node 上，应该在 working node

要给node pool打label然后在deployment指定label，默认的agentpool=wg1

```yaml
# dev.values.yaml
workerPoolLabel: wg1
# admin-authorization-deployment.yaml
template:
    spec:
      nodeSelector:
        agentpool: {{ .Values.workerPoolLabel }}
```

working node 从之前的 2 个根据系统流量自动扩展到 5 个，业务 pod 不会在 system node 抢系统资源导致不稳定发生

手动部署

```bash
kubectl apply -f . -n namespace
kubectl edit ingress -n namespace authentication
       - backend:
          service:
            name: blob-service
            port:
              number: 80
        path: /api/internal-course/video
        pathType: Prefix
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

  > 四层负载均衡：负载均衡器用 ip+port 接收请求，再直接转发到后端对应服务上；工作在传输层

* kind: Ingress

  Ingress 是一种用于管理外部 HTTP 和 HTTPS 访问到 K8s 集群内服务的资源对象。它提供了更复杂的负载均衡和路由规则，通过一个外部入口点将流量引导到集群内部的服务上。
  对外暴露服务，实现http，域名，URI，证书等请求方式，配置规则，Controller控制器通过service服务发现机制动态实现后端Pod路由转发规则的实现

  > 七层负载均衡：负载均衡器根据 虚拟的 url 或主机名 来接收请求，经过处理后再转向相应的后端服务上；工作在应用层

  Ingress 控制器通常会运行一个反向代理负载均衡器（如 Nginx），接收外部请求并根据定义的规则将请求转发到集群内部的服务

  ```yaml
  apiVersion: networking.k8s.io/v1
  kind: Ingress
  metadata:
    name: authentication
  spec:
    ingressClassName: nginx
    rules:
      - host: dev.xxx.com
        http:
          paths:
            - path: /
              pathType: Prefix
      - host: dev.admin.xxx.com
        http:
          paths:
            - path: /
              pathType: Prefix
  ```

* kind: CronJob

  ```yaml
  apiVersion: batch/v1
  kind: CronJob
  metadata:
    name: job-1
  spec:
    schedule: "*/5 * * * *"
    concurrencyPolicy: Forbid
    jobTemplate:
      spec:
        template:
          spec:
            restartPolicy: OnFailure
            imagePullSecrets:
              - name: "{{ .Values.imagePullSecrets }}"
            containers:
              - name:  {{.Values.businessDataSync.name}}
                image: "{{.Values.businessDataSync.appImage.name}}:{{.Values.businessDataSync.appImage.tag }}"
  ```

  ```ts
  // index.ts
  import { sync } from "./syncData";
  import { uploadToBlob } from "./uploadToBlob";

  async function main() {
    const args = process.argv;

    if (args.includes("--upload")) {
      await uploadToBlob();
    } else {
      await sync();
    }
  }

  main()
    .then(() => {
      process.exit(0);
    })
    .catch(() => {
      process.exit(1);
    });
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
