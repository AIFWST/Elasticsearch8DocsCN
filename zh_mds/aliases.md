

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)

[« User agent processor](user-agent-processor.md) [Search your data
»](search-your-data.md)

#Aliases

别名是一组数据流或索引的辅助名称。MostElasticsearch API接受别名代替数据流或索引名称。

您可以随时更改别名的数据流或索引。如果您在应用程序的 Elasticsearch 请求中使用别名，则可以在不停机或更改应用程序代码的情况下重新索引数据。

### 别名类型

有两种类型的别名：

* 数据流别名指向一个或多个数据流。  * 索引别名指向一个或多个索引。

别名不能同时指向数据流和索引。您也不能将数据流的支持索引添加到索引别名。

### 添加别名

要将现有数据流或索引添加到别名，请使用别名API的"添加"操作。如果别名不存在，请求将创建它。

    
    
    response = client.indices.update_aliases(
      body: {
        actions: [
          {
            add: {
              index: 'logs-nginx.access-prod',
              alias: 'logs'
            }
          }
        ]
      }
    )
    puts response
    
    
    POST _aliases
    {
      "actions": [
        {
          "add": {
            "index": "logs-nginx.access-prod",
            "alias": "logs"
          }
        }
      ]
    }

API 的"索引"和"索引"参数支持通配符 ("*")。同时匹配数据流和索引的通配符模式返回错误。

    
    
    POST _aliases
    {
      "actions": [
        {
          "add": {
            "index": "logs-*",
            "alias": "logs"
          }
        }
      ]
    }

### 删除别名

要删除别名，请使用别名 API 的"删除"操作。

    
    
    response = client.indices.update_aliases(
      body: {
        actions: [
          {
            remove: {
              index: 'logs-nginx.access-prod',
              alias: 'logs'
            }
          }
        ]
      }
    )
    puts response
    
    
    POST _aliases
    {
      "actions": [
        {
          "remove": {
            "index": "logs-nginx.access-prod",
            "alias": "logs"
          }
        }
      ]
    }

### 多重操作

您可以使用别名 API 在单个原子操作中执行多个操作。

例如，"logs"别名指向单个数据流。以下请求将流交换为别名。在此交换期间，"logs"别名没有停机时间，并且永远不会同时指向两个流。

    
    
    response = client.indices.update_aliases(
      body: {
        actions: [
          {
            remove: {
              index: 'logs-nginx.access-prod',
              alias: 'logs'
            }
          },
          {
            add: {
              index: 'logs-my_app-default',
              alias: 'logs'
            }
          }
        ]
      }
    )
    puts response
    
    
    POST _aliases
    {
      "actions": [
        {
          "remove": {
            "index": "logs-nginx.access-prod",
            "alias": "logs"
          }
        },
        {
          "add": {
            "index": "logs-my_app-default",
            "alias": "logs"
          }
        }
      ]
    }

### 在创建索引时添加别名

您还可以使用组件或索引模板在创建索引或数据流别名时添加它们。

    
    
    # Component template with index aliases
    PUT _component_template/my-aliases
    {
      "template": {
        "aliases": {
          "my-alias": {}
        }
      }
    }
    
    # Index template with index aliases
    PUT _index_template/my-index-template
    {
      "index_patterns": [
        "my-index-*"
      ],
      "composed_of": [
        "my-aliases",
        "my-mappings",
        "my-settings"
      ],
      "template": {
        "aliases": {
          "yet-another-alias": {}
        }
      }
    }

您还可以在创建索引 API 请求中指定索引别名。

    
    
    response = client.indices.create(
      index: '<my-index-{now/d}-000001>',
      body: {
        aliases: {
          "my-alias": {}
        }
      }
    )
    puts response
    
    
    # PUT <my-index-{now/d}-000001>
    PUT %3Cmy-index-%7Bnow%2Fd%7D-000001%3E
    {
      "aliases": {
        "my-alias": {}
      }
    }

### 视图别名

要获取集群别名的列表，请使用不带参数的获取别名 API。

    
    
    response = client.indices.get_alias
    puts response
    
    
    GET _alias

在"_alias"之前指定数据流或索引以查看其别名。

    
    
    response = client.indices.get_alias(
      index: 'my-data-stream'
    )
    puts response
    
    
    GET my-data-stream/_alias

在"_alias"后指定别名以查看其数据流或索引。

    
    
    response = client.indices.get_alias(
      name: 'logs'
    )
    puts response
    
    
    GET _alias/logs

### 写入索引

您可以使用"is_write_index"为别名指定写入索引或数据流。Elasticsearch 将别名的任何写入请求路由到此索引或数据流。

    
    
    response = client.indices.update_aliases(
      body: {
        actions: [
          {
            add: {
              index: 'logs-nginx.access-prod',
              alias: 'logs'
            }
          },
          {
            add: {
              index: 'logs-my_app-default',
              alias: 'logs',
              is_write_index: true
            }
          }
        ]
      }
    )
    puts response
    
    
    POST _aliases
    {
      "actions": [
        {
          "add": {
            "index": "logs-nginx.access-prod",
            "alias": "logs"
          }
        },
        {
          "add": {
            "index": "logs-my_app-default",
            "alias": "logs",
            "is_write_index": true
          }
        }
      ]
    }

如果别名指向多个索引或数据流，并且未设置"is_write_index"，则该别名将拒绝写入请求。如果索引别名指向 oneindex 并且未设置"is_write_index"，则该索引会自动充当写入索引。数据流别名不会自动设置写入数据流，即使别名指向一个数据流也是如此。

建议使用数据流来存储仅追加时序数据。如果您经常更新或删除现有时序数据，请改用带有写入索引的索引别名。请参阅在没有数据流的情况下管理时序数据。

### 筛选别名

"过滤器"选项使用查询 DSL 来限制别名可以访问的文档。

    
    
    response = client.indices.update_aliases(
      body: {
        actions: [
          {
            add: {
              index: 'my-index-2099.05.06-000001',
              alias: 'my-alias',
              filter: {
                bool: {
                  filter: [
                    {
                      range: {
                        "@timestamp": {
                          gte: 'now-1d/d',
                          lt: 'now/d'
                        }
                      }
                    },
                    {
                      term: {
                        "user.id": 'kimchy'
                      }
                    }
                  ]
                }
              }
            }
          }
        ]
      }
    )
    puts response
    
    
    POST _aliases
    {
      "actions": [
        {
          "add": {
            "index": "my-index-2099.05.06-000001",
            "alias": "my-alias",
            "filter": {
              "bool": {
                "filter": [
                  {
                    "range": {
                      "@timestamp": {
                        "gte": "now-1d/d",
                        "lt": "now/d"
                      }
                    }
                  },
                  {
                    "term": {
                      "user.id": "kimchy"
                    }
                  }
                ]
              }
            }
          }
        }
      ]
    }

###Routing

使用"路由"选项将别名请求路由到特定分片。这使您可以利用分片缓存来加快搜索速度。数据流别名不支持路由选项。

    
    
    response = client.indices.update_aliases(
      body: {
        actions: [
          {
            add: {
              index: 'my-index-2099.05.06-000001',
              alias: 'my-alias',
              routing: '1'
            }
          }
        ]
      }
    )
    puts response
    
    
    POST _aliases
    {
      "actions": [
        {
          "add": {
            "index": "my-index-2099.05.06-000001",
            "alias": "my-alias",
            "routing": "1"
          }
        }
      ]
    }

使用"index_routing"和"search_routing"为索引和搜索指定不同的路由值。如果指定，这些选项将覆盖其各自操作的"路由"值。

    
    
    response = client.indices.update_aliases(
      body: {
        actions: [
          {
            add: {
              index: 'my-index-2099.05.06-000001',
              alias: 'my-alias',
              search_routing: '1',
              index_routing: '2'
            }
          }
        ]
      }
    )
    puts response
    
    
    POST _aliases
    {
      "actions": [
        {
          "add": {
            "index": "my-index-2099.05.06-000001",
            "alias": "my-alias",
            "search_routing": "1",
            "index_routing": "2"
          }
        }
      ]
    }

[« User agent processor](user-agent-processor.md) [Search your data
»](search-your-data.md)
