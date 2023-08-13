

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `norms`](norms.md) [`position_increment_gap` »](position-increment-
gap.md)

##'null_value'

无法索引或搜索"null"值。当字段设置为"null"(或空数组或"null"值数组)时，将被视为该字段没有值。

"null_value"参数允许您将显式的"null"值替换为指定的值，以便可以对其进行索引和搜索。例如：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            status_code: {
              type: 'keyword',
              nil_value: 'NULL'
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
        status_code: nil
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      body: {
        status_code: []
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          term: {
            status_code: 'NULL'
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "status_code": {
            "type":       "keyword",
            "null_value": "NULL" __}
        }
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "status_code": null
    }
    
    PUT my-index-000001/_doc/2
    {
      "status_code": [] __}
    
    GET my-index-000001/_search
    {
      "query": {
        "term": {
          "status_code": "NULL" __}
      }
    }

__

|

将显式"null"值替换为术语"NULL"。   ---|---    __

|

空数组不包含显式的"null"，因此不会替换为"null_value"。   __

|

对"NULL"的查询返回文档 1，但不返回文档 2。   "null_value"的数据类型必须与字段相同。例如，"long"字段不能有字符串"null_value"。

"null_value"仅影响数据的索引方式，不会修改"_source"文档。

[« `norms`](norms.md) [`position_increment_gap` »](position-increment-
gap.md)
