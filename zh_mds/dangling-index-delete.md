

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Delete component template API](indices-delete-component-template.md)
[Delete alias API »](indices-delete-alias.md)

## 删除悬空索引API

删除悬空索引。

###Request

    
    
    DELETE /_dangling/<index-uuid>?accept_data_loss=true

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。

###Description

如果 Elasticsearch 遇到当前集群状态中缺少的索引数据，则认为这些索引处于悬空状态。例如，如果您在 Elasticsearch 节点处于脱机状态时删除了多个 'cluster.indices.tombstones.size' 索引，则可能会发生这种情况。

通过引用悬空索引的 UUID 来删除该索引。使用 列出悬空索引 API 来查找索引的 UUID。

### 路径参数

`<index-uuid>`

     (Required, string) UUID of the index to delete. You can find this using the [List dangling indices API](dangling-indices-list.html "List dangling indices API"). 

### 查询参数

`accept_data_loss`

     (Optional, Boolean) This field must be set to `true` in order to carry out the import, since it will no longer be possible to recover the data from the dangling index. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

[« Delete component template API](indices-delete-component-template.md)
[Delete alias API »](indices-delete-alias.md)
