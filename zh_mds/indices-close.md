

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Clone index API](indices-clone-index.md) [Create index API »](indices-
create-index.md)

## 关闭索引接口

关闭索引。

    
    
    response = client.indices.close(
      index: 'my-index-000001'
    )
    puts response
    
    
    POST /my-index-000001/_close

###Request

"发布/<index>/_close"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标索引或索引别名具有"管理"索引权限。

###Description

您可以使用关闭索引 API 关闭打开的索引。

关闭的索引被阻止进行读/写操作，并且不允许打开的索引允许的所有操作。无法为文档编制索引或在封闭索引中搜索文档。这允许闭合索引不必维护内部数据结构来索引或搜索文档，从而减少集群上的开销。

打开或关闭索引时，主节点负责重新启动索引分片以反映索引的新状态。然后，分片将经历正常的恢复过程。集群会自动复制打开/关闭索引的数据，以确保始终安全地保留足够的分片副本。

您可以打开和关闭多个索引。如果请求显式引用缺少的索引，则会引发错误。可以使用"ignore_unavailable=true"参数禁用此行为。

默认情况下，必须显式命名要打开或关闭的索引。要使用"_all"、"*"或其他通配符表达式打开或关闭索引，请将"action.destructive_requires_name"设置更改为"false"。也可以通过群集更新设置 API 更改此设置。

关闭的索引会占用大量磁盘空间，这可能会导致托管环境中出现问题。可以通过群集设置 API 禁用关闭索引，方法是将"cluster.indices.close.enable"设置为"false"。默认值为"真"。

### 路径参数

`<index>`

    

(可选，字符串)索引名称的逗号分隔列表或通配符表达式用于限制请求。

要关闭所有索引，请使用"_all"或"*"。默认情况下，必须显式命名要关闭的索引。若要指定以"_all"、"*"或其他通配符表达式结尾的索引，请将"action.destructive_requires_name"设置更改为"false"。您可以在"elasticsearch.yml"文件中或使用群集更新设置 API 更新此设置。

### 查询参数

`allow_no_indices`

    

(可选，布尔值)如果为"false"，则当任何通配符表达式、索引别名或"_all"值仅针对缺少或关闭的索引时，请求将返回错误。即使请求以其他打开的索引为目标，此行为也适用。例如，如果索引以"foo"开头但没有索引以"bar"开头，则以"foo*，bar*"为目标的请求将返回错误。

默认为"真"。

`expand_wildcards`

    

(可选，字符串)通配符模式可以匹配的索引类型。如果请求可以以数据流为目标，则此参数确定通配符表达式是否与隐藏的数据流匹配。支持逗号分隔的值，例如"打开，隐藏"。有效值为：

`all`

     Match any data stream or index, including [hidden](api-conventions.html#multi-hidden "Hidden data streams and indices") ones. 
`open`

     Match open, non-hidden indices. Also matches any non-hidden data stream. 
`closed`

     Match closed, non-hidden indices. Also matches any non-hidden data stream. Data streams cannot be closed. 
`hidden`

     Match hidden data streams and hidden indices. Must be combined with `open`, `closed`, or both. 
`none`

     Wildcard patterns are not accepted. 

默认为"打开"。

`ignore_unavailable`

     (Optional, Boolean) If `false`, the request returns an error if it targets a missing or closed index. Defaults to `false`. 
`wait_for_active_shards`

    

(可选，字符串)在继续操作之前必须处于活动状态的分片副本数。设置为"all"或任何正整数，最多为索引中的分片总数("number_of_replicas+1")。默认值：1，主分片。

请参阅活动分片。

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

以下示例演示如何关闭索引：

    
    
    response = client.indices.close(
      index: 'my-index-000001'
    )
    puts response
    
    
    POST /my-index-000001/_close

API 返回以下响应：

    
    
    {
      "acknowledged": true,
      "shards_acknowledged": true,
      "indices": {
        "my-index-000001": {
          "closed": true
        }
      }
    }

[« Clone index API](indices-clone-index.md) [Create index API »](indices-
create-index.md)
