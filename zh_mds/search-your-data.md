

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)

[« Aliases](aliases.md) [Collapse search results »](collapse-search-
results.md)

# 搜索您的数据

_search query_，或_query_，是关于Elasticsearch数据流或索引中数据信息的请求。

您可以将查询视为一个问题，以 Elasticsearch 理解的方式编写。根据您的数据，您可以使用查询来获取以下问题的答案：

* 我的服务器上哪些进程的响应时间超过 500 毫秒？  * 我的网络上的哪些用户在上周内运行了"regsvr32.exe"？  * 我的网站上哪些页面包含特定的单词或短语？

_search_ 由一个或多个查询组成，这些查询被组合并发送到 Elasticsearch。与搜索查询匹配的文档以响应的the_hits_或_search results_返回。

搜索还可能包含用于更好地处理其查询的其他信息。例如，搜索可能仅限于特定索引或仅返回特定数量的结果。

### 运行搜索

您可以使用搜索 API 搜索和聚合存储在 Elasticsearch 数据流或索引中的数据。API 的"查询"请求正文参数接受在查询 DSL 中编写的查询。

以下请求使用"匹配"查询搜索"my-index-000001"。此查询匹配"user.id"值为"kimchy"的文档。

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search
    {
      "query": {
        "match": {
          "user.id": "kimchy"
        }
      }
    }

API 响应返回与 'hits.hits' 属性中的查询匹配的前 10 个文档。

    
    
    {
      "took": 5,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": {
          "value": 1,
          "relation": "eq"
        },
        "max_score": 1.3862942,
        "hits": [
          {
            "_index": "my-index-000001",
            "_id": "kxWFcnMByiguvud1Z8vC",
            "_score": 1.3862942,
            "_source": {
              "@timestamp": "2099-11-15T14:12:12",
              "http": {
                "request": {
                  "method": "get"
                },
                "response": {
                  "bytes": 1070000,
                  "status_code": 200
                },
                "version": "1.1"
              },
              "message": "GET /search HTTP/1.1 200 1070000",
              "source": {
                "ip": "127.0.0.1"
              },
              "user": {
                "id": "kimchy"
              }
            }
          }
        ]
      }
    }

### 定义仅存在于查询中的字段

您可以定义仅作为搜索查询的一部分存在的运行时字段，而不是为数据编制索引然后对其进行搜索。您可以在搜索请求中指定"runtime_mappings"部分来定义运行时字段，该字段可以选择包含无痛脚本。

例如，以下查询定义了一个名为"day_of_week"的运行时字段。包含的脚本根据"@timestamp"字段的值计算星期几，并使用"emit"返回计算值。

该查询还包括对"day_of_week"进行操作的术语聚合。

    
    
    GET /my-index-000001/_search
    {
      "runtime_mappings": {
        "day_of_week": {
          "type": "keyword",
          "script": {
            "source":
            """emit(doc['@timestamp'].value.dayOfWeekEnum
            .getDisplayName(TextStyle.FULL, Locale.ROOT))"""
          }
        }
      },
      "aggs": {
        "day_of_week": {
          "terms": {
            "field": "day_of_week"
          }
        }
      }
    }

响应包括基于"day_of_week"运行时字段的聚合。在"存储桶"下是一个值为"星期日"的"键"。查询根据"day_of_week"运行时字段中定义的脚本动态计算此值，而无需为字段编制索引。

    
    
    {
      ...
      ***
      "aggregations" : {
        "day_of_week" : {
          "doc_count_error_upper_bound" : 0,
          "sum_other_doc_count" : 0,
          "buckets" : [
            {
              "key" : "Sunday",
              "doc_count" : 5
            }
          ]
        }
      }
    }

### 常用搜索选项

您可以使用以下选项自定义搜索。

**查询 DSL** 查询 DSL 支持多种查询类型，您可以混合和匹配以获取所需的结果。查询类型包括：

* 布尔和其他复合查询，可让您根据多个条件组合查询并匹配结果 * 用于筛选和查找完全匹配项的术语级查询 * 搜索引擎中常用的全文查询 * 地理和空间查询

**聚合** 可以使用搜索聚合来获取搜索结果的统计信息和其他分析。聚合可帮助您回答以下问题：

* 我的服务器的平均响应时间是多少？  * 我的网络上用户攻击最多的 IP 地址是什么？  * 客户的总交易收入是多少？

**搜索多个数据流和索引** 您可以使用逗号分隔值和类似 grep 的索引模式在同一请求中搜索多个数据流和索引。您甚至可以从特定索引提升搜索结果。请参阅_Search多个数据流andindices_。

**分页搜索结果** 默认情况下，搜索仅返回前 10 个匹配命中。要检索更多或更少的文档，请参阅_Paginate搜索results_。

**检索所选字段** 搜索响应的"hits.hits"属性包括每个匹配的完整文档"_source"。要仅检索"_source"或其他字段的子集，请参阅_Retrieveselected fields_。

**对搜索结果进行排序** 默认情况下，搜索命中按"_score"排序，""是衡量每个文档与查询匹配程度的相关性分数。要自定义这些分数的计算，请使用"script_score"查询。要按其他字段值对搜索命中进行排序，请参阅_Sortsearch results_。

**运行异步搜索** Elasticsearch 搜索旨在快速运行大量数据，通常在几毫秒内返回结果。因此，默认情况下搜索are_synchronous_。搜索请求在返回响应之前等待完整的结果。

但是，跨大型数据集或多个群集进行搜索时，完整结果可能需要更长的时间。

为了避免长时间的等待，您可以运行 _async_ 或 _async_ 搜索。异步搜索允许您立即检索长时间运行的搜索的部分结果，并在以后获取完整结果。

### 搜索超时

默认情况下，搜索请求不会超时。请求在返回响应之前等待每个分片的完整结果。

虽然异步搜索是为长时间运行的搜索而设计的，但您也可以使用"timeout"参数来指定您希望等待每个分片完成的持续时间。每个分片收集指定时间段内的命中数。如果收集在时间段结束时未完成，Elasticsearch 仅使用到该点之前累积的点击量。搜索请求的总体延迟取决于搜索所需的分片数和并发分片请求数。

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        timeout: '2s',
        query: {
          match: {
            "user.id": 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search
    {
      "timeout": "2s",
      "query": {
        "match": {
          "user.id": "kimchy"
        }
      }
    }

若要为所有搜索请求设置群集范围的默认超时，请使用群集设置 API 配置"search.default_search_timeout"。如果在请求中未传递"timeout"参数，则使用此全局超时持续时间。如果全局搜索超时在搜索请求完成之前过期，则使用任务取消来取消请求。"search.default_search_timeout"设置默认为"-1"(无超时)。

### 搜索取消

您可以使用任务管理 API 取消搜索请求。Elasticsearch 还会在客户端的 HTTP 连接关闭时自动取消搜索请求。我们建议您将客户端设置为在搜索请求中止或超时时关闭 HTTP 连接。

### 跟踪总点击数

通常，如果不访问所有匹配项，就无法准确计算总命中计数，这对于匹配大量文档的查询来说代价高昂。"track_total_hits"参数允许您控制如何跟踪总命中数。鉴于通常具有命中次数的下限就足够了，例如"至少有 10000 次命中"，默认值设置为"10，000"。这意味着请求将准确计算总命中数，最高可达"10，000"次命中。如果您在某个阈值后不需要准确的命中数，那么加快搜索速度是一个很好的权衡。

当设置为"true"时，搜索响应将始终跟踪与查询准确匹配的命中数(例如，当"track_total_hits"设置为true时，"total.relation"将始终等于"eq")。否则，搜索响应中的"total.value"对象中返回的"total.relation"决定了应如何解释"total.value"。值""gte"表示"total.value"是与查询匹配的总命中数的下限，值"eq"表示"total.value"是准确计数。

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        track_total_hits: true,
        query: {
          match: {
            "user.id": 'elkbee'
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "track_total_hits": true,
      "query": {
        "match" : {
          "user.id" : "elkbee"
        }
      }
    }

...返回：

    
    
    {
      "_shards": ...
      "timed_out": false,
      "took": 100,
      "hits": {
        "max_score": 1.0,
        "total" : {
          "value": 2048,    __"relation": "eq" __},
        "hits": ...
      }
    }

__

|

与查询匹配的命中总数。   ---|---    __

|

计数是准确的(例如，"eq"表示等于)。   也可以将"track_total_hits"设置为整数。例如，以下查询将准确跟踪与查询匹配的总命中计数(最多 100 个文档)：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        track_total_hits: 100,
        query: {
          match: {
            "user.id": 'elkbee'
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "track_total_hits": 100,
      "query": {
        "match": {
          "user.id": "elkbee"
        }
      }
    }

响应中的"hits.total.relation"将指示在"hits.total.value"中返回的值是准确的("eq")还是总数("gte")的下限。

例如以下响应：

    
    
    {
      "_shards": ...
      "timed_out": false,
      "took": 30,
      "hits": {
        "max_score": 1.0,
        "total": {
          "value": 42,         __"relation": "eq" __},
        "hits": ...
      }
    }

__

|

42 个文档与查询匹配 ---|--- __

|

并且计数是准确的("EQ")...表示"总计"中返回的命中数准确无误。

如果与查询匹配的总命中数大于"track_total_hits"中设置的值，则响应中的总命中数将指示 thereturn 值是下限：

    
    
    {
      "_shards": ...
      "hits": {
        "max_score": 1.0,
        "total": {
          "value": 100,         __"relation": "gte" __},
        "hits": ...
      }
    }

__

|

至少有 100 个文档与查询 ---|--- __ 匹配

|

这是一个下限("gte")。   如果您根本不需要跟踪命中总数，则可以通过将此选项设置为"false"来缩短查询时间：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        track_total_hits: false,
        query: {
          match: {
            "user.id": 'elkbee'
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "track_total_hits": false,
      "query": {
        "match": {
          "user.id": "elkbee"
        }
      }
    }

...返回：

    
    
    {
      "_shards": ...
      "timed_out": false,
      "took": 10,
      "hits": {             __"max_score": 1.0,
        "hits": ...
      }
    }

__

|

总点击数未知。   ---|--- 最后，您可以通过在请求中将"track_total_hits"设置为"true"来强制准确计数。

### 快速检查匹配文档

如果您只想知道是否有任何文档与特定查询匹配，则可以将"size"设置为"0"以表示我们对搜索结果不感兴趣。您还可以将"terminate_after"设置为"1"，以指示只要找到第一个匹配的文档(每个分片)，就可以终止查询执行。

    
    
    response = client.search(
      q: 'user.id:elkbee',
      size: 0,
      terminate_after: 1
    )
    puts response
    
    
    GET /_search?q=user.id:elkbee&size=0&terminate_after=1

"terminate_after"始终在"post_filter"之后应用，并在分片上收集到足够的命中时停止查询以及聚合执行。尽管聚合的文档计数可能不会反映响应中的"hits.total"，因为聚合是在过滤后**之前应用的。

响应将不包含任何命中，因为"大小"设置为"0"。"hits.total"将等于"0"，表示没有匹配的文档，或大于"0"表示在查询提前终止时至少有同样多的文档与查询匹配。此外，如果查询提前终止，则"terminated_early"标志将在响应中设置为"true"。

    
    
    {
      "took": 3,
      "timed_out": false,
      "terminated_early": true,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped" : 0,
        "failed": 0
      },
      "hits": {
        "total" : {
            "value": 1,
            "relation": "eq"
        },
        "max_score": null,
        "hits": []
      }
    }

响应中的"占用"时间包含此请求处理所花费的毫秒数，在节点收到查询后迅速开始，直到完成所有与搜索相关的工作以及上述 JSON 返回到客户端之前。这意味着它包括在线程池中等待所花费的时间，在整个集群中执行分布式搜索并收集所有结果。

[« Aliases](aliases.md) [Collapse search results »](collapse-search-
results.md)
