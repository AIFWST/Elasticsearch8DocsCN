

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md)

[« Wildcard query](query-dsl-wildcard-query.md) [`minimum_should_match`
parameter »](query-dsl-minimum-should-match.md)

## 文本扩展查询

文本扩展查询使用自然语言处理模型将查询文本转换为令牌权重对列表，然后在针对排名特征字段的查询中使用令牌权重对列表。

### 示例请求

    
    
    GET _search
    {
       "query":{
          "text_expansion":{
             "<rank_features_field>":{
                "model_id":"the model to produce the token weights",
                "model_text":"the query string"
             }
          }
       }
    }

### text_expansion"的顶级参数

`<rank_features_field>`

     (Required, object) The name of the field that contains the token-weight pairs the NLP model created based on the input text. 

### 的顶级参数<rank_features_field>

`model_id`

     (Required, string) The ID of the model to use to convert the query text into token-weight pairs. It must be the same model ID that was used to create the tokens from the input text. 
`model_text`

     (Required, string) The query text you want to use for search. 

###Example

下面是引用 ELSER 模型以执行语义搜索的"text_expansion"查询的示例。有关如何使用 ELSER 和"text_expansion"查询执行语义搜索的更详细说明，请参阅本教程。

    
    
    GET my-index/_search
    {
       "query":{
          "text_expansion":{
             "ml.tokens":{
                "model_id":".elser_model_1",
                "model_text":"How is the weather in Jamaica?"
             }
          }
       }
    }

### 优化text_expansionquery的搜索性能

Max WAND 是 Elasticsearch 使用的一种优化技术，用于跳过无法与当前最佳匹配文档竞争的文档。但是，ELSER 模型生成的令牌不能很好地与 MaxWAND 优化配合使用。因此，启用 Max WAND 实际上会增加"text_expansion"的查询延迟。对于大型数据集，禁用最大 WAND 可降低查询延迟。

最大 WAND 由 track_total_hits 查询参数控制。将track_total_hits设置为 true 会强制 Elasticsearch 考虑所有文档，从而降低"text_expansion"查询的查询延迟。但是，当禁用Max WAND时，其他Elasticsearch查询的运行速度会变慢。

如果要将"text_expansion"查询与复合搜索中的标准文本查询结合使用，建议在决定使用哪个设置之前测量查询性能。

"track_total_hits"选项适用于搜索请求中的所有查询，对于某些查询可能是最佳的，但对其他查询则不是。考虑所有查询的特征，以确定最合适的配置。

[« Wildcard query](query-dsl-wildcard-query.md) [`minimum_should_match`
parameter »](query-dsl-minimum-should-match.md)
