

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Specialized queries](specialized-queries.md)

[« Wrapper query](query-dsl-wrapper-query.md) [Term-level queries »](term-
level-queries.md)

## 固定查询

将所选文档提升为高于与给定查询匹配的文档的排名。此功能通常用于引导搜索者访问特选文档，这些文档在搜索的任何"自然"匹配项之上得到提升。升级者"固定"文档使用存储在"_id"字段中的文档 ID 进行标识。

### 示例请求

    
    
    response = client.search(
      body: {
        query: {
          pinned: {
            ids: [
              '1',
              '4',
              '100'
            ],
            organic: {
              match: {
                description: 'iphone'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "pinned": {
          "ids": [ "1", "4", "100" ],
          "organic": {
            "match": {
              "description": "iphone"
            }
          }
        }
      }
    }

### "固定"的顶级参数

`ids`

     (Optional, array) [Document IDs](mapping-id-field.html "_id field") listed in the order they are to appear in results. Required if `docs` is not specified. 
`docs`

    

(可选，数组)文档按其在结果中显示的顺序列出。如果未指定"ids"，则为必需。您可以为每个文档指定以下属性：

`_id`

     (Required, string) The unique [document ID](mapping-id-field.html "_id field"). 
`_index`

     (Required, string) The index that contains the document. 

`organic`

     Any choice of query used to rank documents which will be ranked below the "pinned" documents. 

### 在特定索引中固定文档

如果要搜索多个索引，可以使用"docs"将文档固定在特定索引中：

    
    
    response = client.search(
      body: {
        query: {
          pinned: {
            docs: [
              {
                _index: 'my-index-000001',
                _id: '1'
              },
              {
                _index: 'my-index-000001',
                _id: '4'
              },
              {
                _index: 'my-index-000002',
                _id: '100'
              }
            ],
            organic: {
              match: {
                description: 'iphone'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "pinned": {
          "docs": [
            {
              "_index": "my-index-000001",
              "_id": "1"
            },
            {
              "_index": "my-index-000001",
              "_id": "4"
            },
            {
              "_index": "my-index-000002",
              "_id": "100"
            }
          ],
          "organic": {
            "match": {
              "description": "iphone"
            }
          }
        }
      }
    }

[« Wrapper query](query-dsl-wrapper-query.md) [Term-level queries »](term-
level-queries.md)
