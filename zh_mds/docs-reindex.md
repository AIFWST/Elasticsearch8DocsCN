

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Document APIs](docs.md)

[« Bulk API](docs-bulk.md) [Term vectors API »](docs-termvectors.md)

## 重新索引接口

将文档从源复制到目标。

源可以是任何现有索引、别名或数据流。目标必须与源不同。例如，不能将数据流重新索引到自身中。

重新索引需要为源中的所有文档启用"_source"。

在调用"_reindex"之前，应根据需要配置目标。重新索引不会从源或其关联模板复制设置。

映射、分片计数、副本等必须提前配置。

    
    
    response = client.reindex(
      body: {
        source: {
          index: 'my-index-000001'
        },
        dest: {
          index: 'my-new-index-000001'
        }
      }
    )
    puts response
    
    
    POST _reindex
    {
      "source": {
        "index": "my-index-000001"
      },
      "dest": {
        "index": "my-new-index-000001"
      }
    }

###Request

"发布/_reindex"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有以下安全权限：

    * The `read` [index privilege](security-privileges.html#privileges-list-indices "Indices privileges") for the source data stream, index, or alias. 
    * The `write` index privilege for the destination data stream, index, or index alias. 
    * To automatically create a data stream or index with an reindex API request, you must have the `auto_configure`, `create_index`, or `manage` index privilege for the destination data stream, index, or alias. 
    * If reindexing from a remote cluster, the `source.remote.user` must have the `monitor` [cluster privilege](security-privileges.html#privileges-list-cluster "Cluster privileges") and the `read` index privilege for the source data stream, index, or alias. 

* 如果从远程群集重新索引，则必须在"elasticsearch.yml"的"reindex.remote.whitelist"设置中明确允许远程主机。请参阅从远程重新索引。  * 自动数据流创建需要启用数据流的匹配索引模板。请参阅_Set数据stream_。

###Description

从源索引中提取文档源，并将文档索引到目标索引中。您可以将所有文档复制到目标索引，或对文档的子集重新编制索引。

就像"_update_by_query"一样，"_reindex"获取源的快照，但其目标必须**不同**，因此不太可能发生版本冲突。可以像索引 API 一样配置"dest"元素来控制乐观并发控制。省略"version_type"或将其设置为"内部"会导致 Elasticsearch 盲目地将文档转储到目标中，覆盖任何碰巧具有相同 ID 的文档。

将"version_type"设置为"外部"会导致 Elasticsearch 保留源中的"版本"，创建任何缺少的文档，并更新目标中版本比源中版本旧的任何文档。

将"op_type"设置为"创建"会导致"_reindex"仅在目标中创建丢失的文档。所有现有文档都将导致版本冲突。

由于数据流是仅追加的，因此对目标数据流的任何重新索引请求都必须具有"创建"op_type。重新索引只能将新文档添加到目标数据流。它无法更新目标数据流中的现有文档。

默认情况下，版本冲突中止"_reindex"过程。要在存在冲突时继续重新索引，请将"冲突"请求正文参数设置为"继续"。在这种情况下，响应包括遇到的版本冲突的计数。请注意，其他错误类型的处理不受"冲突"参数的影响。此外，如果您选择计算版本冲突，则操作可能会尝试从源重新索引比"max_docs"更多的文档，直到它成功地将"max_docs"文档索引到目标中，或者它遍历了源查询中的每个文档。

#### 异步运行重新索引

如果请求包含"wait_for_completion=false"，Elasticsearch 会执行一些预检检查，启动请求，并返回一个可用于取消或获取任务状态的"任务"。Elasticsearch在'_tasks/'处创建此任务的记录作为文档<task_id>。

#### 从多个源重新编制索引

如果有许多源要重新索引，通常最好一次重新索引一个源，而不是使用 glob 模式来选取多个源。这样，如果出现任何错误，您可以通过删除部分完成的源并重新开始来恢复该过程。它还使并行化过程相当简单：拆分源列表以重新索引并并行运行每个列表。

一次性 bash 脚本似乎对此效果很好：

    
    
    for index in i1 i2 i3 i4 i5; do
      curl -HContent-Type:application/json -XPOST localhost:9200/_reindex?pretty -d'{
        "source": {
          "index": "'$index'"
        },
        "dest": {
          "index": "'$index'-reindexed"
        }
      }'
    done

####Throttling

将"requests_per_second"设置为任何正十进制数("1.4"、"6"、"1000"等)，以限制"_reindex"发出索引操作批处理的速率。通过为每个批处理填充等待时间来限制请求。要禁用限制，请将"requests_per_second"设置为"-1"。

限制是通过在批处理之间等待来完成的，以便_reindex可以为内部使用的"滚动"提供考虑到填充的超时。填充时间是批大小除以"requests_per_second"和写入时间之间的差值。默认情况下，批处理大小为"1000"，因此如果"requests_per_second"设置为"500"：

    
    
    target_time = 1000 / 500 per second = 2 seconds
    wait_time = target_time - write_time = 2 seconds - .5 seconds = 1.5 seconds

由于批处理是作为单个"_bulk"请求发出的，因此较大的批处理大小会导致 Elasticsearch 创建许多请求，然后等待一段时间，然后再开始下一个集合。这是"突发"而不是"平滑"。

####Rethrottling

可以使用"_rethrottle"API 在正在运行的重新索引上更改"requests_per_second"的值：

    
    
    $params = [
        'task_id' => 'r1A2WoRbTwKZ516z6NEs5A:36619',
    ];
    $response = $client->reindexRethrottle($params);
    
    
    resp = client.reindex_rethrottle(
        task_id="r1A2WoRbTwKZ516z6NEs5A:36619", requests_per_second="-1",
    )
    print(resp)
    
    
    response = client.reindex_rethrottle(
      task_id: 'r1A2WoRbTwKZ516z6NEs5A:36619',
      requests_per_second: -1
    )
    puts response
    
    
    res, err := es.ReindexRethrottle(
    	"r1A2WoRbTwKZ516z6NEs5A:36619",
    	esapi.IntPtr(-1),
    )
    fmt.Println(res, err)
    
    
    const response = await client.reindexRethrottle({
      task_id: 'r1A2WoRbTwKZ516z6NEs5A:36619',
      requests_per_second: '-1'
    })
    console.log(response)
    
    
    POST _reindex/r1A2WoRbTwKZ516z6NEs5A:36619/_rethrottle?requests_per_second=-1

可以使用任务 API 找到任务 ID。

就像在重新索引 API 上设置它一样，"requests_per_second"可以是"-1"以禁用限制，也可以是任何十进制数(如"1.7"或"12")限制到该级别。加快查询速度的重新加载将立即生效，但减慢查询速度的重新加载将在完成当前批处理后生效。这可以防止滚动超时。

####Slicing

重新索引支持切片滚动以并行化重新索引过程。这种并行化可以提高效率，并提供一种将请求分解为更小部分的便捷方法。

从远程群集重新编制索引不支持手动或自动切片。

##### 手动切片

通过为每个请求提供切片 ID 和切片总数来手动对重新索引请求进行切片：

    
    
    response = client.reindex(
      body: {
        source: {
          index: 'my-index-000001',
          slice: {
            id: 0,
            max: 2
          }
        },
        dest: {
          index: 'my-new-index-000001'
        }
      }
    )
    puts response
    
    response = client.reindex(
      body: {
        source: {
          index: 'my-index-000001',
          slice: {
            id: 1,
            max: 2
          }
        },
        dest: {
          index: 'my-new-index-000001'
        }
      }
    )
    puts response
    
    
    POST _reindex
    {
      "source": {
        "index": "my-index-000001",
        "slice": {
          "id": 0,
          "max": 2
        }
      },
      "dest": {
        "index": "my-new-index-000001"
      }
    }
    POST _reindex
    {
      "source": {
        "index": "my-index-000001",
        "slice": {
          "id": 1,
          "max": 2
        }
      },
      "dest": {
        "index": "my-new-index-000001"
      }
    }

您可以通过以下方式验证这是否有效：

    
    
    response = client.indices.refresh
    puts response
    
    response = client.search(
      index: 'my-new-index-000001',
      size: 0,
      filter_path: 'hits.total'
    )
    puts response
    
    
    GET _refresh
    POST my-new-index-000001/_search?size=0&filter_path=hits.total

这导致了一个合理的"总计"，如下所示：

    
    
    {
      "hits": {
        "total" : {
            "value": 120,
            "relation": "eq"
        }
      }
    }

##### 自动切片

您还可以让"_reindex"自动并行化，使用切片滚动来切片"_id"。使用"切片"指定要使用的切片数：

    
    
    response = client.reindex(
      slices: 5,
      refresh: true,
      body: {
        source: {
          index: 'my-index-000001'
        },
        dest: {
          index: 'my-new-index-000001'
        }
      }
    )
    puts response
    
    
    POST _reindex?slices=5&refresh
    {
      "source": {
        "index": "my-index-000001"
      },
      "dest": {
        "index": "my-new-index-000001"
      }
    }

您还可以通过以下方式验证其是否有效：

    
    
    response = client.search(
      index: 'my-new-index-000001',
      size: 0,
      filter_path: 'hits.total'
    )
    puts response
    
    
    POST my-new-index-000001/_search?size=0&filter_path=hits.total

这导致了一个合理的"总计"，如下所示：

    
    
    {
      "hits": {
        "total" : {
            "value": 120,
            "relation": "eq"
        }
      }
    }

将"slices"设置为"auto"将允许Elasticsearch选择要使用的切片数量。此设置将为每个分片使用一个切片，达到特定限制。如果有多个源，它将根据分片数量最少的索引或支持索引选择切片数。

将"切片"添加到"_reindex"只是自动执行上一节中使用的手动过程，创建子请求，这意味着它有一些怪癖：

* 您可以在任务 API 中看到这些请求。这些子请求是带有"切片"的请求的任务的"子"任务。  * 使用"切片"获取请求的任务状态仅包含已完成切片的状态。  * 这些子请求可单独处理，例如取消和重新发送。  * 使用"切片"重新分配请求将按比例限制未完成的子请求。  * 使用"切片"取消请求将取消每个子请求。  * 由于"切片"的性质，每个子请求都不会得到文档的完美均匀部分。将处理所有文档，但某些切片可能比其他切片大。预计较大的切片具有更均匀的分布。  * 带有"切片"的请求上的"requests_per_second"和"max_docs"等参数按比例分配给每个子请求。结合上面关于分布不均匀的观点，您应该得出结论，将"max_docs"与"切片"一起使用可能不会导致完全"max_docs"文档被重新索引。  * 每个子请求获得的源快照略有不同，尽管这些快照都是在大约相同的时间拍摄的。

##### 选取切片数

如果自动切片，将"切片"设置为"自动"将为大多数索引选择一个合理的数字。如果手动切片或以其他方式调整自动切片，请使用这些准则。

当"切片"数等于索引中的分片数时，查询性能效率最高。如果该数字很大(例如 500)，请选择较小的数字，因为太多的"切片"会影响性能。将"切片"设置为高于分片数量通常不会提高效率并增加开销。

索引性能随切片数在可用资源之间线性扩展。

查询或索引性能是否主导运行时取决于要重新编制索引的文档和群集资源。

#### 重新索引路由

默认情况下，如果"_reindex"看到带有路由的文档，则保留路由，除非脚本对其进行了更改。您可以在"dest"请求上设置"路由"以更改此设置：

`keep`

     Sets the routing on the bulk request sent for each match to the routing on the match. This is the default value. 
`discard`

     Sets the routing on the bulk request sent for each match to `null`. 
`=<some text>`

     Sets the routing on the bulk request sent for each match to all text after the `=`. 

例如，您可以使用以下请求将所有文档从公司名称为"cat"的"源"复制到路由设置为"cat"的"dest"中。

    
    
    $params = [
        'body' => [
            'source' => [
                'index' => 'source',
                'query' => [
                    'match' => [
                        'company' => 'cat',
                    ],
                ],
            ],
            'dest' => [
                'index' => 'dest',
                'routing' => '=cat',
            ],
        ],
    ];
    $response = $client->reindex($params);
    
    
    resp = client.reindex(
        body={
            "source": {
                "index": "source",
                "query": {"match": {"company": "cat"}},
            },
            "dest": {"index": "dest", "routing": "=cat"},
        },
    )
    print(resp)
    
    
    response = client.reindex(
      body: {
        source: {
          index: 'source',
          query: {
            match: {
              company: 'cat'
            }
          }
        },
        dest: {
          index: 'dest',
          routing: '=cat'
        }
      }
    )
    puts response
    
    
    res, err := es.Reindex(
    	strings.NewReader(`{
    	  "source": {
    	    "index": "source",
    	    "query": {
    	      "match": {
    	        "company": "cat"
    	      }
    	    }
    	  },
    	  "dest": {
    	    "index": "dest",
    	    "routing": "=cat"
    	  }
    	}`))
    fmt.Println(res, err)
    
    
    const response = await client.reindex({
      body: {
        source: {
          index: 'source',
          query: {
            match: {
              company: 'cat'
            }
          }
        },
        dest: {
          index: 'dest',
          routing: '=cat'
        }
      }
    })
    console.log(response)
    
    
    POST _reindex
    {
      "source": {
        "index": "source",
        "query": {
          "match": {
            "company": "cat"
          }
        }
      },
      "dest": {
        "index": "dest",
        "routing": "=cat"
      }
    }

默认情况下，"_reindex"使用1000的滚动批次。您可以使用"源"元素中的"大小"字段更改批处理大小：

    
    
    $params = [
        'body' => [
            'source' => [
                'index' => 'source',
                'size' => 100,
            ],
            'dest' => [
                'index' => 'dest',
                'routing' => '=cat',
            ],
        ],
    ];
    $response = $client->reindex($params);
    
    
    resp = client.reindex(
        body={
            "source": {"index": "source", "size": 100},
            "dest": {"index": "dest", "routing": "=cat"},
        },
    )
    print(resp)
    
    
    response = client.reindex(
      body: {
        source: {
          index: 'source',
          size: 100
        },
        dest: {
          index: 'dest',
          routing: '=cat'
        }
      }
    )
    puts response
    
    
    res, err := es.Reindex(
    	strings.NewReader(`{
    	  "source": {
    	    "index": "source",
    	    "size": 100
    	  },
    	  "dest": {
    	    "index": "dest",
    	    "routing": "=cat"
    	  }
    	}`))
    fmt.Println(res, err)
    
    
    const response = await client.reindex({
      body: {
        source: {
          index: 'source',
          size: 100
        },
        dest: {
          index: 'dest',
          routing: '=cat'
        }
      }
    })
    console.log(response)
    
    
    POST _reindex
    {
      "source": {
        "index": "source",
        "size": 100
      },
      "dest": {
        "index": "dest",
        "routing": "=cat"
      }
    }

#### 使用引入管道重新编制索引

重新索引还可以通过指定如下所示的"管道"来使用"引入管道"功能：

    
    
    $params = [
        'body' => [
            'source' => [
                'index' => 'source',
            ],
            'dest' => [
                'index' => 'dest',
                'pipeline' => 'some_ingest_pipeline',
            ],
        ],
    ];
    $response = $client->reindex($params);
    
    
    resp = client.reindex(
        body={
            "source": {"index": "source"},
            "dest": {"index": "dest", "pipeline": "some_ingest_pipeline"},
        },
    )
    print(resp)
    
    
    response = client.reindex(
      body: {
        source: {
          index: 'source'
        },
        dest: {
          index: 'dest',
          pipeline: 'some_ingest_pipeline'
        }
      }
    )
    puts response
    
    
    res, err := es.Reindex(
    	strings.NewReader(`{
    	  "source": {
    	    "index": "source"
    	  },
    	  "dest": {
    	    "index": "dest",
    	    "pipeline": "some_ingest_pipeline"
    	  }
    	}`))
    fmt.Println(res, err)
    
    
    const response = await client.reindex({
      body: {
        source: {
          index: 'source'
        },
        dest: {
          index: 'dest',
          pipeline: 'some_ingest_pipeline'
        }
      }
    })
    console.log(response)
    
    
    POST _reindex
    {
      "source": {
        "index": "source"
      },
      "dest": {
        "index": "dest",
        "pipeline": "some_ingest_pipeline"
      }
    }

### 查询参数

`refresh`

     (Optional, Boolean) If `true`, the request refreshes affected shards to make this operation visible to search. Defaults to `false`. 
`timeout`

    

(可选，时间单位)周期每个索引等待以下操作：

* 自动创建索引 * 动态映射更新 * 等待活动分片

默认为"1m"(一分钟)。这保证了 Elasticsearch 在失败之前至少等待超时。实际等待时间可能会更长，尤其是在发生多次等待时。

`wait_for_active_shards`

    

(可选，字符串)在继续操作之前必须处于活动状态的分片副本数。设置为"all"或任何正整数，最多为索引中的分片总数("number_of_replicas+1")。默认值：1，主分片。

请参阅活动分片。

`wait_for_completion`

     (Optional, Boolean) If `true`, the request blocks until the operation is complete. Defaults to `true`. 
`requests_per_second`

     (Optional, integer) The throttle for this request in sub-requests per second. Defaults to `-1` (no throttle). 
`require_alias`

     (Optional, Boolean) If `true`, the destination must be an [index alias](aliases.html "Aliases"). Defaults to `false`. 
`scroll`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Specifies how long a consistent view of the index should be maintained for scrolled search. 
`slices`

     (Optional, integer) The number of slices this task should be divided into. Defaults to 1 meaning the task isn't sliced into subtasks. 
`max_docs`

     (Optional, integer) Maximum number of documents to process. Defaults to all documents. When set to a value less then or equal to `scroll_size` then a scroll will not be used to retrieve the results for the operation. 

### 请求正文

`conflicts`

     (Optional, enum) Set to `proceed` to continue reindexing even if there are conflicts. Defaults to `abort`. 
`max_docs`

     (Optional, integer) The maximum number of documents to reindex. If [conflicts](docs-reindex.html#conflicts) is equal to `proceed`, reindex could attempt to reindex more documents from the source than `max_docs` until it has successfully indexed `max_docs` documents into the target, or it has gone through every document in the source query. 
`source`

    

`index`

     (Required, string) The name of the data stream, index, or alias you are copying _from_. Also accepts a comma-separated list to reindex from multiple sources. 
`query`

     (Optional, [query object](query-dsl.html "Query DSL")) Specifies the documents to reindex using the Query DSL. 
`remote`

    

`host`

     (Optional, string) The URL for the remote instance of Elasticsearch that you want to index _from_. Required when indexing from remote. 
`username`

     (Optional, string) The username to use for authentication with the remote host. 
`password`

     (Optional, string) The password to use for authentication with the remote host. 
`socket_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) The remote socket read timeout. Defaults to 30 seconds. 
`connect_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) The remote connection timeout. Defaults to 30 seconds. 
`headers`

     (Optional, object) An object containing the headers of ther request. 

`size`

     {Optional, integer) The number of documents to index per batch. Use when indexing from remote to ensure that the batches fit within the on-heap buffer, which defaults to a maximum size of 100 MB. 
`slice`

    

`id`

     (Optional, integer) Slice ID for [manual slicing](docs-reindex.html#docs-reindex-manual-slice "Manual slicing"). 
`max`

     (Optional, integer) Total number of slices. 

`sort`

    

(可选，列表)在<field><direction>编制索引之前要作为排序依据的"："对的逗号分隔列表。与"max_docs"结合使用可控制重新编制索引的文档。

### 在 7.6 中已弃用。

不推荐使用重新索引中的排序。重新索引中的排序从来不能保证按顺序索引文档，并且会阻止重新索引的进一步发展，例如弹性和性能改进。如果与"max_docs"结合使用，请考虑改用查询筛选器。

`_source`

     (Optional, string) If `true` reindexes all source fields. Set to a list to reindex select fields. Defaults to `true`. 

`dest`

    

`index`

     (Required, string) The name of the data stream, index, or index alias you are copying _to_. 
`version_type`

     (Optional, enum) The versioning to use for the indexing operation. Valid values: `internal`, `external`, `external_gt`, `external_gte`. See [Version types](docs-index_.html#index-version-types "Version types") for more information. 
`op_type`

    

(可选，枚举)设置为"创建"以仅索引尚不存在的文档(如果不存在则放置)。有效值："索引"、"创建"。默认为"索引"。

若要重新索引到数据流目标，此参数必须为"创建"。

`pipeline`

     (Optional, string) the name of the [pipeline](docs-reindex.html#reindex-with-an-ingest-pipeline "Reindex with an ingest pipeline") to use. 

`script`

    

`source`

     (Optional, string) The script to run to update the document source or metadata when reindexing. 
`lang`

     (Optional, enum) The script language: `painless`, `expression`, `mustache`, `java`. For more information, see [Scripting](modules-scripting.html "Scripting"). 

### 响应正文

`took`

     (integer) The total milliseconds the entire operation took. 
`timed_out`

     {Boolean) This flag is set to `true` if any of the requests executed during the reindex timed out. 
`total`

     (integer) The number of documents that were successfully processed. 
`updated`

     (integer) The number of documents that were successfully updated, i.e. a document with same ID already existed prior to reindex updating it. 
`created`

     (integer) The number of documents that were successfully created. 
`deleted`

     (integer) The number of documents that were successfully deleted. 
`batches`

     (integer) The number of scroll responses pulled back by the reindex. 
`noops`

     (integer) The number of documents that were ignored because the script used for the reindex returned a `noop` value for `ctx.op`. 
`version_conflicts`

     (integer) The number of version conflicts that reindex hits. 
`retries`

     (integer) The number of retries attempted by reindex. `bulk` is the number of bulk actions retried and `search` is the number of search actions retried. 
`throttled_millis`

     (integer) Number of milliseconds the request slept to conform to `requests_per_second`. 
`requests_per_second`

     (integer) The number of requests per second effectively executed during the reindex. 
`throttled_until_millis`

     (integer) This field should always be equal to zero in a `_reindex` response. It only has meaning when using the [Task API](docs-reindex.html#docs-reindex-task-api "Running reindex asynchronously"), where it indicates the next time (in milliseconds since epoch) a throttled request will be executed again in order to conform to `requests_per_second`. 
`failures`

     (array) Array of failures if there were any unrecoverable errors during the process. If this is non-empty then the request aborted because of those failures. Reindex is implemented using batches and any failure causes the entire process to abort but all failures in the current batch are collected into the array. You can use the `conflicts` option to prevent reindex from aborting on version conflicts. 

###Examples

#### 使用查询重新索引所选文档

您可以通过向"源"添加查询来限制文档。例如，以下请求仅将"kimchy"user.id 的文档复制到"my-new-index-000001"中：

    
    
    response = client.reindex(
      body: {
        source: {
          index: 'my-index-000001',
          query: {
            term: {
              "user.id": 'kimchy'
            }
          }
        },
        dest: {
          index: 'my-new-index-000001'
        }
      }
    )
    puts response
    
    
    POST _reindex
    {
      "source": {
        "index": "my-index-000001",
        "query": {
          "term": {
            "user.id": "kimchy"
          }
        }
      },
      "dest": {
        "index": "my-new-index-000001"
      }
    }

#### 使用"max_docs"重新索引所选文档

您可以通过设置"max_docs"来限制已处理文档的数量。例如，此请求将单个文档从"my-index-000001"复制到"my-new-index-000001"：

    
    
    response = client.reindex(
      body: {
        max_docs: 1,
        source: {
          index: 'my-index-000001'
        },
        dest: {
          index: 'my-new-index-000001'
        }
      }
    )
    puts response
    
    
    POST _reindex
    {
      "max_docs": 1,
      "source": {
        "index": "my-index-000001"
      },
      "dest": {
        "index": "my-new-index-000001"
      }
    }

#### 从多个源重新编制索引

"source"中的"index"属性可以是一个列表，允许您在一个请求中从多个源复制。这将从"my-index-000001"和"my-index-000002"索引复制文档：

    
    
    response = client.reindex(
      body: {
        source: {
          index: [
            'my-index-000001',
            'my-index-000002'
          ]
        },
        dest: {
          index: 'my-new-index-000002'
        }
      }
    )
    puts response
    
    
    POST _reindex
    {
      "source": {
        "index": ["my-index-000001", "my-index-000002"]
      },
      "dest": {
        "index": "my-new-index-000002"
      }
    }

Reindex API 不努力处理 ID 冲突，因此最后一个编写的文档将"获胜"，但顺序通常不可预测，因此依赖此行为不是一个好主意。相反，请确保使用 ascript 的 ID 是唯一的。

#### 使用源筛选器重新索引选择字段

您可以使用源筛选来重新索引原始文档中的字段子集。例如，以下请求仅重新索引每个文档的"user.id"和"_doc"字段：

    
    
    response = client.reindex(
      body: {
        source: {
          index: 'my-index-000001',
          _source: [
            'user.id',
            '_doc'
          ]
        },
        dest: {
          index: 'my-new-index-000001'
        }
      }
    )
    puts response
    
    
    POST _reindex
    {
      "source": {
        "index": "my-index-000001",
        "_source": ["user.id", "_doc"]
      },
      "dest": {
        "index": "my-new-index-000001"
      }
    }

#### 重新索引以更改字段的名称

"_reindex"可用于构建具有重命名字段的索引副本。Sayyou创建一个包含如下所示的文档的索引：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      refresh: true,
      body: {
        text: 'words words',
        flag: 'foo'
      }
    )
    puts response
    
    
    POST my-index-000001/_doc/1?refresh
    {
      "text": "words words",
      "flag": "foo"
    }

但是您不喜欢名称"flag"，并希望将其替换为"tag"._reindex"可以为您创建另一个索引：

    
    
    response = client.reindex(
      body: {
        source: {
          index: 'my-index-000001'
        },
        dest: {
          index: 'my-new-index-000001'
        },
        script: {
          source: 'ctx._source.tag = ctx._source.remove("flag")'
        }
      }
    )
    puts response
    
    
    POST _reindex
    {
      "source": {
        "index": "my-index-000001"
      },
      "dest": {
        "index": "my-new-index-000001"
      },
      "script": {
        "source": "ctx._source.tag = ctx._source.remove(\"flag\")"
      }
    }

现在您可以获取新文档：

    
    
    response = client.get(
      index: 'my-new-index-000001',
      id: 1
    )
    puts response
    
    
    GET my-new-index-000001/_doc/1

这将返回：

    
    
    {
      "found": true,
      "_id": "1",
      "_index": "my-new-index-000001",
      "_version": 1,
      "_seq_no": 44,
      "_primary_term": 1,
      "_source": {
        "text": "words words",
        "tag": "foo"
      }
    }

#### 重新索引每日指数

您可以将"_reindex"与 Painless 结合使用来重新索引每日索引，以将新模板应用于现有文档。

假设您有包含以下文档的索引：

    
    
    $params = [
        'index' => 'metricbeat-2016.05.30',
        'id' => '1',
        'body' => [
            'system.cpu.idle.pct' => 0.908,
        ],
    ];
    $response = $client->index($params);
    $params = [
        'index' => 'metricbeat-2016.05.31',
        'id' => '1',
        'body' => [
            'system.cpu.idle.pct' => 0.105,
        ],
    ];
    $response = $client->index($params);
    
    
    resp = client.index(
        index="metricbeat-2016.05.30",
        id="1",
        refresh=True,
        body={"system.cpu.idle.pct": 0.908},
    )
    print(resp)
    
    resp = client.index(
        index="metricbeat-2016.05.31",
        id="1",
        refresh=True,
        body={"system.cpu.idle.pct": 0.105},
    )
    print(resp)
    
    
    response = client.index(
      index: 'metricbeat-2016.05.30',
      id: 1,
      refresh: true,
      body: {
        "system.cpu.idle.pct": 0.908
      }
    )
    puts response
    
    response = client.index(
      index: 'metricbeat-2016.05.31',
      id: 1,
      refresh: true,
      body: {
        "system.cpu.idle.pct": 0.105
      }
    )
    puts response
    
    
    {
    	res, err := es.Index(
    		"metricbeat-2016.05.30",
    		strings.NewReader(`{
    	  "system.cpu.idle.pct": 0.908
    	}`),
    		es.Index.WithDocumentID("1"),
    		es.Index.WithRefresh("true"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Index(
    		"metricbeat-2016.05.31",
    		strings.NewReader(`{
    	  "system.cpu.idle.pct": 0.105
    	}`),
    		es.Index.WithDocumentID("1"),
    		es.Index.WithRefresh("true"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    
    const response0 = await client.index({
      index: 'metricbeat-2016.05.30',
      id: '1',
      refresh: true,
      body: {
        'system.cpu.idle.pct': 0.908
      }
    })
    console.log(response0)
    
    const response1 = await client.index({
      index: 'metricbeat-2016.05.31',
      id: '1',
      refresh: true,
      body: {
        'system.cpu.idle.pct': 0.105
      }
    })
    console.log(response1)
    
    
    PUT metricbeat-2016.05.30/_doc/1?refresh
    {"system.cpu.idle.pct": 0.908}
    PUT metricbeat-2016.05.31/_doc/1?refresh
    {"system.cpu.idle.pct": 0.105}

'metricbeat-*' 索引的新模板已经加载到 Elasticsearch 中，但它仅适用于新创建的索引。无痛可用于重新索引现有文档并应用新模板。

下面的脚本从索引名称中提取日期，并创建一个附加了"-1"的新索引。来自"metricbeat-2016.05.31"的所有数据将被重新索引到"metricbeat-2016.05.31-1"中。

    
    
    $params = [
        'body' => [
            'source' => [
                'index' => 'metricbeat-*',
            ],
            'dest' => [
                'index' => 'metricbeat',
            ],
            'script' => [
                'lang' => 'painless',
                'source' => 'ctx._index = \'metricbeat-\' + (ctx._index.substring(\'metricbeat-\'.length(), ctx._index.length())) + \'-1\'',
            ],
        ],
    ];
    $response = $client->reindex($params);
    
    
    resp = client.reindex(
        body={
            "source": {"index": "metricbeat-*"},
            "dest": {"index": "metricbeat"},
            "script": {
                "lang": "painless",
                "source": "ctx._index = 'metricbeat-' + (ctx._index.substring('metricbeat-'.length(), ctx._index.length())) + '-1'",
            },
        },
    )
    print(resp)
    
    
    response = client.reindex(
      body: {
        source: {
          index: 'metricbeat-*'
        },
        dest: {
          index: 'metricbeat'
        },
        script: {
          lang: 'painless',
          source: "ctx._index = 'metricbeat-' + (ctx._index.substring('metricbeat-'.length(), ctx._index.length())) + '-1'"
        }
      }
    )
    puts response
    
    
    res, err := es.Reindex(
    	strings.NewReader(`{
    	  "source": {
    	    "index": "metricbeat-*"
    	  },
    	  "dest": {
    	    "index": "metricbeat"
    	  },
    	  "script": {
    	    "lang": "painless",
    	    "source": "ctx._index = 'metricbeat-' + (ctx._index.substring('metricbeat-'.length(), ctx._index.length())) + '-1'"
    	  }
    	}`))
    fmt.Println(res, err)
    
    
    const response = await client.reindex({
      body: {
        source: {
          index: 'metricbeat-*'
        },
        dest: {
          index: 'metricbeat'
        },
        script: {
          lang: 'painless',
          source: "ctx._index = 'metricbeat-' + (ctx._index.substring('metricbeat-'.length(), ctx._index.length())) + '-1'"
        }
      }
    })
    console.log(response)
    
    
    POST _reindex
    {
      "source": {
        "index": "metricbeat-*"
      },
      "dest": {
        "index": "metricbeat"
      },
      "script": {
        "lang": "painless",
        "source": "ctx._index = 'metricbeat-' + (ctx._index.substring('metricbeat-'.length(), ctx._index.length())) + '-1'"
      }
    }

以前 metricbeat 索引中的所有文档现在都可以在 '*-1' 索引中找到。

    
    
    $params = [
        'index' => 'metricbeat-2016.05.30-1',
        'id' => '1',
    ];
    $response = $client->get($params);
    $params = [
        'index' => 'metricbeat-2016.05.31-1',
        'id' => '1',
    ];
    $response = $client->get($params);
    
    
    resp = client.get(index="metricbeat-2016.05.30-1", id="1")
    print(resp)
    
    resp = client.get(index="metricbeat-2016.05.31-1", id="1")
    print(resp)
    
    
    response = client.get(
      index: 'metricbeat-2016.05.30-1',
      id: 1
    )
    puts response
    
    response = client.get(
      index: 'metricbeat-2016.05.31-1',
      id: 1
    )
    puts response
    
    
    {
    	res, err := es.Get("metricbeat-2016.05.30-1", "1", es.Get.WithPretty())
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Get("metricbeat-2016.05.31-1", "1", es.Get.WithPretty())
    	fmt.Println(res, err)
    }
    
    
    const response0 = await client.get({
      index: 'metricbeat-2016.05.30-1',
      id: '1'
    })
    console.log(response0)
    
    const response1 = await client.get({
      index: 'metricbeat-2016.05.31-1',
      id: '1'
    })
    console.log(response1)
    
    
    GET metricbeat-2016.05.30-1/_doc/1
    GET metricbeat-2016.05.31-1/_doc/1

前面的方法还可以与更改字段名称结合使用，以仅将现有数据加载到新索引中，并在需要时重命名任何字段。

#### 提取源的随机子集

"_reindex"可用于提取源的随机子集进行测试：

    
    
    response = client.reindex(
      body: {
        max_docs: 10,
        source: {
          index: 'my-index-000001',
          query: {
            function_score: {
              random_score: {},
              min_score: 0.9
            }
          }
        },
        dest: {
          index: 'my-new-index-000001'
        }
      }
    )
    puts response
    
    
    POST _reindex
    {
      "max_docs": 10,
      "source": {
        "index": "my-index-000001",
        "query": {
          "function_score" : {
            "random_score" : {},
            "min_score" : 0.9    __}
        }
      },
      "dest": {
        "index": "my-new-index-000001"
      }
    }

__

|

您可能需要根据从源中提取的数据的相对数量调整"min_score"。   ---|--- #### 在重新索引期间修改文档编辑

与"_update_by_query"一样，"_reindex"支持修改文档的脚本。与"_update_by_query"不同，该脚本允许修改文档的元数据。本示例增加源文档的版本：

    
    
    response = client.reindex(
      body: {
        source: {
          index: 'my-index-000001'
        },
        dest: {
          index: 'my-new-index-000001',
          version_type: 'external'
        },
        script: {
          source: "if (ctx._source.foo == 'bar') {ctx._version++; ctx._source.remove('foo')}",
          lang: 'painless'
        }
      }
    )
    puts response
    
    
    POST _reindex
    {
      "source": {
        "index": "my-index-000001"
      },
      "dest": {
        "index": "my-new-index-000001",
        "version_type": "external"
      },
      "script": {
        "source": "if (ctx._source.foo == 'bar') {ctx._version++; ctx._source.remove('foo')}",
        "lang": "painless"
      }
    }

就像在"_update_by_query"中一样，您可以设置"ctx.op"来更改在目标上执行的操作：

`noop`

     Set `ctx.op = "noop"` if your script decides that the document doesn't have to be indexed in the destination. This no operation will be reported in the `noop` counter in the [response body](docs-reindex.html#docs-reindex-api-response-body "Response body"). 
`delete`

     Set `ctx.op = "delete"` if your script decides that the document must be deleted from the destination. The deletion will be reported in the `deleted` counter in the [response body](docs-reindex.html#docs-reindex-api-response-body "Response body"). 

将"ctx.op"设置为其他任何内容都会返回错误，在"ctx"中设置任何其他字段也会返回错误。

想想可能性！只是要小心;您可以更改：

* "_id" * "_index" * "_version" * "_routing"

将"_version"设置为"null"或从"ctx"映射中清除它就像不在索引请求中发送版本一样;这将导致在目标中覆盖文档，而不管目标上的版本或您在"_reindex"请求中使用的版本类型如何。

### 从远程重新索引

Reindex 支持从远程 Elasticsearch 集群重新索引：

    
    
    response = client.reindex(
      body: {
        source: {
          remote: {
            host: 'http://otherhost:9200',
            username: 'user',
            password: 'pass'
          },
          index: 'my-index-000001',
          query: {
            match: {
              test: 'data'
            }
          }
        },
        dest: {
          index: 'my-new-index-000001'
        }
      }
    )
    puts response
    
    
    POST _reindex
    {
      "source": {
        "remote": {
          "host": "http://otherhost:9200",
          "username": "user",
          "password": "pass"
        },
        "index": "my-index-000001",
        "query": {
          "match": {
            "test": "data"
          }
        }
      },
      "dest": {
        "index": "my-new-index-000001"
      }
    }

"host"参数必须包含方案、主机、端口(例如"https：//otherhost：9200")和可选路径(例如"https：//otherhost：9200/proxy")。"用户名"和"密码"参数是可选的，当它们存在时，"_reindex"将使用基本身份验证连接到远程Elasticsearch节点。使用基本身份验证时请务必使用"https"，否则密码将以纯文本形式发送。有一系列设置可用于配置"https"连接的行为。

使用 Elastic Cloud 时，还可以通过使用有效的 API 密钥对远程集群进行身份验证：

    
    
    response = client.reindex(
      body: {
        source: {
          remote: {
            host: 'http://otherhost:9200',
            headers: {
              "Authorization": 'ApiKey API_KEY_VALUE'
            }
          },
          index: 'my-index-000001',
          query: {
            match: {
              test: 'data'
            }
          }
        },
        dest: {
          index: 'my-new-index-000001'
        }
      }
    )
    puts response
    
    
    POST _reindex
    {
      "source": {
        "remote": {
          "host": "http://otherhost:9200",
          "headers": {
            "Authorization": "ApiKey API_KEY_VALUE"
          }
        },
        "index": "my-index-000001",
        "query": {
          "match": {
            "test": "data"
          }
        }
      },
      "dest": {
        "index": "my-new-index-000001"
      }
    }

远程主机必须在"elasticsearch.yml"中使用"reindex.remote.whitelist"属性明确允许。它可以设置为逗号分隔的允许远程"主机"和"端口"组合列表。方案被忽略，只使用主机和端口。例如：

    
    
    reindex.remote.whitelist: "otherhost:9200, another:9200, 127.0.10.*:9200, localhost:*"

必须在将协调重新索引的任何节点上配置允许的主机列表。

此功能应该适用于您可能找到的任何版本的 Elasticsearch 的远程集群。这应该允许您通过从旧版本的集群重新索引，从任何版本的 Elasticsearch 升级到当前版本。

Elasticsearch 不支持跨主要版本的向前兼容性。例如，不能将 7.x 群集重新索引到 6.x 群集。

要启用发送到旧版 Elasticsearch 的查询，"query"参数将直接发送到远程主机，无需验证或修改。

从远程群集重新编制索引不支持手动或自动切片。

从远程服务器重新编制索引使用堆上缓冲区，该缓冲区的最大大小默认为 100MB。如果远程索引包含非常大的文档，则需要使用较小的批大小。下面的示例将批大小设置为"10"，这非常非常小。

    
    
    $params = [
        'body' => [
            'source' => [
                'remote' => [
                    'host' => 'http://otherhost:9200',
                ],
                'index' => 'source',
                'size' => 10,
                'query' => [
                    'match' => [
                        'test' => 'data',
                    ],
                ],
            ],
            'dest' => [
                'index' => 'dest',
            ],
        ],
    ];
    $response = $client->reindex($params);
    
    
    resp = client.reindex(
        body={
            "source": {
                "remote": {"host": "http://otherhost:9200"},
                "index": "source",
                "size": 10,
                "query": {"match": {"test": "data"}},
            },
            "dest": {"index": "dest"},
        },
    )
    print(resp)
    
    
    response = client.reindex(
      body: {
        source: {
          remote: {
            host: 'http://otherhost:9200'
          },
          index: 'source',
          size: 10,
          query: {
            match: {
              test: 'data'
            }
          }
        },
        dest: {
          index: 'dest'
        }
      }
    )
    puts response
    
    
    res, err := es.Reindex(
    	strings.NewReader(`{
    	  "source": {
    	    "remote": {
    	      "host": "http://otherhost:9200"
    	    },
    	    "index": "source",
    	    "size": 10,
    	    "query": {
    	      "match": {
    	        "test": "data"
    	      }
    	    }
    	  },
    	  "dest": {
    	    "index": "dest"
    	  }
    	}`))
    fmt.Println(res, err)
    
    
    const response = await client.reindex({
      body: {
        source: {
          remote: {
            host: 'http://otherhost:9200'
          },
          index: 'source',
          size: 10,
          query: {
            match: {
              test: 'data'
            }
          }
        },
        dest: {
          index: 'dest'
        }
      }
    })
    console.log(response)
    
    
    POST _reindex
    {
      "source": {
        "remote": {
          "host": "http://otherhost:9200"
        },
        "index": "source",
        "size": 10,
        "query": {
          "match": {
            "test": "data"
          }
        }
      },
      "dest": {
        "index": "dest"
      }
    }

也可以使用"socket_timeout"字段设置远程连接的套接字读取超时，并使用"connect_timeout"字段设置连接超时。两者都默认为 30 秒。此示例将套接字读取超时设置为 1 分钟，将连接超时设置为 10 秒：

    
    
    $params = [
        'body' => [
            'source' => [
                'remote' => [
                    'host' => 'http://otherhost:9200',
                    'socket_timeout' => '1m',
                    'connect_timeout' => '10s',
                ],
                'index' => 'source',
                'query' => [
                    'match' => [
                        'test' => 'data',
                    ],
                ],
            ],
            'dest' => [
                'index' => 'dest',
            ],
        ],
    ];
    $response = $client->reindex($params);
    
    
    resp = client.reindex(
        body={
            "source": {
                "remote": {
                    "host": "http://otherhost:9200",
                    "socket_timeout": "1m",
                    "connect_timeout": "10s",
                },
                "index": "source",
                "query": {"match": {"test": "data"}},
            },
            "dest": {"index": "dest"},
        },
    )
    print(resp)
    
    
    response = client.reindex(
      body: {
        source: {
          remote: {
            host: 'http://otherhost:9200',
            socket_timeout: '1m',
            connect_timeout: '10s'
          },
          index: 'source',
          query: {
            match: {
              test: 'data'
            }
          }
        },
        dest: {
          index: 'dest'
        }
      }
    )
    puts response
    
    
    res, err := es.Reindex(
    	strings.NewReader(`{
    	  "source": {
    	    "remote": {
    	      "host": "http://otherhost:9200",
    	      "socket_timeout": "1m",
    	      "connect_timeout": "10s"
    	    },
    	    "index": "source",
    	    "query": {
    	      "match": {
    	        "test": "data"
    	      }
    	    }
    	  },
    	  "dest": {
    	    "index": "dest"
    	  }
    	}`))
    fmt.Println(res, err)
    
    
    const response = await client.reindex({
      body: {
        source: {
          remote: {
            host: 'http://otherhost:9200',
            socket_timeout: '1m',
            connect_timeout: '10s'
          },
          index: 'source',
          query: {
            match: {
              test: 'data'
            }
          }
        },
        dest: {
          index: 'dest'
        }
      }
    })
    console.log(response)
    
    
    POST _reindex
    {
      "source": {
        "remote": {
          "host": "http://otherhost:9200",
          "socket_timeout": "1m",
          "connect_timeout": "10s"
        },
        "index": "source",
        "query": {
          "match": {
            "test": "data"
          }
        }
      },
      "dest": {
        "index": "dest"
      }
    }

#### 配置 SSL 参数

从远程重新索引支持可配置的 SSL 设置。这些必须在"elasticsearch.yml"文件中指定，但 securesettings 除外，您将其添加到 Elasticsearch 密钥库中。无法在"_reindex"请求正文中配置 SSL。

支持以下设置：

`reindex.ssl.certificate_authorities`

     List of paths to PEM encoded certificate files that should be trusted. You cannot specify both `reindex.ssl.certificate_authorities` and `reindex.ssl.truststore.path`. 
`reindex.ssl.truststore.path`

     The path to the Java Keystore file that contains the certificates to trust. This keystore can be in "JKS" or "PKCS#12" format. You cannot specify both `reindex.ssl.certificate_authorities` and `reindex.ssl.truststore.path`. 
`reindex.ssl.truststore.password`

     The password to the truststore (`reindex.ssl.truststore.path`). This setting cannot be used with `reindex.ssl.truststore.secure_password`. 
`reindex.ssl.truststore.secure_password` ([Secure](secure-settings.html
"Secure settings"))

     The password to the truststore (`reindex.ssl.truststore.path`). This setting cannot be used with `reindex.ssl.truststore.password`. 
`reindex.ssl.truststore.type`

     The type of the truststore (`reindex.ssl.truststore.path`). Must be either `jks` or `PKCS12`. If the truststore path ends in ".p12", ".pfx" or "pkcs12", this setting defaults to `PKCS12`. Otherwise, it defaults to `jks`. 
`reindex.ssl.verification_mode`

     Indicates the type of verification to protect against man in the middle attacks and certificate forgery. One of `full` (verify the hostname and the certificate path), `certificate` (verify the certificate path, but not the hostname) or `none` (perform no verification - this is strongly discouraged in production environments). Defaults to `full`. 
`reindex.ssl.certificate`

     Specifies the path to the PEM encoded certificate (or certificate chain) to be used for HTTP client authentication (if required by the remote cluster) This setting requires that `reindex.ssl.key` also be set. You cannot specify both `reindex.ssl.certificate` and `reindex.ssl.keystore.path`. 
`reindex.ssl.key`

     Specifies the path to the PEM encoded private key associated with the certificate used for client authentication (`reindex.ssl.certificate`). You cannot specify both `reindex.ssl.key` and `reindex.ssl.keystore.path`. 
`reindex.ssl.key_passphrase`

     Specifies the passphrase to decrypt the PEM encoded private key (`reindex.ssl.key`) if it is encrypted. Cannot be used with `reindex.ssl.secure_key_passphrase`. 
`reindex.ssl.secure_key_passphrase` ([Secure](secure-settings.html "Secure
settings"))

     Specifies the passphrase to decrypt the PEM encoded private key (`reindex.ssl.key`) if it is encrypted. Cannot be used with `reindex.ssl.key_passphrase`. 
`reindex.ssl.keystore.path`

     Specifies the path to the keystore that contains a private key and certificate to be used for HTTP client authentication (if required by the remote cluster). This keystore can be in "JKS" or "PKCS#12" format. You cannot specify both `reindex.ssl.key` and `reindex.ssl.keystore.path`. 
`reindex.ssl.keystore.type`

     The type of the keystore (`reindex.ssl.keystore.path`). Must be either `jks` or `PKCS12`. If the keystore path ends in ".p12", ".pfx" or "pkcs12", this setting defaults to `PKCS12`. Otherwise, it defaults to `jks`. 
`reindex.ssl.keystore.password`

     The password to the keystore (`reindex.ssl.keystore.path`). This setting cannot be used with `reindex.ssl.keystore.secure_password`. 
`reindex.ssl.keystore.secure_password` ([Secure](secure-settings.html "Secure
settings"))

     The password to the keystore (`reindex.ssl.keystore.path`). This setting cannot be used with `reindex.ssl.keystore.password`. 
`reindex.ssl.keystore.key_password`

     The password for the key in the keystore (`reindex.ssl.keystore.path`). Defaults to the keystore password. This setting cannot be used with `reindex.ssl.keystore.secure_key_password`. 
`reindex.ssl.keystore.secure_key_password` ([Secure](secure-settings.html
"Secure settings"))

     The password for the key in the keystore (`reindex.ssl.keystore.path`). Defaults to the keystore password. This setting cannot be used with `reindex.ssl.keystore.key_password`. 

[« Bulk API](docs-bulk.md) [Term vectors API »](docs-termvectors.md)
