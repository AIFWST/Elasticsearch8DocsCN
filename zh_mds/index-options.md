

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `index`](mapping-index.md) [`index_phrases` »](index-phrases.md)

##'index_options'

"index_options"参数控制将哪些信息添加到倒排索引以进行搜索和突出显示。只有基于术语的字段类型(如"文本"和"关键字")支持此配置。

该参数接受以下值之一。每个值从前面列出的值中检索信息。例如，"频率"包含"文档";"职位"包含"频率"和"文档"。

`docs`

     Only the doc number is indexed. Can answer the question _Does this term exist in this field?_
`freqs`

     Doc number and term frequencies are indexed. Term frequencies are used to score repeated terms higher than single terms. 
`positions` (default)

     Doc number, term frequencies, and term positions (or order) are indexed. Positions can be used for [proximity or phrase queries](query-dsl-match-query-phrase.html "Match phrase query"). 
`offsets`

     Doc number, term frequencies, positions, and start and end character offsets (which map the term back to the original string) are indexed. Offsets are used by the [unified highlighter](highlighting.html#unified-highlighter "Unified highlighter") to speed up highlighting. 
    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            text: {
              type: 'text',
              index_options: 'offsets'
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
        text: 'Quick brown fox'
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          match: {
            text: 'brown fox'
          }
        },
        highlight: {
          fields: {
            text: {}
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "text": {
            "type": "text",
            "index_options": "offsets"
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "text": "Quick brown fox"
    }
    
    GET my-index-000001/_search
    {
      "query": {
        "match": {
          "text": "brown fox"
        }
      },
      "highlight": {
        "fields": {
          "text": {} __}
      }
    }

__

|

默认情况下，"文本"字段将使用帖子进行突出显示，因为"偏移量"已编制索引。   ---|--- « '索引' 'index_phrases' »