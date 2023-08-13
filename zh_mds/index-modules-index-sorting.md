

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Index
modules](index-modules.md)

[« History retention](index-modules-history-retention.md) [Use index sorting
to speed up conjunctions »](index-modules-index-sorting-conjunctions.md)

## 索引排序

在 Elasticsearch 中创建新索引时，可以配置每个分片中的段的排序方式。默认情况下，Lucene 不应用任何排序。"index.sort.*"设置定义了应使用哪些字段对每个段内的文档进行排序。

嵌套字段与索引排序不兼容，因为它们依赖于嵌套文档存储在连续文档 ID 中的假设，索引排序可能会破坏这些 ID 中。如果在包含嵌套字段的索引上激活了索引排序，则会引发错误。

例如，下面的示例演示如何定义单个字段的排序：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          index: {
            "sort.field": 'date',
            "sort.order": 'desc'
          }
        },
        mappings: {
          properties: {
            date: {
              type: 'date'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "settings": {
        "index": {
          "sort.field": "date", __"sort.order": "desc" __}
      },
      "mappings": {
        "properties": {
          "date": {
            "type": "date"
          }
        }
      }
    }

__

|

此索引按"日期"字段排序 ---|--- __

|

...​按降序排列。   也可以按多个字段对索引进行排序：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          index: {
            "sort.field": [
              'username',
              'date'
            ],
            "sort.order": [
              'asc',
              'desc'
            ]
          }
        },
        mappings: {
          properties: {
            username: {
              type: 'keyword',
              doc_values: true
            },
            date: {
              type: 'date'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "settings": {
        "index": {
          "sort.field": [ "username", "date" ], __"sort.order": [ "asc", "desc" ] __}
      },
      "mappings": {
        "properties": {
          "username": {
            "type": "keyword",
            "doc_values": true
          },
          "date": {
            "type": "date"
          }
        }
      }
    }

__

|

此索引首先按"用户名"排序，然后按"日期"排序 ---|--- __

|

...​"用户名"字段按升序排列，"日期"字段按降序排列。   索引排序支持以下设置：

`index.sort.field`

     The list of fields used to sort the index. Only `boolean`, `numeric`, `date` and `keyword` fields with `doc_values` are allowed here. 
`index.sort.order`

    

要用于每个字段的排序顺序。顺序选项可以具有以下值：

* 'asc'：用于升序 * 'desc'：用于降序。

`index.sort.mode`

    

Elasticsearch 支持按多值字段排序。mode 选项控制选取用于对文档进行排序的值。mode 选项可以具有以下值：

* "min"：选择最低值。  * "max"：选择最大值。

`index.sort.missing`

    

缺少的参数指定应如何处理缺少该字段的文档。缺失值可以具有以下值：

* "_last"：没有字段值的文档最后排序。  * "_first"：没有字段值的文档首先排序。

索引排序只能在创建索引时定义一次。不允许在现有索引上添加或更新排序。索引排序在索引吞吐量方面也有成本，因为文档必须在刷新和合并时排序。在激活此功能之前，应测试对应用程序的影响。

### 提前终止搜索请求

默认情况下，在 Elasticsearch 中，搜索请求必须访问与查询匹配的每个文档，以检索按指定排序排序的排名靠前的文档。尽管当索引排序和搜索排序相同时，可以限制每个段应访问的文档数，以检索全局排名靠前的 N 个文档。例如，假设我们有一个索引，其中包含按时间戳字段排序的事件：

    
    
    response = client.indices.create(
      index: 'events',
      body: {
        settings: {
          index: {
            "sort.field": 'timestamp',
            "sort.order": 'desc'
          }
        },
        mappings: {
          properties: {
            timestamp: {
              type: 'date'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT events
    {
      "settings": {
        "index": {
          "sort.field": "timestamp",
          "sort.order": "desc" __}
      },
      "mappings": {
        "properties": {
          "timestamp": {
            "type": "date"
          }
        }
      }
    }

__

|

此索引按时间戳降序排序(最近的在前) ---|--- 您可以使用以下命令搜索最近 10 个事件：

    
    
    response = client.search(
      index: 'events',
      body: {
        size: 10,
        sort: [
          {
            timestamp: 'desc'
          }
        ]
      }
    )
    puts response
    
    
    GET /events/_search
    {
      "size": 10,
      "sort": [
        { "timestamp": "desc" }
      ]
    }

Elasticsearch 将检测到每个段的顶级文档已经在索引中排序，并且只会比较每个段的前 N 个文档。收集与查询匹配的其余文档，以计算结果总数并生成聚合。

如果您只查找最近 10 个事件，并且对与查询匹配的文档总数不感兴趣，则可以将"track_total_hits"设置为 false：

    
    
    response = client.search(
      index: 'events',
      body: {
        size: 10,
        sort: [
          {
            timestamp: 'desc'
          }
        ],
        track_total_hits: false
      }
    )
    puts response
    
    
    GET /events/_search
    {
      "size": 10,
      "sort": [ __{ "timestamp": "desc" }
      ],
      "track_total_hits": false
    }

__

|

索引排序将用于对排名靠前的文档进行排名，每个段将在前 10 个匹配项后提前终止集合。   ---|--- 这一次，Elasticsearch 不会尝试计算文档数量，并且能够在每个段收集 N 个文档后立即终止查询。

    
    
    {
      "_shards": ...
       "hits" : {  __"max_score" : null,
          "hits" : []
      },
      "took": 20,
      "timed_out": false
    }

__

|

由于提前终止，与查询匹配的命中总数未知。   ---|---聚合将收集与查询匹配的所有文档，无论"track_total_hits"的值如何

[« History retention](index-modules-history-retention.md) [Use index sorting
to speed up conjunctions »](index-modules-index-sorting-conjunctions.md)
