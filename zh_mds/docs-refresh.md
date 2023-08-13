

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Document APIs](docs.md)

[« Multi term vectors API](docs-multi-termvectors.md) [Optimistic
concurrency control »](optimistic-concurrency-control.md)

##'？刷新'

索引、更新、删除和批量 API 支持设置"刷新"，以控制何时此请求所做的更改对搜索可见。以下是允许的值：

空字符串或"true"

     Refresh the relevant primary and replica shards (not the whole index) immediately after the operation occurs, so that the updated document appears in search results immediately. This should **ONLY** be done after careful thought and verification that it does not lead to poor performance, both from an indexing and a search standpoint. 
`wait_for`

     Wait for the changes made by the request to be made visible by a refresh before replying. This doesn't force an immediate refresh, rather, it waits for a refresh to happen. Elasticsearch automatically refreshes shards that have changed every `index.refresh_interval` which defaults to one second. That setting is [dynamic](index-modules.html#dynamic-index-settings "Dynamic index settings"). Calling the [Refresh](indices-refresh.html "Refresh API") API or setting `refresh` to `true` on any of the APIs that support it will also cause a refresh, in turn causing already running requests with `refresh=wait_for` to return. 
`false` (the default)

     Take no refresh related actions. The changes made by this request will be made visible at some point after the request returns. 

#### 选择要使用的设置

除非您有充分的理由等待更改变得可见，否则请始终使用"刷新=false"(默认设置)。最简单和最快的选择是从 URL 中省略"刷新"参数。

如果绝对必须使请求所做的更改与请求同步可见，则必须在Elasticsearch上放置更多负载("true")和等待响应("wait_for")之间进行选择。以下是应该为该决定提供信息的几点：

* 与"true"相比，对索引所做的更改越多，"wait_for"节省的工作量就越多。如果索引每"index.refresh_interval"只更改一次，则不会节省任何工作。  * "true"创建效率较低的索引构造(微小段)，这些构造稍后必须合并到更高效的索引构造(较大的段)中。这意味着"true"的成本在索引时支付以创建小段，在搜索时支付以搜索小段，在合并时支付以创建较大的段。  * 切勿连续启动多个"刷新=wait_for"请求。相反，将它们批处理成一个带有"refresh=wait_for"的批量请求，Elasticsearch 将并行启动它们，只有在它们全部完成后才会返回。  * 如果刷新间隔设置为"-1"，则禁用自动刷新，则具有"refresh=wait_for"的请求将无限期等待，直到某些操作导致刷新。相反，将"index.refresh_interval"设置为比默认值(如"200ms")短的内容将使"刷新=wait_for"恢复得更快，但仍会产生低效的段。  * "refresh=wait_for"仅影响它所在的请求，但通过立即强制刷新，"refresh=true"将影响其他正在进行的请求。一般来说，如果你有一个正在运行的系统，你不想打扰，那么'refresh=wait_for'是一个较小的修改。

#### '刷新=wait_for' 可以强制刷新

如果当该分片上已经有"index.max_refresh_listeners"(默认为 1000)请求等待刷新时出现"refresh=wait_for"请求，则该请求的行为就像将"刷新"设置为"true"一样：它将强制刷新。这保证了当"刷新=wait_for"请求返回时，其更改对搜索可见，同时防止对被阻止的请求进行未经检查的资源使用。如果请求因为侦听器插槽不足而强制刷新，则其响应将包含"forced_refresh"：true。

批量请求只占用它们接触的每个分片上的一个插槽，无论它们修改分片多少次。

####Examples

这些将创建一个文档并立即刷新索引，使其可见：

    
    
    PUT /test/_doc/1?refresh
    {"test": "test"}
    PUT /test/_doc/2?refresh=true
    {"test": "test"}

这些将创建一个文档，而无需执行任何操作来使其可见以供搜索：

    
    
    PUT /test/_doc/3
    {"test": "test"}
    PUT /test/_doc/4?refresh=false
    {"test": "test"}

这将创建一个文档并等待它对搜索可见：

    
    
    response = client.index(
      index: 'test',
      id: 4,
      refresh: 'wait_for',
      body: {
        test: 'test'
      }
    )
    puts response
    
    
    PUT /test/_doc/4?refresh=wait_for
    {"test": "test"}

[« Multi term vectors API](docs-multi-termvectors.md) [Optimistic
concurrency control »](optimistic-concurrency-control.md)
