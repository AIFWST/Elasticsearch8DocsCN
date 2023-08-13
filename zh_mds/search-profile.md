

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search APIs](search.md)

[« Explain API](search-explain.md) [Field capabilities API »](search-field-
caps.md)

## 配置文件接口

配置文件 API 是一种调试工具，会显著增加搜索执行开销。

提供有关在搜索请求中执行各个组件的详细计时信息。

###Description

配置文件 API 使用户深入了解如何在低级别执行搜索请求，以便用户可以了解某些请求运行缓慢的原因，并采取措施改进它们。请注意，Profile API 不会测量网络延迟、请求在队列中花费的时间或在协调节点上合并分片响应所花费的时间。

配置文件 API 的输出非常详细，尤其是跨多个分片执行的复杂请求。建议漂亮地打印响应，以帮助理解输出。

###Examples

任何"_search"请求都可以通过添加顶级"配置文件"参数来分析：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        profile: true,
        query: {
          match: {
            message: 'GET /search'
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search
    {
      "profile": true, __"query" : {
        "match" : { "message" : "GET /search" }
      }
    }

__

|

将顶级"配置文件"参数设置为"true"将为搜索启用分析。   ---|--- API 返回以下结果：

    
    
    {
      "took": 25,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": {
          "value": 5,
          "relation": "eq"
        },
        "max_score": 0.17402273,
        "hits": [...] __},
      "profile": {
        "shards": [
          {
            "id": "[2aE02wS1R8q_QFnYu6vDVQ][my-index-000001][0]",
            "searches": [
              {
                "query": [
                  {
                    "type": "BooleanQuery",
                    "description": "message:get message:search",
                    "time_in_nanos" : 11972972,
                    "breakdown" : {
                      "set_min_competitive_score_count": 0,
                      "match_count": 5,
                      "shallow_advance_count": 0,
                      "set_min_competitive_score": 0,
                      "next_doc": 39022,
                      "match": 4456,
                      "next_doc_count": 5,
                      "score_count": 5,
                      "compute_max_score_count": 0,
                      "compute_max_score": 0,
                      "advance": 84525,
                      "advance_count": 1,
                      "score": 37779,
                      "build_scorer_count": 2,
                      "create_weight": 4694895,
                      "shallow_advance": 0,
                      "create_weight_count": 1,
                      "build_scorer": 7112295,
                      "count_weight": 0,
                      "count_weight_count": 0
                    },
                    "children": [
                      {
                        "type": "TermQuery",
                        "description": "message:get",
                        "time_in_nanos": 3801935,
                        "breakdown": {
                          "set_min_competitive_score_count": 0,
                          "match_count": 0,
                          "shallow_advance_count": 3,
                          "set_min_competitive_score": 0,
                          "next_doc": 0,
                          "match": 0,
                          "next_doc_count": 0,
                          "score_count": 5,
                          "compute_max_score_count": 3,
                          "compute_max_score": 32487,
                          "advance": 5749,
                          "advance_count": 6,
                          "score": 16219,
                          "build_scorer_count": 3,
                          "create_weight": 2382719,
                          "shallow_advance": 9754,
                          "create_weight_count": 1,
                          "build_scorer": 1355007,
                          "count_weight": 0,
                          "count_weight_count": 0
                        }
                      },
                      {
                        "type": "TermQuery",
                        "description": "message:search",
                        "time_in_nanos": 205654,
                        "breakdown": {
                          "set_min_competitive_score_count": 0,
                          "match_count": 0,
                          "shallow_advance_count": 3,
                          "set_min_competitive_score": 0,
                          "next_doc": 0,
                          "match": 0,
                          "next_doc_count": 0,
                          "score_count": 5,
                          "compute_max_score_count": 3,
                          "compute_max_score": 6678,
                          "advance": 12733,
                          "advance_count": 6,
                          "score": 6627,
                          "build_scorer_count": 3,
                          "create_weight": 130951,
                          "shallow_advance": 2512,
                          "create_weight_count": 1,
                          "build_scorer": 46153,
                          "count_weight": 0,
                          "count_weight_count": 0
                        }
                      }
                    ]
                  }
                ],
                "rewrite_time": 451233,
                "collector": [
                  {
                    "name": "SimpleTopScoreDocCollector",
                    "reason": "search_top_hits",
                    "time_in_nanos": 775274
                  }
                ]
              }
            ],
            "aggregations": [],
            "fetch": {
              "type": "fetch",
              "description": "",
              "time_in_nanos": 660555,
              "breakdown": {
                "next_reader": 7292,
                "next_reader_count": 1,
                "load_stored_fields": 299325,
                "load_stored_fields_count": 5,
                "load_source": 3863,
                "load_source_count": 5
              },
              "debug": {
                "stored_fields": ["_id", "_routing", "_source"]
              },
              "children": [
                {
                  "type": "FetchSourcePhase",
                  "description": "",
                  "time_in_nanos": 20443,
                  "breakdown": {
                    "next_reader": 745,
                    "next_reader_count": 1,
                    "process": 19698,
                    "process_count": 5
                  },
                  "debug": {
                    "fast_path": 5
                  }
                },
                {
                  "type": "StoredFieldsPhase",
                  "description": "",
                  "time_in_nanos": 5310,
                  "breakdown": {
                    "next_reader": 745,
                    "next_reader_count": 1,
                    "process": 4445,
                    "process_count": 5
                  }
                }
              ]
            }
          }
        ]
      }
    }

__

|

将返回搜索结果，但为简洁起见，此处省略了搜索结果。   ---|--- 即使对于简单的查询，响应也相对复杂。在转向更复杂的示例之前，让我们逐个分解。

配置文件响应的整体结构如下：

    
    
    {
       "profile": {
            "shards": [
               {
                  "id": "[2aE02wS1R8q_QFnYu6vDVQ][my-index-000001][0]",  __"searches": [
                     {
                        "query": [...], __"rewrite_time": 51443, __"collector": [...] __}
                  ],
                  "aggregations": [...], __"fetch": {...} __}
            ]
         }
    }

__

|

将为参与响应的每个分片返回一个配置文件，并由唯一 ID 标识。   ---|---    __

|

查询计时和其他调试信息。   __

|

累计重写时间。   __

|

每个收集器的名称和调用计时。   __

|

聚合计时、调用计数和调试信息。   __

|

获取计时和调试信息。   由于搜索请求可能会针对 anindex 中的一个或多个分片执行，并且搜索可能涵盖一个或多个索引，因此配置文件响应中的顶级元素是"分片"对象数组。每个分片对象都列出其唯一标识分片的"id"。ID 的格式为 '[nodeID][indexName][shardID]"。

配置文件本身可能包含一个或多个"搜索"，其中搜索是针对基础 Lucene 索引执行的查询。用户提交的大多数搜索请求只会对 Luceneindex 执行一次"搜索"。但偶尔会执行多个搜索，例如包括全局聚合(需要对全局上下文执行辅助"match_all"查询)。

在每个"搜索"对象中，将有两个分析信息的数组："查询"数组和"收集器"数组。在"搜索"对象旁边是一个"聚合"对象，其中包含聚合的配置文件信息。将来可能会添加更多部分，例如"建议"，"突出显示"等。

还将有一个"重写"指标，显示重写查询所花费的总时间(以纳秒为单位)。

与其他统计信息 API 一样，配置文件 API 支持人类可读的输出。这可以通过在查询字符串中添加"？human=true"来启用。在这种情况下，输出包含额外的"时间"字段，其中包含四舍五入的人类可读的计时信息(例如，"时间"："391，9ms"，"时间"："123.3micros")。

### 分析查询

Profile API 提供的详细信息直接公开了 Lucene 类名和概念，这意味着对结果的完整解释需要相当高级的 Lucene 知识。本页尝试提供 Lucene 如何执行查询的速成课程，以便您可以使用配置文件 API 成功诊断和调试查询，但这只是一个概述。为了完全理解，请参考 Lucene 的文档以及某些地方的代码。

话虽如此，通常不需要完全了解来修复慢查询。例如，通常只要看到查询的特定组件很慢就足够了，并且不一定理解为什么该查询的"高级"阶段是原因。

#### '查询'部分

"查询"部分包含Lucene在特定分片上执行的查询树的详细时间。此查询树的整体结构类似于原始的 Elasticsearch 查询，但可能略有(或有时非常)不同。它还将使用相似但并不总是相同的命名。使用我们之前的"匹配"查询示例，让我们分析"查询"部分：

    
    
    "query": [
        {
           "type": "BooleanQuery",
           "description": "message:get message:search",
           "time_in_nanos": "11972972",
           "breakdown": {...},               __"children": [
              {
                 "type": "TermQuery",
                 "description": "message:get",
                 "time_in_nanos": "3801935",
                 "breakdown": {...}
              },
              {
                 "type": "TermQuery",
                 "description": "message:search",
                 "time_in_nanos": "205654",
                 "breakdown": {...}
              }
           ]
        }
    ]

__

|

为简单起见，省略了故障时间。   ---|--- 基于配置文件结构，我们可以看到我们的"match"查询被Lucene重写为具有两个子句的BooleanQuery(都包含aTermQuery)。"type"字段显示Lucene类名，并且通常与Elasticsearch中的等效名称对齐。"description"字段显示查询的Lucene解释文本，并可用于帮助区分查询的各个部分(例如，"message：get"和"message：search"都是TermQuery的，否则看起来相同。

"time_in_nanos"字段显示，整个布尔查询的执行需要 ~11.9 毫秒。记录的时间包括所有儿童。

"细分"字段将提供有关时间花费方式的详细统计数据，我们稍后会看看。最后，"子"数组列出了可能存在的任何子查询。因为我们搜索了两个值("getsearch")，所以我们的布尔查询包含两个子术语查询。它们具有相同的信息(类型，时间，故障等)。允许孩子有自己的孩子。

#### 时序细分

"细分"组件列出了有关低级Lucene执行的详细计时统计信息：

    
    
    "breakdown": {
      "set_min_competitive_score_count": 0,
      "match_count": 5,
      "shallow_advance_count": 0,
      "set_min_competitive_score": 0,
      "next_doc": 39022,
      "match": 4456,
      "next_doc_count": 5,
      "score_count": 5,
      "compute_max_score_count": 0,
      "compute_max_score": 0,
      "advance": 84525,
      "advance_count": 1,
      "score": 37779,
      "build_scorer_count": 2,
      "create_weight": 4694895,
      "shallow_advance": 0,
      "create_weight_count": 1,
      "build_scorer": 7112295,
      "count_weight": 0,
      "count_weight_count": 0
    }

计时以挂钟纳秒为单位列出，根本没有规范化。关于整体"time_in_nanos"的所有警告都适用于此处。分解的目的是让你感受一下 A) Lucene 中的什么机器实际上在消耗时间，以及 B) 各种组件之间的时间差异大小。与总时间一样，细分包括所有儿童时间。

统计数据的含义如下：

##### 所有参数：

`create_weight`

|

Lucene 中的查询必须能够在多个 IndexSearcher 中重用(将其视为针对特定 LuceneIndex 执行搜索的引擎)。这使Lucene陷入了一个棘手的境地，因为许多查询需要累积与使用它的索引关联的临时状态/统计信息，但查询合约要求它必须是不可变的。   为了解决这个问题，Lucene要求每个查询生成一个权重对象，该对象充当临时上下文对象来保存与此特定(IndexSearcher，Query)元组关联的状态。"权重"指标显示此过程需要多长时间---|---"build_scorer"

|

此参数显示为查询生成记分器所需的时间。AScorer 是一种循环访问匹配文档并生成每个文档分数的机制(例如，"foo"与文档的匹配程度如何？请注意，这记录的是生成 Scorer 对象所需的时间，而不是实际对文档进行评分。某些查询对 Scorer 的初始化速度更快或更慢，具体取决于优化、复杂性等。   这也可能显示与缓存相关的计时(如果启用和/或适用于查询"next_doc"

|

Lucene 方法"next_doc"返回与查询匹配的下一个文档的文档 ID。此统计信息显示确定哪个文档是下一个匹配项所花费的时间，该过程因查询的性质而异。Next_doc 是 advance() 的一种特殊形式，对于 Lucene 中的许多查询来说更方便。它相当于 advance(docId() +1) 'advance'

|

"advance"是next_doc的"较低级别"版本：它的作用与查找下一个匹配文档的目的相同，但需要调用查询来执行额外的任务，例如识别和移动跳过等。但是，并非所有查询都可以使用next_doc，因此这些查询也会计时"高级"。   连词(例如布尔值中的"必须"子句)是"提前""匹配"的典型使用者

|

某些查询(如短语查询)使用"两阶段"过程匹配文档。首先，文档是"大致"匹配的，如果它大约匹配，则使用更严格(和昂贵)的过程进行第二次检查。第二阶段验证是"匹配"统计衡量的内容。   例如，短语查询首先通过确保短语中的所有术语都存在于文档中来大致检查文档。如果所有术语都存在，则执行第二阶段验证以确保术语符合形成短语的顺序，这比仅检查术语是否存在相对昂贵。   由于此两阶段过程仅由少数查询使用，因此"匹配"统计信息通常为零"分数"

|

这记录了通过记分器"*_count"对特定文档进行评分所需的时间

|

记录特定方法的调用次数。例如，'"next_doc_count"： 2，' 表示在两个不同的文档上调用了 'nextDoc()' 方法。这可用于通过比较不同查询组件之间的计数来帮助判断查询的选择性。   #### '收藏家'部分编辑

响应的"收集器"部分显示高级执行详细信息。Lucene 通过定义一个"收集器"来工作，该收集器负责协调匹配文档的遍历、评分和收集。收集器也是单个查询如何记录聚合结果、执行无作用域的"全局"查询、执行查询后筛选器等。

看前面的例子：

    
    
    "collector": [
      {
        "name": "SimpleTopScoreDocCollector",
        "reason": "search_top_hits",
        "time_in_nanos": 775274
      }
    ]

我们看到一个名为"SimpleTopScoreDocCollector"的单个收集器被包装成"CancellableCollector"。'SimpleTopScoreDocCollector' 是 Elasticsearch 使用的默认"评分和排序""Collector"。"原因"字段尝试给出类名的简单英文描述。"time_in_nanos"类似于查询树中的时间：包含所有子项的挂钟时间。同样，"子"列出了所有子收集器。Elasticsearch使用包装"SimpleTopScoreDocCollector"的"CancellableCollector"来检测当前搜索是否已取消，并在搜索发生时立即停止收集文档。

应该注意的是，收集器时间与查询时间无关。它们是独立计算、组合和归一化的！由于 Lucene 执行的性质，不可能将收集器中的时间"合并"到查询部分，因此它们显示在单独的部分中。

作为参考，各种收集器的原因有：

`search_sorted`

|

对文档进行评分和排序的收集器。这是最常见的收集器，将在大多数简单的搜索中看到 ---|--- 'search_count'

|

仅计算与查询匹配的文档数，但不提取源的收集器。当将"size： 0"指定为"search_terminate_after_count"时，会出现这种情况

|

在找到"n"个匹配文档后终止搜索执行的收集器。当将"terminate_after_count"查询参数指定为"search_min_score"时，会出现这种情况

|

仅返回分数大于"n"的匹配文档的收集器。当指定顶级参数"min_score"时，会出现这种情况。   "search_multi"

|

包装其他几个收集器的收集器。当搜索、聚合、全局 aggs 和post_filters的组合组合到单个搜索中时，会出现这种情况。   "search_timeout"

|

在指定时间段后停止执行的收集器。当指定了"超时"顶级参数时，可以看到这种情况。   "聚合"

|

Elasticsearch 用来针对查询范围运行聚合的收集器。单个"聚合"收集器用于收集**所有**聚合的文档，因此您将在名称中看到聚合列表。   "global_aggregation"

|

针对全局查询范围(而不是指定查询)执行聚合的收集器。由于全局范围必然与执行的查询不同，因此它必须执行自己的match_all查询(您将看到该查询已添加到"查询"部分)以收集整个数据集 #### '重写'部分编辑

Lucene 中的所有查询都会经历一个"重写"过程。查询(及其子查询)可以重写一次或多次，并且该过程将继续，直到查询停止更改。此过程允许 Lucene 执行优化，例如删除冗余子句、替换一个查询以获得更高效的执行路径等。例如，布尔值 -> 布尔值 -> TermQuery 可以重写为 TermQuery，因为在这种情况下所有布尔值都是不必要的。

重写过程很复杂且难以显示，因为查询可能会发生巨大变化。总重写时间不显示中间结果，而是简单地显示为一个值(以纳秒为单位)。此值是累积值，包含重写所有查询的总时间。

#### 更复杂的示例

为了演示稍微复杂的查询和相关结果，我们可以分析以下查询：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        profile: true,
        query: {
          term: {
            "user.id": {
              value: 'elkbee'
            }
          }
        },
        aggregations: {
          my_scoped_agg: {
            terms: {
              field: 'http.response.status_code'
            }
          },
          my_global_agg: {
            global: {},
            aggregations: {
              my_level_agg: {
                terms: {
                  field: 'http.response.status_code'
                }
              }
            }
          }
        },
        post_filter: {
          match: {
            message: 'search'
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search
    {
      "profile": true,
      "query": {
        "term": {
          "user.id": {
            "value": "elkbee"
          }
        }
      },
      "aggs": {
        "my_scoped_agg": {
          "terms": {
            "field": "http.response.status_code"
          }
        },
        "my_global_agg": {
          "global": {},
          "aggs": {
            "my_level_agg": {
              "terms": {
                "field": "http.response.status_code"
              }
            }
          }
        }
      },
      "post_filter": {
        "match": {
          "message": "search"
        }
      }
    }

此示例具有：

* 查询 * 作用域聚合 * 全局聚合 * post_filter

API 返回以下结果：

    
    
    {
      ...
      "profile": {
        "shards": [
          {
            "id": "[P6-vulHtQRWuD4YnubWb7A][my-index-000001][0]",
            "searches": [
              {
                "query": [
                  {
                    "type": "TermQuery",
                    "description": "message:search",
                    "time_in_nanos": 141618,
                    "breakdown": {
                      "set_min_competitive_score_count": 0,
                      "match_count": 0,
                      "shallow_advance_count": 0,
                      "set_min_competitive_score": 0,
                      "next_doc": 0,
                      "match": 0,
                      "next_doc_count": 0,
                      "score_count": 0,
                      "compute_max_score_count": 0,
                      "compute_max_score": 0,
                      "advance": 3942,
                      "advance_count": 4,
                      "count_weight_count": 0,
                      "score": 0,
                      "build_scorer_count": 2,
                      "create_weight": 38380,
                      "shallow_advance": 0,
                      "count_weight": 0,
                      "create_weight_count": 1,
                      "build_scorer": 99296
                    }
                  },
                  {
                    "type": "TermQuery",
                    "description": "user.id:elkbee",
                    "time_in_nanos": 163081,
                    "breakdown": {
                      "set_min_competitive_score_count": 0,
                      "match_count": 0,
                      "shallow_advance_count": 0,
                      "set_min_competitive_score": 0,
                      "next_doc": 2447,
                      "match": 0,
                      "next_doc_count": 4,
                      "score_count": 4,
                      "compute_max_score_count": 0,
                      "compute_max_score": 0,
                      "advance": 3552,
                      "advance_count": 1,
                      "score": 5027,
                      "count_weight_count": 0,
                      "build_scorer_count": 2,
                      "create_weight": 107840,
                      "shallow_advance": 0,
                      "count_weight": 0,
                      "create_weight_count": 1,
                      "build_scorer": 44215
                    }
                  }
                ],
                "rewrite_time": 4769,
                "collector": [
                  {
                    "name": "MultiCollector",
                    "reason": "search_multi",
                    "time_in_nanos": 1945072,
                    "children": [
                      {
                        "name": "FilteredCollector",
                        "reason": "search_post_filter",
                        "time_in_nanos": 500850,
                        "children": [
                          {
                            "name": "SimpleTopScoreDocCollector",
                            "reason": "search_top_hits",
                            "time_in_nanos": 22577
                          }
                        ]
                      },
                      {
                        "name": "BucketCollectorWrapper: [BucketCollectorWrapper[bucketCollector=[my_scoped_agg, my_global_agg]]]",
                        "reason": "aggregation",
                        "time_in_nanos": 867617
                      }
                    ]
                  }
                ]
              }
            ],
            "aggregations": [...], __"fetch": {...}
          }
        ]
      }
    }

__

|

省略了"聚合"部分，因为下一节将介绍该部分。   ---|--- 如您所见，输出比以前更详细。查询的所有主要部分都表示为：

1. 第一个"术语查询"(user.id：elkbee)表示主要的"术语"查询。  2. 第二个"术语查询"(消息：搜索)表示"post_filter"查询。

收集器树相当简单，显示了单个CancellableCollector如何包装MultiCollector，该多重收集器还包装aFilteredCollector以执行post_filter(并反过来包装正常评分SimpleCollector)，一个BucketCollector来运行所有作用域聚合。

#### 了解多术语查询输出

需要特别注意查询的"多术语查询"类。这包括通配符、正则表达式和模糊查询。这些查询发出非常详细的响应，并且结构不大。

实质上，这些查询会基于每个段重写自己。如果您想象通配符查询"b*"，它在技术上可以匹配任何以字母"b"开头的标记。不可能枚举所有可能的组合，因此 Lucene 在正在评估的段的上下文中重写查询，例如，一个段可能包含标记 '[bar， baz]'，因此查询重写为 "bar" 和 "baz" 的 BooleanQuery 组合。另一个段可能只有标记"[bakery]"，因此查询重写为单个 TermQueryfor "bakery"。

由于这种动态的、每段的重写，干净的树结构变得扭曲，不再遵循一个干净的"谱系"，显示一个查询如何重写到下一个查询。目前，我们所能做的就是道歉，并建议您折叠该查询子项的详细信息，如果它太混乱。幸运的是，所有的计时统计信息都是正确的，只是不是响应中的物理布局，因此，如果您发现细节太难解释，则只需分析顶级 MultiTermQuery 并忽略其子项就足够了。

希望这将在未来的迭代中得到解决，但这是一个棘手的问题，仍在进行中。:)

#### 性能分析聚合

##### '聚合'部分

"聚合"部分包含由特定分片执行的聚合树的详细时间。此聚合树的整体结构将类似于您的原始 Elasticsearch 请求。让我们再次执行上一个查询，并查看这次的聚合配置文件：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        profile: true,
        query: {
          term: {
            "user.id": {
              value: 'elkbee'
            }
          }
        },
        aggregations: {
          my_scoped_agg: {
            terms: {
              field: 'http.response.status_code'
            }
          },
          my_global_agg: {
            global: {},
            aggregations: {
              my_level_agg: {
                terms: {
                  field: 'http.response.status_code'
                }
              }
            }
          }
        },
        post_filter: {
          match: {
            message: 'search'
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search
    {
      "profile": true,
      "query": {
        "term": {
          "user.id": {
            "value": "elkbee"
          }
        }
      },
      "aggs": {
        "my_scoped_agg": {
          "terms": {
            "field": "http.response.status_code"
          }
        },
        "my_global_agg": {
          "global": {},
          "aggs": {
            "my_level_agg": {
              "terms": {
                "field": "http.response.status_code"
              }
            }
          }
        }
      },
      "post_filter": {
        "match": {
          "message": "search"
        }
      }
    }

这将生成以下聚合配置文件输出：

    
    
    {
      "profile": {
        "shards": [
          {
            "aggregations": [
              {
                "type": "NumericTermsAggregator",
                "description": "my_scoped_agg",
                "time_in_nanos": 79294,
                "breakdown": {
                  "reduce": 0,
                  "build_aggregation": 30885,
                  "build_aggregation_count": 1,
                  "initialize": 2623,
                  "initialize_count": 1,
                  "reduce_count": 0,
                  "collect": 45786,
                  "collect_count": 4,
                  "build_leaf_collector": 18211,
                  "build_leaf_collector_count": 1,
                  "post_collection": 929,
                  "post_collection_count": 1
                },
                "debug": {
                  "total_buckets": 1,
                  "result_strategy": "long_terms",
                  "built_buckets": 1
                }
              },
              {
                "type": "GlobalAggregator",
                "description": "my_global_agg",
                "time_in_nanos": 104325,
                "breakdown": {
                  "reduce": 0,
                  "build_aggregation": 22470,
                  "build_aggregation_count": 1,
                  "initialize": 12454,
                  "initialize_count": 1,
                  "reduce_count": 0,
                  "collect": 69401,
                  "collect_count": 4,
                  "build_leaf_collector": 8150,
                  "build_leaf_collector_count": 1,
                  "post_collection": 1584,
                  "post_collection_count": 1
                },
                "debug": {
                  "built_buckets": 1
                },
                "children": [
                  {
                    "type": "NumericTermsAggregator",
                    "description": "my_level_agg",
                    "time_in_nanos": 76876,
                    "breakdown": {
                      "reduce": 0,
                      "build_aggregation": 13824,
                      "build_aggregation_count": 1,
                      "initialize": 1441,
                      "initialize_count": 1,
                      "reduce_count": 0,
                      "collect": 61611,
                      "collect_count": 4,
                      "build_leaf_collector": 5564,
                      "build_leaf_collector_count": 1,
                      "post_collection": 471,
                      "post_collection_count": 1
                    },
                    "debug": {
                      "total_buckets": 1,
                      "result_strategy": "long_terms",
                      "built_buckets": 1
                    }
                  }
                ]
              }
            ]
          }
        ]
      }
    }

从配置文件结构中，我们可以看到"my_scoped_agg"在内部作为"NumericTermsAggregator"运行(因为它聚合的字段"http.response.status_code"是一个数值字段)。在同一层面上，我们看到来自"my_global_agg"的"GlobalAggregator"。然后，该聚合具有一个子项"NumericTermsAggregator"，该子项来自第二个术语对"http.response.status_code"的聚合。

"time_in_nanos"字段显示每个聚合执行的时间，并包含所有子项。虽然总时间很有用，但"细分"字段将提供有关时间花费方式的详细统计数据。

某些聚合可能会返回专家"调试"信息，这些信息描述了聚合底层执行的功能，这些信息"对那些对聚合有用的人很有用，但我们不希望在其他方面有用。它们在版本、聚合和聚合执行策略之间可能会有很大差异。

#### 时序细分

"细分"组件列出了有关低级执行的详细统计信息：

    
    
    "breakdown": {
      "reduce": 0,
      "build_aggregation": 30885,
      "build_aggregation_count": 1,
      "initialize": 2623,
      "initialize_count": 1,
      "reduce_count": 0,
      "collect": 45786,
      "collect_count": 4,
      "build_leaf_collector": 18211,
      "build_leaf_collector_count": 1
    }

"细分"组件中的每个属性对应于聚合的内部方法。例如，"build_leaf_collector"属性测量运行聚合的"getLeafCollector()"方法所花费的纳秒数。以"_count"结尾的属性记录特定方法的调用次数。例如，"collect_count"：2"表示在两个不同文档上称为"collect()"的聚合。"reduce"属性保留供将来使用，并始终返回"0"。

计时以挂钟纳秒为单位列出，根本没有规范化。关于整体"时间"的所有警告都适用于此处。分解的目的是让你感受一下 A) Elasticsearch 中的哪些机器实际上是在消耗时间，以及 B) 各个组件之间的时间差异大小。与总时间一样，细分包括所有儿童时间。

#### 剖析获取

所有获取文档的分片都将在配置文件中有一个"获取"部分。让我们执行一个小搜索并查看抓取配置文件：

    
    
    response = client.search(
      index: 'my-index-000001',
      filter_path: 'profile.shards.fetch',
      body: {
        profile: true,
        query: {
          term: {
            "user.id": {
              value: 'elkbee'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search?filter_path=profile.shards.fetch
    {
      "profile": true,
      "query": {
        "term": {
          "user.id": {
            "value": "elkbee"
          }
        }
      }
    }

这是抓取配置文件：

    
    
    {
      "profile": {
        "shards": [
          {
            "fetch": {
              "type": "fetch",
              "description": "",
              "time_in_nanos": 660555,
              "breakdown": {
                "next_reader": 7292,
                "next_reader_count": 1,
                "load_stored_fields": 299325,
                "load_stored_fields_count": 5,
                "load_source": 3863,
                "load_source_count": 5
              },
              "debug": {
                "stored_fields": ["_id", "_routing", "_source"]
              },
              "children": [
                {
                  "type": "FetchSourcePhase",
                  "description": "",
                  "time_in_nanos": 20443,
                  "breakdown": {
                    "next_reader": 745,
                    "next_reader_count": 1,
                    "process": 19698,
                    "process_count": 5
                  },
                  "debug": {
                    "fast_path": 4
                  }
                },
                {
                  "type": "StoredFieldsPhase",
                  "description": "",
                  "time_in_nanos": 5310,
                  "breakdown": {
                    "next_reader": 745,
                    "next_reader_count": 1,
                    "process": 4445,
                    "process_count": 5
                  }
                }
              ]
            }
          }
        ]
      }
    }

由于这是有关 Elasticsearch 执行获取方式的调试信息，因此它可以从一个请求到另一个请求以及从一个版本到另一个版本。偶数补丁版本可能会更改此处的输出。缺乏一致性使其对调试很有用。

无论如何！"time_in_nanos"表示抓取阶段的总时间。"细分"计算和乘以我们在"next_reader"中每个段的准备工作和在"load_stored_fields"中加载存储字段所花费的时间。调试包含杂项非计时信息，特别是"stored_fields"列出了获取必须加载的存储字段。如果它是一个空列表，那么 fetch 将完全跳过加载存储的字段。

"子"部分列出了执行实际提取工作的子阶段，"细分"包含"next_reader"中每个段准备的计数和时间以及"进程中每个文档获取"的计数和时间。

我们努力加载获取前端所需的所有存储字段。这往往会使"_source"阶段持续几微秒。在这种情况下，"_source"阶段的真实成本隐藏在细分的"load_stored_fields"部分。可以通过设置"_source"：false，"stored_fields"：["_none_"]"来完全跳过加载存储的字段。

#### 分析DFS

DFS 阶段在查询阶段之前运行，以收集与查询相关的全局信息。它目前用于两种情况：

1. 当"search_type"设置为"dfs_query_then_fetch"且索引有多个分片时。  2. 当搜索请求包含 knn 部分时。

这两种情况都可以通过在搜索请求中将"profile"设置为"true"来进行分析。

##### Profiling DFSStatistics

当"search_type"设置为"dfs_query_then_fetch"并且索引具有多个分片时，dfs 阶段将收集术语统计信息以提高搜索结果的相关性。

以下是在使用"dfs_query_then_fetch"的搜索中将"配置文件"设置为"true"的示例：

让我们首先设置一个具有多个分片的索引，并在"关键字"字段上索引一对具有不同值的文档。

    
    
    response = client.indices.create(
      index: 'my-dfs-index',
      body: {
        settings: {
          number_of_shards: 2,
          number_of_replicas: 1
        },
        mappings: {
          properties: {
            "my-keyword": {
              type: 'keyword'
            }
          }
        }
      }
    )
    puts response
    
    response = client.bulk(
      index: 'my-dfs-index',
      refresh: true,
      body: [
        {
          index: {
            _id: '1'
          }
        },
        {
          "my-keyword": 'a'
        },
        {
          index: {
            _id: '2'
          }
        },
        {
          "my-keyword": 'b'
        }
      ]
    )
    puts response
    
    
    PUT my-dfs-index
    {
      "settings": {
        "number_of_shards": 2, __"number_of_replicas": 1
      },
      "mappings": {
          "properties": {
            "my-keyword": { "type": "keyword" }
          }
        }
    }
    
    POST my-dfs-index/_bulk?refresh=true
    { "index" : { "_id" : "1" } }
    { "my-keyword" : "a" }
    { "index" : { "_id" : "2" } }
    { "my-keyword" : "b" }

__

|

"my-dfs-index"是用多个分片创建的。   ---|--- 通过索引设置，我们现在可以分析搜索查询的 dfs 阶段。对于此示例，我们使用术语查询。

    
    
    response = client.search(
      index: 'my-dfs-index',
      search_type: 'dfs_query_then_fetch',
      pretty: true,
      size: 0,
      body: {
        profile: true,
        query: {
          term: {
            "my-keyword": {
              value: 'a'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my-dfs-index/_search?search_type=dfs_query_then_fetch&pretty&size=0 __{
      "profile": true, __"query": {
        "term": {
          "my-keyword": {
            "value": "a"
          }
        }
      }
    }

__

|

"search_type"url 参数设置为"dfs_query_then_fetch"以确保运行 dfs 阶段。   ---|---    __

|

"配置文件"参数设置为"true"。   在响应中，我们看到一个配置文件，其中包括每个分片的"dfs"部分以及其余搜索阶段的配置文件输出。分片的"dfs"部分之一如下所示：

    
    
    "dfs" : {
        "statistics" : {
            "type" : "statistics",
            "description" : "collect term statistics",
            "time_in_nanos" : 236955,
            "breakdown" : {
                "term_statistics" : 4815,
                "collection_statistics" : 27081,
                "collection_statistics_count" : 1,
                "create_weight" : 153278,
                "term_statistics_count" : 1,
                "rewrite_count" : 0,
                "create_weight_count" : 1,
                "rewrite" : 0
            }
        }
    }

在此响应的"dfs.statistics"部分中，我们看到一个"time_in_nanos"，这是收集此分片的术语统计信息以及各个部分的进一步细分所花费的总时间。

##### Profiling kNNSearch

k 最近邻 (kNN) 搜索在 dfs 阶段运行。

以下是在具有"knn"部分的搜索中将"配置文件"设置为"true"的示例：

让我们首先设置一个包含多个密集向量的索引。

    
    
    response = client.indices.create(
      index: 'my-knn-index',
      body: {
        mappings: {
          properties: {
            "my-vector": {
              type: 'dense_vector',
              dims: 3,
              index: true,
              similarity: 'l2_norm'
            }
          }
        }
      }
    )
    puts response
    
    response = client.bulk(
      index: 'my-knn-index',
      refresh: true,
      body: [
        {
          index: {
            _id: '1'
          }
        },
        {
          "my-vector": [
            1,
            5,
            -20
          ]
        },
        {
          index: {
            _id: '2'
          }
        },
        {
          "my-vector": [
            42,
            8,
            -15
          ]
        },
        {
          index: {
            _id: '3'
          }
        },
        {
          "my-vector": [
            15,
            11,
            23
          ]
        }
      ]
    )
    puts response
    
    
    PUT my-knn-index
    {
      "mappings": {
        "properties": {
          "my-vector": {
            "type": "dense_vector",
            "dims": 3,
            "index": true,
            "similarity": "l2_norm"
          }
        }
      }
    }
    
    POST my-knn-index/_bulk?refresh=true
    { "index": { "_id": "1" } }
    { "my-vector": [1, 5, -20] }
    { "index": { "_id": "2" } }
    { "my-vector": [42, 8, -15] }
    { "index": { "_id": "3" } }
    { "my-vector": [15, 11, 23] }

通过索引设置，我们现在可以分析 kNN 搜索查询。

    
    
    response = client.search(
      index: 'my-knn-index',
      body: {
        profile: true,
        knn: {
          field: 'my-vector',
          query_vector: [
            -5,
            9,
            -12
          ],
          k: 3,
          num_candidates: 100
        }
      }
    )
    puts response
    
    
    POST my-knn-index/_search
    {
      "profile": true, __"knn": {
        "field": "my-vector",
        "query_vector": [-5, 9, -12],
        "k": 3,
        "num_candidates": 100
      }
    }

__

|

"配置文件"参数设置为"true"。   ---|--- 在响应中，我们看到一个配置文件，其中包括一个"knn"部分作为每个分片的"dfs"部分的一部分，以及其余搜索阶段的配置文件输出。

分片的"dfs.knn"部分之一如下所示：

    
    
    "dfs" : {
        "knn" : [
            {
            "query" : [
                {
                    "type" : "DocAndScoreQuery",
                    "description" : "DocAndScore[100]",
                    "time_in_nanos" : 444414,
                    "breakdown" : {
                      "set_min_competitive_score_count" : 0,
                      "match_count" : 0,
                      "shallow_advance_count" : 0,
                      "set_min_competitive_score" : 0,
                      "next_doc" : 1688,
                      "match" : 0,
                      "next_doc_count" : 3,
                      "score_count" : 3,
                      "compute_max_score_count" : 0,
                      "compute_max_score" : 0,
                      "advance" : 4153,
                      "advance_count" : 1,
                      "score" : 2099,
                      "build_scorer_count" : 2,
                      "create_weight" : 128879,
                      "shallow_advance" : 0,
                      "create_weight_count" : 1,
                      "build_scorer" : 307595,
                      "count_weight": 0,
                      "count_weight_count": 0
                    }
                }
            ],
            "rewrite_time" : 1275732,
            "collector" : [
                {
                    "name" : "SimpleTopScoreDocCollector",
                    "reason" : "search_top_hits",
                    "time_in_nanos" : 17163
                }
            ]
        }   ]
    }

在响应的"dfs.knn"部分中，我们可以看到查询，重写和收集器的时序的输出。与许多其他查询不同，kNN 搜索在查询重写期间完成大部分工作。这意味着"rewrite_time"代表在kNNsearch上花费的时间。

#### 性能分析注意事项

与任何探查器一样，档案 API 引入了不可忽略的搜索执行开销。检测低级方法调用(如"collect"、"advance"和"next_doc")的行为可能相当昂贵，因为这些方法是在紧密循环中调用的。因此，默认情况下，不应在生产设置中启用分析，并且不应与非分析的查询时间进行比较。性能分析只是一种诊断工具。

在某些情况下，特殊的 Lucene 优化被禁用，因为它们不适合分析。这可能会导致某些查询报告的相对时间大于其非分析的对应项，但与分析查询中的其他组件相比，通常不会产生重大影响。

####Limitations

* 性能分析当前不测量网络开销。  * 性能分析也不考虑在队列中花费的时间、在协调节点上合并分片响应或构建全局序数(用于加快搜索速度的内部数据结构)等其他工作。  * 分析统计信息目前不可用于建议。  * 目前无法分析聚合的减少阶段。  * 探查器正在检测内部结构，这些内部内部结构可能会因版本而异。生成的 json 应该被认为是不稳定的，尤其是"调试"部分中的内容。

[« Explain API](search-explain.md) [Field capabilities API »](search-field-
caps.md)
