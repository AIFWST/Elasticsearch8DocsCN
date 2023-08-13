

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« Mapping parameters](mapping-params.md) [`coerce` »](coerce.md)

##'分析器'

只有"文本"字段支持"分析器"映射参数。

"分析器"参数指定在索引或搜索"文本"字段时用于文本分析的分析器。

除非使用"search_analyzer"映射参数覆盖，否则此分析器将用于索引和搜索分析。请参阅指定分析器。

我们建议在生产中使用分析仪之前对其进行测试。请参见测试分析器。

"分析器"设置不能使用更新映射 API 在现有字段上更新。

###'search_quote_analyzer'

"search_quote_analyzer"设置允许您为短语指定分析器，这在处理禁用非索引字对于短语查询时特别有用。

要禁用短语的停用词，需要使用三个分析器设置的字段：

1. "分析器"设置，用于索引所有术语，包括停用词 2.非短语查询的"search_analyzer"设置，将删除停用词 3.短语查询的"search_quote_analyzer"设置，不会删除停用词

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_analyzer: {
                type: 'custom',
                tokenizer: 'standard',
                filter: [
                  'lowercase'
                ]
              },
              my_stop_analyzer: {
                type: 'custom',
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'english_stop'
                ]
              }
            },
            filter: {
              english_stop: {
                type: 'stop',
                stopwords: '_english_'
              }
            }
          }
        },
        mappings: {
          properties: {
            title: {
              type: 'text',
              analyzer: 'my_analyzer',
              search_analyzer: 'my_stop_analyzer',
              search_quote_analyzer: 'my_analyzer'
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
        title: 'The Quick Brown Fox'
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      body: {
        title: 'A Quick Brown Fox'
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          query_string: {
            query: '"the quick brown fox"'
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
       "settings":{
          "analysis":{
             "analyzer":{
                "my_analyzer":{ __"type":"custom",
                   "tokenizer":"standard",
                   "filter":[
                      "lowercase"
                   ]
                },
                "my_stop_analyzer":{ __"type":"custom",
                   "tokenizer":"standard",
                   "filter":[
                      "lowercase",
                      "english_stop"
                   ]
                }
             },
             "filter":{
                "english_stop":{
                   "type":"stop",
                   "stopwords":"_english_"
                }
             }
          }
       },
       "mappings":{
           "properties":{
              "title": {
                 "type":"text",
                 "analyzer":"my_analyzer", __"search_analyzer":"my_stop_analyzer", __"search_quote_analyzer":"my_analyzer" __}
          }
       }
    }
    
    PUT my-index-000001/_doc/1
    {
       "title":"The Quick Brown Fox"
    }
    
    PUT my-index-000001/_doc/2
    {
       "title":"A Quick Brown Fox"
    }
    
    GET my-index-000001/_search
    {
       "query":{
          "query_string":{
             "query":"\"the quick brown fox\"" __}
       }
    }

可以使用更新映射 API 在现有字段上更新"search_quote_analyzer"设置。

__

|

"my_analyzer"分析器，用于标记所有术语，包括停用词 ---|--- __

|

"my_stop_analyzer"分析器，用于删除停用词 __

|

指向将在索引时使用的"my_analyzer"分析器的"分析器"设置__

|

指向"my_stop_analyzer"并删除非短语查询的停止字的"search_analyzer"设置 __

|

指向"my_analyzer"分析器的"search_quote_analyzer"设置，并确保不会从短语查询中删除停用词 __

|

由于查询用引号括起来，因此被检测为短语查询因此，"search_quote_analyzer"启动并确保不会从查询中删除停用词。然后，"my_analyzer"分析器将返回以下标记"the"、"quick"、"brown"、"fox"]，这些标记将与其中一个文档匹配。同时，术语查询将使用"my_stop_analyzer"分析器进行分析，该分析器将过滤掉停用词。因此，搜索"快棕色狐狸"或"快速棕色狐狸"将返回两个文档，因为两个文档都包含以下标记["快速"，"棕色"，"狐狸"]。如果没有"search_quote_analyzer"，就不可能对短语查询进行精确匹配，因为短语查询中的停用词将被删除导致两个文档匹配。   [« 映射参数'胁迫' »