

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Close index API](indices-close.md) [Create or update alias API
»](indices-add-alias.md)

## 创建索引接口

创建新索引。

    
    
    response = client.indices.create(
      index: 'my-index-000001'
    )
    puts response
    
    
    PUT /my-index-000001

###Request

'放/<index>'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则必须对目标索引具有"create_index"或"管理"索引权限。要将索引添加到别名，您必须具有别名的"管理"索引权限。

###Description

您可以使用创建索引 API 向 Elasticsearchcluster 添加新索引。创建索引时，可以指定以下内容：

* 索引设置 * 索引中字段的映射 * 索引别名

### 路径参数

`<index>`

    

(必需，字符串)要创建的索引的名称。

索引名称必须满足以下条件：

* 仅限小写 * 不能包含 '\'， '/'， '*'， '？''， '<'， '>'， '|'， ' ' (空格字符)， '，'， '#' * 7.0 之前的索引可能包含冒号 ('：')，但该冒号已被弃用，在 7.0+ 中不受支持 * 不能以 '-'、'_'、'+' 开头 * 不能是 '." 或 '..' * 不能超过 255 字节(注意是字节，因此多字节字符将更快地计入 255 限制) * 不推荐使用以 '." 开头的名称，隐藏索引和插件管理的内部索引除外

### 查询参数

`wait_for_active_shards`

    

(可选，字符串)在继续操作之前必须处于活动状态的分片副本数。设置为"all"或任何正整数，最多为索引中的分片总数("number_of_replicas+1")。默认值：1，主分片。

请参阅活动分片。

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 请求正文

`aliases`

    

(可选，对象的对象)索引的别名。

"别名"对象的属性

`<alias>`

    

(必填，对象)键是别名。索引别名支持日期数学。

对象正文包含别名的选项。支持空对象。

""的属性<alias>

`filter`

     (Optional, [Query DSL object](query-dsl.html "Query DSL")) Query used to limit documents the alias can access. 
`index_routing`

     (Optional, string) Value used to route indexing operations to a specific shard. If specified, this overwrites the `routing` value for indexing operations. 
`is_hidden`

     (Optional, Boolean) If `true`, the alias is [hidden](api-conventions.html#multi-hidden "Hidden data streams and indices"). Defaults to `false`. All indices for the alias must have the same `is_hidden` value. 
`is_write_index`

     (Optional, Boolean) If `true`, the index is the [write index](aliases.html#write-index "Write index") for the alias. Defaults to `false`. 
`routing`

     (Optional, string) Value used to route indexing and search operations to a specific shard. 
`search_routing`

     (Optional, string) Value used to route search operations to a specific shard. If specified, this overwrites the `routing` value for search operations. 

`mappings`

    

(可选，映射对象)索引中字段的映射。如果指定，此映射可以包括：

* 字段名称 * 字段数据类型 * 映射参数

请参阅映射。

`settings`

     (Optional, [index setting object](index-modules.html#index-modules-settings "Index Settings")) Configuration options for the index. See [Index Settings](index-modules.html#index-modules-settings "Index Settings"). 

###Examples

#### 索引设置

创建的每个索引都可以具有与之关联的特定设置，这些设置在正文中定义：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          index: {
            number_of_shards: 3,
            number_of_replicas: 2
          }
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001
    {
      "settings": {
        "index": {
          "number_of_shards": 3,  __"number_of_replicas": 2 __}
      }
    }

__

|

"number_of_shards"的默认值为 1 ---|--- __

|

"number_of_replicas"的默认值为 1(即每个主分片一个副本)或更简化

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          number_of_shards: 3,
          number_of_replicas: 2
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001
    {
      "settings": {
        "number_of_shards": 3,
        "number_of_replicas": 2
      }
    }

您不必在"设置"部分中明确指定"索引"部分。

有关创建索引时可以设置的所有不同索引级别设置的更多信息，请查看索引模块部分。

####Mappings

创建索引 API 允许提供映射定义：

    
    
    response = client.indices.create(
      index: 'test',
      body: {
        settings: {
          number_of_shards: 1
        },
        mappings: {
          properties: {
            "field1": {
              type: 'text'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.Create(
    	"test",
    	es.Indices.Create.WithBody(strings.NewReader(`{
    	  "settings": {
    	    "number_of_shards": 1
    	  },
    	  "mappings": {
    	    "properties": {
    	      "field1": {
    	        "type": "text"
    	      }
    	    }
    	  }
    	}`)),
    )
    fmt.Println(res, err)
    
    
    PUT /test
    {
      "settings": {
        "number_of_shards": 1
      },
      "mappings": {
        "properties": {
          "field1": { "type": "text" }
        }
      }
    }

####Aliases

创建索引 API 还允许提供一组别名：

    
    
    response = client.indices.create(
      index: 'test',
      body: {
        aliases: {
          "alias_1": {},
          "alias_2": {
            filter: {
              term: {
                "user.id": 'kimchy'
              }
            },
            routing: 'shard-1'
          }
        }
      }
    )
    puts response
    
    
    PUT /test
    {
      "aliases": {
        "alias_1": {},
        "alias_2": {
          "filter": {
            "term": { "user.id": "kimchy" }
          },
          "routing": "shard-1"
        }
      }
    }

索引别名还支持日期数学。

    
    
    response = client.indices.create(
      index: 'logs',
      body: {
        aliases: {
          "<logs_{now/M}>": {}
        }
      }
    )
    puts response
    
    
    PUT /logs
    {
      "aliases": {
        "<logs_{now/M}>": {}
      }
    }

#### 等待活动分片

默认情况下，索引创建仅在每个分片的主副本已启动或请求超时时向客户端返回响应。索引创建响应将指示发生的情况：

    
    
    {
      "acknowledged": true,
      "shards_acknowledged": true,
      "index": "logs"
    }

"已确认"表示索引是否已在集群中成功创建，而"shards_acknowledged"表示在超时之前是否为索引中的每个分片启动了必要数量的分片副本。请注意，"已确认"或"shards_acknowledged"仍可能为"假"，但索引创建成功。这些值简单地指示操作是否在超时之前完成。如果"aknowledged"是"false"，那么我们在使用新创建的索引更新集群状态之前超时，但它可能很快就会被创建。如果 'shards_acknowledged' 是 'false'，那么我们在启动必要数量的分片之前超时(默认情况下只是主分片)，即使集群状态已成功更新以反映新创建的索引(即 'acknowledged=true')。

我们可以通过索引设置"index.write.wait_for_active_shards"更改仅等待主分片启动的默认值(请注意，更改此设置也会影响所有后续写入操作的"wait_for_active_shards"值)：

    
    
    response = client.indices.create(
      index: 'test',
      body: {
        settings: {
          "index.write.wait_for_active_shards": '2'
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.Create(
    	"test",
    	es.Indices.Create.WithBody(strings.NewReader(`{
    	  "settings": {
    	    "index.write.wait_for_active_shards": "2"
    	  }
    	}`)),
    )
    fmt.Println(res, err)
    
    
    PUT /test
    {
      "settings": {
        "index.write.wait_for_active_shards": "2"
      }
    }

或通过请求参数"wait_for_active_shards"：

    
    
    $params = [
        'index' => 'test',
    ];
    $response = $client->indices()->create($params);
    
    
    resp = client.indices.create(index="test", wait_for_active_shards="2")
    print(resp)
    
    
    response = client.indices.create(
      index: 'test',
      wait_for_active_shards: 2
    )
    puts response
    
    
    res, err := es.Indices.Create("test?wait_for_active_shards=2")
    fmt.Println(res, err)
    
    
    const response = await client.indices.create({
      index: 'test',
      wait_for_active_shards: '2'
    })
    console.log(response)
    
    
    PUT /test?wait_for_active_shards=2

可以在此处找到"wait_for_active_shards"及其可能值的详细说明。

[« Close index API](indices-close.md) [Create or update alias API
»](indices-add-alias.md)
