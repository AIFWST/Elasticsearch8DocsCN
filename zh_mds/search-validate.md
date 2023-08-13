

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search APIs](search.md)

[« Count API](search-count.md) [Terms enum API »](search-terms-enum.md)

## 验证接口

验证可能成本高昂的查询而不执行它。

    
    
    response = client.indices.validate_query(
      index: 'my-index-000001',
      q: 'user.id:kimchy'
    )
    puts response
    
    
    GET my-index-000001/_validate/query?q=user.id:kimchy

###Request

'获取 /<target>/_validate<query>/'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"读取"索引权限。

###Description

验证 API 允许您在不执行查询的情况下验证可能成本高昂的查询。查询可以作为路径参数发送，也可以在请求正文中发送。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases to search. Supports wildcards (`*`). To search all data streams or indices, omit this parameter or use `*` or `_all`. 
`query`

     (Optional, [query object](query-dsl.html "Query DSL")) Defines the search definition using the [Query DSL](query-dsl.html "Query DSL"). 

### 查询参数

`all_shards`

     (Optional, Boolean) If `true`, the validation is executed on all shards instead of one random shard per index. Defaults to `false`. 
`allow_no_indices`

    

(可选，布尔值)如果为"false"，则当任何通配符表达式、索引别名或"_all"值仅针对缺少或关闭的索引时，请求将返回错误。即使请求以其他打开的索引为目标，此行为也适用。例如，如果索引以"foo"开头但没有索引以"bar"开头，则以"foo*，bar*"为目标的请求将返回错误。

默认为"假"。

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

`explain`

     (Optional, Boolean) If `true`, the response returns detailed information if an error has occurred. Defaults to `false`. 
`ignore_unavailable`

     (Optional, Boolean) If `false`, the request returns an error if it targets a missing or closed index. Defaults to `false`. 
`lenient`

    

(可选，布尔值)如果为"true"，则将忽略查询字符串中基于格式的查询失败(例如向数值字段提供文本)。默认为"假"。

仅当指定了"q"查询字符串参数时，才能使用此参数。

`rewrite`

     (Optional, Boolean) If `true`, returns a more detailed explanation showing the actual Lucene query that will be executed. Defaults to `false`. 
`q`

     (Optional, string) Query in the Lucene query string syntax. 

###Examples

    
    
    response = client.bulk(
      index: 'my-index-000001',
      refresh: true,
      body: [
        {
          index: {
            _id: 1
          }
        },
        {
          user: {
            id: 'kimchy'
          },
          "@timestamp": '2099-11-15T14:12:12',
          message: 'trying out Elasticsearch'
        },
        {
          index: {
            _id: 2
          }
        },
        {
          user: {
            id: 'kimchi'
          },
          "@timestamp": '2099-11-15T14:12:13',
          message: 'My user ID is similar to kimchy!'
        }
      ]
    )
    puts response
    
    
    PUT my-index-000001/_bulk?refresh
    {"index":{"_id":1}}
    {"user" : { "id": "kimchy" }, "@timestamp" : "2099-11-15T14:12:12", "message" : "trying out Elasticsearch"}
    {"index":{"_id":2}}
    {"user" : { "id": "kimchi" }, "@timestamp" : "2099-11-15T14:12:13", "message" : "My user ID is similar to kimchy!"}

发送有效查询时：

    
    
    response = client.indices.validate_query(
      index: 'my-index-000001',
      q: 'user.id:kimchy'
    )
    puts response
    
    
    GET my-index-000001/_validate/query?q=user.id:kimchy

响应包含"valid：true"：

    
    
    {"valid":true,"_shards":{"total":1,"successful":1,"failed":0}}

查询也可以在请求正文中发送：

    
    
    response = client.indices.validate_query(
      index: 'my-index-000001',
      body: {
        query: {
          bool: {
            must: {
              query_string: {
                query: '*:*'
              }
            },
            filter: {
              term: {
                "user.id": 'kimchy'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_validate/query
    {
      "query" : {
        "bool" : {
          "must" : {
            "query_string" : {
              "query" : "*:*"
            }
          },
          "filter" : {
            "term" : { "user.id" : "kimchy" }
          }
        }
      }
    }

在正文中发送的查询必须嵌套在"查询"键中，与搜索 api 相同

如果查询无效，则"有效"将为"假"。这里的查询是无效的，因为 Elasticsearch 知道"post_date"字段应该是动态映射的日期，而 _foo_ 没有正确解析为日期：

    
    
    response = client.indices.validate_query(
      index: 'my-index-000001',
      body: {
        query: {
          query_string: {
            query: '@timestamp:foo',
            lenient: false
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_validate/query
    {
      "query": {
        "query_string": {
          "query": "@timestamp:foo",
          "lenient": false
        }
      }
    }
    
    
    {"valid":false,"_shards":{"total":1,"successful":1,"failed":0}}

#### 解释参数

可以指定"解释"参数以获取有关查询失败原因的更多详细信息：

    
    
    response = client.indices.validate_query(
      index: 'my-index-000001',
      explain: true,
      body: {
        query: {
          query_string: {
            query: '@timestamp:foo',
            lenient: false
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_validate/query?explain=true
    {
      "query": {
        "query_string": {
          "query": "@timestamp:foo",
          "lenient": false
        }
      }
    }

API 返回以下响应：

    
    
    {
      "valid" : false,
      "_shards" : {
        "total" : 1,
        "successful" : 1,
        "failed" : 0
      },
      "explanations" : [ {
        "index" : "my-index-000001",
        "valid" : false,
        "error" : "my-index-000001/IAEc2nIXSSunQA_suI0MLw] QueryShardException[failed to create query:...failed to parse date field [foo]"
      } ]
    }

#### 重写参数

当查询有效时，说明默认为该查询的字符串表示形式。将"重写"设置为"true"时，说明会更详细地显示将要执行的实际 Lucene 查询。

    
    
    response = client.indices.validate_query(
      index: 'my-index-000001',
      rewrite: true,
      body: {
        query: {
          more_like_this: {
            like: {
              _id: '2'
            },
            boost_terms: 1
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_validate/query?rewrite=true
    {
      "query": {
        "more_like_this": {
          "like": {
            "_id": "2"
          },
          "boost_terms": 1
        }
      }
    }

API 返回以下响应：

    
    
    {
       "valid": true,
       "_shards": {
          "total": 1,
          "successful": 1,
          "failed": 0
       },
       "explanations": [
          {
             "index": "my-index-000001",
             "valid": true,
             "explanation": "((user:terminator^3.71334 plot:future^2.763601 plot:human^2.8415773 plot:sarah^3.4193945 plot:kyle^3.8244398 plot:cyborg^3.9177752 plot:connor^4.040236 plot:reese^4.7133346 ... )~6) -ConstantScore(_id:2)) #(ConstantScore(_type:_doc))^0.0"
          }
       ]
    }

#### 重写和all_shardsparameters

默认情况下，请求仅在随机选择的单个分片上执行。查询的详细说明可能取决于被命中的分片，因此可能因请求而异。因此，在查询重写的情况下，应该使用"all_shards"参数来获取所有可用分片的响应。

    
    
    response = client.indices.validate_query(
      index: 'my-index-000001',
      rewrite: true,
      all_shards: true,
      body: {
        query: {
          match: {
            "user.id": {
              query: 'kimchy',
              fuzziness: 'auto'
            }
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_validate/query?rewrite=true&all_shards=true
    {
      "query": {
        "match": {
          "user.id": {
            "query": "kimchy",
            "fuzziness": "auto"
          }
        }
      }
    }

API 返回以下响应：

    
    
    {
      "valid": true,
      "_shards": {
        "total": 1,
        "successful": 1,
        "failed": 0
      },
      "explanations": [
        {
          "index": "my-index-000001",
          "shard": 0,
          "valid": true,
          "explanation": "(user.id:kimchi)^0.8333333 user.id:kimchy"
        }
      ]
    }

[« Count API](search-count.md) [Terms enum API »](search-terms-enum.md)
