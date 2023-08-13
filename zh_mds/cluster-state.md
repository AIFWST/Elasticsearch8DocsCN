

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cluster APIs](cluster.md)

[« Cluster reroute API](cluster-reroute.md) [Cluster stats API »](cluster-
stats.md)

## 集群状态接口

返回群集状态的内部表示形式，用于调试或诊断目的。

###Request

'获取/_cluster/状态/<metrics>/<target>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

###Description

_cluster state_是一种内部数据结构，可跟踪每个节点所需的各种信息，包括：

* 集群中其他节点的身份和属性 * 集群范围的设置 * 索引元数据，包括每个索引的映射和设置 * 集群中每个分片副本的位置和状态

选定的主节点可确保集群中的每个节点都具有相同集群状态的副本。群集状态 API 允许检索此内部状态的表示形式，以便进行调试或诊断。您可能需要查阅 Elasticsearch 源代码来确定响应的确切含义。

默认情况下，集群状态 API 会将请求路由到选定的主节点，因为此节点是集群状态的权威源。您还可以通过添加查询参数"？local=true"来检索处理 API 请求的节点上保存的集群状态。

Elasticsearch 可能需要花费大量精力来计算在较大的集群中对此 API 的响应，并且响应可能包含大量数据。如果反复使用此 API，您的集群可能会变得不稳定。

响应是内部数据结构的表示形式。它的格式不受与其他更稳定的 API 相同的兼容性保证的约束，并且可能会因版本而异。**请勿使用外部监视工具查询此 API。 相反，请使用其他更稳定的群集 API 获取所需的信息。

### 路径参数

集群状态有时可能非常大，Elasticsearch 在计算对此 API 的响应时可能会消耗大量资源。要减小响应的大小，您可以仅请求您感兴趣的集群状态部分：

`<metrics>`

    

(可选，字符串)以下选项的逗号分隔列表：

`_all`

     Shows all metrics. 
`blocks`

     Shows the `blocks` part of the response. 
`master_node`

     Shows the `master_node` part of the response. 
`metadata`

     Shows the `metadata` part of the response. If you supply a comma separated list of indices, the returned output will only contain metadata for these indices. 
`nodes`

     Shows the `nodes` part of the response. 
`routing_nodes`

     Shows the `routing_nodes` part of the response. 
`routing_table`

     Shows the `routing_table` part of the response. If you supply a comma separated list of indices, the returned output will only contain the routing table for these indices. 
`version`

     Shows the cluster state version. 

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases used to limit the request. Supports wildcards (`*`). To target all data streams and indices, omit this parameter or use `*` or `_all`. 

### 查询参数

`allow_no_indices`

    

(可选，布尔值)如果为"true"，则将忽略解析为无具体索引的通配符索引表达式。(这包括"_all"字符串或未指定索引的情况)。

默认为"真"。

`expand_wildcards`

     (Optional, string) Whether to expand wildcard expression to concrete indices that are open, closed or both. Available options: `open`, `closed`, `none`, `all`. 
`flat_settings`

     (Optional, Boolean) If `true`, returns settings in flat format. Defaults to `false`. 
`ignore_unavailable`

     (Optional, Boolean) If `true`, unavailable indices (missing or closed) will be ignored. 
`local`

     (Optional, Boolean) If `true`, the request retrieves information from the local node only. Defaults to `false`, which means information is retrieved from the master node. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`wait_for_metadata_version`

     (Optional, integer) Waits for the metadata version to be equal or greater than the specified metadata version. 
`wait_for_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Specifies the maximum time to wait for wait_for_metadata_version before timing out. 

###Examples

以下示例仅返回"foo"和"bar"数据流或索引的"元数据"和"routing_table"数据：

    
    
    response = client.cluster.state(
      metric: 'metadata,routing_table',
      index: 'foo,bar'
    )
    puts response
    
    
    GET /_cluster/state/metadata,routing_table/foo,bar

下一个示例返回 'foo' 和 'bar' 的所有可用元数据：

    
    
    response = client.cluster.state(
      metric: '_all',
      index: 'foo,bar'
    )
    puts response
    
    
    GET /_cluster/state/_all/foo,bar

此示例仅返回"块"元数据：

    
    
    response = client.cluster.state(
      metric: 'blocks'
    )
    puts response
    
    
    GET /_cluster/state/blocks

[« Cluster reroute API](cluster-reroute.md) [Cluster stats API »](cluster-
stats.md)
