

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Flush API](indices-flush.md) [Get alias API »](indices-get-alias.md)

## 强制合并接口

强制合并一个或多个索引的分片。对于数据流，API 强制合并流的支持索引的分片。

    
    
    response = client.indices.forcemerge(
      index: 'my-index-000001'
    )
    puts response
    
    
    POST /my-index-000001/_forcemerge

###Request

"发布/<target>/_forcemerge"

"发布/_forcemerge"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"维护"或"管理"索引权限。

###Description

使用强制合并 API 强制合并一个或多个索引的分片。合并通过将其中一些段合并在一起来减少每个分片中的段数，还可以释放已删除文档使用的空间。合并通常是自动发生的，但有时手动触发合并很有用。

**我们建议仅强制合并只读索引(意味着索引不再接收写入)。** 更新或删除文档时，旧版本不会立即删除，而是软删除并标有"逻辑删除"。这些软删除的文档会在常规段合并期间自动清理。但是强制合并可能会导致产生非常大(> 5GB)的段，这些段不符合常规合并的条件。因此，软删除文档的数量可能会快速增长，从而导致磁盘使用率更高，搜索性能更差。如果定期强制合并索引接收写入，这也会使快照更加昂贵，因为新文档无法增量备份。

#### 强制合并期间的块

调用此 API 块，直到合并完成(除非请求 containswait_for_completion=false，默认为 true)。如果客户端连接在完成之前丢失，则强制合并过程将在后台继续。任何强制合并相同索引的新请求也将阻塞，直到正在进行的强制合并完成。

#### 运行力异步合并

如果请求包含"wait_for_completion=false"，Elasticsearch 会执行一些预检检查，启动请求，并返回一个可用于获取任务状态的"任务"。但是，您无法取消此任务，因为强制合并任务不可取消。Elasticsearch在'_tasks/'处创建此任务的记录作为文档<task_id>。完成任务后，您应该删除任务文档，以便 Elasticsearch 可以回收空间。

#### 强制合并多个索引

您可以通过定位来强制将多个索引与单个请求合并：

* 包含多个后备索引的一个或多个数据流 * 多个索引 * 一个或多个别名 * 集群中的所有数据流和索引

每个目标分片都使用"force_merge"线程池单独强制合并。默认情况下，每个节点只有一个"force_merge"线程，这意味着该节点上的分片一次强制合并一个。如果你在阳极上扩展"force_merge"线程池，那么它将强制并行合并其分片。

强制合并使被合并分片的存储空间暂时增加，如果"max_num_segments"参数设置为"1"，则其大小最多增加一倍，因为所有段都需要重写为新段。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases used to limit the request. Supports wildcards (`*`). To target all data streams and indices, omit this parameter or use `*` or `_all`. 

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

`flush`

     (Optional, Boolean) If `true`, Elasticsearch performs a [flush](indices-flush.html "Flush API") on the indices after the force merge. Defaults to `true`. 
`ignore_unavailable`

     (Optional, Boolean) If `false`, the request returns an error if it targets a missing or closed index. Defaults to `false`. 
`max_num_segments`

    

(可选，整数)要合并到的段数。要完全合并索引，请将其设置为"1"。

默认为检查是否需要执行合并。如果是这样，请执行它。

不能在同一请求中指定此参数和"only_expunge_deletes"。

`only_expunge_deletes`

    

(可选，布尔值)如果为"true"，则清除包含已删除文档百分比超过"index.merge.policy.expunge_deletes_allowed"(默认为 10%)的所有句段。默认为"假"。

在 Lucene 中，文档不会从段中删除;只是标记为已删除。在合并期间，将创建一个不包含这些文档删除内容的新段。

不能在同一请求中指定此参数和"max_num_segments"。

`wait_for_completion`

    

(可选，布尔值)如果为"true"，则请求将阻止，直到操作完成。默认为"真"。

###Examples

#### 强制合并特定数据流或索引

    
    
    response = client.indices.forcemerge(
      index: 'my-index-000001'
    )
    puts response
    
    
    POST /my-index-000001/_forcemerge

#### 强制合并多个数据流或索引

    
    
    response = client.indices.forcemerge(
      index: 'my-index-000001,my-index-000002'
    )
    puts response
    
    
    POST /my-index-000001,my-index-000002/_forcemerge

#### 强制合并所有索引

    
    
    response = client.indices.forcemerge
    puts response
    
    
    POST /_forcemerge

#### 数据流和基于时间的索引

强制合并对于管理数据流的较旧后备索引和其他基于时间的索引非常有用，尤其是在滚动更新之后。在这些情况下，每个索引仅在特定时间段内接收索引流量。一旦索引不再收到写入操作，其分片就可以强制合并到单个段。

    
    
    response = client.indices.forcemerge(
      index: '.ds-my-data-stream-2099.03.07-000001',
      max_num_segments: 1
    )
    puts response
    
    
    POST /.ds-my-data-stream-2099.03.07-000001/_forcemerge?max_num_segments=1

这可能是一个好主意，因为单段分片有时可以使用更简单、更高效的数据结构来执行搜索。

[« Flush API](indices-flush.md) [Get alias API »](indices-get-alias.md)
