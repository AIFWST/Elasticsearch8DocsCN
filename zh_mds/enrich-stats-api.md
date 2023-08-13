

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Enrich APIs](enrich-apis.md)

[« Execute enrich policy API](execute-enrich-policy-api.md) [EQL APIs
»](eql-apis.md)

## 丰富统计信息API

返回扩充协调器统计信息和有关当前正在执行的扩充策略的信息。

    
    
    response = client.enrich.stats
    puts response
    
    
    GET /_enrich/_stats

###Request

"获取/_enrich/_stats"

### 响应正文

`executing_policies`

    

(对象数组)包含有关当前正在执行的每个扩充策略的信息的对象。

返回的参数包括：

`name`

     (String) Name of the enrich policy. 
`task`

     ([Task object](tasks.html "Task management API")) Object containing detailed information about the policy execution task. 

`coordinator_stats`

    

(对象数组)包含有关配置扩充处理器的每个协调最节点的信息的对象。

返回的参数包括：

`node_id`

     (String) ID of the ingest node coordinating search requests for configured enrich processors. 
`queue_size`

     (Integer) Number of search requests in the queue. 
`remote_requests_current`

     (Integer) Current number of outstanding remote requests. 
`remote_requests_total`

    

(整数)自节点启动以来执行的未完成远程请求数。

在大多数情况下，一个远程请求包括多个搜索请求。这取决于执行远程请求时队列中的搜索请求数。

`executed_searches_total`

     (Integer) Number of search requests that enrich processors have executed since node startup. 

`cache_stats`

    

(对象数组)包含有关每个摄取节点的丰富缓存统计信息的对象。

返回的参数包括：

`node_id`

     (String) ID of the ingest node with a enrich cache. 
`count`

     (Integer) Number of cached entries. 
`hits`

     (Integer) The number of enrich lookups served from cache. 
`missed`

     (Integer) The number of time enrich lookups couldn't be served from cache. 
`evictions`

     (Integer) The number cache entries evicted from the cache. 

###Examples

    
    
    response = client.enrich.stats
    puts response
    
    
    GET /_enrich/_stats

API 返回以下响应：

    
    
    {
      "executing_policies": [
        {
          "name": "my-policy",
          "task": {
            "id": 124,
            "type": "direct",
            "action": "cluster:admin/xpack/enrich/execute",
            "start_time_in_millis": 1458585884904,
            "running_time_in_nanos": 47402,
            "cancellable": false,
            "parent_task_id": "oTUltX4IQMOUUVeiohTt8A:123",
            "headers": {
              "X-Opaque-Id": "123456"
            }
          }
        }
      ],
      "coordinator_stats": [
        {
          "node_id": "1sFM8cmSROZYhPxVsiWew",
          "queue_size": 0,
          "remote_requests_current": 0,
          "remote_requests_total": 0,
          "executed_searches_total": 0
        }
      ],
      "cache_stats": [
        {
          "node_id": "1sFM8cmSROZYhPxVsiWew",
          "count": 0,
          "hits": 0,
          "misses": 0,
          "evictions": 0
        }
      ]
    }

[« Execute enrich policy API](execute-enrich-policy-api.md) [EQL APIs
»](eql-apis.md)
