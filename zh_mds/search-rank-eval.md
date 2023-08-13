

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search APIs](search.md)

[« Field capabilities API](search-field-caps.md) [Vector tile search API
»](search-vector-tile-api.md)

## 排名评估接口

允许您通过一组典型搜索查询评估排名搜索结果的质量。

###Request

"获取/<target>/_rank_eval"

"发布/<target>/_rank_eval"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"读取"索引权限。

###Description

排名评估 API 允许您通过一组典型搜索查询来评估排名搜索结果的质量。给定这组查询和手动评级文档列表，"_rank_eval"端点计算并返回典型的信息检索指标_mean例如倒数rank_、_precision_ 或 _discounted 累积gain_。

搜索质量评估首先查看搜索应用程序的用户以及他们正在搜索的内容。用户有specific_information need_;例如，他们正在网上商店寻找礼物，或者想为下一个假期预订航班。他们通常在搜索框或其他网络表单中输入一些搜索词。所有这些信息，以及关于用户的元信息(例如浏览器、位置、早期偏好等)然后被转换为对底层搜索系统的查询。

搜索工程师面临的挑战是将这种转换过程从用户条目调整为具体的查询，以便搜索结果包含与用户信息需求最相关的信息。只有当在典型用户查询的代表性测试套件中不断评估搜索结果质量时，才能做到这一点，以便某个特定查询的排名改进不会对其他类型的查询的排名产生负面影响。

为了开始搜索质量评估，您需要三个基本要素：

1. 要评估查询性能的文档集合，通常是一个或多个数据流或索引。  2. 用户输入到系统中的典型搜索请求的集合。  3. 一组文档评级，代表文档与搜索请求的相关性。

请务必注意，每个测试查询需要一组文档评级，并且相关性判断基于输入查询的用户的信息需求。

排名评估 API 提供了一种在排名评估请求中使用此信息的便捷方法来计算不同的搜索评估指标。这为您提供了对整体搜索质量的初步估计，以及在微调应用程序中查询生成的各个方面时要优化的度量。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases used to limit the request. Supports wildcards (`*`). To target all data streams and indices, omit this parameter or use `*` or `_all`. 

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

在最基本的形式中，对"_rank_eval"端点的请求有两个部分：

    
    
    GET /my-index-000001/_rank_eval
    {
      "requests": [ ... ],                            __"metric": { __"mean_reciprocal_rank": { ... } __}
    }

__

|

一组典型的搜索请求，以及它们提供的评级 ---|--- __

|

定义要计算 __ 的评估指标

|

特定指标及其参数 请求部分包含应用程序特有的多个搜索请求，以及每个特定搜索请求的文档评级。

    
    
    GET /my-index-000001/_rank_eval
    {
      "requests": [
        {
          "id": "amsterdam_query",                                  __"request": { __"query": { "match": { "text": "amsterdam" } }
          },
          "ratings": [ __{ "_index": "my-index-000001", "_id": "doc1", "rating": 0 },
            { "_index": "my-index-000001", "_id": "doc2", "rating": 3 },
            { "_index": "my-index-000001", "_id": "doc3", "rating": 1 }
          ]
        },
        {
          "id": "berlin_query",
          "request": {
            "query": { "match": { "text": "berlin" } }
          },
          "ratings": [
            { "_index": "my-index-000001", "_id": "doc1", "rating": 1 }
          ]
        }
      ]
    }

__

|

搜索请求的 ID，用于稍后对结果详细信息进行分组。   ---|---    __

|

正在计算的查询。   __

|

文档评级列表。每个条目都包含以下参数：

* "_index"：文档的索引。对于数据流，这应该是文档的支持索引。  * "_id"：文档 ID。  * "评级"：文档与此搜索请求的相关性。

文档"评级"可以是任何整数值，用于在用户定义的刻度上表示文档的相关性。对于某些指标，只需给出二进制评级(例如"0"表示不相关，"1"表示相关)就足够了，而其他指标可以使用更细粒度的量表。

#### 基于模板的排名评估

作为必须为每个测试请求提供单个查询的替代方法，可以在评估请求中指定查询模板，并在以后引用它们。这样，具有类似结构且仅在参数上不同的查询不必在"请求"部分中一直重复。在典型的搜索系统中，用户输入通常会填充到一小组查询模板中，这有助于使评估请求更加简洁。

    
    
    GET /my-index-000001/_rank_eval
    {
       [...]
      "templates": [
         {
            "id": "match_one_field_query",  __"template": { __"inline": {
                    "query": {
                      "match": { "{{field}}": { "query": "{{query_string}}" }}
                    }
                }
            }
         }
      ],
      "requests": [
          {
             "id": "amsterdam_query",
             "ratings": [ ... ],
             "template_id": "match_one_field_query", __"params": { __"query_string": "amsterdam",
                "field": "text"
              }
         },
        [...]
    }

__

|

模板 ID ---|--- __

|

要使用的模板定义 __

|

对以前定义的模板 __ 的引用

|

用于填充模板的参数 您还可以使用存储的搜索模板。

    
    
    GET /my_index/_rank_eval
    {
       [...]
      "templates": [
         {
            "id": "match_one_field_query",  __"template": { __"id": "match_one_field_query"
            }
         }
      ],
      "requests": [...]
    }

__

|

用于请求的模板 ID ---|--- __

|

存储在群集状态中的模板 ID #### 可用评估指标编辑

"指标"部分确定将使用哪些可用的评估指标。支持以下指标：

##### K(P@k) 时的精度

此指标衡量相关结果在前 k 个搜索结果中的比例。它是众所周知的Precision#Precision)度量的一种形式，只查看前k个文档。它是前 k 个结果中相关文档的比例。精度为 10 (P@10) 值为 0.6 则意味着 10 个热门点击中有 6 个与用户的信息需求相关。

P@k作为一个简单的评估指标效果很好，具有易于理解和解释的好处。集合中的文档需要被评为与当前查询相关或不相关。P@k是基于 aset 的指标，不考虑相关文档在前 k 个结果中的位置，因此在位置 10 中包含一个相关结果的 10 个结果的排名与在位置 1 中包含 1 个相关结果的 10 个结果的排名同样好。

    
    
    response = client.rank_eval(
      index: 'my-index-000001',
      body: {
        requests: [
          {
            id: 'JFK query',
            request: {
              query: {
                match_all: {}
              }
            },
            ratings: []
          }
        ],
        metric: {
          precision: {
            k: 20,
            relevant_rating_threshold: 1,
            ignore_unlabeled: false
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_rank_eval
    {
      "requests": [
        {
          "id": "JFK query",
          "request": { "query": { "match_all": {} } },
          "ratings": []
        } ],
      "metric": {
        "precision": {
          "k": 20,
          "relevant_rating_threshold": 1,
          "ignore_unlabeled": false
        }
      }
    }

"精度"指标采用以下可选参数

参数 |描述 ---|--- 'k'

|

设置每个查询检索的最大文档数。此值将代替查询中常用的"size"参数。默认值为 10。   "relevant_rating_threshold"

|

设置评级阈值，高于该阈值的文档被视为"相关"。默认为"1"。   "ignore_unlabeled"

|

控制搜索结果中未标记的文档的计数方式。如果设置为 to_true_ ，则忽略未标记的文档，并且两者都不计为相关或不相关。设置为 _false_(默认值)，它们被视为不相关。   ##### 在 K(R@k)编辑处召回

此指标衡量前 k 个搜索结果中的相关结果总数。这是众所周知的Recall#Recall)度量的一种形式。它是前 k 个结果中相关文档相对于所有可能的相关结果的比例。召回值为0.5的10(R@10)则意味着8个相关文档中的4个，关于用户的信息需求，在10个热门中被检索到。

R@k作为一个简单的评估指标效果很好，具有易于理解和解释的好处。集合中的文档需要被评为与当前查询相关或不相关。R@k是基于 aset 的指标，不考虑相关文档在前 k 个结果中的位置，因此在位置 10 中包含一个相关结果的 10 个结果的排名与在位置 1 中包含 10 个相关结果的 10 个结果的排名同样好。

    
    
    response = client.rank_eval(
      index: 'my-index-000001',
      body: {
        requests: [
          {
            id: 'JFK query',
            request: {
              query: {
                match_all: {}
              }
            },
            ratings: []
          }
        ],
        metric: {
          recall: {
            k: 20,
            relevant_rating_threshold: 1
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_rank_eval
    {
      "requests": [
        {
          "id": "JFK query",
          "request": { "query": { "match_all": {} } },
          "ratings": []
        } ],
      "metric": {
        "recall": {
          "k": 20,
          "relevant_rating_threshold": 1
        }
      }
    }

"召回"指标采用以下可选参数

参数 |描述 ---|--- 'k'

|

设置每个查询检索的最大文档数。此值将代替查询中常用的"size"参数。默认值为 10。   "relevant_rating_threshold"

|

设置评级阈值，高于该阈值的文档被视为"相关"。默认为"1"。   ##### 平均倒数编辑

对于测试套件中的每个查询，此指标计算第一个相关文档排名的倒数。例如，在位置 3 中找到第一个相关结果意味着倒数排名为 1/3。每个查询的倒数在测试套件中的所有查询中取平均值，以给出平均倒数。

    
    
    response = client.rank_eval(
      index: 'my-index-000001',
      body: {
        requests: [
          {
            id: 'JFK query',
            request: {
              query: {
                match_all: {}
              }
            },
            ratings: []
          }
        ],
        metric: {
          mean_reciprocal_rank: {
            k: 20,
            relevant_rating_threshold: 1
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_rank_eval
    {
      "requests": [
        {
          "id": "JFK query",
          "request": { "query": { "match_all": {} } },
          "ratings": []
        } ],
      "metric": {
        "mean_reciprocal_rank": {
          "k": 20,
          "relevant_rating_threshold": 1
        }
      }
    }

"mean_reciprocal_rank"指标采用以下可选参数

参数 |描述 ---|--- 'k'

|

设置每个查询检索的最大文档数。此值将代替查询中常用的"size"参数。默认值为 10。   "relevant_rating_threshold"

|

设置评级阈值，高于该阈值的文档被视为"相关"。默认为"1"。   ##### 贴现累积收益 (DCG)编辑

与上述两个指标相比，折扣累积增益同时考虑了搜索结果的排名和评级。

假设高度相关的文档出现在结果列表的顶部时对用户更有用。因此，DCG 公式减少了搜索排名较低的文档的高评级对总体 DCG 指标的贡献。

    
    
    response = client.rank_eval(
      index: 'my-index-000001',
      body: {
        requests: [
          {
            id: 'JFK query',
            request: {
              query: {
                match_all: {}
              }
            },
            ratings: []
          }
        ],
        metric: {
          dcg: {
            k: 20,
            normalize: false
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_rank_eval
    {
      "requests": [
        {
          "id": "JFK query",
          "request": { "query": { "match_all": {} } },
          "ratings": []
        } ],
      "metric": {
        "dcg": {
          "k": 20,
          "normalize": false
        }
      }
    }

"dcg"指标采用以下可选参数：

参数 |描述 ---|--- 'k'

|

设置每个查询检索的最大文档数。此值将代替查询中常用的"size"参数。默认值为 10。   "正常化"

|

如果设置为"true"，则此指标将计算标准化 DCG。   ##### 预期倒数排名 (ERR)编辑

预期倒数排名 (ERR) 是分级相关性案例(Olivier Chapelle、Donald Metzler、YaZhang 和 Pierre Grinspan)的经典倒数的扩展。2009 年 1 月。分级相关性的预期倒数排名。

它基于搜索级联模型的假设，在该模型中，用户按顺序浏览排名的搜索结果，并在满足信息需求的第一个文档处停止。出于这个原因，它是问答和导航查询的良好指标，但对于面向调查的信息需求来说，用户有兴趣在前 k 个结果中查找许多相关文档，则不太重要。

该指标对用户停止读取结果列表的位置的倒数预期进行建模。这意味着排名靠前的相关文档将对总分做出很大贡献。但是，如果同一文档出现在较低的排名中，则对分数的贡献要小得多;如果之前有一些相关(但可能不太相关)的文档，则更是如此。这样，ERR 指标会折减在非常相关的文档之后显示的文档。这在相关文档的排序中引入了依赖关系的概念，例如精度或DCG不考虑在内。

    
    
    response = client.rank_eval(
      index: 'my-index-000001',
      body: {
        requests: [
          {
            id: 'JFK query',
            request: {
              query: {
                match_all: {}
              }
            },
            ratings: []
          }
        ],
        metric: {
          expected_reciprocal_rank: {
            maximum_relevance: 3,
            k: 20
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_rank_eval
    {
      "requests": [
        {
          "id": "JFK query",
          "request": { "query": { "match_all": {} } },
          "ratings": []
        } ],
      "metric": {
        "expected_reciprocal_rank": {
          "maximum_relevance": 3,
          "k": 20
        }
      }
    }

"expected_reciprocal_rank"指标采用以下参数：

参数 |描述 ---|--- 'maximum_relevance'

|

必需参数。用户提供的相关性判断中使用的最高相关性等级。   'k'

|

设置每个查询检索的最大文档数。此值将代替查询中常用的"size"参数。默认值为 10。   #### 响应格式编辑

"_rank_eval"端点的响应包含已定义质量指标的总体计算结果、包含测试套件中每个查询结果细分的"详细信息"部分以及显示单个查询潜在错误的可选"失败"部分。响应具有以下格式：

    
    
    {
      "rank_eval": {
        "metric_score": 0.4,                          __"details": {
          "my_query_id1": { __"metric_score": 0.6, __"unrated_docs": [ __{
                "_index": "my-index-000001",
                "_id": "1960795"
              }, ...
            ],
            "hits": [
              {
                "hit": { __"_index": "my-index-000001",
                  "_type": "page",
                  "_id": "1528558",
                  "_score": 7.0556192
                },
                "rating": 1
              }, ...
            ],
            "metric_details": { __"precision": {
                "relevant_docs_retrieved": 6,
                "docs_retrieved": 10
              }
            }
          },
          "my_query_id2": { [... ] }
        },
        "failures": { [... ] }
      }
    }

__

|

通过定义的指标 ---|--- __ 计算的总体评估质量

|

"详细信息"部分包含原始"请求"部分中每个查询的一个条目，由搜索请求 ID __ 键入

|

"详细信息"部分中的"metric_score"显示了此查询对全局质量指标分数的贡献 __

|

"unrated_docs"部分包含此查询的搜索结果中没有评级值的每个文档的"_index"和"_id"条目。这可用于要求用户为这些文档提供评级 __

|

"点击"部分显示一组搜索结果及其提供的评级 __

|

"metric_details"提供有关计算质量指标的其他信息(例如，有多少检索到的文档是相关的)。每个指标的内容各不相同，但可以更好地解释结果 « 字段功能 API 矢量图块搜索 API»