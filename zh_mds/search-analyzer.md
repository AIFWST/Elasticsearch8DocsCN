

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `properties`](properties.md) [`similarity` »](similarity.md)

##'search_analyzer'

通常，应在索引时和搜索时应用相同的分析器，以确保查询中的字词与倒排索引中的字词采用相同的格式。

但是，有时在搜索时使用不同的分析器可能是有意义的，例如使用"edge_ngram"标记器进行自动完成或使用搜索时同义词时。

默认情况下，查询将使用字段映射中定义的"分析器"，但这可以用"search_analyzer"设置覆盖：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            filter: {
              autocomplete_filter: {
                type: 'edge_ngram',
                min_gram: 1,
                max_gram: 20
              }
            },
            analyzer: {
              autocomplete: {
                type: 'custom',
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'autocomplete_filter'
                ]
              }
            }
          }
        },
        mappings: {
          properties: {
            text: {
              type: 'text',
              analyzer: 'autocomplete',
              search_analyzer: 'standard'
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
        text: 'Quick Brown Fox'
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          match: {
            text: {
              query: 'Quick Br',
              operator: 'and'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "settings": {
        "analysis": {
          "filter": {
            "autocomplete_filter": {
              "type": "edge_ngram",
              "min_gram": 1,
              "max_gram": 20
            }
          },
          "analyzer": {
            "autocomplete": { __"type": "custom",
              "tokenizer": "standard",
              "filter": [
                "lowercase",
                "autocomplete_filter"
              ]
            }
          }
        }
      },
      "mappings": {
        "properties": {
          "text": {
            "type": "text",
            "analyzer": "autocomplete", __"search_analyzer": "standard" __}
        }
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "text": "Quick Brown Fox" __}
    
    GET my-index-000001/_search
    {
      "query": {
        "match": {
          "text": {
            "query": "Quick Br", __"operator": "and"
          }
        }
      }
    }

__

|

用于定义自定义"自动完成"分析器的分析设置。   ---|---    __

|

"文本"字段在索引时使用"自动完成"分析器，但在搜索时使用"标准"分析器。   __

|

此字段的索引为术语：[ 'q'， 'qu'， 'qui'， 'quic'， 'quick'， 'b'， 'br'， 'bro'， 'brow'， 'brown'， 'f'， 'fo'， 'fox' ] __

|

查询将搜索这两个术语："quick"、"br"] 有关此示例的完整说明，请参阅 [索引时间键入时搜索。

可以使用更新映射 API 在现有字段上更新"search_analyzer"设置。请注意，为此，任何现有的"分析器"设置和"类型"都需要在更新的字段定义中重复。

[« `properties`](properties.md) [`similarity` »](similarity.md)
