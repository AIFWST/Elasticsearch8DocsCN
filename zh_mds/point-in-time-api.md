

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search APIs](search.md)

[« Async search](async-search.md) [kNN search API »](knn-search-api.md)

## 时间点接口

默认情况下，搜索请求针对目标索引的最新可见数据(称为时间点)执行。Elasticsearch pit(时间点)是一个轻量级视图，用于显示数据在启动时的状态。在某些情况下，最好使用同一时间点执行多个搜索请求。例如，如果在search_after请求之间发生刷新，则这些请求的结果可能不一致，因为搜索之间发生的更改仅在最近的时间点可见。

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"读取"索引权限。

要在时间点 (PIT) 中搜索别名，您必须对别名的数据流或索引具有"读取"索引权限。

###Examples

在搜索请求中使用时间点之前，必须显式打开时间点。keep_alive参数告诉 Elasticsearch 它应该让一个时间点存活多长时间，例如 '？keep_alive=5m'。

    
    
    response = client.open_point_in_time(
      index: 'my-index-000001',
      keep_alive: '1m'
    )
    puts response
    
    
    POST /my-index-000001/_pit?keep_alive=1m

上述请求的结果包括一个"id"，应将其传递给搜索请求的"pit"参数的"id"。

    
    
    POST /_search  __{
        "size": 100, __"query": {
            "match" : {
                "title" : "elasticsearch"
            }
        },
        "pit": {
    	    "id":  "46ToAwMDaWR5BXV1aWQyKwZub2RlXzMAAAAAAAAAACoBYwADaWR4BXV1aWQxAgZub2RlXzEAAAAAAAAAAAEBYQADaWR5BXV1aWQyKgZub2RlXzIAAAAAAAAAAAwBYgACBXV1aWQyAAAFdXVpZDEAAQltYXRjaF9hbGw_gAAAAA==", __"keep_alive": "1m" __}
    }

__

|

带有"pit"参数的搜索请求不得指定"索引"、"路由"或"首选项"，因为这些参数是从时间点复制的。   ---|---    __

|

就像常规搜索一样，您可以使用"发件人"和"大小"来浏览搜索结果，最多前 10，000 次点击。如果要检索更多命中，请将 PIT 与"search_after"一起使用。   __

|

"id"参数告诉Elasticsearch从这个时间点使用上下文来执行请求。   __

|

"keep_alive"参数告诉 Elasticsearch 应该延长该时间点的生存时间多长时间。   开放时间点请求和每个后续搜索请求可以返回不同的"id";因此，始终将最近收到的"ID"用于下一个搜索请求。

### 保持时间活动点

传递给打开时间点请求和搜索请求的"keep_alive"参数会延长相应时间点的生存时间。该值(例如"1m"，请参阅时间单位)不需要足够长来处理所有数据 - 它只需要足够长才能处理下一个请求。

通常，后台合并过程通过将较小的段合并在一起以创建新的较大段来优化索引。一旦不再需要较小的段，它们就会被删除。但是，开放时间点可防止删除旧段，因为它们仍在使用中。

保持较旧的段处于活动状态意味着需要更多的磁盘空间和文件句柄。确保已将节点配置为具有足够的可用文件句柄。请参阅文件描述符。

此外，如果区段包含已删除或更新的文档，则时间点必须跟踪区段中的每个文档在初始搜索请求时是否处于活动状态。如果索引上有许多打开的时间点，并且需要持续删除或更新，请确保节点具有足够的堆空间。请注意，时间点不会阻止其关联的索引被删除。

您可以使用节点统计信息 API 检查打开了多少时间点(即搜索上下文)：

    
    
    $params = [
        'metric' => 'indices',
        'index_metric' => 'search',
    ];
    $response = $client->nodes()->stats($params);
    
    
    resp = client.nodes.stats(metric="indices", index_metric="search")
    print(resp)
    
    
    response = client.nodes.stats(
      metric: 'indices',
      index_metric: 'search'
    )
    puts response
    
    
    res, err := es.Nodes.Stats(
    	es.Nodes.Stats.WithMetric([]string{"indices"}...),
    	es.Nodes.Stats.WithIndexMetric([]string{"search"}...),
    )
    fmt.Println(res, err)
    
    
    const response = await client.nodes.stats({
      metric: 'indices',
      index_metric: 'search'
    })
    console.log(response)
    
    
    GET /_nodes/stats/indices/search

### 关闭时间点API

时间点在其"keep_alive"过后自动关闭。但是，如上一节所述，保持时间点是有代价的。一旦搜索请求中不再使用时间点，应立即关闭它们。

    
    
    response = client.close_point_in_time(
      body: {
        id: '46ToAwMDaWR5BXV1aWQyKwZub2RlXzMAAAAAAAAAACoBYwADaWR4BXV1aWQxAgZub2RlXzEAAAAAAAAAAAEBYQADaWR5BXV1aWQyKgZub2RlXzIAAAAAAAAAAAwBYgACBXV1aWQyAAAFdXVpZDEAAQltYXRjaF9hbGw_gAAAAA=='
      }
    )
    puts response
    
    
    DELETE /_pit
    {
        "id" : "46ToAwMDaWR5BXV1aWQyKwZub2RlXzMAAAAAAAAAACoBYwADaWR4BXV1aWQxAgZub2RlXzEAAAAAAAAAAAEBYQADaWR5BXV1aWQyKgZub2RlXzIAAAAAAAAAAAwBYgACBXV1aWQyAAAFdXVpZDEAAQltYXRjaF9hbGw_gAAAAA=="
    }

API 返回以下响应：

    
    
    {
       "succeeded": true, __"num_freed": 3 __}

__

|

如果为 true，则成功关闭与时间点 ID 关联的所有搜索上下文 ---|--- __

|

已成功关闭的搜索上下文数 ### 搜索切片编辑

在分页浏览大量文档时，将搜索拆分为多个切片以独立使用它们会很有帮助：

    
    
    GET /_search
    {
      "slice": {
        "id": 0,                      __"max": 2 __},
      "query": {
        "match": {
          "message": "foo"
        }
      },
      "pit": {
        "id": "46ToAwMDaWR5BXV1aWQyKwZub2RlXzMAAAAAAAAAACoBYwADaWR4BXV1aWQxAgZub2RlXzEAAAAAAAAAAAEBYQADaWR5BXV1aWQyKgZub2RlXzIAAAAAAAAAAAwBYgACBXV1aWQyAAAFdXVpZDEAAQltYXRjaF9hbGw_gAAAAA=="
      }
    }
    
    GET /_search
    {
      "slice": {
        "id": 1,
        "max": 2
      },
      "pit": {
        "id": "46ToAwMDaWR5BXV1aWQyKwZub2RlXzMAAAAAAAAAACoBYwADaWR4BXV1aWQxAgZub2RlXzEAAAAAAAAAAAEBYQADaWR5BXV1aWQyKgZub2RlXzIAAAAAAAAAAAwBYgACBXV1aWQyAAAFdXVpZDEAAQltYXRjaF9hbGw_gAAAAA=="
      },
      "query": {
        "match": {
          "message": "foo"
        }
      }
    }

__

|

切片的 id ---|--- __

|

最大切片数 第一个请求的结果返回属于第一个切片的文档 (id： 0)，第二个请求的结果返回第二个切片中的文档。由于最大切片数设置为 2，因此两个请求的结果并集等效于不切片的时间点搜索的结果。默认情况下，拆分首先在分片上完成，然后在每个分片上本地完成。本地拆分根据 Lucene 文档 ID 对分片的连续范围进行分区。

例如，如果分片数等于 2，并且用户请求了 4 个切片，则切片 0 和 2 将分配给第一个分片，切片 1 和 3 分配给第二个分片。

所有切片应使用相同的时间点 ID。如果使用不同的 PIT ID，则切片可能会重叠并丢失文档。这是因为拆分标准基于 Lucene 文档 ID，这些文档 ID 在索引更改时不稳定。

[« Async search](async-search.md) [kNN search API »](knn-search-api.md)
