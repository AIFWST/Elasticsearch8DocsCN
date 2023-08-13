

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Autoscaling APIs](autoscaling-apis.md)

[« Create or update autoscaling policy API](autoscaling-put-autoscaling-
policy.md) [Delete autoscaling policy API »](autoscaling-delete-autoscaling-
policy.md)

## 获取自动伸缩容量接口

此功能专为 ElasticsearchService、Elastic Cloud Enterprise 和 Kubernetes 上的 ElasticCloud 间接使用而设计。不支持直接使用。

获取自动缩放容量。

###Request

    
    
    GET /_autoscaling/capacity/

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_autoscaling"集群权限。有关详细信息，请参阅安全权限。

###Description

此 API 根据配置的自动缩放策略获取当前的自动缩放容量。此 API 将返回信息，以便根据当前工作负载适当调整群集大小。

"required_capacity"计算为为策略启用的所有单个决策程序的"required_capacity"结果的最大值。

操作员应验证"current_nodes"是否与操作员对群集的了解相匹配，以避免根据过时或不完整的信息做出自动缩放决策。

响应包含特定于决策程序的信息，可用于诊断自动缩放确定需要特定容量的方式和原因。此信息仅用于诊断。请勿使用此信息做出自动缩放决策。

### 响应正文

`policies`

    

(对象)包含策略名称到容量结果的映射

"策略"的属性

`<policy_name>`

    

(对象)包含策略的容量信息

""的属性<policy_name>

`required_capacity`

    

(对象)包含策略所需的容量。

"required_capacity"的属性

`node`

    

(对象)包含每个节点所需的最小节点大小，确保单个分片或 ML 作业可以放入单个节点。

"节点"的属性

`storage`

     (integer) Bytes of storage required per node. 
`memory`

     (integer) Bytes of memory required per node. 
`processors`

     (float) Number of processors (vCPUs) required per node. 

`total`

    

(对象)包含策略所需的总大小。

"总计"的属性

`storage`

     (integer) Total bytes of storage required for the policy. 
`memory`

     (integer) Total bytes of memory required for the policy. 
`processors`

     (float) Total number of processors (vCPUs) required for the policy. 

`current_capacity`

    

(对象)包含受策略管理的节点的当前容量，即 Elasticsearch 计算所基于的节点。

"current_capacity"的属性

`node`

    

(对象)包含受策略管理的节点的最大大小。

"节点"的属性

`storage`

     (integer) Maximum bytes of storage of a node. 
`memory`

     (integer) Maximum bytes of memory of a node. 
`processors`

     (float) Maximum number of processors (vCPUs) of a node. 

`total`

    

(对象)包含节点的当前总存储和内存大小由策略管理。

"总计"的属性

`storage`

     (integer) Current bytes of storage available for the policy. 
`memory`

     (integer) Current bytes of memory available for the policy. 
`processors`

     Current number of processors (vCPUs) available for the policy. 

`current_nodes`

    

(对象数组)用于容量计算的节点列表。

"current_nodes"中元素的属性

`name`

     (string) Name of the node. 

`deciders`

    

(对象)容量由各个决策程序产生，允许深入了解如何计算外部级别"required_capacity"。

"决策程序"的属性

`<decider_name>`

    

(对象)为策略启用的特定决策程序的容量结果。

""的属性<decider_name>

`required_capacity`

    

(对象)所需容量由决策程序确定。

"required_capacity"的属性

`node`

    

(对象)包含每个节点所需的最小节点大小，确保单个分片或机器学习作业可以放入单个节点。

"节点"的属性

`storage`

     (integer) Bytes of storage required per node. 
`memory`

     (integer) Bytes of memory required per node. 
`processors`

     (float) Number of processors (vCPUs) required per node. 

`total`

    

(对象)包含策略所需的总大小。

"总计"的属性

`storage`

     (integer) Total bytes of storage required for the policy. 
`memory`

     (integer) Total bytes of memory required for the policy. 
`processors`

     (float) Total number of processors (vCPUs) required for the policy. 

`reason_summary`

     (string) Description of the basis for the decider's result. 
`reason_details`

     (object) A per-decider structure containing details about the basis for the deciders' result. The contents should not be relied on for application purposes and are not subject to backwards compatibility guarantees. 

###Examples

此示例检索当前的自动缩放容量。

    
    
    GET /_autoscaling/capacity

API 返回以下结果：

    
    
    {
      policies: {}
    }

[« Create or update autoscaling policy API](autoscaling-put-autoscaling-
policy.md) [Delete autoscaling policy API »](autoscaling-delete-autoscaling-
policy.md)
