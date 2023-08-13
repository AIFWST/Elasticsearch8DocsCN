

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Get mapping API](indices-get-mapping.md) [Index recovery API »](indices-
recovery.md)

## 导入悬空索引API

导入悬空索引。

###Request

    
    
    POST /_dangling/<index-uuid>?accept_data_loss=true

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。

###Description

如果 Elasticsearch 遇到当前集群状态中缺少的索引数据，则认为这些索引处于悬空状态。例如，如果您在 Elasticsearch 节点处于脱机状态时删除了多个 'cluster.indices.tombstones.size' 索引，则可能会发生这种情况。

通过引用单个索引的 UUID 将单个索引导入集群。使用 Listdangling 索引 API 查找索引的 UUID。

### 路径参数

`<index-uuid>`

     (Required, string) UUID of the index to import, which you can find using the [List dangling indices API](dangling-indices-list.html "List dangling indices API"). 

### 查询参数

`accept_data_loss`

     (Required, Boolean) This field must be set to `true` to import a dangling index. Because Elasticsearch cannot know where the dangling index data came from or determine which shard copies are fresh and which are stale, it cannot guarantee that the imported data represents the latest state of the index when it was last in the cluster. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

以下示例演示如何导入悬空索引：

    
    
    POST /_dangling/zmM4e0JtBkeUjiHD-MihPQ?accept_data_loss=true

API 返回以下响应：

    
    
    {
      "acknowledged" : true
    }

[« Get mapping API](indices-get-mapping.md) [Index recovery API »](indices-
recovery.md)
