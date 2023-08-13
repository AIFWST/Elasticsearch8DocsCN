

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `format`](mapping-date-format.md) [`ignore_malformed` »](ignore-
malformed.md)

##'ignore_above'

长度超过"ignore_above"设置的字符串将不会编制索引或存储。对于字符串数组，"ignore_above"将分别应用于每个数组元素，并且不会索引或存储长度超过"ignore_above"的字符串元素。

所有字符串/数组元素仍将出现在"_source"字段中，如果后者被启用，这是 Elasticsearch 中的默认设置。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            message: {
              type: 'keyword',
              ignore_above: 20
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        message: 'Syntax error'
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      body: {
        message: 'Syntax error with some long stacktrace'
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        aggregations: {
          messages: {
            terms: {
              field: 'message'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "message": {
            "type": "keyword",
            "ignore_above": 20 __}
        }
      }
    }
    
    PUT my-index-000001/_doc/1 __{
      "message": "Syntax error"
    }
    
    PUT my-index-000001/_doc/2 __{
      "message": "Syntax error with some long stacktrace"
    }
    
    GET my-index-000001/_search __{
      "aggs": {
        "messages": {
          "terms": {
            "field": "message"
          }
        }
      }
    }

__

|

此字段将忽略任何长度超过 20 个字符的字符串。   ---|---    __

|

本文档已成功编制索引。   __

|

此文档将被索引，但不索引"消息"字段。   __

|

搜索返回这两个文档，但术语聚合中仅存在第一个文档。   可以使用更新映射 API 在现有字段上更新"ignore_above"设置。

此选项对于防止 Lucene 的术语字节长度限制"32766"也很有用。

"ignore_above"的值是_character count_，但Lucene计算字节数。如果使用包含许多非 ASCII 字符的 UTF-8 文本，则可能需要将限制设置为 '32766 / 4 = 8191'，因为 UTF-8 字符最多可能占用 4 个字节。

[« `format`](mapping-date-format.md) [`ignore_malformed` »](ignore-
malformed.md)
