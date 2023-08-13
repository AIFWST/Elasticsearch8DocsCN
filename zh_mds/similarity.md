

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `search_analyzer`](search-analyzer.md) [`store` »](mapping-store.md)

##'相似性'

Elasticsearch 允许您配置文本评分算法或_similarity_per字段。"相似性"设置提供了一种选择文本相似性算法的简单方法，而不是默认的"BM25"，例如"布尔"。

只有基于文本的字段类型(如"文本"和"关键字")支持此配置。

可以通过调整内置相似性的参数来配置自定义相似性。有关此专家选项的更多详细信息，请参阅相似性模块。

开箱即用的唯一相似之处是：

`BM25`

     The [Okapi BM25 algorithm](https://en.wikipedia.org/wiki/Okapi_BM25). The algorithm used by default in Elasticsearch and Lucene. 
`boolean`

     A simple boolean similarity, which is used when full-text ranking is not needed and the score should only be based on whether the query terms match or not. Boolean similarity gives terms a score equal to their query boost. 

首次创建字段时，可以在字段级别设置"相似性"，如下所示：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            default_field: {
              type: 'text'
            },
            boolean_sim_field: {
              type: 'text',
              similarity: 'boolean'
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
          "default_field": { __"type": "text"
          },
          "boolean_sim_field": {
            "type": "text",
            "similarity": "boolean" __}
        }
      }
    }

__

|

"default_field"使用"BM25"相似性。   ---|---    __

|

"boolean_sim_field"使用"布尔"相似性。   « "search_analyzer" "商店" »