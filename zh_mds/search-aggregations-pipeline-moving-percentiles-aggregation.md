

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Pipeline aggregations](search-
aggregations-pipeline.md)

[« Moving function aggregation](search-aggregations-pipeline-movfn-
aggregation.md) [Normalize aggregation »](search-aggregations-pipeline-
normalize-aggregation.md)

## 移动百分位数聚合

给定一系列有序的百分位数，移动百分位数聚合将在这些百分位数上滑动一个窗口，并允许用户计算累积百分位数。

这在概念上与移动函数管道聚合非常相似，只是它适用于百分位数草图而不是实际的存储桶值。

###Syntax

"moving_percentiles"聚合单独如下所示：

    
    
    {
      "moving_percentiles": {
        "buckets_path": "the_percentile",
        "window": 10
      }
    }

**表 74.'moving_percentiles' 参数**

参数名称 |描述 |必填 |默认值 ---|---|---|--- 'buckets_path'

|

指向感兴趣的百分位数的路径(有关详细信息，请参阅"buckets_path"语法

|

Required

|   "窗口"

|

要在直方图上"滑动"的窗口大小。

|

Required

|   "移位"

|

窗口位置的移动。

|

Optional

|

0 "moving_percentiles"聚合必须嵌入到"直方图"或"date_histogram"聚合中。它们可以像任何其他指标聚合一样嵌入：

    
    
    response = client.search(
      body: {
        size: 0,
        aggregations: {
          my_date_histo: {
            date_histogram: {
              field: 'date',
              calendar_interval: '1M'
            },
            aggregations: {
              the_percentile: {
                percentiles: {
                  field: 'price',
                  percents: [
                    1,
                    99
                  ]
                }
              },
              the_movperc: {
                moving_percentiles: {
                  buckets_path: 'the_percentile',
                  window: 10
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /_search
    {
      "size": 0,
      "aggs": {
        "my_date_histo": {                          __"date_histogram": {
            "field": "date",
            "calendar_interval": "1M"
          },
          "aggs": {
            "the_percentile": { __"percentiles": {
                "field": "price",
                "percents": [ 1.0, 99.0 ]
              }
            },
            "the_movperc": {
              "moving_percentiles": {
                "buckets_path": "the_percentile", __"window": 10
              }
            }
          }
        }
      }
    }

__

|

在"时间戳"字段上构造一个名为"my_date_histo"的"date_histogram"，间隔为一天---|---__

|

"百分位数"指标用于计算字段的百分位数。   __

|

最后，我们指定一个使用"the_percentile"草图作为其输入的"moving_percentiles"聚合。   移动百分位数是通过首先在字段上指定"直方图"或"date_histogram"来构建的。然后，在该直方图内添加一个百分位指标。最后，"moving_percentiles"嵌入在直方图中。然后使用"buckets_path"参数"指向"直方图内的百分位数聚合(有关"buckets_path"语法的说明，请参阅"buckets_path"语法)。

以下是可能的响应：

    
    
    {
       "took": 11,
       "timed_out": false,
       "_shards": ...,
       "hits": ...,
       "aggregations": {
          "my_date_histo": {
             "buckets": [
                 {
                     "key_as_string": "2015/01/01 00:00:00",
                     "key": 1420070400000,
                     "doc_count": 3,
                     "the_percentile": {
                         "values": {
                           "1.0": 151.0,
                           "99.0": 200.0
                         }
                     }
                 },
                 {
                     "key_as_string": "2015/02/01 00:00:00",
                     "key": 1422748800000,
                     "doc_count": 2,
                     "the_percentile": {
                         "values": {
                           "1.0": 10.4,
                           "99.0": 49.6
                         }
                     },
                     "the_movperc": {
                       "values": {
                         "1.0": 151.0,
                         "99.0": 200.0
                       }
                     }
                 },
                 {
                     "key_as_string": "2015/03/01 00:00:00",
                     "key": 1425168000000,
                     "doc_count": 2,
                     "the_percentile": {
                        "values": {
                          "1.0": 175.25,
                          "99.0": 199.75
                        }
                     },
                     "the_movperc": {
                        "values": {
                          "1.0": 11.6,
                          "99.0": 200.0
                        }
                     }
                 }
             ]
          }
       }
    }

"moving_percentiles"聚合的输出格式继承自引用的"百分位数"聚合的格式。

移动百分位数管道聚合始终使用"跳过"间隙策略运行。

### 移位参数

默认情况下("shift = 0")，用于计算的窗口是不包括当前存储桶的最后一个"n"值。将"移位"增加 1 将起始窗口位置向右移动"1"。

* 要将当前存储桶包含在窗口中，请使用"shift = 1"。  * 对于中心对齐(当前存储桶前后的"n / 2"值)，请使用"shift = window / 2"。  * 对于右对齐(当前存储桶后的"n"值)，请使用"shift = 窗口"。

如果窗口边缘中的任何一个移动到数据系列的边框之外，窗口将收缩以仅包含可用值。

[« Moving function aggregation](search-aggregations-pipeline-movfn-
aggregation.md) [Normalize aggregation »](search-aggregations-pipeline-
normalize-aggregation.md)
