

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search APIs](search.md)

[« Terms enum API](search-terms-enum.md) [Profile API »](search-
profile.md)

## 解释接口

返回有关特定文档为何匹配(或不匹配)查询的信息。

    
    
    response = client.explain(
      index: 'my-index-000001',
      id: 0,
      body: {
        query: {
          match: {
            message: 'elasticsearch'
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_explain/0
    {
      "query" : {
        "match" : { "message" : "elasticsearch" }
      }
    }

###Request

'获取 /<index>/_explain<id>/'

'发布 /<index>/_explain<id>/'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则必须对目标索引具有"读取"索引权限。

###Description

解释 API 计算查询和特定文档的分数解释。无论文档是否匹配特定查询，这都可以提供有用的反馈。

### 路径参数

`<id>`

     (Required, integer) Defines the document ID. 
`<index>`

    

(必需，字符串)用于限制请求的索引名称。

只能为此参数提供一个索引名称。

### 查询参数

`analyzer`

    

(可选，字符串)用于查询字符串的分析器。

仅当指定了"q"查询字符串参数时，才能使用此参数。

`analyze_wildcard`

    

(可选，布尔值)如果为"true"，则分析通配符和前缀查询。默认为"假"。

仅当指定了"q"查询字符串参数时，才能使用此参数。

`default_operator`

    

(可选，字符串)查询字符串查询的默认运算符：AND 或 OR。默认为"或"。

仅当指定了"q"查询字符串参数时，才能使用此参数。

`df`

    

(可选，字符串)用作默认值的字段，其中查询字符串中未提供字段前缀。

仅当指定了"q"查询字符串参数时，才能使用此参数。

`lenient`

    

(可选，布尔值)如果为"true"，则将忽略查询字符串中基于格式的查询失败(例如向数值字段提供文本)。默认为"假"。

仅当指定了"q"查询字符串参数时，才能使用此参数。

`preference`

     (Optional, string) Specifies the node or shard the operation should be performed on. Random by default. 
`q`

     (Optional, string) Query in the Lucene query string syntax. 
`stored_fields`

     (Optional, string) A comma-separated list of stored fields to return in the response. 
`routing`

     (Optional, string) Custom value used to route operations to a specific shard. 
`_source`

     (Optional, string) True or false to return the `_source` field or not, or a list of fields to return. 
`_source_excludes`

    

(可选，字符串)要从响应中排除的源字段的逗号分隔列表。

您还可以使用此参数从"_source_includes"查询参数中指定的子集中排除字段。

如果"_source"参数为"false"，则忽略此参数。

`_source_includes`

    

(可选，字符串)要包含在响应中的源字段的逗号分隔列表。

如果指定此参数，则仅返回这些源字段。您可以使用"_source_excludes"查询参数从此子集中排除字段。

如果"_source"参数为"false"，则忽略此参数。

### 请求正文

`query`

     (Optional, [query object](query-dsl.html "Query DSL")) Defines the search definition using the [Query DSL](query-dsl.html "Query DSL"). 

###Examples

    
    
    response = client.explain(
      index: 'my-index-000001',
      id: 0,
      body: {
        query: {
          match: {
            message: 'elasticsearch'
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_explain/0
    {
      "query" : {
        "match" : { "message" : "elasticsearch" }
      }
    }

API 返回以下响应：

    
    
    {
       "_index":"my-index-000001",
       "_id":"0",
       "matched":true,
       "explanation":{
          "value":1.6943598,
          "description":"weight(message:elasticsearch in 0) [PerFieldSimilarity], result of:",
          "details":[
             {
                "value":1.6943598,
                "description":"score(freq=1.0), computed as boost * idf * tf from:",
                "details":[
                   {
                      "value":2.2,
                      "description":"boost",
                      "details":[]
                   },
                   {
                      "value":1.3862944,
                      "description":"idf, computed as log(1 + (N - n + 0.5) / (n + 0.5)) from:",
                      "details":[
                         {
                            "value":1,
                            "description":"n, number of documents containing term",
                            "details":[]
                         },
                         {
                            "value":5,
                            "description":"N, total number of documents with field",
                            "details":[]
                         }
                      ]
                   },
                   {
                      "value":0.5555556,
                      "description":"tf, computed as freq / (freq + k1 * (1 - b + b * dl / avgdl)) from:",
                      "details":[
                         {
                            "value":1.0,
                            "description":"freq, occurrences of term within document",
                            "details":[]
                         },
                         {
                            "value":1.2,
                            "description":"k1, term saturation parameter",
                            "details":[]
                         },
                         {
                            "value":0.75,
                            "description":"b, length normalization parameter",
                            "details":[]
                         },
                         {
                            "value":3.0,
                            "description":"dl, length of field",
                            "details":[]
                         },
                         {
                            "value":5.4,
                            "description":"avgdl, average length of field",
                            "details":[]
                         }
                      ]
                   }
                ]
             }
          ]
       }
    }

还有一种更简单的方法可以通过"q"参数指定查询。然后解析指定的"q"参数值，就像使用了"query_string"查询一样。解释 API 中"q"参数的示例用法：

    
    
    response = client.explain(
      index: 'my-index-000001',
      id: 0,
      q: 'message:search'
    )
    puts response
    
    
    GET /my-index-000001/_explain/0?q=message:search

API 返回与上一个请求相同的结果。

[« Terms enum API](search-terms-enum.md) [Profile API »](search-
profile.md)
