

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Security settings in Elasticsearch](security-settings.md) [Snapshot and
restore settings »](snapshot-settings.md)

## 分片请求缓存设置

当针对一个索引或多个索引运行搜索请求时，每个涉及的分片在本地执行搜索并将其本地结果返回给_coordinating node_，将这些分片级结果合并为"全局"结果集。

分片级请求缓存模块在每个分片上缓存本地结果。这允许频繁使用(并且可能很重)的搜索请求几乎立即返回结果。请求缓存非常适合日志记录用例，其中只有最新的索引被主动更新 - 来自旧索引的结果将直接从缓存中提供。

默认情况下，请求缓存将仅缓存搜索请求的结果，其中"size=0"，因此它不会缓存"命中"，但会缓存"hits.total"，聚合和建议。

大多数使用"now"的查询(请参阅日期数学)都无法缓存。

使用非确定性 API 调用的脚本化查询(例如"Math.random()"或"new Date()")不会被缓存。

#### 缓存失效

缓存是智能的 - 它保持与未缓存搜索相同的_near真实time_承诺。

每当分片刷新以选取对文档的更改或更新映射时，缓存的结果都会自动失效。换句话说，您将始终从缓存中获得与匿名缓存搜索请求相同的结果。

刷新间隔越长，即使文档发生更改，缓存条目的有效期也就越长。如果缓存已满，则将逐出最近最少使用的缓存键。

可以使用"清除缓存"API 手动使缓存过期：

    
    
    response = client.indices.clear_cache(
      index: 'my-index-000001,my-index-000002',
      request: true
    )
    puts response
    
    
    POST /my-index-000001,my-index-000002/_cache/clear?request=true

#### 启用和禁用缓存

默认情况下启用缓存，但在创建新索引时可以禁用缓存，如下所示：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          "index.requests.cache.enable": false
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001
    {
      "settings": {
        "index.requests.cache.enable": false
      }
    }

也可以使用"更新设置"API在现有索引上动态启用或禁用它：

    
    
    response = client.indices.put_settings(
      index: 'my-index-000001',
      body: {
        "index.requests.cache.enable": true
      }
    )
    puts response
    
    
    PUT /my-index-000001/_settings
    { "index.requests.cache.enable": true }

#### 根据请求启用和禁用缓存

"request_cache"查询字符串参数可用于基于**每个请求**启用或禁用缓存。如果设置，它将覆盖索引级别设置：

    
    
    response = client.search(
      index: 'my-index-000001',
      request_cache: true,
      body: {
        size: 0,
        aggregations: {
          popular_colors: {
            terms: {
              field: 'colors'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search?request_cache=true
    {
      "size": 0,
      "aggs": {
        "popular_colors": {
          "terms": {
            "field": "colors"
          }
        }
      }
    }

"size"大于 0 的请求将不会缓存，即使在索引设置中启用了请求缓存也是如此。若要缓存这些请求，需要使用此处详述的查询字符串参数。

#### 缓存键

整个 JSON 正文的哈希用作缓存键。这意味着，如果 JSON 发生更改(例如，如果键以不同的顺序输出)，则缓存键将无法识别。

大多数 JSON 库都支持 _canonical_ 模式，该模式可确保 JSON 密钥始终以相同的顺序发出。可以在应用程序中使用此规范模式，以确保始终以相同的方式序列化请求。

#### 缓存设置

缓存在节点级别进行管理，默认最大大小为堆的"1%"。这可以在"config/elasticsearch.yml"文件中更改：

    
    
    indices.requests.cache.size: 2%

此外，您可以使用"index.requests.cache.expire"设置为缓存结果指定 TTL，但应该没有理由这样做。请记住，刷新索引时，过时的结果会自动失效。此设置仅出于完整性考虑而提供。

#### 监视缓存使用情况

缓存的大小(以字节为单位)和逐出次数可以通过"索引统计"API 按索引查看：

    
    
    response = client.indices.stats(
      metric: 'request_cache',
      human: true
    )
    puts response
    
    
    GET /_stats/request_cache?human

或使用"节点统计"API 按节点：

    
    
    response = client.nodes.stats(
      metric: 'indices',
      index_metric: 'request_cache',
      human: true
    )
    puts response
    
    
    GET /_nodes/stats/indices/request_cache?human

[« Security settings in Elasticsearch](security-settings.md) [Snapshot and
restore settings »](snapshot-settings.md)
