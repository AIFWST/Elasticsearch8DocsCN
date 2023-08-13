

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cluster APIs](cluster.md)

[« Cluster allocation explain API](cluster-allocation-explain.md) [Cluster
health API »](cluster-health.md)

## 集群获取设置接口

返回群集范围的设置。

    
    
    response = client.cluster.get_settings
    puts response
    
    
    GET /_cluster/settings

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

###Request

"获取/_cluster/设置"

###Description

默认情况下，此 API 调用仅返回已显式定义的设置，但也可以通过调用"include_defaults"参数来包含默认设置。

### 查询参数

`flat_settings`

     (Optional, Boolean) If `true`, returns settings in flat format. Defaults to `false`. 
`include_defaults`

     (Optional, Boolean) If `true`, returns default cluster settings from the local node. Defaults to `false`. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

[« Cluster allocation explain API](cluster-allocation-explain.md) [Cluster
health API »](cluster-health.md)
