

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Update index settings API](indices-update-settings.md) [Index lifecycle
management APIs »](index-lifecycle-management-api.md)

## 更新映射接口

向现有数据流或索引添加新字段。您还可以使用此 API 更改现有字段的搜索设置。

对于数据流，默认情况下，这些更改将应用于所有后备索引。

    
    
    response = client.indices.put_mapping(
      index: 'my-index-000001',
      body: {
        properties: {
          email: {
            type: 'keyword'
          }
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001/_mapping
    {
      "properties": {
        "email": {
          "type": "keyword"
        }
      }
    }

###Request

"放 /<target>/_mapping"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"管理"索引权限。

[7.9] 在 7.9 中已弃用。 如果请求以索引或索引别名为目标，您还可以使用"创建"、"create_doc"、"索引"或"写入"索引权限更新其映射。

### 路径参数

`<target>`

     (Required, string) Comma-separated list of data streams, indices, and aliases used to limit the request. Supports wildcards (`*`). To target all data streams and indices, omit this parameter or use `*` or `_all`. 

### 查询参数

`allow_no_indices`

    

(可选，布尔值)如果为"false"，则当任何通配符表达式、索引别名或"_all"值仅针对缺少或关闭的索引时，请求将返回错误。即使请求以其他打开的索引为目标，此行为也适用。例如，如果索引以"foo"开头但没有索引以"bar"开头，则以"foo*，bar*"为目标的请求将返回错误。

默认为"假"。

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
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`write_index_only`

     (Optional, Boolean) If `true`, the mappings are applied only to the current write index for the target. Defaults to `false`. 

### 请求正文

`properties`

    

(必需，映射对象)字段的映射。对于新字段，此映射可以包括：

* 字段名称 * 字段数据类型 * 映射参数

对于现有字段，请参阅更改现有字段的映射。

###Examples

#### 单目标示例

更新映射 API 需要现有的数据流或索引。以下创建索引 API请求创建没有映射的"发布"索引。

    
    
    $params = [
        'index' => 'publications',
    ];
    $response = $client->indices()->create($params);
    
    
    resp = client.indices.create(index="publications")
    print(resp)
    
    
    response = client.indices.create(
      index: 'publications'
    )
    puts response
    
    
    res, err := es.Indices.Create("publications")
    fmt.Println(res, err)
    
    
    const response = await client.indices.create({
      index: 'publications'
    })
    console.log(response)
    
    
    PUT /publications

以下更新映射 API 请求将"标题"(一个新的"文本"字段)添加到"发布"索引。

    
    
    $params = [
        'index' => 'publications',
        'body' => [
            'properties' => [
                'title' => [
                    'type' => 'text',
                ],
            ],
        ],
    ];
    $response = $client->indices()->putMapping($params);
    
    
    resp = client.indices.put_mapping(
        index="publications", body={"properties": {"title": {"type": "text"}}},
    )
    print(resp)
    
    
    response = client.indices.put_mapping(
      index: 'publications',
      body: {
        properties: {
          title: {
            type: 'text'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.PutMapping(
    	[]string{"publications"},
    	strings.NewReader(`{
    	  "properties": {
    	    "title": {
    	      "type": "text"
    	    }
    	  }
    	}`),
    )
    fmt.Println(res, err)
    
    
    const response = await client.indices.putMapping({
      index: 'publications',
      body: {
        properties: {
          title: {
            type: 'text'
          }
        }
      }
    })
    console.log(response)
    
    
    PUT /publications/_mapping
    {
      "properties": {
        "title":  { "type": "text"}
      }
    }

#### 多个目标

更新映射 API 可以通过单个请求应用于多个数据流或索引。例如，您可以同时更新"my-index-000001"和"my-index-000002"索引的映射：

    
    
    response = client.indices.create(
      index: 'my-index-000001'
    )
    puts response
    
    response = client.indices.create(
      index: 'my-index-000002'
    )
    puts response
    
    response = client.indices.put_mapping(
      index: 'my-index-000001,my-index-000002',
      body: {
        properties: {
          user: {
            properties: {
              name: {
                type: 'keyword'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    # Create the two indices
    PUT /my-index-000001
    PUT /my-index-000002
    
    # Update both mappings
    PUT /my-index-000001,my-index-000002/_mapping
    {
      "properties": {
        "user": {
          "properties": {
            "name": {
              "type": "keyword"
            }
          }
        }
      }
    }

#### 向现有对象字段添加新属性

您可以使用更新映射 API 向现有"对象"字段添加新属性。若要了解其工作原理，请尝试以下示例。

使用创建索引 API 创建具有"name"对象字段和内部"第一个"文本字段的索引。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            name: {
              properties: {
                first: {
                  type: 'text'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.Create(
    	"my-index-000001",
    	es.Indices.Create.WithBody(strings.NewReader(`{
    	  "mappings": {
    	    "properties": {
    	      "name": {
    	        "properties": {
    	          "first": {
    	            "type": "text"
    	          }
    	        }
    	      }
    	    }
    	  }
    	}`)),
    )
    fmt.Println(res, err)
    
    
    PUT /my-index-000001
    {
      "mappings": {
        "properties": {
          "name": {
            "properties": {
              "first": {
                "type": "text"
              }
            }
          }
        }
      }
    }

使用更新映射 API 将新的内部"最后一个"文本字段添加到"名称"字段。

    
    
    response = client.indices.put_mapping(
      index: 'my-index-000001',
      body: {
        properties: {
          name: {
            properties: {
              last: {
                type: 'text'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.PutMapping(
    	[]string{"my-index-000001"},
    	strings.NewReader(`{
    	  "properties": {
    	    "name": {
    	      "properties": {
    	        "last": {
    	          "type": "text"
    	        }
    	      }
    	    }
    	  }
    	}`),
    )
    fmt.Println(res, err)
    
    
    PUT /my-index-000001/_mapping
    {
      "properties": {
        "name": {
          "properties": {
            "last": {
              "type": "text"
            }
          }
        }
      }
    }

#### 向现有字段添加多字段

多字段允许您以不同的方式为同一字段编制索引。您可以使用更新映射 API 更新"字段"映射参数，并为现有字段启用多字段。

如果在添加多字段时索引(或数据流)包含文档，则这些文档将没有新多字段的值。您可以使用按查询更新 API 填充新的多字段。

若要了解其工作原理，请尝试以下示例。

使用创建索引 API 创建包含"城市"文本字段的索引。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            city: {
              type: 'text'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.Create(
    	"my-index-000001",
    	es.Indices.Create.WithBody(strings.NewReader(`{
    	  "mappings": {
    	    "properties": {
    	      "city": {
    	        "type": "text"
    	      }
    	    }
    	  }
    	}`)),
    )
    fmt.Println(res, err)
    
    
    PUT /my-index-000001
    {
      "mappings": {
        "properties": {
          "city": {
            "type": "text"
          }
        }
      }
    }

虽然文本字段适用于全文搜索，但不会分析关键字字段，并且可能更适合排序或聚合。

使用更新映射 API 为"城市"字段启用多字段。此请求添加了"city.raw"关键字多字段，可用于排序。

    
    
    response = client.indices.put_mapping(
      index: 'my-index-000001',
      body: {
        properties: {
          city: {
            type: 'text',
            fields: {
              raw: {
                type: 'keyword'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.PutMapping(
    	[]string{"my-index-000001"},
    	strings.NewReader(`{
    	  "properties": {
    	    "city": {
    	      "type": "text",
    	      "fields": {
    	        "raw": {
    	          "type": "keyword"
    	        }
    	      }
    	    }
    	  }
    	}`),
    )
    fmt.Println(res, err)
    
    
    PUT /my-index-000001/_mapping
    {
      "properties": {
        "city": {
          "type": "text",
          "fields": {
            "raw": {
              "type": "keyword"
            }
          }
        }
      }
    }

#### 更改现有字段支持的映射参数

每个映射参数的文档指示是否可以使用更新映射 API 为现有字段更新它。例如，可以使用更新映射 API 更新"ignore_above"参数。

若要了解其工作原理，请尝试以下示例。

使用创建索引 API 创建包含"user_id"关键字字段的索引。"user_id"字段的"ignore_above"参数值为"20"。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            user_id: {
              type: 'keyword',
              ignore_above: 20
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.Create(
    	"my-index-000001",
    	es.Indices.Create.WithBody(strings.NewReader(`{
    	  "mappings": {
    	    "properties": {
    	      "user_id": {
    	        "type": "keyword",
    	        "ignore_above": 20
    	      }
    	    }
    	  }
    	}`)),
    )
    fmt.Println(res, err)
    
    
    PUT /my-index-000001
    {
      "mappings": {
        "properties": {
          "user_id": {
            "type": "keyword",
            "ignore_above": 20
          }
        }
      }
    }

使用更新映射 API 将"ignore_above"参数值更改为"100"。

    
    
    response = client.indices.put_mapping(
      index: 'my-index-000001',
      body: {
        properties: {
          user_id: {
            type: 'keyword',
            ignore_above: 100
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.PutMapping(
    	[]string{"my-index-000001"},
    	strings.NewReader(`{
    	  "properties": {
    	    "user_id": {
    	      "type": "keyword",
    	      "ignore_above": 100
    	    }
    	  }
    	}`),
    )
    fmt.Println(res, err)
    
    
    PUT /my-index-000001/_mapping
    {
      "properties": {
        "user_id": {
          "type": "keyword",
          "ignore_above": 100
        }
      }
    }

#### 更改现有字段的映射

除支持的映射参数外，您无法更改现有字段的映射或字段类型。更改现有字段可能会使已编制索引的数据无效。

如果需要更改数据流的 backingindex 中字段的映射，请参阅更改数据流的映射和设置。

如果需要更改其他索引中字段的映射，请使用正确的映射创建一个新索引，并将数据重新索引到该索引中。

若要了解如何更改索引中现有字段的映射，请尝试以下示例。

使用创建索引 API 创建具有"user_id"字段和"long"字段类型的索引。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            user_id: {
              type: 'long'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001
    {
      "mappings" : {
        "properties": {
          "user_id": {
            "type": "long"
          }
        }
      }
    }

使用索引 API 为多个具有"user_id"字段值的文档编制索引。

    
    
    response = client.index(
      index: 'my-index-000001',
      refresh: 'wait_for',
      body: {
        user_id: 12_345
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      refresh: 'wait_for',
      body: {
        user_id: 12_346
      }
    )
    puts response
    
    
    POST /my-index-000001/_doc?refresh=wait_for
    {
      "user_id" : 12345
    }
    
    POST /my-index-000001/_doc?refresh=wait_for
    {
      "user_id" : 12346
    }

要将"user_id"字段更改为"关键字"字段类型，请使用创建索引 API 创建具有正确映射的新索引。

    
    
    response = client.indices.create(
      index: 'my-new-index-000001',
      body: {
        mappings: {
          properties: {
            user_id: {
              type: 'keyword'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /my-new-index-000001
    {
      "mappings" : {
        "properties": {
          "user_id": {
            "type": "keyword"
          }
        }
      }
    }

使用重新索引 API 将文档从旧索引复制到新索引。

    
    
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
    
    
    POST /_reindex
    {
      "source": {
        "index": "my-index-000001"
      },
      "dest": {
        "index": "my-new-index-000001"
      }
    }

#### 重命名字段

重命名字段将使已在旧字段名称下编制索引的数据无效。相反，添加"别名"字段以创建备用字段名称。

例如，使用创建索引 API 创建包含"user_identifier"字段的索引。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            user_identifier: {
              type: 'keyword'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.Create(
    	"my-index-000001",
    	es.Indices.Create.WithBody(strings.NewReader(`{
    	  "mappings": {
    	    "properties": {
    	      "user_identifier": {
    	        "type": "keyword"
    	      }
    	    }
    	  }
    	}`)),
    )
    fmt.Println(res, err)
    
    
    PUT /my-index-000001
    {
      "mappings": {
        "properties": {
          "user_identifier": {
            "type": "keyword"
          }
        }
      }
    }

使用更新映射 API 为现有"user_identifier"字段添加"user_id"字段别名。

    
    
    response = client.indices.put_mapping(
      index: 'my-index-000001',
      body: {
        properties: {
          user_id: {
            type: 'alias',
            path: 'user_identifier'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.PutMapping(
    	[]string{"my-index-000001"},
    	strings.NewReader(`{
    	  "properties": {
    	    "user_id": {
    	      "type": "alias",
    	      "path": "user_identifier"
    	    }
    	  }
    	}`),
    )
    fmt.Println(res, err)
    
    
    PUT /my-index-000001/_mapping
    {
      "properties": {
        "user_id": {
          "type": "alias",
          "path": "user_identifier"
        }
      }
    }

[« Update index settings API](indices-update-settings.md) [Index lifecycle
management APIs »](index-lifecycle-management-api.md)
