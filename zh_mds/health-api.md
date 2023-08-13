

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cluster APIs](cluster.md)

[« Cluster health API](cluster-health.md) [Cluster reroute API »](cluster-
reroute.md)

## 健康接口

一个 API，用于报告 Elasticsearch 集群的健康状态。

###Request

"获取/_health_report"

"获取/_health_report/<indicator>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

###Description

运行状况 API 返回一个报告，其中包含 Elasticsearchcluster 的健康状态。该报告包含组成 Elasticsearchfunctional 的指标列表。

每个指示器的运行状况为："绿色"、"未知"、"黄色"或"红色"。该指标将提供解释和元数据，说明其当前健康状况的原因。

群集的状态由最差指示器状态控制。

如果指标的状态为非绿色，则指标结果中可能会出现影响列表，详细说明受健康问题负面影响的功能。每次影响都带有严重性级别、受影响的系统区域以及对系统影响的简单描述。

某些运行状况指示器可以确定运行状况问题的根本原因，并规定一组可以执行的步骤，以改善系统的运行状况。根本原因和补救步骤包含在"诊断"中。诊断包含详细说明根本原因分析的原因、包含解决问题所执行步骤的简要说明的操作、受影响资源的列表(如果适用)以及用于修复诊断问题的详细分步故障排除指南。

健康指标对非绿色健康状况进行根本原因分析。当频繁调用时，这可能会产生计算开销。设置运行状况的 API 自动轮询时，将"详细"设置为"false"以禁用更昂贵的分析逻辑。

### 路径参数

`<indicator>`

    

(可选，字符串)将返回的信息限制为特定指标。支持的指标包括：

`master_is_stable`

     Reports health issues regarding the stability of the node that is seen as the master by the node handling the health request. In case of enough observed master changes in a short period of time this indicator will aim to diagnose and report back useful information regarding the cluster formation issues it detects. 
`shards_availability`

     Reports health issues regarding shard assignments. 
`disk`

     Reports health issues caused by lack of disk space. 
`ilm`

     Reports health issues related to Indexing Lifecycle Management. 
`repository_integrity`

     Tracks repository integrity and reports health issues that arise if repositories become corrupted. 
`slm`

     Reports health issues related to Snapshot Lifecycle Management. 
`shards_capacity`

     Reports health issues related to the shards capacity of the cluster. 

### 查询参数

`verbose`

     (Optional, Boolean) If `true`, the response includes additional details that help explain the status of each non-green indicator. These details include additional troubleshooting metrics and sometimes a root cause analysis of a health status. Defaults to `true`. 
`size`

     (Optional, integer) The maximum number of affected resources to return. As a diagnosis can return multiple types of affected resources this parameter will limit the number of resources returned for each type to the configured value (e.g. a diagnosis could return `1000` affected indices and `1000` affected nodes). Defaults to `1000`. 

### 响应正文

`cluster_name`

     (string) The name of the cluster. 
`status`

    

(可选，字符串)群集的运行状况，基于群集中所有指标的聚合状态。如果请求特定指标的运行状况，则将省略此顶级状态。状态为：

`green`

     The cluster is healthy. 
`unknown`

     The health of the cluster could not be determined. 
`yellow`

     The functionality of a cluster is in a degraded state and may need remediation to avoid the health becoming `red`. 
`red`

     The cluster is experiencing an outage or certain features are unavailable for use. 

`indicators`

    

(对象)有关群集指示器运行状况的信息。

"指标"的属性

`<indicator>`

    

(对象)包含指示器的运行状况结果。

""的属性<indicator>

`status`

    

(字符串)指标的运行状况。状态为：

`green`

     The indicator is healthy. 
`unknown`

     The health of the indicator could not be determined. 
`yellow`

     The functionality of an indicator is in a degraded state and may need remediation to avoid the health becoming `red`. 
`red`

     The indicator is experiencing an outage or certain features are unavailable for use. 

`symptom`

     (string) A message providing information about the current health status. 
`details`

     (Optional, object) An object that contains additional information about the cluster that has lead to the current health status result. This data is unstructured, and each indicator returns [a unique set of details](health-api.html#health-api-response-details "Indicator Details"). Details will not be calculated if the `verbose` property is set to false. 
`impacts`

    

(可选，数组)如果返回非正常状态，指示器可能包括此运行状况对群集的影响列表。

"影响"的属性

`severity`

     (integer) How important this impact is to the functionality of the cluster. A value of 1 is the highest severity, with larger values indicating lower severity. 
`description`

     (string) A description of the impact on the cluster. 
`impact_areas`

    

(字符串数组)这会影响的群集功能区域。可能的值为：

* "搜索" * "摄取" * "备份" * "deployment_management"

`diagnosis`

    

(可选，数组)如果返回不正常状态，指示器可能包括一个诊断列表，这些诊断列表封装了运行状况问题的原因以及为修正问题而要采取的操作。如果"详细"属性为假，则不会计算诊断。

"诊断"的属性

`cause`

     (string) A description of a root cause of this health problem. 
`action`

     (string) A brief description the steps that should be taken to remediate the problem. A more detailed step-by-step guide to remediate the problem is provided by the `help_url` field. 
`affected_resources`

     (Optional, array of strings) If the root cause pertains to multiple resources in the cluster (like indices, shards, nodes, etc…​) this will hold all resources that this diagnosis is applicable for. 
`help_url`

     (string) A link to the troubleshooting guide that'll fix the health problem. 

### 指标详情

运行状况 API 中的每个运行状况指示器都会返回一组详细信息，以进一步说明系统的状态。详细信息具有每个指标独有的内容和结构。

####master_is_stable

`current_master`

    

(对象)有关当前当选的主控服务器的信息。

"current_master"的属性

`node_id`

     (string) The node id of the currently elected master, or null if no master is elected. 
`name`

     (string) The node name of the currently elected master, or null if no master is elected. 

`recent_masters`

    

(可选，数组)在最近的时间窗口中已选择或替换为主节点的列表。如果主节点变化得足够快以引起问题，则此字段存在，并且当指示器为"绿色"时，也会显示为附加信息。此数组仅包含选定的主控形状，并且 _not_ 不包含没有选定主控形状的时间段的空条目。

"recent_masters"的属性

`node_id`

     (string) The node id of a recently active master node. 
`name`

     (string) The node name of a recently active master node. 

`exception_fetching_history`

    

(可选，对象)如果正在查询的节点发现选定的主节点反复降级，则会从最近选择的主节点请求主节点历史记录以进行诊断。如果获取此远程历史记录失败，则会在此详细信息字段中返回异常信息。

"exception_fetching_history"的属性

`message`

     (string) The exception message for the failed history fetch operation. 
`stack_trace`

     (string) The stack trace for the failed history fetch operation. 

`cluster_formation`

    

(可选，数组)如果最近没有选定的主节点，则被查询的节点将尝试收集有关集群无法形成的原因的信息，或者为什么被查询的节点无法加入集群(如果已形成)。此数组可以包含每个主节点的集群形成视图的任何条目。

"cluster_formation"的属性

`node_id`

     (string) The node id of a master-eligible node 
`name`

     (Optional, string) The node name of a master-eligible node 
`cluster_formation_message`

     (string) A detailed description explaining what went wrong with cluster formation, or why this node was unable to join the cluster if it has formed. 

####shards_availability

`unassigned_primaries`

     (int) The number of primary shards that are unassigned for reasons other than initialization or relocation. 
`initializing_primaries`

     (int) The number of primary shards that are initializing or recovering. 
`creating_primaries`

     (int) The number of primary shards that are unassigned because they have been very recently created. 
`restarting_primaries`

     (int) The number of primary shards that are relocating because of a node shutdown operation. 
`started_primaries`

     (int) The number of primary shards that are active and available on the system. 
`unassigned_replicas`

     (int) The number of replica shards that are unassigned for reasons other than initialization or relocation. 
`initializing_replicas`

     (int) The number of replica shards that are initializing or recovering. 
`restarting_replicas`

     (int) The number of replica shards that are relocating because of a node shutdown operation. 
`started_replicas`

     (int) The number of replica shards that are active and available on the system. 

####disk

`indices_with_readonly_block`

     (int) The number of indices the system enforced a read-only index block (`index.blocks.read_only_allow_delete`) on because the cluster is running out of space. 
`nodes_with_enough_disk_space`

     (int) The number of nodes that have enough available disk space to function. 
`nodes_over_high_watermark`

     (int) The number of nodes that are running low on disk and it is likely that they will run out of space. Their disk usage has tripped the [high watermark threshold](modules-cluster.html#cluster-routing-watermark-high). 
`nodes_over_flood_stage_watermark`

     (int) The number of nodes that have run out of disk. Their disk usage has tripped the [flood stage watermark threshold](modules-cluster.html#cluster-routing-flood-stage). 
`unknown_nodes`

     (int) The number of nodes for which it was not possible to determine their disk health. 

####repository_integrity

`total_repositories`

     (Optional, int) The number of currently configured repositories on the system. If there are no repositories configured then this detail is omitted. 
`corrupted_repositories`

     (Optional, int) The number of repositories on the system that have been determined to be corrupted. If there are no corrupted repositories detected, this detail is omitted. 
`corrupted`

     (Optional, array of strings) If corrupted repositories have been detected in the system, the names of up to ten of them are displayed in this field. If no corrupted repositories are found, this detail is omitted. 

####ilm

`ilm_status`

     (string) The current status of the Indexing Lifecycle Management feature. Either `STOPPED`, `STOPPING`, or `RUNNING`. 
`policies`

     (int) The number of index lifecycle policies that the system is managing. 
`stagnating_indices`

     (int) the number of indices managed by index lifecycle management that has been stagnant longer than expected. 
`stagnating_indices_per_action`

    

(可选，地图)按操作分组的停滞时间比预期更长的指数数量摘要。

"stagnating_indices_per_action"的属性

`downsample`

     (int) The number of stagnant indices in the `downsample` action. 
`allocate`

     (int) The number of stagnant indices in the `allocate` action. 
`shrink`

     (int) The number of stagnant indices in the `shrink` action. 
`searchable_snapshot`

     (int) The number of stagnant indices in the `searchable_snapshot` action. 
`rollover`

     (int) The number of stagnant indices in the `rollver` action. 
`forcemerge`

     (int) The number of stagnant indices in the `forcemerge` action. 
`delete`

     (int) The number of stagnant indices in the `delete` action. 
`migrate`

     (int) The number of stagnant indices in the `migrate` action. 

####slm

`slm_status`

     (string) The current status of the Snapshot Lifecycle Management feature. Either `STOPPED`, `STOPPING`, or `RUNNING`. 
`policies`

     (int) The number of snapshot policies that the system is managing. 
`unhealthy_policies`

     (map) A detailed view on the policies that are considered unhealthy due to having several consecutive unssuccesful invocations. The `count` key represents the number of unhealthy policies (int). The `invocations_since_last_success` key will report a map where the unhealthy policy name is the key and it's corresponding number of failed invocations is the value. 

####shards_capacity

`data`

    

(地图)包含不属于冻结层的数据节点的分片当前容量信息的视图。

"数据"的属性

`max_shards_in_cluster`

     (int) Indicates the maximum number of shards that the cluster can hold. 
`current_used_shards`

     (optional, int) The total number of shards hold by the cluster. Only displayed in the case the indicator's status is `red` or `yellow`. 

`frozen`

    

(地图)包含属于冻结层的数据节点的分片当前容量信息的视图。

"冷冻"的性质

`max_shards_in_cluster`

     (int) Indicates the maximum number of shards the cluster can hold for the partially mounted indices. 
`current_used_shards`

     (optional, int) The total number of shards the partially mounted indices have in the cluster. Only displayed in the case the indicator's status is `red` or `yellow`. 

###Examples

    
    
    response = client.health_report
    puts response
    
    
    GET _health_report

无论当前状态如何，API 都会返回包含所有指标的响应。

    
    
    response = client.health_report(
      feature: 'shards_availability'
    )
    puts response
    
    
    GET _health_report/shards_availability

API 仅返回分片可用性指示器的响应。

    
    
    response = client.health_report(
      verbose: false
    )
    puts response
    
    
    GET _health_report?verbose=false

API 返回包含所有运行状况指标的响应，但不会计算响应的详细信息或根本原因分析。如果要监视运行状况 API，并且不希望每次调用计算其他故障排除详细信息的开销，这将非常有用。

[« Cluster health API](cluster-health.md) [Cluster reroute API »](cluster-
reroute.md)
