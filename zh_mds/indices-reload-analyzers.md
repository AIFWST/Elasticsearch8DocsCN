

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md)

[« Delete shutdown API](delete-shutdown.md) [Repositories metering APIs
»](repositories-metering-apis.md)

## 重新加载搜索分析器API

重新加载索引的搜索分析器及其资源。对于数据流，API 会重新加载流的支持索引的搜索分析器和资源。

    
    
    response = client.indices.reload_search_analyzers(
      index: 'my-index-000001'
    )
    puts response
    
    response = client.indices.clear_cache(
      index: 'my-index-000001',
      request: true
    )
    puts response
    
    
    POST /my-index-000001/_reload_search_analyzers
    POST /my-index-000001/_cache/clear?request=true

重新加载搜索分析器后，应清除请求缓存，以确保它不包含从以前版本的分析器派生的响应。

###Request

"发布/<target>/_reload_search_analyzers"

"获取/<target>/_reload_search_analyzers"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"管理"索引权限。

###Description

可以使用重新加载搜索分析器 API 来选取对搜索分析器的"synonym_graph"或"同义词"令牌筛选器中使用的同义词文件的更改。若要符合条件，令牌筛选器必须具有"true"的"可更新"标志，并且仅在搜索分析器中使用。

此 API 不会对索引的每个分片执行重新加载。相反，它会对包含索引分片的每个节点执行重新加载。因此，API 返回的总分片计数可能与索引分片数不同。

由于重新加载会影响具有索引分片的每个节点，因此在使用此 API 之前，更新集群中每个数据节点(包括不包含分片副本的节点)上的同义词文件非常重要。这可确保同义词文件在集群中的所有位置更新，以防将来重新定位分片。

### 路径参数

`<target>`

     (Required, string) Comma-separated list of data streams, indices, and aliases used to limit the request. Supports wildcards (`*`). To target all data streams and indices, use `*` or `_all`. 

### 查询参数

`allow_no_indices`

    

(可选，布尔值)如果为"false"，则当任何通配符表达式、索引别名或"_all"值仅针对缺少或关闭的索引时，请求将返回错误。即使请求以其他打开的索引为目标，此行为也适用。例如，如果索引以"foo"开头但没有索引以"bar"开头，则以"foo*，bar*"为目标的请求将返回错误。

默认为"真"。

`expand_wildcards`

    

(可选，字符串)通配符模式可以匹配的索引类型。如果请求可以以数据流为目标，则此参数确定通配符表达式是否与隐藏的数据流匹配。支持逗号分隔的值，例如"打开，隐藏"。有效值为：

`all`

     Match any data stream or index, including [hidden](api-conventions.html#multi-hidden "Hidden data streams and indices") ones. 
`open`

     Match open, non-hidden indices. Also matches any non-hidden data stream. 
`closed`

     Match closed, non-hidden indices. Also matches any non-hidden data stream. Data streams cannot be closed. 
`hidden`

     Match hidden data streams and hidden indices. Must be combined with `open`, `closed`, or both. 
`none`

     Wildcard patterns are not accepted. 

默认为"打开"。

`ignore_unavailable`

     (Optional, Boolean) If `false`, the request returns an error if it targets a missing or closed index. Defaults to `false`. 

###Examples

使用创建索引 API 创建具有包含可更新同义词筛选器的搜索分析器的索引。

使用以下分析器作为索引分析器会导致错误。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          index: {
            analysis: {
              analyzer: {
                my_synonyms: {
                  tokenizer: 'whitespace',
                  filter: [
                    'synonym'
                  ]
                }
              },
              filter: {
                synonym: {
                  type: 'synonym_graph',
                  synonyms_path: 'analysis/synonym.txt',
                  updateable: true
                }
              }
            }
          }
        },
        mappings: {
          properties: {
            text: {
              type: 'text',
              analyzer: 'standard',
              search_analyzer: 'my_synonyms'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001
    {
      "settings": {
        "index": {
          "analysis": {
            "analyzer": {
              "my_synonyms": {
                "tokenizer": "whitespace",
                "filter": [ "synonym" ]
              }
            },
            "filter": {
              "synonym": {
                "type": "synonym_graph",
                "synonyms_path": "analysis/synonym.txt",  __"updateable": true __}
            }
          }
        }
      },
      "mappings": {
        "properties": {
          "text": {
            "type": "text",
            "analyzer": "standard",
            "search_analyzer": "my_synonyms" __}
        }
      }
    }

__

|

包括同义词文件。   ---|---    __

|

将令牌筛选器标记为可更新。   __

|

将分析器标记为搜索分析器。   更新同义词文件后，使用分析器重新加载 API 重新加载搜索分析器并选取文件更改。

    
    
    response = client.indices.reload_search_analyzers(
      index: 'my-index-000001'
    )
    puts response
    
    
    POST /my-index-000001/_reload_search_analyzers

API 返回以下响应。

    
    
    {
      "_shards": {
        "total": 2,
        "successful": 2,
        "failed": 0
      },
      "reload_details": [
        {
          "index": "my-index-000001",
          "reloaded_analyzers": [
            "my_synonyms"
          ],
          "reloaded_node_ids": [
            "mfdqTXn_T7SGr2Ho2KT8uw"
          ]
        }
      ]
    }

[« Delete shutdown API](delete-shutdown.md) [Repositories metering APIs
»](repositories-metering-apis.md)
