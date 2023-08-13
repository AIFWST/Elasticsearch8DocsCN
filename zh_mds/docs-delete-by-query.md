

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Document APIs](docs.md)

[« Delete API](docs-delete.md) [Update API »](docs-update.md)

## 通过查询接口删除

删除与指定查询匹配的文档。

    
    
    response = client.delete_by_query(
      index: 'my-index-000001',
      body: {
        query: {
          match: {
            "user.id": 'elkbee'
          }
        }
      }
    )
    puts response
    
    
    POST /my-index-000001/_delete_by_query
    {
      "query": {
        "match": {
          "user.id": "elkbee"
        }
      }
    }

###Request

"发布/<target>/_delete_by_query"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有以下索引权限：

    * `read`
    * `delete` or `write`

###Description

可以使用与搜索 API 相同的语法在请求 URI 或请求正文中指定查询条件。

当您提交按查询删除请求时，Elasticsearch 会在开始处理请求时获取数据流或索引的快照，并使用"内部"版本控制删除匹配的文档。如果文档在拍摄快照和处理删除操作之间发生更改，则会导致版本冲突，并且删除操作将失败。

版本等于 0 的文档无法使用"按查询删除"删除，因为"内部"版本控制不支持将 0 作为有效版本号。

在处理按查询删除请求时，Elasticsearch 会按顺序执行多个搜索请求，以查找要删除的所有匹配文档。对每批匹配文档执行批量删除请求。如果搜索或批量请求被拒绝，则请求最多重试 10 次，并呈指数回退。如果达到最大重试限制，则在响应中返回处理暂停和所有失败的请求。成功完成的任何删除请求仍会保留，不会回滚。

您可以选择计算版本冲突，而不是通过将"冲突"设置为"继续"来停止和返回。请注意，如果您选择计算版本冲突，该操作可能会尝试从源中删除比"max_docs"更多的文档，直到它成功删除了"max_docs"文档，或者它遍历了源查询中的每个文档。

#### 刷新分片

指定"refresh"参数会在请求完成后刷新 deleteby 查询中涉及的所有分片。这与删除 API 的"刷新"参数不同，后者只会导致接收删除请求的分片被刷新。与删除 API 不同，它不支持"wait_for"。

#### 异步运行查询删除

如果请求包含"wait_for_completion=false"，Elasticsearch 会执行一些预检检查，启动请求，并返回一个可用于取消或获取任务状态的"任务"。Elasticsearch 在 '.tasks/task/${taskId}' 创建此任务的记录作为文档。完成任务后，您应该删除任务文档，以便 Elasticsearch 可以回收空间。

#### 等待活动分片

"wait_for_active_shards"控制在继续请求之前，分片必须有多少副本处于活动状态。有关详细信息，请参阅活动分片。"timeout"控制每个写入请求等待不可用分片变为可用的时间。两者都完全按照它们在批量 API 中的工作方式工作。按查询删除使用滚动搜索，因此您还可以指定"scroll"参数来控制它使搜索上下文保持活动状态的时间，例如"？scroll=10m"。默认值为 5 分钟。

#### 限制删除请求

若要控制按查询删除发出批量删除操作的速率，可以将"requests_per_second"设置为任何正十进制数。这会为每个批次填充一个等待时间来限制速率。将"requests_per_second"设置为"-1"以禁用限制。

限制在批处理之间使用等待时间，以便可以为内部滚动请求提供超时，该超时将请求填充考虑在内。填充时间是批大小除以"requests_per_second"和写入时间之间的差值。默认情况下，批大小为"1000"，因此如果"requests_per_second"设置为"500"：

    
    
    target_time = 1000 / 500 per second = 2 seconds
    wait_time = target_time - write_time = 2 seconds - .5 seconds = 1.5 seconds

由于批处理是作为单个"_bulk"请求发出的，因此较大的批处理大小会导致 Elasticsearch 创建许多请求并在开始下一组请求之前等待。这是"突发"而不是"平滑"。

####Slicing

按查询删除支持切片滚动以并行执行删除过程。这可以提高效率，并提供一种将请求分解为更小部分的便捷方法。

将"切片"设置为"自动"可为大多数数据流和索引选择一个合理的数字。如果要手动切片或以其他方式调整自动切片，请记住：

* 当"切片"数等于索引或后备索引中的分片数时，查询性能最有效。如果该数字很大(例如 500)，请选择较小的数字，因为过多的"切片"会损害性能。将"切片"设置为高于分片数量通常不会提高效率并增加开销。  * 删除性能随切片数在可用资源之间线性扩展。

查询或删除性能是否主导运行时取决于要重新编制索引的文档和群集资源。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases to search. Supports wildcards (`*`). To search all data streams or indices, omit this parameter or use `* or `_all`. 

### 查询参数

`allow_no_indices`

    

(可选，布尔值)如果为"false"，则当任何通配符表达式、索引别名或"_all"值仅针对缺少或关闭的索引时，请求将返回错误。即使请求以其他打开的索引为目标，此行为也适用。例如，如果索引以"foo"开头但没有索引以"bar"开头，则以"foo*，bar*"为目标的请求将返回错误。

默认为"真"。

`analyzer`

    

(可选，字符串)用于查询字符串的分析器。

仅当指定了"q"查询字符串参数时，才能使用此参数。

`analyze_wildcard`

    

(可选，布尔值)如果为"true"，则分析通配符和前缀查询。默认为"假"。

仅当指定了"q"查询字符串参数时，才能使用此参数。

`conflicts`

     (Optional, string) What to do if delete by query hits version conflicts: `abort` or `proceed`. Defaults to `abort`. 
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

默认为"打开"。

`ignore_unavailable`

     (Optional, Boolean) If `false`, the request returns an error if it targets a missing or closed index. Defaults to `false`. 
`lenient`

    

(可选，布尔值)如果为"true"，则将忽略查询字符串中基于格式的查询失败(例如向数值字段提供文本)。默认为"假"。

仅当指定了"q"查询字符串参数时，才能使用此参数。

`max_docs`

     (Optional, integer) Maximum number of documents to process. Defaults to all documents. When set to a value less then or equal to `scroll_size` then a scroll will not be used to retrieve the results for the operation. 
`preference`

     (Optional, string) Specifies the node or shard the operation should be performed on. Random by default. 
`q`

     (Optional, string) Query in the Lucene query string syntax. 
`request_cache`

     (Optional, Boolean) If `true`, the request cache is used for this request. Defaults to the index-level setting. 
`refresh`

     (Optional, Boolean) If `true`, Elasticsearch refreshes all shards involved in the delete by query after the request completes. Defaults to `false`. 
`requests_per_second`

     (Optional, integer) The throttle for this request in sub-requests per second. Defaults to `-1` (no throttle). 
`routing`

     (Optional, string) Custom value used to route operations to a specific shard. 
`scroll`

     (Optional, [time value](api-conventions.html#time-units "Time units")) Period to retain the [search context](paginate-search-results.html#scroll-search-context "Keeping the search context alive") for scrolling. See [Scroll search results](paginate-search-results.html#scroll-search-results "Scroll search results"). 
`scroll_size`

     (Optional, integer) Size of the scroll request that powers the operation. Defaults to 1000. 
`search_type`

    

(可选，字符串)搜索操作的类型。可用选项：

* "query_then_fetch" * "dfs_query_then_fetch"

`search_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Explicit timeout for each search request. Defaults to no timeout. 
`slices`

     (Optional, integer) The number of slices this task should be divided into. Defaults to 1 meaning the task isn't sliced into subtasks. 
`sort`

     (Optional, string) A comma-separated list of <field>:<direction> pairs. 
`stats`

     (Optional, string) Specific `tag` of the request for logging and statistical purposes. 
`terminate_after`

    

(可选，整数)每个分片要收集的最大文档数。如果查询达到此限制，Elasticsearch 会提前终止查询。Elasticsearch 在排序之前收集文档。

请谨慎使用。Elasticsearch 将此参数应用于处理请求的每个分片。如果可能，让 Elasticsearch 自动执行提前终止。避免为跨多个数据层使用支持索引的数据流为目标的请求指定此参数。

`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period each deletion request [waits for active shards](docs-index_.html#index-wait-for-active-shards "Active shards"). Defaults to `1m` (one minute). 
`version`

     (Optional, Boolean) If `true`, returns the document version as part of a hit. 
`wait_for_active_shards`

    

(可选，字符串)在继续操作之前必须处于活动状态的分片副本数。设置为"all"或任何正整数，最多为索引中的分片总数("number_of_replicas+1")。默认值：1，主分片。

请参阅活动分片。

### 请求正文

`query`

     (Optional, [query object](query-dsl.html "Query DSL")) Specifies the documents to delete using the [Query DSL](query-dsl.html "Query DSL"). 

### 响应正文

JSON 响应如下所示：

    
    
    {
      "took" : 147,
      "timed_out": false,
      "total": 119,
      "deleted": 119,
      "batches": 1,
      "version_conflicts": 0,
      "noops": 0,
      "retries": {
        "bulk": 0,
        "search": 0
      },
      "throttled_millis": 0,
      "requests_per_second": -1.0,
      "throttled_until_millis": 0,
      "failures" : [ ]
    }

`took`

     The number of milliseconds from start to end of the whole operation. 
`timed_out`

     This flag is set to `true` if any of the requests executed during the delete by query execution has timed out. 
`total`

     The number of documents that were successfully processed. 
`deleted`

     The number of documents that were successfully deleted. 
`batches`

     The number of scroll responses pulled back by the delete by query. 
`version_conflicts`

     The number of version conflicts that the delete by query hit. 
`noops`

     This field is always equal to zero for delete by query. It only exists so that delete by query, update by query, and reindex APIs return responses with the same structure. 
`retries`

     The number of retries attempted by delete by query. `bulk` is the number of bulk actions retried, and `search` is the number of search actions retried. 
`throttled_millis`

     Number of milliseconds the request slept to conform to `requests_per_second`. 
`requests_per_second`

     The number of requests per second effectively executed during the delete by query. 
`throttled_until_millis`

     This field should always be equal to zero in a `_delete_by_query` response. It only has meaning when using the [Task API](tasks.html "Task management API"), where it indicates the next time (in milliseconds since epoch) a throttled request will be executed again in order to conform to `requests_per_second`. 
`failures`

     Array of failures if there were any unrecoverable errors during the process. If this is non-empty then the request aborted because of those failures. Delete by query is implemented using batches, and any failure causes the entire process to abort but all failures in the current batch are collected into the array. You can use the `conflicts` option to prevent reindex from aborting on version conflicts. 

###Examples

从"my-index-000001"数据流或索引中删除所有文档：

    
    
    response = client.delete_by_query(
      index: 'my-index-000001',
      conflicts: 'proceed',
      body: {
        query: {
          match_all: {}
        }
      }
    )
    puts response
    
    
    POST my-index-000001/_delete_by_query?conflicts=proceed
    {
      "query": {
        "match_all": {}
      }
    }

从多个数据流或索引中删除文档：

    
    
    response = client.delete_by_query(
      index: 'my-index-000001,my-index-000002',
      body: {
        query: {
          match_all: {}
        }
      }
    )
    puts response
    
    
    POST /my-index-000001,my-index-000002/_delete_by_query
    {
      "query": {
        "match_all": {}
      }
    }

将按查询操作删除限制为特定路由值的分片：

    
    
    response = client.delete_by_query(
      index: 'my-index-000001',
      routing: 1,
      body: {
        query: {
          range: {
            age: {
              gte: 10
            }
          }
        }
      }
    )
    puts response
    
    
    POST my-index-000001/_delete_by_query?routing=1
    {
      "query": {
        "range" : {
            "age" : {
               "gte" : 10
            }
        }
      }
    }

默认情况下，"_delete_by_query"使用1000的滚动批次。您可以使用"scroll_size"URL 参数更改批处理大小：

    
    
    response = client.delete_by_query(
      index: 'my-index-000001',
      scroll_size: 5000,
      body: {
        query: {
          term: {
            "user.id": 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    POST my-index-000001/_delete_by_query?scroll_size=5000
    {
      "query": {
        "term": {
          "user.id": "kimchy"
        }
      }
    }

使用唯一属性删除文档：

    
    
    response = client.delete_by_query(
      index: 'my-index-000001',
      body: {
        query: {
          term: {
            "user.id": 'kimchy'
          }
        },
        max_docs: 1
      }
    )
    puts response
    
    
    POST my-index-000001/_delete_by_query
    {
      "query": {
        "term": {
          "user.id": "kimchy"
        }
      },
      "max_docs": 1
    }

##### 手动切片

通过提供切片 ID 和切片总数，通过查询手动对删除进行切片：

    
    
    response = client.delete_by_query(
      index: 'my-index-000001',
      body: {
        slice: {
          id: 0,
          max: 2
        },
        query: {
          range: {
            "http.response.bytes": {
              lt: 2_000_000
            }
          }
        }
      }
    )
    puts response
    
    response = client.delete_by_query(
      index: 'my-index-000001',
      body: {
        slice: {
          id: 1,
          max: 2
        },
        query: {
          range: {
            "http.response.bytes": {
              lt: 2_000_000
            }
          }
        }
      }
    )
    puts response
    
    
    POST my-index-000001/_delete_by_query
    {
      "slice": {
        "id": 0,
        "max": 2
      },
      "query": {
        "range": {
          "http.response.bytes": {
            "lt": 2000000
          }
        }
      }
    }
    POST my-index-000001/_delete_by_query
    {
      "slice": {
        "id": 1,
        "max": 2
      },
      "query": {
        "range": {
          "http.response.bytes": {
            "lt": 2000000
          }
        }
      }
    }

您可以验证是否适用于：

    
    
    response = client.indices.refresh
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      size: 0,
      filter_path: 'hits.total',
      body: {
        query: {
          range: {
            "http.response.bytes": {
              lt: 2_000_000
            }
          }
        }
      }
    )
    puts response
    
    
    GET _refresh
    POST my-index-000001/_search?size=0&filter_path=hits.total
    {
      "query": {
        "range": {
          "http.response.bytes": {
            "lt": 2000000
          }
        }
      }
    }

这会产生一个合理的"总计"，如下所示：

    
    
    {
      "hits": {
        "total" : {
            "value": 0,
            "relation": "eq"
        }
      }
    }

##### 使用自动切片

您还可以让按查询删除自动并行化，使用切片滚动来切片_id"。使用"切片"指定要使用的切片数：

    
    
    response = client.delete_by_query(
      index: 'my-index-000001',
      refresh: true,
      slices: 5,
      body: {
        query: {
          range: {
            "http.response.bytes": {
              lt: 2_000_000
            }
          }
        }
      }
    )
    puts response
    
    
    POST my-index-000001/_delete_by_query?refresh&slices=5
    {
      "query": {
        "range": {
          "http.response.bytes": {
            "lt": 2000000
          }
        }
      }
    }

您还可以验证是否适用于：

    
    
    response = client.search(
      index: 'my-index-000001',
      size: 0,
      filter_path: 'hits.total',
      body: {
        query: {
          range: {
            "http.response.bytes": {
              lt: 2_000_000
            }
          }
        }
      }
    )
    puts response
    
    
    POST my-index-000001/_search?size=0&filter_path=hits.total
    {
      "query": {
        "range": {
          "http.response.bytes": {
            "lt": 2000000
          }
        }
      }
    }

这会产生一个合理的"总计"，如下所示：

    
    
    {
      "hits": {
        "total" : {
            "value": 0,
            "relation": "eq"
        }
      }
    }

将"slices"设置为"auto"将允许Elasticsearch选择要使用的切片数量。此设置将为每个分片使用一个切片，达到特定限制。如果有多个源数据流或索引，它将根据分片数最少的索引或后备索引选择切片数。

将"切片"添加到"_delete_by_query"只是自动化上一节中使用的手动过程，创建子请求，这意味着它有一些怪癖：

* 您可以在任务 API 中看到这些请求。这些子请求是带有"切片"的请求的任务的"子"任务。  * 使用"切片"获取请求的任务状态仅包含已完成切片的状态。  * 这些子请求可单独处理，例如取消和重新发送。  * 使用"切片"重新分配请求将按比例限制未完成的子请求。  * 使用"切片"取消请求将取消每个子请求。  * 由于"切片"的性质，每个子请求都不会得到文档的完美均匀部分。将处理所有文档，但某些切片可能比其他切片大。预计较大的切片具有更均匀的分布。  * 带有"切片"的请求上的"requests_per_second"和"max_docs"等参数按比例分配给每个子请求。结合上面关于分布不均匀的观点，您应该得出结论，将"max_docs"与"切片"一起使用可能不会导致完全"max_docs"文档被删除。  * 每个子请求都会获得略有不同的源数据流或索引快照，尽管这些快照都是在大约相同的时间拍摄的。

##### 更改请求的限制

可以通过查询使用"_rethrottle"API 在正在运行的删除时更改"requests_per_second"的值。加快查询速度的重新激活会立即生效，但减慢查询速度的重新限制会在完成当前批处理后生效，以防止滚动超时。

    
    
    $params = [
        'task_id' => 'r1A2WoRbTwKZ516z6NEs5A:36619',
    ];
    $response = $client->deleteByQueryRethrottle($params);
    
    
    resp = client.delete_by_query_rethrottle(
        task_id="r1A2WoRbTwKZ516z6NEs5A:36619", requests_per_second="-1",
    )
    print(resp)
    
    
    response = client.delete_by_query_rethrottle(
      task_id: 'r1A2WoRbTwKZ516z6NEs5A:36619',
      requests_per_second: -1
    )
    puts response
    
    
    res, err := es.DeleteByQueryRethrottle(
    	"r1A2WoRbTwKZ516z6NEs5A:36619",
    	esapi.IntPtr(-1),
    )
    fmt.Println(res, err)
    
    
    const response = await client.deleteByQueryRethrottle({
      task_id: 'r1A2WoRbTwKZ516z6NEs5A:36619',
      requests_per_second: '-1'
    })
    console.log(response)
    
    
    POST _delete_by_query/r1A2WoRbTwKZ516z6NEs5A:36619/_rethrottle?requests_per_second=-1

使用任务 API 获取任务 ID.将"requests_per_second"设置为任何正十进制值，或将"-1"设置为禁用限制。

#### 通过查询操作获取删除状态

使用任务 API 通过查询操作获取删除的状态：

    
    
    $response = $client->tasks()->list();
    
    
    resp = client.tasks.list(detailed="true", actions="*/delete/byquery")
    print(resp)
    
    
    response = client.tasks.list(
      detailed: true,
      actions: '*/delete/byquery'
    )
    puts response
    
    
    res, err := es.Tasks.List(
    	es.Tasks.List.WithActions("*/delete/byquery"),
    	es.Tasks.List.WithDetailed(true),
    )
    fmt.Println(res, err)
    
    
    const response = await client.tasks.list({
      detailed: 'true',
      actions: '*/delete/byquery'
    })
    console.log(response)
    
    
    GET _tasks?detailed=true&actions=*/delete/byquery

响应如下所示：

    
    
    {
      "nodes" : {
        "r1A2WoRbTwKZ516z6NEs5A" : {
          "name" : "r1A2WoR",
          "transport_address" : "127.0.0.1:9300",
          "host" : "127.0.0.1",
          "ip" : "127.0.0.1:9300",
          "attributes" : {
            "testattr" : "test",
            "portsfile" : "true"
          },
          "tasks" : {
            "r1A2WoRbTwKZ516z6NEs5A:36619" : {
              "node" : "r1A2WoRbTwKZ516z6NEs5A",
              "id" : 36619,
              "type" : "transport",
              "action" : "indices:data/write/delete/byquery",
              "status" : {    __"total" : 6154,
                "updated" : 0,
                "created" : 0,
                "deleted" : 3500,
                "batches" : 36,
                "version_conflicts" : 0,
                "noops" : 0,
                "retries": 0,
                "throttled_millis": 0
              },
              "description" : ""
            }
          }
        }
      }
    }

__

|

此对象包含实际状态。它就像响应 JSON 一样，添加了重要的"总计"字段。"总计"是重新索引预期执行的操作总数。您可以通过添加"已更新"、"已创建"和"已删除"字段来估计进度。当请求的总和等于"总计"字段时，请求将完成。   ---|--- 使用任务 ID，您可以直接查找任务：

    
    
    $params = [
        'task_id' => 'r1A2WoRbTwKZ516z6NEs5A:36619',
    ];
    $response = $client->tasks()->get($params);
    
    
    resp = client.tasks.get(task_id="r1A2WoRbTwKZ516z6NEs5A:36619")
    print(resp)
    
    
    response = client.tasks.get(
      task_id: 'r1A2WoRbTwKZ516z6NEs5A:36619'
    )
    puts response
    
    
    res, err := es.Tasks.Get(
    	"r1A2WoRbTwKZ516z6NEs5A:36619",
    )
    fmt.Println(res, err)
    
    
    const response = await client.tasks.get({
      task_id: 'r1A2WoRbTwKZ516z6NEs5A:36619'
    })
    console.log(response)
    
    
    GET /_tasks/r1A2WoRbTwKZ516z6NEs5A:36619

此 API 的优点是它与 'wait_for_completion=false' 集成以透明地返回已完成任务的状态。如果任务完成并且设置了"wait_for_completion=false"，那么它将返回"结果"或"错误"字段。此功能的成本是"wait_for_completion=false"在'.tasks/task/${taskId}'创建的文档。删除该文档由您决定。

##### 通过查询操作取消删除

任何查询删除都可以使用任务取消 API 取消：

    
    
    $params = [
        'task_id' => 'r1A2WoRbTwKZ516z6NEs5A:36619',
    ];
    $response = $client->tasks()->cancel($params);
    
    
    resp = client.tasks.cancel(task_id="r1A2WoRbTwKZ516z6NEs5A:36619")
    print(resp)
    
    
    response = client.tasks.cancel(
      task_id: 'r1A2WoRbTwKZ516z6NEs5A:36619'
    )
    puts response
    
    
    res, err := es.Tasks.Cancel(
    	es.Tasks.Cancel.WithTaskID("r1A2WoRbTwKZ516z6NEs5A:36619"),
    )
    fmt.Println(res, err)
    
    
    const response = await client.tasks.cancel({
      task_id: 'r1A2WoRbTwKZ516z6NEs5A:36619'
    })
    console.log(response)
    
    
    POST _tasks/r1A2WoRbTwKZ516z6NEs5A:36619/_cancel

可以使用任务 API 找到任务 ID。

取消应该会很快发生，但可能需要几秒钟。上面的任务状态 API 将继续列出按查询删除任务，直到此任务检查它是否已取消并自行终止。

[« Delete API](docs-delete.md) [Update API »](docs-update.md)
