

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Searchable snapshots APIs](searchable-snapshots-
apis.md)

[« Cache stats API](searchable-snapshots-api-cache-stats.md) [Clear cache
API »](searchable-snapshots-api-clear-cache.md)

## 可搜索快照统计信息API

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

检索有关可搜索快照的统计信息。

###Request

'获取/_searchable_snapshots/统计"

'获取/<target>/_searchable_snapshots/统计"

###Prerequisites

如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。您还必须具有目标数据流或索引的"管理"索引权限。

###Description

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams and indices to retrieve statistics for. To retrieve statistics for all data streams and indices, omit this parameter. 

###Examples

检索索引"my-index"的统计信息：

    
    
    response = client.searchable_snapshots.stats(
      index: 'my-index'
    )
    puts response
    
    
    GET /my-index/_searchable_snapshots/stats

[« Cache stats API](searchable-snapshots-api-cache-stats.md) [Clear cache
API »](searchable-snapshots-api-clear-cache.md)
