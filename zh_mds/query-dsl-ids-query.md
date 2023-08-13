

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Term-level queries](term-level-queries.md)

[« Fuzzy query](query-dsl-fuzzy-query.md) [Prefix query »](query-dsl-prefix-
query.md)

##IDs

根据文档的 ID 返回文档。此查询使用存储在"_id"字段中的文档 ID。

### 示例请求

    
    
    response = client.search(
      body: {
        query: {
          ids: {
            values: [
              '1',
              '4',
              '100'
            ]
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "ids" : {
          "values" : ["1", "4", "100"]
        }
      }
    }

### "ids"的顶级参数

`values`

     (Required, array of strings) An array of [document IDs](mapping-id-field.html "_id field"). 

[« Fuzzy query](query-dsl-fuzzy-query.md) [Prefix query »](query-dsl-prefix-
query.md)
