

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Index
modules](index-modules.md)

[« Similarity module](index-modules-similarity.md) [Store »](index-modules-
store.md)

## 慢日志

### 搜索慢日志

分片级慢速搜索日志允许将慢速搜索(查询和获取阶段)记录到专用日志文件中。

可以为执行的查询阶段和获取阶段设置阈值，下面是一个示例：

    
    
    index.search.slowlog.threshold.query.warn: 10s
    index.search.slowlog.threshold.query.info: 5s
    index.search.slowlog.threshold.query.debug: 2s
    index.search.slowlog.threshold.query.trace: 500ms
    
    index.search.slowlog.threshold.fetch.warn: 1s
    index.search.slowlog.threshold.fetch.info: 800ms
    index.search.slowlog.threshold.fetch.debug: 500ms
    index.search.slowlog.threshold.fetch.trace: 200ms

上述所有设置都是_动态_的，可以使用更新索引设置 API 为每个索引设置。例如：

    
    
    response = client.indices.put_settings(
      index: 'my-index-000001',
      body: {
        "index.search.slowlog.threshold.query.warn": '10s',
        "index.search.slowlog.threshold.query.info": '5s',
        "index.search.slowlog.threshold.query.debug": '2s',
        "index.search.slowlog.threshold.query.trace": '500ms',
        "index.search.slowlog.threshold.fetch.warn": '1s',
        "index.search.slowlog.threshold.fetch.info": '800ms',
        "index.search.slowlog.threshold.fetch.debug": '500ms',
        "index.search.slowlog.threshold.fetch.trace": '200ms'
      }
    )
    puts response
    
    
    PUT /my-index-000001/_settings
    {
      "index.search.slowlog.threshold.query.warn": "10s",
      "index.search.slowlog.threshold.query.info": "5s",
      "index.search.slowlog.threshold.query.debug": "2s",
      "index.search.slowlog.threshold.query.trace": "500ms",
      "index.search.slowlog.threshold.fetch.warn": "1s",
      "index.search.slowlog.threshold.fetch.info": "800ms",
      "index.search.slowlog.threshold.fetch.debug": "500ms",
      "index.search.slowlog.threshold.fetch.trace": "200ms"
    }

默认情况下，阈值处于禁用状态(设置为"-1")。

日志记录是在分片级别范围内完成的，这意味着在特定分片内执行搜索请求。它不包含整个搜索请求，可以广播到多个分片以执行。分片级别日志记录的一些好处是，与请求级别相比，特定计算机上的实际执行是关联。

搜索慢速日志文件在"log4j2.properties"文件中配置。

#### 识别搜索慢日志原点

确定触发缓慢运行查询的原因通常很有用。如果调用是使用"X-Opaque-ID"标头发起的，则用户 ID 将作为附加的 **id** 字段包含在搜索慢日志中

    
    
    {
      "type": "index_search_slowlog",
      "timestamp": "2030-08-30T11:59:37,786+02:00",
      "level": "WARN",
      "component": "i.s.s.query",
      "cluster.name": "distribution_run",
      "node.name": "node-0",
      "message": "[index6][0]",
      "took": "78.4micros",
      "took_millis": "0",
      "total_hits": "0 hits",
      "stats": "[]",
      "search_type": "QUERY_THEN_FETCH",
      "total_shards": "1",
      "source": "{\"query\":{\"match_all\":{\"boost\":1.0}}}",
      "id": "MY_USER_ID",
      "cluster.uuid": "Aq-c-PAeQiK3tfBYtig9Bw",
      "node.id": "D7fUYfnfTLa2D7y-xw6tZg"
    }

### 索引慢日志

索引慢日志，在功能上类似于搜索慢日志。日志文件名以"_index_indexing_slowlog.json"结尾。日志和阈值的配置方式与搜索慢日志相同。索引慢日志示例：

    
    
    index.indexing.slowlog.threshold.index.warn: 10s
    index.indexing.slowlog.threshold.index.info: 5s
    index.indexing.slowlog.threshold.index.debug: 2s
    index.indexing.slowlog.threshold.index.trace: 500ms
    index.indexing.slowlog.source: 1000

上述所有设置都是_动态_的，可以使用更新索引设置 API 为每个索引设置。例如：

    
    
    response = client.indices.put_settings(
      index: 'my-index-000001',
      body: {
        "index.indexing.slowlog.threshold.index.warn": '10s',
        "index.indexing.slowlog.threshold.index.info": '5s',
        "index.indexing.slowlog.threshold.index.debug": '2s',
        "index.indexing.slowlog.threshold.index.trace": '500ms',
        "index.indexing.slowlog.source": '1000'
      }
    )
    puts response
    
    
    PUT /my-index-000001/_settings
    {
      "index.indexing.slowlog.threshold.index.warn": "10s",
      "index.indexing.slowlog.threshold.index.info": "5s",
      "index.indexing.slowlog.threshold.index.debug": "2s",
      "index.indexing.slowlog.threshold.index.trace": "500ms",
      "index.indexing.slowlog.source": "1000"
    }

默认情况下，Elasticsearch 会将_source的前 1000 个字符记录在慢日志中。您可以使用"index.indexing.slowlog.source"进行更改。将其设置为"false"或"0"将完全跳过记录源，而将其设置为"true"将记录整个源，无论大小如何。默认情况下，原始"_source"会重新格式化，以确保它适合单个日志行。如果保留原始文档格式很重要，您可以通过将"index.indexing.slowlog.reformat"设置为"false"来关闭重新格式化，这将导致源"按原样"记录，并可能跨越多个日志行。

索引慢速日志文件在"log4j2.properties"文件中配置。

### 慢日志级别

您可以通过设置适当的阈值来模拟搜索或索引慢日志级别，使"更详细"的记录器关闭。例如，如果我们想模拟"index.indexing.slowlog.level： INFO"，那么我们需要做的就是将"index.indexing.slowlog.threshold.index.debug"和"index.indexing.slowlog.threshold.index.trace"设置为"-1"。

[« Similarity module](index-modules-similarity.md) [Store »](index-modules-
store.md)
