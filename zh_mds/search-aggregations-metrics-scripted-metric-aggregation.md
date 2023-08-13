

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« Rate aggregation](search-aggregations-metrics-rate-aggregation.md) [Stats
aggregation »](search-aggregations-metrics-stats-aggregation.md)

## 脚本化指标聚合

使用脚本执行以提供指标输出的指标聚合。

使用脚本可能会导致搜索速度变慢。请参阅脚本、缓存和搜索速度。

Example:

    
    
    response = client.search(
      index: 'ledger',
      size: 0,
      body: {
        query: {
          match_all: {}
        },
        aggregations: {
          profit: {
            scripted_metric: {
              init_script: 'state.transactions = []',
              map_script: "state.transactions.add(doc.type.value == 'sale' ? doc.amount.value : -1 * doc.amount.value)",
              combine_script: 'double profit = 0; for (t in state.transactions) { profit += t } return profit',
              reduce_script: 'double profit = 0; for (a in states) { profit += a } return profit'
            }
          }
        }
      }
    )
    puts response
    
    
    POST ledger/_search?size=0
    {
      "query": {
        "match_all": {}
      },
      "aggs": {
        "profit": {
          "scripted_metric": {
            "init_script": "state.transactions = []", __"map_script": "state.transactions.add(doc.type.value == 'sale' ? doc.amount.value : -1 * doc.amount.value)",
            "combine_script": "double profit = 0; for (t in state.transactions) { profit += t } return profit",
            "reduce_script": "double profit = 0; for (a in states) { profit += a } return profit"
          }
        }
      }
    }

__

|

"init_script"是一个可选参数，所有其他脚本都是必需的。   ---|--- 上面的聚合演示了如何使用脚本聚合计算销售和成本交易的总利润。

上述聚合的响应：

    
    
    {
      "took": 218,
      ...
      "aggregations": {
        "profit": {
          "value": 240.0
        }
      }
    }

上面的示例也可以使用存储的脚本指定，如下所示：

    
    
    response = client.search(
      index: 'ledger',
      size: 0,
      body: {
        aggregations: {
          profit: {
            scripted_metric: {
              init_script: {
                id: 'my_init_script'
              },
              map_script: {
                id: 'my_map_script'
              },
              combine_script: {
                id: 'my_combine_script'
              },
              params: {
                field: 'amount'
              },
              reduce_script: {
                id: 'my_reduce_script'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST ledger/_search?size=0
    {
      "aggs": {
        "profit": {
          "scripted_metric": {
            "init_script": {
              "id": "my_init_script"
            },
            "map_script": {
              "id": "my_map_script"
            },
            "combine_script": {
              "id": "my_combine_script"
            },
            "params": {
              "field": "amount"           __},
            "reduce_script": {
              "id": "my_reduce_script"
            }
          }
        }
      }
    }

__

|

必须在全局"params"对象中指定"init"、"map"和"combine"脚本的脚本参数，以便在脚本之间共享。   ---|--- 有关指定脚本的更多详细信息，请参阅脚本文档。

### 允许的返回类型

虽然任何有效的脚本对象都可以在单个脚本中使用，但脚本必须仅返回或存储在"state"对象中：

* 基元类型 * 字符串 * 映射(仅包含此处列出的类型的键和值) * 数组(仅包含此处列出的类型的元素)

### 脚本范围

脚本化指标聚合在其执行的 4 个阶段使用脚本：

init_script

    

在收集任何文件之前执行。允许聚合设置任何初始状态。

在上面的例子中，"init_script"在"state"对象中创建了一个数组"事务"。

map_script

    

每个收集的文档执行一次。这是必需的脚本。如果指定了nocombine_script，则结果状态需要存储在"state"对象中。

在上面的示例中，"map_script"检查类型字段的值。如果值为 _sale_，则金额字段的值将添加到发生业务数组中。如果类型字段的值不是 _sale_，则金额字段的否定值将添加到发生业务中。

combine_script

    

文档收集完成后在每个分片上执行一次。这是必需的脚本。允许聚合合并从每个分片返回的状态。

在上面的例子中，"combine_script"遍历所有存储的事务，对"利润"变量中的值求和，最后返回"利润"。

reduce_script

    

在所有分片返回结果后，在协调节点上执行一次。这是必需的脚本。该脚本提供了对可变"状态"的访问，该状态是每个分片上combine_script结果的数组。

在上面的例子中，'reduce_script'遍历每个分片返回的'利润'，对值求和，然后返回最终的组合利润，该利润将在聚合的响应中返回。

### 工作示例

想象一下，您将以下文档索引为包含 2 个分片的索引：

    
    
    response = client.bulk(
      index: 'transactions',
      refresh: true,
      body: [
        {
          index: {
            _id: 1
          }
        },
        {
          type: 'sale',
          amount: 80
        },
        {
          index: {
            _id: 2
          }
        },
        {
          type: 'cost',
          amount: 10
        },
        {
          index: {
            _id: 3
          }
        },
        {
          type: 'cost',
          amount: 30
        },
        {
          index: {
            _id: 4
          }
        },
        {
          type: 'sale',
          amount: 130
        }
      ]
    )
    puts response
    
    
    PUT /transactions/_bulk?refresh
    {"index":{"_id":1}}
    {"type": "sale","amount": 80}
    {"index":{"_id":2}}
    {"type": "cost","amount": 10}
    {"index":{"_id":3}}
    {"type": "cost","amount": 30}
    {"index":{"_id":4}}
    {"type": "sale","amount": 130}

假设文档 1 和 3 最终位于分片 A 上，文档 2 和 4 在分片 B 上结束。以下是上述示例的每个阶段的聚合结果的细分。

#### Beforeinit_script

"state"被初始化为一个新的空对象。

    
    
    "state" : {}

#### Afterinit_script

在执行任何文档收集之前，在每个分片上运行一次，因此我们将在每个分片上都有一个副本：

分片 A

    
    
    
    "state" : {
        "transactions" : []
    }

碎片 B

    
    
    
    "state" : {
        "transactions" : []
    }

#### Aftermap_script

每个分片收集其文档并对收集的每个文档运行map_script：

分片 A

    
    
    
    "state" : {
        "transactions" : [ 80, -30 ]
    }

碎片 B

    
    
    
    "state" : {
        "transactions" : [ -10, 130 ]
    }

#### Aftercombine_script

文档收集完成后，combine_script在每个分片上执行，并将所有交易减少为每个分片的单个利润数字(通过对交易数组中的值求和)，该数字被传递回协调节点：

分片 A

     50 
Shard B

     120 

#### Afterreduce_script

reduce_script接收一个"状态"数组，其中包含每个分片的组合脚本的结果：

    
    
    "states" : [
        50,
        120
    ]

它将分片的响应减少到最终的整体利润数字(通过对值求和)，并将其作为聚合的结果返回以产生响应：

    
    
    {
      ...
    
      "aggregations": {
        "profit": {
          "value": 170
        }
      }
    }

### 其他参数

params

|

自选。一个对象，其内容将作为变量传递给"init_script"、"map_script"和"combine_script"。这对于允许用户控制聚合的行为以及在脚本之间存储状态非常有用。如果未指定，则默认值等效于提供：

    
    
    "params" : {}  
  
---|---  
  
### Empty
buckets[edit](https://github.com/elastic/elasticsearch/edit/8.9/docs/reference/aggregations/metrics/scripted-
metric-aggregation.asciidoc "Edit this page on GitHub")

如果脚本化指标聚合的父存储桶未收集任何文档，则将从分片返回具有"null"值的空聚合响应。在这种情况下，"reduce_script"的"状态"变量将包含"null"作为来自该分片的响应。因此，"reduce_script"应该期望并处理来自分片的"空"响应。

[« Rate aggregation](search-aggregations-metrics-rate-aggregation.md) [Stats
aggregation »](search-aggregations-metrics-stats-aggregation.md)
