

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md)

[« Troubleshooting Watcher](watcher-troubleshooting.md) [Troubleshooting
shards capacity health issues »](troubleshooting-shards-capacity-issues.md)

## 疑难解答搜索

当您查询数据时，Elasticsearch 可能会返回错误、无搜索结果或结果顺序意外。本指南介绍如何排查搜索问题。

### 确保数据流、索引或别名存在

当您尝试查询的数据流、索引或别名不存在时，Elasticsearch 会返回"index_not_found_exception"。当您拼错名称或数据已索引到其他数据流或索引时，可能会发生这种情况。

使用现有 API 检查数据流、索引或别名是否存在：

    
    
    response = client.indices.exists(
      index: 'my-data-stream'
    )
    puts response
    
    
    HEAD my-data-stream

使用数据流统计信息 API 列出所有数据流：

    
    
    response = client.indices.data_streams_stats(
      human: true
    )
    puts response
    
    
    GET /_data_stream/_stats?human=true

使用获取索引 API 列出所有索引及其别名：

    
    
    response = client.indices.get(
      index: '_all',
      filter_path: '*.aliases'
    )
    puts response
    
    
    GET _all?filter_path=*.aliases

如果要查询的某些索引不可用，则可以检索部分搜索结果，而不是错误。将"ignore_unavailable"设置为"true"：

    
    
    response = client.search(
      index: 'my-alias',
      ignore_unavailable: true
    )
    puts response
    
    
    GET /my-alias/_search?ignore_unavailable=true

### 确保数据流或索引包含数据

当搜索请求未返回任何命中时，数据流或索引可能包含 nodata。当存在数据引入问题时，可能会发生这种情况。例如，数据可能已索引到具有其他名称的数据流或索引。

使用计数 API 检索数据流或索引中的文档数。检查响应中的"count"是否不是0。

    
    
    response = client.count(
      index: 'my-index-000001'
    )
    puts response
    
    
    GET /my-index-000001/_count

在 Kibana 中未获得搜索结果时，请检查是否选择了正确的数据视图和有效的时间范围。此外，请确保数据视图已配置正确的时间字段。

### 检查字段是否存在及其功能

查询不存在的字段不会返回任何结果。使用字段功能 API 检查字段是否存在：

    
    
    response = client.field_caps(
      index: 'my-index-000001',
      fields: 'my-field'
    )
    puts response
    
    
    GET /my-index-000001/_field_caps?fields=my-field

如果该字段不存在，请检查数据引入过程。该字段可能具有不同的名称。

如果字段存在，请求将返回字段的类型以及它是否可搜索和可聚合。

    
    
    {
      "indices": [
        "my-index-000001"
      ],
      "fields": {
        "my-field": {
          "keyword": {
            "type": "keyword",         __"metadata_field": false,
            "searchable": true, __"aggregatable": true __}
        }
      }
    }

__

|

该字段在此索引中属于"关键字"类型。   ---|---    __

|

该字段可在此索引中搜索。   __

|

该字段可在此索引中聚合。   ### 检查字段的映射编辑

字段的功能由其映射决定。若要检索映射，请使用获取映射 API：

    
    
    response = client.indices.get_mapping(
      index: 'my-index-000001'
    )
    puts response
    
    
    GET /my-index-000001/_mappings

如果查询"文本"字段，请注意可能已配置的分析器。您可以使用分析 API 检查字段的分析器如何处理值和查询词：

    
    
    response = client.indices.analyze(
      index: 'my-index-000001',
      body: {
        field: 'my-field',
        text: 'this is a test'
      }
    )
    puts response
    
    
    GET /my-index-000001/_analyze
    {
      "field" : "my-field",
      "text" : "this is a test"
    }

要更改现有字段的映射，请参阅更改字段的映射。

### 检查字段的值

使用"exists"查询检查是否存在返回字段值的文档。检查响应中的"计数"是否不为 0。

    
    
    response = client.count(
      index: 'my-index-000001',
      body: {
        query: {
          exists: {
            field: 'my-field'
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_count
    {
      "query": {
        "exists": {
          "field": "my-field"
        }
      }
    }

如果字段是可聚合的，则可以使用聚合来检查字段的值。对于"关键字"字段，您可以使用术语聚合来检索字段的最常见值：

    
    
    response = client.search(
      index: 'my-index-000001',
      filter_path: 'aggregations',
      body: {
        size: 0,
        aggregations: {
          top_values: {
            terms: {
              field: 'my-field',
              size: 10
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search?filter_path=aggregations
    {
      "size": 0,
      "aggs": {
        "top_values": {
          "terms": {
            "field": "my-field",
            "size": 10
          }
        }
      }
    }

对于数值字段，您可以使用统计信息聚合来了解字段的值分布：

    
    
    response = client.search(
      index: 'my-index-000001',
      filter_path: 'aggregations',
      body: {
        aggregations: {
          "my-num-field-stats": {
            stats: {
              field: 'my-num-field'
            }
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search?filter_path=aggregations
    {
      "aggs": {
        "my-num-field-stats": {
          "stats": {
            "field": "my-num-field"
          }
        }
      }
    }

如果该字段未返回任何值，请检查数据引入过程。该字段可能具有不同的名称。

### 检查最新值

对于时序数据，请确认在尝试的时间范围内存在未筛选的数据。例如，如果您尝试查询"@timestamp"字段的最新数据，请运行以下命令以查看最大"@timestamp"是否在尝试范围内：

    
    
    response = client.search(
      index: 'my-index-000001',
      sort: '@timestamp:desc',
      size: 1
    )
    puts response
    
    
    GET my-index-000001/_search?sort=@timestamp:desc&size=1

### 验证、解释和分析查询

当查询返回意外结果时，Elasticsearch 提供了几种工具来调查原因。

验证 API 使您能够验证查询。使用 'rewrite' 参数返回 Lucene 查询，弹性搜索查询被重写为：

    
    
    response = client.indices.validate_query(
      index: 'my-index-000001',
      rewrite: true,
      body: {
        query: {
          match: {
            "user.id": {
              query: 'kimchy',
              fuzziness: 'auto'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_validate/query?rewrite=true
    {
      "query": {
        "match": {
          "user.id": {
            "query": "kimchy",
            "fuzziness": "auto"
          }
        }
      }
    }

使用说明 API 找出特定文档匹配或不匹配查询的原因：

    
    
    response = client.explain(
      index: 'my-index-000001',
      id: 0,
      body: {
        query: {
          match: {
            message: 'elasticsearch'
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_explain/0
    {
      "query" : {
        "match" : { "message" : "elasticsearch" }
      }
    }

配置文件 API 提供有关搜索请求的详细计时信息。要直观地表示结果，请使用搜索分析器在 Kibana 中。

要在 Kibana 中排查查询问题，请在工具栏中选择"**检查**"。接下来，选择"**请求**"。您现在可以复制 Kibana 发送到 Elasticsearch 的查询，以便在控制台中进行进一步分析。

### 检查索引设置

索引设置可以影响搜索结果。例如，"index.query.default_field"设置，它确定在查询指定 noexplicit 字段时查询的字段。使用获取索引设置 API 检索索引的设置：

    
    
    response = client.indices.get_settings(
      index: 'my-index-000001'
    )
    puts response
    
    
    GET /my-index-000001/_settings

您可以使用更新索引设置 API 更新动态索引设置。更改数据流的动态索引设置需要更改数据流使用的索引模板。

对于静态设置，您需要使用正确的设置创建新索引。接下来，可以将数据重新索引到该索引中。有关数据流，请参阅更改数据流的静态索引设置。

### 查找慢查询

慢日志有助于查明执行缓慢的搜索请求。在顶部启用审核日志记录有助于确定查询源。将以下设置添加到"elasticsearch.yml"配置文件以跟踪查询。生成的日志记录很详细，因此在不进行故障排除时禁用这些设置。

    
    
    xpack.security.audit.enabled: true
    xpack.security.audit.logfile.events.include: _all
    xpack.security.audit.logfile.events.emit_request_body: true

有关更多信息，请参阅高级调优：查找和修复缓慢的 Elasticsearchquery。

[« Troubleshooting Watcher](watcher-troubleshooting.md) [Troubleshooting
shards capacity health issues »](troubleshooting-shards-capacity-issues.md)
