

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search APIs](search.md)

[« kNN search API](knn-search-api.md) [Scroll API »](scroll-api.md)

## 倒数排名融合

此功能为技术预览版，可能会在将来的版本中进行更改或删除。语法可能会在正式发布之前发生变化。 Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持约束。

倒数秩融合(RRF)是一种将具有不同相关性指标的多个结果集组合成单个结果集的方法。RRF不需要调整，不同的相关性指标不必相互关联即可获得高质量的结果。

RRF 使用以下公式来确定每个文档的排名分数：

    
    
    score = 0.0
    for q in queries:
        if d in result(q):
            score += 1.0 / ( k + rank( result(q), d ) )
    return score
    
    # where
    # k is a ranking constant
    # q is a query in the set of queries
    # d is a document in the result set of q
    # result(q) is the result set of q
    # rank( result(q), d ) is d's rank within the result(q) starting from 1

### 倒数排名融合API

您可以使用 RRF 作为搜索的一部分，以使用来自查询、子搜索和/或 knn 搜索组合的结果集对文档进行组合和排名。至少需要 2 个结果集才能从指定源进行排名。

"rrf"参数是一个可选对象，定义为搜索请求的排名参数的一部分。'rrf'对象包含以下参数：

`rank_constant`

     (Optional, integer) This value determines how much influence documents in individual result sets per query have over the final ranked result set. A higher value indicates that lower ranked documents have more influence. This value must be greater than or equal to `1`. Defaults to `60`. 
`window_size`

     (Optional, integer) This value determines the size of the individual result sets per query. A higher value will improve result relevance at the cost of performance. The final ranked result set is pruned down to the search request's <<search-size-param, size>. `window_size` must be greater than or equal to `size` and greater than or equal to `1`. Defaults to `100`. 

使用 RRF 的示例请求：

    
    
    GET example-index/_search
    {
        "query": {
            "term": {
                "text": "shoes"
            }
        },
        "knn": {
            "field": "vector",
            "query_vector": [1.25, 2, 3.5],
            "k": 50,
            "num_candidates": 100
        },
        "rank": {
            "rrf": {
                "window_size": 50,
                "rank_constant": 20
            }
        }
    }

在上面的例子中，我们首先执行 kNN 搜索以获得其全局前 50 个结果。然后我们执行查询以获得其全局前 50 个结果。之后，在一个协调节点上，我们将knn搜索结果与查询结果相结合，并根据RRF方法对它们进行排名，以获得最终的前10个结果。

请注意，如果 knn 搜索中的"k"大于"window_size"，则结果将被截断为"window_size"。如果"k"小于"window_size"，则结果为"k"大小。

### 倒数排名融合支持的功能

RRF 确实支持：

* 子搜索 * 聚合 * 来自

RRF 目前不支持：

* 滚动 * 时间点 * 排序 * 重新评分 * 建议者 * 突出显示 * 折叠 * 解释 * 分析

使用 RRF 进行搜索时，使用不受支持的功能会导致异常。

### 使用子搜索的倒数排名融合

子搜索提供了一种使用 RRF 组合和排名多个搜索的方法。

将 RRF 与子搜索一起使用的示例请求：

    
    
    GET example-index/_search
    {
        "sub_searches": [
            {
                "query": {
                    "term": {
                        "text": "blue shoes sale"
                    }
                }
            },
            {
                "query": {
                    "text_expansion":{
                        "ml.tokens":{
                            "model_id":"my_elser_model",
                            "model_text":"What blue shoes are on sale?"
                         }
                    }
                }
            }
        ],
        "rank": {
            "rrf": {
                "window_size": 50,
                "rank_constant": 20
            }
        }
    }

在上面的例子中，我们彼此独立地执行两个子搜索中的每一个。首先，我们使用标准 BM25 评分算法运行"蓝鞋销售"的术语查询。然后，我们使用 ELSER 评分算法运行"哪些蓝色鞋子在打折？"的文本扩展查询。RRF 允许我们将完全独立的评分算法生成的两个结果集与相同的权重组合在一起。这不仅消除了使用线性组合来确定适当权重的需要，而且 RRF 还表明可以单独提高任一查询的相关性。

### 倒数秩融合完整示例

我们首先为具有文本字段、向量字段和整数字段的索引创建映射，并为多个文档编制索引。在本例中，我们将使用只有一个维度的向量，以使排名更易于解释。

    
    
    response = client.indices.create(
      index: 'example-index',
      body: {
        mappings: {
          properties: {
            text: {
              type: 'text'
            },
            vector: {
              type: 'dense_vector',
              dims: 1,
              index: true,
              similarity: 'l2_norm'
            },
            integer: {
              type: 'integer'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'example-index',
      id: 1,
      body: {
        text: 'rrf',
        vector: [
          5
        ],
        integer: 1
      }
    )
    puts response
    
    response = client.index(
      index: 'example-index',
      id: 2,
      body: {
        text: 'rrf rrf',
        vector: [
          4
        ],
        integer: 2
      }
    )
    puts response
    
    response = client.index(
      index: 'example-index',
      id: 3,
      body: {
        text: 'rrf rrf rrf',
        vector: [
          3
        ],
        integer: 1
      }
    )
    puts response
    
    response = client.index(
      index: 'example-index',
      id: 4,
      body: {
        text: 'rrf rrf rrf rrf',
        integer: 2
      }
    )
    puts response
    
    response = client.index(
      index: 'example-index',
      id: 5,
      body: {
        vector: [
          0
        ],
        integer: 1
      }
    )
    puts response
    
    response = client.indices.refresh(
      index: 'example-index'
    )
    puts response
    
    
    PUT example-index
    {
      "mappings": {
            "properties": {
                "text" : {
                    "type" : "text"
                },
                "vector": {
                    "type": "dense_vector",
                    "dims": 1,
                    "index": true,
                    "similarity": "l2_norm"
                },
                "integer" : {
                    "type" : "integer"
                }
            }
        }
    }
    
    PUT example-index/_doc/1
    {
        "text" : "rrf",
        "vector" : [5],
        "integer": 1
    }
    
    PUT example-index/_doc/2
    {
        "text" : "rrf rrf",
        "vector" : [4],
        "integer": 2
    }
    
    PUT example-index/_doc/3
    {
        "text" : "rrf rrf rrf",
        "vector" : [3],
        "integer": 1
    }
    
    PUT example-index/_doc/4
    {
        "text" : "rrf rrf rrf rrf",
        "integer": 2
    }
    
    PUT example-index/_doc/5
    {
        "vector" : [0],
        "integer": 1
    }
    
    POST example-index/_refresh

我们现在使用 RRF 执行搜索，其中包含查询、kNN 搜索和术语聚合。

    
    
    GET example-index/_search
    {
        "query": {
            "term": {
                "text": "rrf"
            }
        },
        "knn": {
            "field": "vector",
            "query_vector": [3],
            "k": 5,
            "num_candidates": 5
        },
        "rank": {
            "rrf": {
                "window_size": 5,
                "rank_constant": 1
            }
        },
        "size": 3,
        "aggs": {
            "int_count": {
                "terms": {
                    "field": "integer"
                }
            }
        }
    }

我们收到带有排名"点击"和术语聚合结果的响应。请注意，"_score"是"null"，我们改为使用"_rank"来显示我们排名靠前的文档。

    
    
    {
        "took": ...,
        "timed_out" : false,
        "_shards" : {
            "total" : 1,
            "successful" : 1,
            "skipped" : 0,
            "failed" : 0
        },
        "hits" : {
            "total" : {
                "value" : 5,
                "relation" : "eq"
            },
            "max_score" : null,
            "hits" : [
                {
                    "_index" : "example-index",
                    "_id" : "3",
                    "_score" : null,
                    "_rank" : 1,
                    "_source" : {
                        "integer" : 1,
                        "vector" : [
                            3
                        ],
                        "text" : "rrf rrf rrf"
                    }
                },
                {
                    "_index" : "example-index",
                    "_id" : "2",
                    "_score" : null,
                    "_rank" : 2,
                    "_source" : {
                        "integer" : 2,
                        "vector" : [
                            4
                        ],
                        "text" : "rrf rrf"
                    }
                },
                {
                    "_index" : "example-index",
                    "_id" : "4",
                    "_score" : null,
                    "_rank" : 3,
                    "_source" : {
                        "integer" : 2,
                        "text" : "rrf rrf rrf rrf"
                    }
                }
            ]
        },
        "aggregations" : {
            "int_count" : {
                "doc_count_error_upper_bound" : 0,
                "sum_other_doc_count" : 0,
                "buckets" : [
                    {
                        "key" : 1,
                        "doc_count" : 3
                    },
                    {
                        "key" : 2,
                        "doc_count" : 2
                    }
                ]
            }
        }
    }

让我们分解一下这些点击是如何排名的。我们首先分别运行查询和 kNN 搜索，以收集它们各自的命中数。

首先，我们查看查询的命中率。

    
    
    "hits" : [
        {
            "_index" : "example-index",
            "_id" : "4",
            "_score" : 0.16152832,              __"_source" : {
                "integer" : 2,
                "text" : "rrf rrf rrf rrf"
            }
        },
        {
            "_index" : "example-index",
            "_id" : "3", __"_score" : 0.15876243,
            "_source" : {
                "integer" : 1,
                "vector" : [3],
                "text" : "rrf rrf rrf"
            }
        },
        {
            "_index" : "example-index",
            "_id" : "2", __"_score" : 0.15350538,
            "_source" : {
                "integer" : 2,
                "vector" : [4],
                "text" : "rrf rrf"
            }
        },
        {
            "_index" : "example-index",
            "_id" : "1", __"_score" : 0.13963442,
            "_source" : {
                "integer" : 1,
                "vector" : [5],
                "text" : "rrf"
            }
        }
    ]

__

|

排名 1， '_id' 4 ---|--- __

|

排名 2， '_id' 3 __

|

排名 3， '_id' 2 __

|

排名 4，"_id" 1 请注意，我们的第一次命中没有"矢量"字段的值。现在，我们查看 kNN 搜索的结果。

    
    
    "hits" : [
        {
            "_index" : "example-index",
            "_id" : "3",                   __"_score" : 1.0,
            "_source" : {
                "integer" : 1,
                "vector" : [3],
                "text" : "rrf rrf rrf"
            }
        },
        {
            "_index" : "example-index",
            "_id" : "2", __"_score" : 0.5,
            "_source" : {
                "integer" : 2,
                "vector" : [4],
                "text" : "rrf rrf"
            }
        },
        {
            "_index" : "example-index",
            "_id" : "1", __"_score" : 0.2,
            "_source" : {
                "integer" : 1,
                "vector" : [5],
                "text" : "rrf"
            }
        },
        {
            "_index" : "example-index",
            "_id" : "5", __"_score" : 0.1,
            "_source" : {
                "integer" : 1,
                "vector" : [0]
            }
        }
    ]

__

|

排名 1， '_id' 3 ---|--- __

|

等级 2， '_id' 2 __

|

排名 3， '_id' 1 __

|

排名 4，'_id' 5 现在，我们可以采用两个单独排名的结果集，并将 RRF公式应用于它们以获得最终排名。

    
    
    # doc  | query     | knn       | score
    _id: 1 = 1.0/(1+4) + 1.0/(1+3) = 0.4500
    _id: 2 = 1.0/(1+3) + 1.0/(1+2) = 0.5833
    _id: 3 = 1.0/(1+2) + 1.0/(1+1) = 0.8333
    _id: 4 = 1.0/(1+1)             = 0.5000
    _id: 5 =             1.0/(1+4) = 0.2000

我们根据 RRF 公式对文档进行排名，"window_size"为"5"，截断 RRF 结果集中底部的"2"文档，"大小"为"3"。我们以"_id：3"作为"_rank：1"，"_id：2"作为"_rank：2"，将"_id：4"作为"_rank：3"结束。此排名与原始 RRF 搜索的结果集匹配。

[« kNN search API](knn-search-api.md) [Scroll API »](scroll-api.md)
