

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `null_value`](null-value.md) [`properties` »](properties.md)

##'position_increment_gap'

分析的文本字段会考虑术语位置，以便能够支持邻近感应或短语查询。使用多个值为文本字段编制索引时，会在值之间添加"假"间隙，以防止大多数短语查询在值之间匹配。此间隙的大小使用"position_increment_gap"配置，默认为"100"。

例如：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        names: [
          'John Abraham',
          'Lincoln Smith'
        ]
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          match_phrase: {
            names: {
              query: 'Abraham Lincoln'
            }
          }
        }
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          match_phrase: {
            names: {
              query: 'Abraham Lincoln',
              slop: 101
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/1
    {
      "names": [ "John Abraham", "Lincoln Smith"]
    }
    
    GET my-index-000001/_search
    {
      "query": {
        "match_phrase": {
          "names": {
            "query": "Abraham Lincoln" __}
        }
      }
    }
    
    GET my-index-000001/_search
    {
      "query": {
        "match_phrase": {
          "names": {
            "query": "Abraham Lincoln",
            "slop": 101 __}
        }
      }
    }

__

|

此短语查询与我们的文档不匹配，这是完全预期的。   ---|---    __

|

这个短语查询与我们的文档匹配，即使"亚伯拉罕"和"林肯"在不同的字符串中，因为"slop">"position_increment_gap"。   可以在映射中指定"position_increment_gap"。例如：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            names: {
              type: 'text',
              position_increment_gap: 0
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
        names: [
          'John Abraham',
          'Lincoln Smith'
        ]
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          match_phrase: {
            names: 'Abraham Lincoln'
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "names": {
            "type": "text",
            "position_increment_gap": 0 __}
        }
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "names": [ "John Abraham", "Lincoln Smith"]
    }
    
    GET my-index-000001/_search
    {
      "query": {
        "match_phrase": {
          "names": "Abraham Lincoln" __}
      }
    }

__

|

下一个数组元素中的第一个项将是 0 项，与前一个数组元素中的最后一个项分开。   ---|---    __

|

短语查询与我们的文档匹配，这很奇怪，但它是我们在映射中要求的。   « "null_value"属性" »