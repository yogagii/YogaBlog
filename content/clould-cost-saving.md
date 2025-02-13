Title: Cloud Cost Saving
Date: 2025-02-13
Category: Cloud
Tags: Azure
Author: Yoga

## AKS

以下是降低Azure服务成本的四种方法的比较：

**1. 使用 Azure Kubernetes 服务 (AKS) 中的群集自动缩放程序**

Azure AKS是有autoscaling能力的，它可以监测node上所有pod的综合负载，在超过阈值时自动减少node数量或增加数量，min/max的node数量可以指定，autoscaling有默认规则，也可以进一步定制化。

https://learn.microsoft.com/zh-cn/azure/aks/cluster-autoscaler?tabs=azure-cli

- **原理**：AKS的集群自动缩放程序可以根据集群的资源需求自动调整节点池中的节点数量。当工作负载增加时，自动缩放程序会添加更多节点；当工作负载减少时，它会移除多余的节点，从而优化资源使用并降低成本。
- **优点**：无需手动干预，能够根据实时需求动态调整资源，确保在满足应用性能要求的同时，避免资源浪费。
- **缺点**：需要一定的时间来响应资源需求的变化，可能会存在短暂的资源不足或过剩的情况。

**2. 使用 Kubernetes Event-driven Autoscaling (KEDA) 加载项简化的应用程序自动缩放**

AKS支持Kubernetes Event-driven Autoscaling (KEDA) 方式来使用external event driven的方式来支持application scale-to-zero。但使用KEDA的方式相对复杂

https://learn.microsoft.com/zh-cn/azure/aks/keda-about

- **原理**：KEDA是一种开源组件，可以根据事件数量动态缩放工作负载。它通过扩展Kubernetes的自定义资源定义（CRD），即_ScaledObject_，来描述应用程序应如何根据特定流量进行缩放。
- **优点**：提供了更细粒度的控制，能够根据实际的事件流量进行缩放，避免了基于资源利用率的传统缩放方法可能导致的过度配置。此外，KEDA支持丰富的Azure KEDA缩放器，可以与多种事件源集成，实现更灵活的缩放策略。
- **缺点**：需要与Kubernetes的水平Pod自动缩放器（HPA）配合使用，且在某些情况下，可能会因为事件源的复杂性而导致配置和管理较为复杂。

**3. 定时启动和停止 Azure Kubernetes 服务 (AKS) 节点池**

shutdown AKS里的node pool，通过CLI 命令行可以把AKS里的node pool关闭（system pool不能关闭），这样node pool就降为0了

https://learn.microsoft.com/zh-cn/azure/aks/start-stop-nodepools

- **原理**：通过设置定时任务，在业务高峰期启动节点池，在业务低谷期停止节点池。这样可以在不需要资源时节省成本，同时在需要时快速恢复服务。
- **优点**：能够根据已知的业务周期性需求，精确控制资源的使用时间，避免在非工作时间支付不必要的费用。
- **缺点**：需要预先知道业务的高峰期和低谷期，并且在业务需求突然变化时，可能无法及时调整。

**4. 定时停止和启动 Azure Kubernetes 服务 (AKS) 群集**

https://learn.microsoft.com/zh-cn/azure/aks/start-stop-cluster?tabs=azure-cli

- **原理**：与定时启动和停止节点池类似，但操作对象是整个AKS集群。在不需要使用集群时，将其完全停止，以节省所有相关资源的成本；在需要时再启动集群。
- **优点**：最大程度地节省成本，因为当集群停止时，不会产生任何计算资源的费用。
- **缺点**：启动和停止整个集群可能需要更长的时间，这可能会导致服务中断。此外，频繁地启动和停止集群可能会对集群的稳定性和性能产生一定影响。

总结
- 如果你的工作负载具有可预测的周期性需求，并且你希望在非工作时间节省成本，**定时启动和停止节点池**或**定时停止和启动AKS集群**可能是较好的选择。
- 如果你的工作负载需求变化较为频繁且不可预测，**使用AKS的集群自动缩放程序**或**KEDA**将更适

### 定时启动和停止整个AKS集群

vi ~/.bashrc
```bash
# AZURE SPN
export AZURE_CLIENT_ID="xxx"
export AZURE_CLIENT_SECRET="xxx"
```
source ~/.bashrc

vi start-aks.sh
```sh
#!/bin/bash

CLUSTER_NAME="xxx"
RESOURCE_GROUP="xxx"
TENANT="xxx"
SUBSCRIPTION="xxx"
LOG_FILE="aks_log.txt"

az cloud set --name AzureChinaCloud
az login --service-principal --tenant $TENANT -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET
az account set --subscription $SUBSCRIPTION

# 记录当前时间
echo "$(date): Starting AKS cluster '$CLUSTER_NAME' ..." >> $LOG_FILE

# 运行Azure CLI命令以启动AKS
az aks start --name $CLUSTER_NAME --resource-group $RESOURCE_GROUP

# 检查命令的退出状态
if [ $? -eq 0 ]; then
    echo "$(date): Successfully started AKS cluster '$CLUSTER_NAME'." >> $LOG_FILE
else
    echo "$(date): Failed to start AKS cluster '$CLUSTER_NAME'." >> $LOG_FILE
fi
```

crontab -e
```bash
0 18 * * * /bin/bash /app/aks/start-aks.sh
```
