

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Document APIs](docs.md)

[« Get API](docs-get.md) [Delete by query API »](docs-delete-by-query.md)

## 删除接口

从指定的索引中删除 JSON 文档。

###Request

"删除/<index>/_doc/<_id>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标索引或索引别名具有"删除"或"写入"索引权限。

###Description

使用 DELETE 从索引中删除文档。必须指定索引名和文档 ID。

您无法将删除请求直接发送到数据流。要删除数据流中的文档，必须以包含该文档的支持索引为目标。请参阅更新或删除后备索引中的文档。

##### 乐观并发控制

删除操作可以设置为有条件的，并且仅在为文档的上次修改分配了由"if_seq_no"和"if_primary_term"参数指定的序列号和主要术语时才执行。如果检测到不匹配，该操作将导致"版本冲突异常"和状态代码 409。有关更多详细信息，请参阅乐观并发控制。

#####Versioning

每个编制索引的文档都经过版本控制。删除文档时，可以指定"版本"以确保我们尝试删除的相关文档实际上正在被删除，并且在此期间没有更改。对文档执行的每个写入操作(包括删除操作)都会导致其版本递增。已删除文档的版本号在删除后短时间内保持可用，以允许控制并发操作。已删除文档的版本保持可用的时间长度由"index.gc_deletes"索引设置确定，默认为 60 秒。

#####Routing

如果在编制索引期间使用传送，则还需要指定传送值才能删除文档。

如果"_routing"映射设置为"必需"并且未指定路由值，则删除 API 将引发"路由缺失异常"并拒绝请求。

例如：

    
    
    response = client.delete(
      index: 'my-index-000001',
      id: 1,
      routing: 'shard-1'
    )
    puts response
    
    
    DELETE /my-index-000001/_doc/1?routing=shard-1

此请求删除 ID 为"1"的文档，但它是根据用户路由的。如果未指定正确的工艺路线，则不会删除该文档。

##### 自动创建索引

如果使用外部版本控制变体，则删除操作会自动创建指定的索引(如果不存在)。有关手动创建索引的信息，请参阅创建索引API。

#####Distributed

删除操作被哈希到特定的分片 ID 中。然后，它被重定向到该 id 组中的主分片，并复制(如果需要)到该 id 组中的分片副本。

##### 等待活动分片

发出删除请求时，您可以设置 'wait_for_active_shards' 参数，要求在开始处理删除请求之前，最小数量的分片副本处于活动状态。有关更多详细信息和使用示例，请参阅此处。

#####Refresh

控制此请求所做的更改何时可供搜索。看到'刷新'。

#####Timeout

执行删除操作时，分配用于执行删除操作的主分片可能不可用。造成这种情况的一些原因可能是主分片当前正在从存储中恢复或正在进行重新定位。默认情况下，删除操作将在主分片上等待最多 1 分钟，然后失败并响应错误。"timeout"参数可用于显式指定它等待的时间。下面是将其设置为 5 分钟的示例：

    
    
    response = client.delete(
      index: 'my-index-000001',
      id: 1,
      timeout: '5m'
    )
    puts response
    
    
    DELETE /my-index-000001/_doc/1?timeout=5m

### 路径参数

`<index>`

     (Required, string) Name of the target index. 
`<_id>`

     (Required, string) Unique identifier for the document. 

### 查询参数

`if_seq_no`

     (Optional, integer) Only perform the operation if the document has this sequence number. See [Optimistic concurrency control](docs-index_.html#optimistic-concurrency-control-index "Optimistic concurrency control"). 
`if_primary_term`

     (Optional, integer) Only perform the operation if the document has this primary term. See [Optimistic concurrency control](docs-index_.html#optimistic-concurrency-control-index "Optimistic concurrency control"). 
`refresh`

     (Optional, enum) If `true`, Elasticsearch refreshes the affected shards to make this operation visible to search, if `wait_for` then wait for a refresh to make this operation visible to search, if `false` do nothing with refreshes. Valid values: `true`, `false`, `wait_for`. Default: `false`. 
`routing`

     (Optional, string) Custom value used to route operations to a specific shard. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to [wait for active shards](docs-index_.html#index-wait-for-active-shards "Active shards"). Defaults to `1m` (one minute). 
`version`

     (Optional, integer) Explicit version number for concurrency control. The specified version must match the current version of the document for the request to succeed. 
`version_type`

     (Optional, enum) Specific version type: `external`, `external_gte`. 
`wait_for_active_shards`

    

(可选，字符串)在继续操作之前必须处于活动状态的分片副本数。设置为"all"或任何正整数，最多为索引中的分片总数("number_of_replicas+1")。默认值：1，主分片。

请参阅活动分片。

###Examples

从"my-index-000001"索引中删除 JSON 文档"1"：

    
    
    response = client.delete(
      index: 'my-index-000001',
      id: 1
    )
    puts response
    
    
    DELETE /my-index-000001/_doc/1

API 返回以下结果：

    
    
    {
      "_shards": {
        "total": 2,
        "failed": 0,
        "successful": 2
      },
      "_index": "my-index-000001",
      "_id": "1",
      "_version": 2,
      "_primary_term": 1,
      "_seq_no": 5,
      "result": "deleted"
    }

[« Get API](docs-get.md) [Delete by query API »](docs-delete-by-query.md)
