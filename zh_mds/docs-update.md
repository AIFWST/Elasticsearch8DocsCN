

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Document APIs](docs.md)

[« Delete by query API](docs-delete-by-query.md) [Update By Query API
»](docs-update-by-query.md)

## 更新接口

使用指定的脚本更新文档。

###Request

"发布/<index>/_update/<_id>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标索引或索引别名具有"索引"或"写入"索引权限。

###Description

使您能够编写文档更新脚本。该脚本可以更新、删除或跳过修改文档。更新 API 还支持传递部分文档，该文档将合并到现有文档中。要完全替换现有文档，请使用"索引"API。

此操作：

1. 从索引中获取文档(与分片并置)。  2. 运行指定的脚本。  3. 为结果编制索引。

文档仍必须重新编制索引，但使用"update"会删除一些网络往返，并减少 GET 和索引操作之间发生版本冲突的可能性。

必须启用"_source"字段才能使用"更新"。除了"_source"之外，您还可以通过"ctx"映射访问以下变量："_index"、"_type"、"_id"、"_version"、"_routing"和"_now"(当前时间戳)。

### 路径参数

`<index>`

     (Required, string) Name of the target index. By default, the index is created automatically if it doesn't exist. For more information, see [Automatically create data streams and indices](docs-index_.html#index-creation "Automatically create data streams and indices"). 
`<_id>`

     (Required, string) Unique identifier for the document to be updated. 

### 查询参数

`if_seq_no`

     (Optional, integer) Only perform the operation if the document has this sequence number. See [Optimistic concurrency control](docs-index_.html#optimistic-concurrency-control-index "Optimistic concurrency control"). 
`if_primary_term`

     (Optional, integer) Only perform the operation if the document has this primary term. See [Optimistic concurrency control](docs-index_.html#optimistic-concurrency-control-index "Optimistic concurrency control"). 
`lang`

     (Optional, string) The script language. Default: `painless`. 
`require_alias`

     (Optional, Boolean) If `true`, the destination must be an [index alias](aliases.html "Aliases"). Defaults to `false`. 
`refresh`

     (Optional, enum) If `true`, Elasticsearch refreshes the affected shards to make this operation visible to search, if `wait_for` then wait for a refresh to make this operation visible to search, if `false` do nothing with refreshes. Valid values: `true`, `false`, `wait_for`. Default: `false`. 
`retry_on_conflict`

     (Optional, integer) Specify how many times should the operation be retried when a conflict occurs. Default: 0. 
`routing`

     (Optional, string) Custom value used to route operations to a specific shard. 
`_source`

     (Optional, list) Set to `false` to disable source retrieval (default: `true`). You can also specify a comma-separated list of the fields you want to retrieve. 
`_source_excludes`

     (Optional, list) Specify the source fields you want to exclude. 
`_source_includes`

     (Optional, list) Specify the source fields you want to retrieve. 
`timeout`

    

(可选，时间单位)时间段等待以下操作：

* 动态映射更新 * 等待活动分片

默认为"1m"(一分钟)。这保证了 Elasticsearch 在失败之前至少等待超时。实际等待时间可能会更长，尤其是在发生多次等待时。

`wait_for_active_shards`

    

(可选，字符串)在继续操作之前必须处于活动状态的分片副本数。设置为"all"或任何正整数，最多为索引中的分片总数("number_of_replicas+1")。默认值：1，主分片。

请参阅活动分片。

###Examples

首先，让我们索引一个简单的文档：

    
    
    response = client.index(
      index: 'test',
      id: 1,
      body: {
        counter: 1,
        tags: [
          'red'
        ]
      }
    )
    puts response
    
    
    res, err := es.Index(
    	"test",
    	strings.NewReader(`{
    	  "counter": 1,
    	  "tags": [
    	    "red"
    	  ]
    	}`),
    	es.Index.WithDocumentID("1"),
    	es.Index.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    PUT test/_doc/1
    {
      "counter" : 1,
      "tags" : ["red"]
    }

若要递增计数器，可以使用以下脚本提交更新请求：

    
    
    response = client.update(
      index: 'test',
      id: 1,
      body: {
        script: {
          source: 'ctx._source.counter += params.count',
          lang: 'painless',
          params: {
            count: 4
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Update(
    	"test",
    	"1",
    	strings.NewReader(`{
    	  "script": {
    	    "source": "ctx._source.counter += params.count",
    	    "lang": "painless",
    	    "params": {
    	      "count": 4
    	    }
    	  }
    	}`),
    	es.Update.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    POST test/_update/1
    {
      "script" : {
        "source": "ctx._source.counter += params.count",
        "lang": "painless",
        "params" : {
          "count" : 4
        }
      }
    }

同样，您可以使用和更新脚本将标签添加到标签列表中(这只是一个列表，因此即使存在标签也会添加)：

    
    
    response = client.update(
      index: 'test',
      id: 1,
      body: {
        script: {
          source: 'ctx._source.tags.add(params.tag)',
          lang: 'painless',
          params: {
            tag: 'blue'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Update(
    	"test",
    	"1",
    	strings.NewReader(`{
    	  "script": {
    	    "source": "ctx._source.tags.add(params.tag)",
    	    "lang": "painless",
    	    "params": {
    	      "tag": "blue"
    	    }
    	  }
    	}`),
    	es.Update.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    POST test/_update/1
    {
      "script": {
        "source": "ctx._source.tags.add(params.tag)",
        "lang": "painless",
        "params": {
          "tag": "blue"
        }
      }
    }

您还可以从标签列表中删除标签。用于"删除"标签的 Painless 函数采用要删除的元素的数组索引。为避免可能的运行时错误，您首先需要确保标记存在。如果列表包含标记的重复项，则此脚本只会删除一个匹配项。

    
    
    response = client.update(
      index: 'test',
      id: 1,
      body: {
        script: {
          source: 'if (ctx._source.tags.contains(params.tag)) { ctx._source.tags.remove(ctx._source.tags.indexOf(params.tag)) }',
          lang: 'painless',
          params: {
            tag: 'blue'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Update(
    	"test",
    	"1",
    	strings.NewReader(`{
    	  "script": {
    	    "source": "if (ctx._source.tags.contains(params.tag)) { ctx._source.tags.remove(ctx._source.tags.indexOf(params.tag)) }",
    	    "lang": "painless",
    	    "params": {
    	      "tag": "blue"
    	    }
    	  }
    	}`),
    	es.Update.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    POST test/_update/1
    {
      "script": {
        "source": "if (ctx._source.tags.contains(params.tag)) { ctx._source.tags.remove(ctx._source.tags.indexOf(params.tag)) }",
        "lang": "painless",
        "params": {
          "tag": "blue"
        }
      }
    }

您还可以在文档中添加和删除字段。例如，此脚本添加字段"new_field"：

    
    
    response = client.update(
      index: 'test',
      id: 1,
      body: {
        script: "ctx._source.new_field = 'value_of_new_field'"
      }
    )
    puts response
    
    
    res, err := es.Update(
    	"test",
    	"1",
    	strings.NewReader(`{
    	  "script": "ctx._source.new_field = 'value_of_new_field'"
    	}`),
    	es.Update.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    POST test/_update/1
    {
      "script" : "ctx._source.new_field = 'value_of_new_field'"
    }

相反，此脚本删除字段"new_field"：

    
    
    response = client.update(
      index: 'test',
      id: 1,
      body: {
        script: "ctx._source.remove('new_field')"
      }
    )
    puts response
    
    
    res, err := es.Update(
    	"test",
    	"1",
    	strings.NewReader(`{
    	  "script": "ctx._source.remove('new_field')"
    	}`),
    	es.Update.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    POST test/_update/1
    {
      "script" : "ctx._source.remove('new_field')"
    }

以下脚本从对象字段中删除子字段：

    
    
    response = client.update(
      index: 'test',
      id: 1,
      body: {
        script: "ctx._source['my-object'].remove('my-subfield')"
      }
    )
    puts response
    
    
    POST test/_update/1
    {
      "script": "ctx._source['my-object'].remove('my-subfield')"
    }

除了更新文档，您还可以更改从脚本中执行的操作。例如，如果"标签"字段包含"绿色"，则此请求将删除文档，否则它不执行任何操作("noop")：

    
    
    response = client.update(
      index: 'test',
      id: 1,
      body: {
        script: {
          source: "if (ctx._source.tags.contains(params.tag)) { ctx.op = 'delete' } else { ctx.op = 'noop' }",
          lang: 'painless',
          params: {
            tag: 'green'
          }
        }
      }
    )
    puts response
    
    
    POST test/_update/1
    {
      "script": {
        "source": "if (ctx._source.tags.contains(params.tag)) { ctx.op = 'delete' } else { ctx.op = 'noop' }",
        "lang": "painless",
        "params": {
          "tag": "green"
        }
      }
    }

##### 更新文档的一部分

以下部分更新向现有文档添加新字段：

    
    
    response = client.update(
      index: 'test',
      id: 1,
      body: {
        doc: {
          name: 'new_name'
        }
      }
    )
    puts response
    
    
    res, err := es.Update(
    	"test",
    	"1",
    	strings.NewReader(`{
    	  "doc": {
    	    "name": "new_name"
    	  }
    	}`),
    	es.Update.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    POST test/_update/1
    {
      "doc": {
        "name": "new_name"
      }
    }

如果同时指定了"doc"和"script"，则忽略"doc"。如果指定脚本化更新，请在脚本中包含要更新的字段。

##### 检测 noopupdates

默认情况下，不更改任何内容的更新会检测到它们不会更改任何内容并返回"结果"："noop"：

    
    
    response = client.update(
      index: 'test',
      id: 1,
      body: {
        doc: {
          name: 'new_name'
        }
      }
    )
    puts response
    
    
    res, err := es.Update(
    	"test",
    	"1",
    	strings.NewReader(`{
    	  "doc": {
    	    "name": "new_name"
    	  }
    	}`),
    	es.Update.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    POST test/_update/1
    {
      "doc": {
        "name": "new_name"
      }
    }

如果"name"的值已经是"new_name"，则忽略更新请求，响应中的"result"元素返回"noop"：

    
    
    {
       "_shards": {
            "total": 0,
            "successful": 0,
            "failed": 0
       },
       "_index": "test",
       "_id": "1",
       "_version": 2,
       "_primary_term": 1,
       "_seq_no": 1,
       "result": "noop"
    }

您可以通过设置"detect_noop"：false"来禁用此行为：

    
    
    response = client.update(
      index: 'test',
      id: 1,
      body: {
        doc: {
          name: 'new_name'
        },
        detect_noop: false
      }
    )
    puts response
    
    
    res, err := es.Update(
    	"test",
    	"1",
    	strings.NewReader(`{
    	  "doc": {
    	    "name": "new_name"
    	  },
    	  "detect_noop": false
    	}`),
    	es.Update.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    POST test/_update/1
    {
      "doc": {
        "name": "new_name"
      },
      "detect_noop": false
    }

#####Upsert

如果文档尚不存在，则"upsert"元素的内容将作为新文档插入。如果文档存在，则执行"脚本"：

    
    
    response = client.update(
      index: 'test',
      id: 1,
      body: {
        script: {
          source: 'ctx._source.counter += params.count',
          lang: 'painless',
          params: {
            count: 4
          }
        },
        upsert: {
          counter: 1
        }
      }
    )
    puts response
    
    
    res, err := es.Update(
    	"test",
    	"1",
    	strings.NewReader(`{
    	  "script": {
    	    "source": "ctx._source.counter += params.count",
    	    "lang": "painless",
    	    "params": {
    	      "count": 4
    	    }
    	  },
    	  "upsert": {
    	    "counter": 1
    	  }
    	}`),
    	es.Update.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    POST test/_update/1
    {
      "script": {
        "source": "ctx._source.counter += params.count",
        "lang": "painless",
        "params": {
          "count": 4
        }
      },
      "upsert": {
        "counter": 1
      }
    }

##### 脚本化插入

要运行脚本，无论文档是否存在，请将"scripted_upsert"设置为"true"：

    
    
    response = client.update(
      index: 'test',
      id: 1,
      body: {
        scripted_upsert: true,
        script: {
          source: "\n      if ( ctx.op == 'create' ) {\n        ctx._source.counter = params.count\n      } else {\n        ctx._source.counter += params.count\n      }\n    ",
          params: {
            count: 4
          }
        },
        upsert: {}
      }
    )
    puts response
    
    
    POST test/_update/1
    {
      "scripted_upsert": true,
      "script": {
        "source": """
          if ( ctx.op == 'create' ) {
            ctx._source.counter = params.count
          } else {
            ctx._source.counter += params.count
          }
        """,
        "params": {
          "count": 4
        }
      },
      "upsert": {}
    }

##### Doc asupsert

您可以将"doc_as_upsert"设置为"true"以使用"doc"的内容作为"upsert"值，而不是发送部分"文档"和"更新插入"文档：

    
    
    response = client.update(
      index: 'test',
      id: 1,
      body: {
        doc: {
          name: 'new_name'
        },
        doc_as_upsert: true
      }
    )
    puts response
    
    
    res, err := es.Update(
    	"test",
    	"1",
    	strings.NewReader(`{
    	  "doc": {
    	    "name": "new_name"
    	  },
    	  "doc_as_upsert": true
    	}`),
    	es.Update.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    POST test/_update/1
    {
      "doc": {
        "name": "new_name"
      },
      "doc_as_upsert": true
    }

不支持将引入管道与"doc_as_upsert"一起使用。

[« Delete by query API](docs-delete-by-query.md) [Update By Query API
»](docs-update-by-query.md)
