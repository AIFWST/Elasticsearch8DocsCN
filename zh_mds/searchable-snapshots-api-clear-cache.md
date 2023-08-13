

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Searchable snapshots APIs](searchable-snapshots-
apis.md)

[« Searchable snapshot statistics API](searchable-snapshots-api-stats.md)
[Security APIs »](security-api.md)

## 清除缓存接口

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

从共享高速缓存中清除部分装入索引的索引和数据流。

###Request

"发布/_searchable_snapshots/缓存/清除"

'POST /<target>/_searchable_snapshots/cache/clear'

###Prerequisites

如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。您还必须具有目标数据流、索引或别名的"管理"索引权限。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases to clear from the cache. Supports wildcards (`*`). To clear the entire cache, omit this parameter. 

###Examples

清除索引"my-index"的缓存：

    
    
    response = client.searchable_snapshots.clear_cache(
      index: 'my-index'
    )
    puts response
    
    
    POST /my-index/_searchable_snapshots/cache/clear

[« Searchable snapshot statistics API](searchable-snapshots-api-stats.md)
[Security APIs »](security-api.md)
