

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Roll up or
transform your data](data-rollup-transform.md) ›[Rolling up historical
data](xpack-rollup.md)

[« Rollup API quick reference](rollup-api-quickref.md) [Understanding groups
»](rollup-understanding-groups.md)

## 汇总入门

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

对于版本 8.5 及更高版本，我们建议对汇总进行缩减采样，以降低时序数据的存储成本。

若要使用汇总功能，需要创建一个或多个"汇总作业"。这些作业在后台连续运行，并汇总您指定的一个或多个索引，将滚动的文档放在二级索引中(也是您选择的)。

假设您有一系列保存传感器数据的每日索引("sensor-2017-01-01"、"sensor-2017-01-02"等)。示例文档可能如下所示：

    
    
    {
      "timestamp": 1516729294000,
      "temperature": 200,
      "voltage": 5.2,
      "node": "a"
    }

#### 创建汇总作业

我们希望将这些文档汇总为每小时摘要，这将使我们能够生成任何时间间隔为一小时或更长时间的报告和仪表板。汇总作业可能如下所示：

    
    
    PUT _rollup/job/sensor
    {
      "index_pattern": "sensor-*",
      "rollup_index": "sensor_rollup",
      "cron": "*/30 * * * * ?",
      "page_size": 1000,
      "groups": {
        "date_histogram": {
          "field": "timestamp",
          "fixed_interval": "60m"
        },
        "terms": {
          "fields": [ "node" ]
        }
      },
      "metrics": [
        {
          "field": "temperature",
          "metrics": [ "min", "max", "sum" ]
        },
        {
          "field": "voltage",
          "metrics": [ "avg" ]
        }
      ]
    }

我们给作业"sensor"的ID(在url中："PUT _rollup/job/sensor")，并告诉它汇总索引模式"sensor-*"。此作业将查找并汇总与该模式匹配的任何索引。然后，汇总摘要存储在"sensor_rollup"索引中。

"cron"参数控制作业激活的时间和频率。当汇总作业的 cron 计划触发时，它将从上次激活后停止的位置开始汇总。因此，如果将 cron 配置为每 30 秒运行一次，则作业将处理索引到"sensor-*"索引中的最后 30 秒数据。

相反，如果将 cron 配置为每天午夜运行一次，则作业将处理过去 24 小时的数据。选择在很大程度上是首选项，具体取决于您希望汇总的"实时"程度，以及您是否希望连续处理或将其移动到非高峰时间。

接下来，我们定义一组"组"。从本质上讲，我们正在定义我们希望在以后查询数据时透视的维度。此作业中的分组允许我们在"时间戳"字段上使用"date_histogram"聚合，每小时汇总一次。它还允许我们在"节点"字段上运行术语聚合。

**日期直方图间隔与 cron 计划**

您会注意到，作业的 cron 配置为每 30 秒运行一次，但thedate_histogram配置为每隔 60 分钟汇总一次。这些关系如何？

date_histogram控制已保存数据的粒度。数据将按小时间隔汇总，您将无法进行精细查询。cron 只是控制进程何时查找要汇总的新数据。每隔 30 秒，它就会查看是否有新的一小时数据并将其汇总。如果没有，作业将重新进入睡眠状态。

通常，在大间隔(1小时)上定义这么小的cron(30s)是没有意义的，因为大多数激活只会回到睡眠状态。但这也没有错，工作会做正确的事情。

定义应为数据生成哪些组后，接下来配置应收集哪些指标。默认情况下，仅为每个组收集"doc_counts"。为了使汇总有用，您通常会添加平均值、最小值、最大值等指标。在这个例子中，指标相当简单：我们希望保存"温度"场的最小/最大/总和，以及"电压"场的平均值。

**平均值不可组合？！**

如果您以前使用过汇总，则可能会对平均值持谨慎态度。Ifan平均值以10分钟的间隔保存，对于较大的间隔通常没有用。您不能平均六个 10 分钟的平均值来找到每小时平均值;平均值的平均值不等于总平均值。

出于这个原因，其他系统倾向于省略以多个间隔平均或存储平均值的功能，以支持更灵活的查询。

相反，数据汇总功能将"计数"和"总和"保存在定义的时间间隔内。这允许我们在大于或等于定义间隔的任何间隔内重建平均值。这为最小的存储成本提供了最大的灵活性...而且您不必担心平均值准确性(这里没有平均值！

有关作业语法的更多详细信息，请参阅创建汇总作业。

执行上述命令并创建作业后，您将收到以下响应：

    
    
    {
      "acknowledged": true
    }

#### 启动作业

创建作业后，它将处于非活动状态。作业需要在开始处理数据之前启动(这允许您稍后停止它们，作为暂时暂停的一种方式，而无需删除配置)。

要启动作业，请执行以下命令：

    
    
    response = client.rollup.start_job(
      id: 'sensor'
    )
    puts response
    
    
    POST _rollup/job/sensor/_start

#### 搜索滚动结果

在作业运行并处理了一些数据后，我们可以使用 Rollupsearch 终结点执行一些搜索。汇总功能旨在使您可以使用您习惯的相同查询 DSL 语法...它只是碰巧在汇总的数据上运行。

例如，采用以下查询：

    
    
    response = client.rollup.rollup_search(
      index: 'sensor_rollup',
      body: {
        size: 0,
        aggregations: {
          max_temperature: {
            max: {
              field: 'temperature'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /sensor_rollup/_rollup_search
    {
      "size": 0,
      "aggregations": {
        "max_temperature": {
          "max": {
            "field": "temperature"
          }
        }
      }
    }

这是一个简单的聚合，用于计算"温度"场的最大值。但您会注意到它被发送到"sensor_rollup"索引而不是原始的"sensor-*"索引。您还会注意到它正在使用"_rollup_search"端点。否则，语法完全符合您的预期。

如果要执行该查询，则会收到类似于异常聚合响应的结果：

    
    
    {
      "took" : 102,
      "timed_out" : false,
      "terminated_early" : false,
      "_shards" : ... ,
      "hits" : {
        "total" : {
            "value": 0,
            "relation": "eq"
        },
        "max_score" : 0.0,
        "hits" : [ ]
      },
      "aggregations" : {
        "max_temperature" : {
          "value" : 202.0
        }
      }
    }

唯一值得注意的区别是 Rollup 搜索结果的"命中"为零，因为我们不再真正搜索原始的实时数据。否则它是相同的语法。

这里有一些有趣的收获。首先，即使数据以每小时的间隔汇总并按节点名称进行分区，我们 rane 的查询只是计算所有文档的最高温度。在作业中配置的"组"不是查询的必需元素，它们只是您可以分区的额外维度。其次，请求和响应语法与普通DSL几乎相同，使其易于集成到仪表板和应用程序中。

最后，我们可以使用我们定义的那些分组字段来构造一个更复杂的查询：

    
    
    response = client.rollup.rollup_search(
      index: 'sensor_rollup',
      body: {
        size: 0,
        aggregations: {
          timeline: {
            date_histogram: {
              field: 'timestamp',
              fixed_interval: '7d'
            },
            aggregations: {
              nodes: {
                terms: {
                  field: 'node'
                },
                aggregations: {
                  max_temperature: {
                    max: {
                      field: 'temperature'
                    }
                  },
                  avg_voltage: {
                    avg: {
                      field: 'voltage'
                    }
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /sensor_rollup/_rollup_search
    {
      "size": 0,
      "aggregations": {
        "timeline": {
          "date_histogram": {
            "field": "timestamp",
            "fixed_interval": "7d"
          },
          "aggs": {
            "nodes": {
              "terms": {
                "field": "node"
              },
              "aggs": {
                "max_temperature": {
                  "max": {
                    "field": "temperature"
                  }
                },
                "avg_voltage": {
                  "avg": {
                    "field": "voltage"
                  }
                }
              }
            }
          }
        }
      }
    }

返回相应的响应：

    
    
    {
       "took" : 93,
       "timed_out" : false,
       "terminated_early" : false,
       "_shards" : ... ,
       "hits" : {
         "total" : {
            "value": 0,
            "relation": "eq"
         },
         "max_score" : 0.0,
         "hits" : [ ]
       },
       "aggregations" : {
         "timeline" : {
           "buckets" : [
             {
               "key_as_string" : "2018-01-18T00:00:00.000Z",
               "key" : 1516233600000,
               "doc_count" : 6,
               "nodes" : {
                 "doc_count_error_upper_bound" : 0,
                 "sum_other_doc_count" : 0,
                 "buckets" : [
                   {
                     "key" : "a",
                     "doc_count" : 2,
                     "max_temperature" : {
                       "value" : 202.0
                     },
                     "avg_voltage" : {
                       "value" : 5.1499998569488525
                     }
                   },
                   {
                     "key" : "b",
                     "doc_count" : 2,
                     "max_temperature" : {
                       "value" : 201.0
                     },
                     "avg_voltage" : {
                       "value" : 5.700000047683716
                     }
                   },
                   {
                     "key" : "c",
                     "doc_count" : 2,
                     "max_temperature" : {
                       "value" : 202.0
                     },
                     "avg_voltage" : {
                       "value" : 4.099999904632568
                     }
                   }
                 ]
               }
             }
           ]
         }
       }
    }

除了更复杂(日期直方图和术语聚合，加上额外的平均指标)之外，您会注意到date_histogram使用"7d"间隔而不是"60m"。

####Conclusion

本快速入门应简要概述了汇总公开的核心功能。设置汇总时需要考虑更多提示和事项，您可以在本节的其余部分找到这些提示和事项。您还可以浏览 REST API，了解可用的概述。

[« Rollup API quick reference](rollup-api-quickref.md) [Understanding groups
»](rollup-understanding-groups.md)
