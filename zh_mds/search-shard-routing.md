

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Search your
data](search-your-data.md)

[« Search multiple data streams and indices](search-multiple-indices.md)
[Search templates »](search-template.md)

## 搜索分片路由

为了防止硬件故障并增加搜索容量，Elasticsearch 可以将索引数据的副本存储在多个节点上的多个分片上。运行搜索请求时，Elasticsearch 会选择一个包含索引数据副本的节点，并将搜索请求转发到该节点的分片。此过程称为_search分片routing_或 _routeting_。

### 自适应副本选择

默认情况下，Elasticsearch 使用副本_adaptive selection_来路由搜索请求。此方法使用分片分配感知和以下条件选择符合条件的节点：

* 协调节点和合格节点之间先前请求的响应时间 * 合格节点运行先前搜索所花费的时间 * 合格节点的"搜索"线程池的队列大小

自适应副本选择旨在减少搜索延迟。但是，您可以通过使用群集设置 API 将"cluster.routing.use_adaptive_replica_selection"设置为"false"来禁用自适应副本选择。如果禁用，Elasticsearch 使用循环方法路由搜索请求，这可能会导致搜索速度变慢。

### 设置首选项

默认情况下，自适应副本选择从所有符合条件的节点和分片中进行选择。但是，您可能只需要来自本地节点的数据，或者希望根据其硬件将搜索路由到特定节点。或者，您可能希望将重复搜索发送到同一分片以利用缓存。

要限制符合搜索请求条件的节点和分片集，请使用搜索 API 的"首选项"查询参数。

例如，以下请求使用"首选项"_local"搜索"my-index-000001"。这会将搜索限制为本地节点上的分片。如果本地节点不包含索引数据的分片副本，则该请求使用对另一个符合条件的节点的自适应副本选择作为回退。

    
    
    response = client.search(
      index: 'my-index-000001',
      preference: '_local',
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search?preference=_local
    {
      "query": {
        "match": {
          "user.id": "kimchy"
        }
      }
    }

您还可以使用"首选项"参数根据提供的字符串将搜索路由到特定分片。如果集群状态和所选分片未更改，则使用相同的"首选项"字符串的搜索将按相同的顺序路由到相同的分片。

我们建议使用唯一的"首选项"字符串，例如用户名或网络会话 ID。此字符串不能以"_"开头。

可以使用此选项为常用搜索和资源密集型搜索提供缓存结果。如果分片的数据没有更改，则使用相同的"首选项"字符串重复搜索将从sameshard请求缓存中检索结果。对于时序用例(例如日志记录)，旧索引中的数据很少更新，可以直接从此缓存中提供。

以下请求使用"my-custom-shard-string"的"首选项"字符串搜索"my-index-000001"。

    
    
    response = client.search(
      index: 'my-index-000001',
      preference: 'my-custom-shard-string',
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search?preference=my-custom-shard-string
    {
      "query": {
        "match": {
          "user.id": "kimchy"
        }
      }
    }

如果集群状态或所选分片发生更改，则相同的"首选项"字符串可能不会以相同的顺序将搜索路由到相同的分片。发生这种情况的原因有很多，包括分片重定位和分片故障。Anode 还可以拒绝搜索请求，Elasticsearch 会将其重新路由到另一个节点。

### 使用路由值

为文档编制索引时，可以指定可选的路由值，该值将文档路由到特定分片。

例如，以下索引请求使用"my-routing-value"路由文档。

    
    
    POST /my-index-000001/_doc?routing=my-routing-value
    {
      "@timestamp": "2099-11-15T13:12:00",
      "message": "GET /search HTTP/1.1 200 1070000",
      "user": {
        "id": "kimchy"
      }
    }

可以在搜索 API 的"路由"查询参数中使用相同的路由值。这可确保搜索在用于索引文档的同一分片上运行。

    
    
    response = client.search(
      index: 'my-index-000001',
      routing: 'my-routing-value',
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search?routing=my-routing-value
    {
      "query": {
        "match": {
          "user.id": "kimchy"
        }
      }
    }

您还可以提供多个逗号分隔的路由值：

    
    
    response = client.search(
      index: 'my-index-000001',
      routing: 'my-routing-value,my-routing-value-2',
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search?routing=my-routing-value,my-routing-value-2
    {
      "query": {
        "match": {
          "user.id": "kimchy"
        }
      }
    }

### 搜索并发性和并行性

默认情况下，Elasticsearch 不会根据请求命中的分片数量拒绝搜索请求。但是，命中大量分片会显著增加 CPU 和内存使用率。

有关防止具有大量分片的索引的提示，请参阅 _Size yourshards_。

您可以使用"max_concurrent_shard_requests"查询参数来控制每个节点搜索请求可以命中的最大并发分片数。这可以防止单个请求使群集过载。参数默认为最大值为"5"。

    
    
    response = client.search(
      index: 'my-index-000001',
      max_concurrent_shard_requests: 3,
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search?max_concurrent_shard_requests=3
    {
      "query": {
        "match": {
          "user.id": "kimchy"
        }
      }
    }

您还可以使用"action.search.shard_count.limit"集群设置来设置搜索分片限制并拒绝命中过多分片的请求。您可以使用集群设置API配置"action.search.shard_count.limit"。

[« Search multiple data streams and indices](search-multiple-indices.md)
[Search templates »](search-template.md)
