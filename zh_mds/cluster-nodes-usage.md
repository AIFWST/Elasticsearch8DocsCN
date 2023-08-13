

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cluster APIs](cluster.md)

[« Cluster update settings API](cluster-update-settings.md) [Nodes hot
threads API »](cluster-nodes-hot-threads.md)

## 节点功能使用接口

返回有关功能使用情况的信息。

###Request

"获取/_nodes/使用情况"

'GET /_nodes/<node_id>/usage'

'获取/_nodes/使用/<metric>'

'GET /_nodes//<node_id>usage/<metric>'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

###Description

群集节点使用情况 API 允许您检索有关每个节点的功能使用情况的信息。此处介绍了所有节点的选择性选项。

### 路径参数

`<metric>`

    

(可选，字符串)将返回的信息限制为特定指标。以下选项的逗号分隔列表：

`_all`

     Returns all stats. 
`rest_actions`

     Returns the REST actions classname with a count of the number of times that action has been called on the node. 

`<node_id>`

     (Optional, string) Comma-separated list of node IDs or names used to limit returned information. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

休息操作示例：

    
    
    response = client.nodes.usage
    puts response
    
    
    GET _nodes/usage

API 返回以下响应：

    
    
    {
      "_nodes": {
        "total": 1,
        "successful": 1,
        "failed": 0
      },
      "cluster_name": "my_cluster",
      "nodes": {
        "pQHNt5rXTTWNvUgOrdynKg": {
          "timestamp": 1492553961812, __"since": 1492553906606, __"rest_actions": {
            "nodes_usage_action": 1,
            "create_index_action": 1,
            "document_get_action": 1,
            "search_action": 19, __"nodes_info_action": 36
          },
          "aggregations": {
            ...
          }
        }
      }
    }

__

|

执行此节点使用请求时的时间戳。   ---|---    __

|

使用情况信息记录开始时的时间戳。这相当于节点启动的时间。   __

|

此节点的搜索操作已调用 19 次。   « 集群更新设置 API 节点热线程 API »