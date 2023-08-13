

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Bucket aggregations](search-aggregations-bucket.md) [Auto-interval date
histogram aggregation »](search-aggregations-bucket-autodatehistogram-
aggregation.md)

## 邻接矩阵聚合

返回邻接矩阵形式的存储桶聚合。该请求提供命名筛选器表达式的集合，类似于"筛选器"聚合请求。响应中的每个存储桶表示相交筛选器矩阵中的一个非空单元格。

给定名为"A"、"B"和"C"的筛选器，响应将返回具有以下名称的存储桶：

|一 |乙 |C ---|---|---|--- **A**

|

A

|

A&B

|

A&C **B**

|

|

B

|

B&C **C**

|

|

|

C 相交的存储桶(例如"A&C")使用两个过滤器名称的组合和默认分隔符"&"进行标记。请注意，响应不包括"C&A"存储桶，因为这将与"A&C"文档集相同。据说矩阵是_对称_的，所以我们只返回它的一半。为此，我们对过滤器名称字符串进行排序，并始终使用一对中最小的值作为分隔符左侧的值。

###Example

以下"交互"聚合使用"adjacency_matrix"来确定哪些个人组交换了电子邮件。

    
    
    response = client.bulk(
      index: 'emails',
      refresh: true,
      body: [
        {
          index: {
            _id: 1
          }
        },
        {
          accounts: [
            'hillary',
            'sidney'
          ]
        },
        {
          index: {
            _id: 2
          }
        },
        {
          accounts: [
            'hillary',
            'donald'
          ]
        },
        {
          index: {
            _id: 3
          }
        },
        {
          accounts: [
            'vladimir',
            'donald'
          ]
        }
      ]
    )
    puts response
    
    response = client.search(
      index: 'emails',
      body: {
        size: 0,
        aggregations: {
          interactions: {
            adjacency_matrix: {
              filters: {
                "grpA": {
                  terms: {
                    accounts: [
                      'hillary',
                      'sidney'
                    ]
                  }
                },
                "grpB": {
                  terms: {
                    accounts: [
                      'donald',
                      'mitt'
                    ]
                  }
                },
                "grpC": {
                  terms: {
                    accounts: [
                      'vladimir',
                      'nigel'
                    ]
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT emails/_bulk?refresh
    { "index" : { "_id" : 1 } }
    { "accounts" : ["hillary", "sidney"]}
    { "index" : { "_id" : 2 } }
    { "accounts" : ["hillary", "donald"]}
    { "index" : { "_id" : 3 } }
    { "accounts" : ["vladimir", "donald"]}
    
    GET emails/_search
    {
      "size": 0,
      "aggs" : {
        "interactions" : {
          "adjacency_matrix" : {
            "filters" : {
              "grpA" : { "terms" : { "accounts" : ["hillary", "sidney"] }},
              "grpB" : { "terms" : { "accounts" : ["donald", "mitt"] }},
              "grpC" : { "terms" : { "accounts" : ["vladimir", "nigel"] }}
            }
          }
        }
      }
    }

响应包含存储桶，其中包含每个筛选器的文档计数和筛选器组合。没有匹配文档的存储桶将从响应中排除。

    
    
    {
      "took": 9,
      "timed_out": false,
      "_shards": ...,
      "hits": ...,
      "aggregations": {
        "interactions": {
          "buckets": [
            {
              "key":"grpA",
              "doc_count": 2
            },
            {
              "key":"grpA&grpB",
              "doc_count": 1
            },
            {
              "key":"grpB",
              "doc_count": 2
            },
            {
              "key":"grpB&grpC",
              "doc_count": 1
            },
            {
              "key":"grpC",
              "doc_count": 1
            }
          ]
        }
      }
    }

###Parameters

`filters`

    

(必填，对象)用于创建存储桶的筛选器。

"过滤器"的属性

`<filter>`

    

(必需，查询 DSL 对象)用于筛选文档的查询。键是筛选器名称。

至少需要一个筛选器。筛选器的总数不能超过"index.query.bool.max_clause_count"设置。请参阅筛选器限制。

`separator`

     (Optional, string) Separator used to concatenate filter names. Defaults to `&`. 

### 响应正文

`key`

     (string) Filters for the bucket. If the bucket uses multiple filters, filter names are concatenated using a `separator`. 
`doc_count`

     (integer) Number of documents matching the bucket's filters. 

###Usage

此聚合本身可以提供创建无向加权图所需的所有数据。但是，当与子聚合(如"date_histogram")一起使用时，结果可以提供执行动态网络分析所需的额外数据级别，其中检查交互_over time_变得很重要。

### 过滤器限制

对于 N 过滤器，生成的桶矩阵可以是 N²/2，这可能很昂贵。断路器设置可防止结果产生过多的存储桶，并避免过多的磁盘查找"index.query.bool.max_clause_count"设置用于限制过滤器的数量。

[« Bucket aggregations](search-aggregations-bucket.md) [Auto-interval date
histogram aggregation »](search-aggregations-bucket-autodatehistogram-
aggregation.md)
