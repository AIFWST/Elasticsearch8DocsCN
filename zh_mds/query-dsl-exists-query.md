

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Term-level queries](term-level-queries.md)

[« Term-level queries](term-level-queries.md) [Fuzzy query »](query-dsl-
fuzzy-query.md)

## 存在查询

返回包含字段索引值的文档。

由于各种原因，文档字段可能不存在索引值：

* 源 JSON 中的字段为"空"或"[]" * 该字段在映射中设置了"索引"：false" * 字段值的长度超过了映射中的"ignore_above"设置 * 字段值格式不正确，映射中定义了"ignore_malformed"

### 示例请求

    
    
    response = client.search(
      body: {
        query: {
          exists: {
            field: 'user'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "exists": {
    	      "field": "user"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "exists": {
          "field": "user"
        }
      }
    }

### "存在"的顶级参数

`field`

    

(必需，字符串)要搜索的字段的名称。

如果 JSON 值为"null"或"[]"，则字段被视为不存在，但这些值将指示该字段确实存在：

* 空字符串，例如"""或"-"" * 包含"null"和另一个值的数组，例如"null"，"foo"]" * 自定义 ["null-value"，在字段映射中定义

###Notes

#### 查找缺少索引值的文档

若要查找缺少字段索引值的文档，请将"must_not"布尔查询与"存在"查询一起使用。

以下搜索返回缺少"user.id"字段索引值的文档。

    
    
    response = client.search(
      body: {
        query: {
          bool: {
            must_not: {
              exists: {
                field: 'user.id'
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
        "bool": {
          "must_not": {
            "exists": {
              "field": "user.id"
            }
          }
        }
      }
    }

[« Term-level queries](term-level-queries.md) [Fuzzy query »](query-dsl-
fuzzy-query.md)
