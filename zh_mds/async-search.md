

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search APIs](search.md)

[« Search API](search-search.md) [Point in time API »](point-in-time-
api.md)

## 异步搜索

异步搜索 API 允许异步执行搜索请求、监视其进度，并在部分结果可用时检索部分结果。

### 提交异步搜索API

异步执行搜索请求。它接受与搜索 API 相同的参数和请求正文。

    
    
    response = client.async_search.submit(
      index: 'sales*',
      size: 0,
      body: {
        sort: [
          {
            date: {
              order: 'asc'
            }
          }
        ],
        aggregations: {
          sale_date: {
            date_histogram: {
              field: 'date',
              calendar_interval: '1d'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales*/_async_search?size=0
    {
      "sort": [
        { "date": { "order": "asc" } }
      ],
      "aggs": {
        "sale_date": {
          "date_histogram": {
            "field": "date",
            "calendar_interval": "1d"
          }
        }
      }
    }

响应包含正在执行的搜索的标识符。以后可以使用此 ID 检索搜索的最终结果。当前可用的搜索结果作为"响应"对象的一部分返回。

    
    
    {
      "id" : "FmRldE8zREVEUzA2ZVpUeGs2ejJFUFEaMkZ5QTVrSTZSaVN3WlNFVmtlWHJsdzoxMDc=", __"is_partial" : true, __"is_running" : true, __"start_time_in_millis" : 1583945890986,
      "expiration_time_in_millis" : 1584377890986,
      "response" : {
        "took" : 1122,
        "timed_out" : false,
        "num_reduce_phases" : 0,
        "_shards" : {
          "total" : 562, __"successful" : 3, __"skipped" : 0,
          "failed" : 0
        },
        "hits" : {
          "total" : {
            "value" : 157483, __"relation" : "gte"
          },
          "max_score" : null,
          "hits" : [ ]
        }
      }
    }

__

|

异步搜索的标识符，可用于监视其进度、检索其结果和/或删除它 ---|--- __

|

当查询不再运行时，指示搜索是失败还是在所有分片上成功完成。执行查询时，"is_partial"始终设置为"true" __

|

搜索是否仍在执行或已完成 __

|

搜索将在多少个分片上执行，总体__

|

有多少个分片成功完成了搜索 __

|

当前有多少文档与查询匹配，这些文档属于已完成搜索的分片 尽管查询不再运行，因此"is_running"设置为"false"，但结果可能是部分的。如果在某些分片返回其结果后搜索失败，或者当协调异步搜索的节点死亡时，就会发生这种情况。

可以通过提供"wait_for_completion_timeout"参数(默认为"1"秒)来阻止并等待搜索完成到某个超时。当异步搜索在此类超时内完成时，响应将不包含 ID，因为结果不会存储在群集中。默认为"false"的"keep_on_completion"参数可以设置为"true"，以请求存储结果以供以后检索，当搜索在"wait_for_completion_timeout"中完成时也是如此。

您还可以通过"keep_alive"参数指定异步搜索需要多长时间，该参数默认为"5d"(五天)。正在进行的异步搜索和任何保存的搜索结果将在此时间段后删除。

当结果的主要排序是索引字段时，分片将根据它们为该字段持有的最小值和最大值进行排序，因此部分结果按照请求的排序条件变得可用。

提交异步搜索 API 支持与搜索 API 相同的参数，但有些参数具有不同的默认值：

* "batched_reduce_size"默认为"5"：这会影响部分结果可用的频率，每当分片结果减少时就会发生这种情况。每次协调节点收到一定数量的新分片响应(默认为"5")时，都会执行部分缩减。  * 'request_cache' 默认为 'true' * 'pre_filter_shard_size' 默认为 '1' 并且无法更改：这是为了强制执行预过滤器往返以从每个分片中检索统计信息，以便跳过那些肯定不保存任何与查询匹配的文档的分片。  * "ccs_minimize_roundtrips"默认为"假"。执行跨集群搜索时，将其设置为"true"可能会改善整体搜索延迟，尤其是在搜索具有大量分片的集群时。但是，当设置为"true"时，在所有集群上完成搜索之前，不会收到远程群集上的搜索进度。有关详细信息，请参阅跨clusters__Search。

异步搜索不支持仅包含建议部分的滚动或搜索请求。

默认情况下，Elasticsearch 不允许存储大于 10Mb 的异步搜索响应，尝试这样做会导致错误。可以通过更改"search.max_async_search_response_size"群集级别设置来设置存储的异步搜索响应的最大允许大小。

### 获取异步搜索

获取异步搜索 API 在给定其 ID 的情况下检索以前提交的异步搜索请求的结果。如果启用了 Elasticsearch 安全功能，则对特定异步搜索结果的访问仅限于提交该搜索的用户或 API 密钥。

    
    
    response = client.async_search.get(
      id: 'FmRldE8zREVEUzA2ZVpUeGs2ejJFUFEaMkZ5QTVrSTZSaVN3WlNFVmtlWHJsdzoxMDc='
    )
    puts response
    
    
    GET /_async_search/FmRldE8zREVEUzA2ZVpUeGs2ejJFUFEaMkZ5QTVrSTZSaVN3WlNFVmtlWHJsdzoxMDc=
    
    
    {
      "id" : "FmRldE8zREVEUzA2ZVpUeGs2ejJFUFEaMkZ5QTVrSTZSaVN3WlNFVmtlWHJsdzoxMDc=",
      "is_partial" : true, __"is_running" : true, __"start_time_in_millis" : 1583945890986,
      "expiration_time_in_millis" : 1584377890986, __"response" : {
        "took" : 12144,
        "timed_out" : false,
        "num_reduce_phases" : 46, __"_shards" : {
          "total" : 562,
          "successful" : 188, __"skipped" : 0,
          "failed" : 0
        },
        "hits" : {
          "total" : {
            "value" : 456433,
            "relation" : "eq"
          },
          "max_score" : null,
          "hits" : [ ]
        },
        "aggregations" : { __"sale_date" :  {
            "buckets" : []
          }
        }
      }
    }

__

|

当查询不再运行时，指示搜索是失败还是在所有分片上成功完成。执行查询时，"is_partial"始终设置为"true"---|---__

|

搜索是否仍在执行或已完成 __

|

异步搜索何时过期 __

|

指示已执行的结果缩减次数。如果此数字与上次检索到的结果相比增加，则搜索响应中可能包含其他结果 __

|

指示已执行查询的分片数。请注意，为了将 forshard 结果包含在搜索响应中，需要先减少它们。   __

|

部分聚合结果来自已完成查询执行的分片。   调用获取异步搜索 API 时，还可以提供"wait_for_completion_timeout"参数，以便等待搜索完成，直到提供的超时。如果在超时到期之前可用，将返回最终结果，否则将在超时到期后返回当前可用结果。默认情况下，不设置超时，这意味着将返回当前可用的结果，而无需任何额外的等待。

"keep_alive"参数指定异步搜索在群集中应可用的时间。如果未指定，将使用具有相应提交异步请求的"keep_alive"集。否则，可以覆盖该值并延长请求的有效性。当此期限到期时，搜索(如果仍在运行)将被取消。如果搜索完成，则删除其保存的结果。

### 获取异步搜索状态

获取异步搜索状态 API 在不检索搜索结果的情况下，仅显示以前提交的异步搜索请求的状态，给定其"id"。如果启用了 Elasticsearch 安全功能，则对获取异步搜索状态 API 的访问仅限于monitoring_user角色。

    
    
    response = client.async_search.status(
      id: 'FmRldE8zREVEUzA2ZVpUeGs2ejJFUFEaMkZ5QTVrSTZSaVN3WlNFVmtlWHJsdzoxMDc='
    )
    puts response
    
    
    GET /_async_search/status/FmRldE8zREVEUzA2ZVpUeGs2ejJFUFEaMkZ5QTVrSTZSaVN3WlNFVmtlWHJsdzoxMDc=
    
    
    {
      "id" : "FmRldE8zREVEUzA2ZVpUeGs2ejJFUFEaMkZ5QTVrSTZSaVN3WlNFVmtlWHJsdzoxMDc=",
      "is_running" : true,
      "is_partial" : true,
      "start_time_in_millis" : 1583945890986,
      "expiration_time_in_millis" : 1584377890986,
      "_shards" : {
          "total" : 562,
          "successful" : 188, __"skipped" : 0,
          "failed" : 0
      }
    }

__

|

指示到目前为止已执行查询的分片数。   ---|--- 对于已完成的异步搜索，状态响应具有附加的"completion_status"字段，该字段显示已完成的异步搜索的状态代码。

    
    
    {
      "id" : "FmRldE8zREVEUzA2ZVpUeGs2ejJFUFEaMkZ5QTVrSTZSaVN3WlNFVmtlWHJsdzoxMDc=",
      "is_running" : false,
      "is_partial" : false,
      "start_time_in_millis" : 1583945890986,
      "expiration_time_in_millis" : 1584377890986,
      "_shards" : {
          "total" : 562,
          "successful" : 562,
          "skipped" : 0,
          "failed" : 0
      },
     "completion_status" : 200 __}

__

|

指示异步搜索已成功完成。   ---|--- { "id" ： "FmRldE8zREVEUzA2ZVpUeGs2ejJFUFEaMkZ5QTVrSTZSaVN3WlNFVmtlWHJsdzoxMDc="， "is_running" ： false， "is_partial" ： true， "start_time_in_millis" ： 1583945890986， "expiration_time_in_millis" ： 1584377890986， "_shards" ： { "total" ： 562， "成功" ： 450， "跳过" ： 0， "失败" ： 112 }， "completion_status" ： 503 __}

__

|

指示异步搜索已完成，但出现错误。   ---|--- ### 删除异步搜索编辑

可以使用删除异步搜索 API 按 ID 手动删除异步搜索。如果搜索仍在运行，搜索请求将被取消。否则，将删除保存的搜索结果。

    
    
    response = client.async_search.delete(
      id: 'FmRldE8zREVEUzA2ZVpUeGs2ejJFUFEaMkZ5QTVrSTZSaVN3WlNFVmtlWHJsdzoxMDc='
    )
    puts response
    
    
    DELETE /_async_search/FmRldE8zREVEUzA2ZVpUeGs2ejJFUFEaMkZ5QTVrSTZSaVN3WlNFVmtlWHJsdzoxMDc=

如果启用了 Elasticsearch 安全功能，则特定异步搜索的删除仅限于：

* 提交原始搜索请求的经过身份验证的用户。  * 具有"cancel_task"群集权限的用户。

[« Search API](search-search.md) [Point in time API »](point-in-time-
api.md)
