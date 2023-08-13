

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Metadata fields](mapping-fields.md)

[« `_field_names` field](mapping-field-names-field.md) [`_id` field
»](mapping-id-field.md)

## '_ignored'字段

"_ignored"字段索引并存储文档中每个字段的名称，这些字段在为文档编制索引时被忽略。例如，当字段格式不正确且"ignore_malformed"已打开时，或者当"关键字"字段值超过其可选的"ignore_above"设置时，可能会出现这种情况。

此字段可通过"term"、"terms"和"exists"查询进行搜索，并作为搜索命中的一部分返回。

例如，以下查询匹配具有一个或多个被忽略字段的所有文档：

    
    
    response = client.search(
      body: {
        query: {
          exists: {
            field: '_ignored'
          }
        }
      }
    )
    puts response
    
    
    GET _search
    {
      "query": {
        "exists": {
          "field": "_ignored"
        }
      }
    }

同样，以下查询查找在索引时忽略其"@timestamp"字段的所有文档：

    
    
    response = client.search(
      body: {
        query: {
          term: {
            _ignored: '@timestamp'
          }
        }
      }
    )
    puts response
    
    
    GET _search
    {
      "query": {
        "term": {
          "_ignored": "@timestamp"
        }
      }
    }

[« `_field_names` field](mapping-field-names-field.md) [`_id` field
»](mapping-id-field.md)
