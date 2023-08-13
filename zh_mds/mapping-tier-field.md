

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Metadata fields](mapping-fields.md)

[« `_source` field](mapping-source-field.md) [Mapping parameters »](mapping-
params.md)

## '_tier'字段

跨多个索引执行查询时，有时需要将保存在给定数据层("data_hot"、"data_warm"、"data_cold"或"data_frozen")节点上的索引作为目标。"_tier"字段允许匹配文档索引到的索引的"tier_preference"设置。首选值在某些查询中可访问：

    
    
    response = client.index(
      index: 'index_1',
      id: 1,
      body: {
        text: 'Document in index 1'
      }
    )
    puts response
    
    response = client.index(
      index: 'index_2',
      id: 2,
      refresh: true,
      body: {
        text: 'Document in index 2'
      }
    )
    puts response
    
    response = client.search(
      index: 'index_1,index_2',
      body: {
        query: {
          terms: {
            _tier: [
              'data_hot',
              'data_warm'
            ]
          }
        }
      }
    )
    puts response
    
    
    PUT index_1/_doc/1
    {
      "text": "Document in index 1"
    }
    
    PUT index_2/_doc/2?refresh=true
    {
      "text": "Document in index 2"
    }
    
    GET index_1,index_2/_search
    {
      "query": {
        "terms": {
          "_tier": ["data_hot", "data_warm"] __}
      }
    }

__

|

对"_tier"字段进行查询 ---|--- 通常，查询将使用"terms"查询来列出感兴趣的层，但您可以在重写为"term"查询的任何查询中使用"_tier"字段，例如"匹配"、"query_string"、"术语"、"术语"或"simple_query_string"查询，以及"前缀"和"通配符"查询。但是，它不支持"正则表达式"和"模糊"查询。

索引的"tier_preference"设置是按优先级顺序排列的以逗号分隔的层名列表，即首先列出托管索引的首选层，然后列出可能有许多回退选项。查询匹配仅考虑第一个首选项(列表的第一个值)。

[« `_source` field](mapping-source-field.md) [Mapping parameters »](mapping-
params.md)
