

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Term-level queries](term-level-queries.md)

[« IDs](query-dsl-ids-query.md) [Range query »](query-dsl-range-query.md)

## 前缀查询

返回在提供的字段中包含特定前缀的文档。

### 示例请求

以下搜索返回"user.id"字段包含以"ki"开头的术语的文档。

    
    
    response = client.search(
      body: {
        query: {
          prefix: {
            "user.id": {
              value: 'ki'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "prefix": {
          "user.id": {
            "value": "ki"
          }
        }
      }
    }

### 前缀"的顶级参数

`<field>`

     (Required, object) Field you wish to search. 

### 参数 '<field>'

`value`

     (Required, string) Beginning characters of terms you wish to find in the provided `<field>`. 
`rewrite`

     (Optional, string) Method used to rewrite the query. For valid values and more information, see the [`rewrite` parameter](query-dsl-multi-term-rewrite.html "rewrite parameter"). 
`case_insensitive` [7.10.0]  Added in 7.10.0.

     (Optional, Boolean) Allows ASCII case insensitive matching of the value with the indexed field values when set to true. Default is false which means the case sensitivity of matching depends on the underlying field's mapping. 

###Notes

#### 简短请求示例

您可以通过组合""和"值"参数来简化"前缀"查询语法<field>。例如：

    
    
    response = client.search(
      body: {
        query: {
          prefix: {
            user: 'ki'
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "prefix" : { "user" : "ki" }
      }
    }

#### 加快前缀查询

您可以使用"index_prefixes"映射参数加快前缀查询速度。如果启用，Elasticsearchindex将根据配置设置在单独的字段中添加前缀。这使得 Elasticsearch 可以更有效地运行前缀查询，但代价是索引更大。

#### 允许昂贵的查询

如果"search.allow_expensive_queries"设置为 false，则不会执行前缀查询。但是，如果启用了"index_prefixes"，则会构建一个优化的查询，该查询不会被视为缓慢，并且尽管有此设置，仍将执行。

[« IDs](query-dsl-ids-query.md) [Range query »](query-dsl-range-query.md)
