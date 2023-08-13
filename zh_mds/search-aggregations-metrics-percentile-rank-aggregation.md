

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« Min aggregation](search-aggregations-metrics-min-aggregation.md)
[Percentiles aggregation »](search-aggregations-metrics-percentile-
aggregation.md)

## 百分位排名聚合

一种"多值"指标聚合，用于计算从聚合文档中提取的数值的一个或多个百分位数。可以从文档中的特定数字或直方图字段中提取这些值。

请参阅百分位数是(通常)近似近似值")，压缩和执行提示，以获取有关百分位数排名聚合的近似值、性能和内存使用的建议

百分位排名显示低于确定值的观测值的百分比。例如，如果某个值大于或等于观测值的 95%，则称其处于第 95 个百分位等级。

假设您的数据由网站加载时间组成。您可能有一个服务协议，即 95% 的页面加载在 500 毫秒内完成，99% 的页面加载在 600 毫秒内完成。

让我们看一下表示加载时间的百分位数范围：

    
    
    response = client.search(
      index: 'latency',
      body: {
        size: 0,
        aggregations: {
          load_time_ranks: {
            percentile_ranks: {
              field: 'load_time',
              values: [
                500,
                600
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET latency/_search
    {
      "size": 0,
      "aggs": {
        "load_time_ranks": {
          "percentile_ranks": {
            "field": "load_time",   __"values": [ 500, 600 ]
          }
        }
      }
    }

__

|

字段"load_time"必须是数值字段 ---|--- 响应将如下所示：

    
    
    {
      ...
    
     "aggregations": {
        "load_time_ranks": {
          "values": {
            "500.0": 55.0,
            "600.0": 64.0
          }
        }
      }
    }

根据此信息，您可以确定您正在达到 99% 加载时间目标，但尚未完全达到 95% 加载时间目标

### 键控响应

默认情况下，"keyed"标志设置为"true"，将唯一的字符串键与每个存储桶相关联，并以哈希而不是数组的形式返回范围。将"键控"标志设置为"false"将禁用此行为：

    
    
    response = client.search(
      index: 'latency',
      body: {
        size: 0,
        aggregations: {
          load_time_ranks: {
            percentile_ranks: {
              field: 'load_time',
              values: [
                500,
                600
              ],
              keyed: false
            }
          }
        }
      }
    )
    puts response
    
    
    GET latency/_search
    {
      "size": 0,
      "aggs": {
        "load_time_ranks": {
          "percentile_ranks": {
            "field": "load_time",
            "values": [ 500, 600 ],
            "keyed": false
          }
        }
      }
    }

Response:

    
    
    {
      ...
    
      "aggregations": {
        "load_time_ranks": {
          "values": [
            {
              "key": 500.0,
              "value": 55.0
            },
            {
              "key": 600.0,
              "value": 64.0
            }
          ]
        }
      }
    }

###Script

如果需要针对未编制索引的值运行聚合，请使用运行时字段。例如，如果我们的加载时间以毫秒为单位，但我们希望以秒为单位计算百分位数：

    
    
    response = client.search(
      index: 'latency',
      body: {
        size: 0,
        runtime_mappings: {
          "load_time.seconds": {
            type: 'long',
            script: {
              source: "emit(doc['load_time'].value / params.timeUnit)",
              params: {
                "timeUnit": 1000
              }
            }
          }
        },
        aggregations: {
          load_time_ranks: {
            percentile_ranks: {
              values: [
                500,
                600
              ],
              field: 'load_time.seconds'
            }
          }
        }
      }
    )
    puts response
    
    
    GET latency/_search
    {
      "size": 0,
      "runtime_mappings": {
        "load_time.seconds": {
          "type": "long",
          "script": {
            "source": "emit(doc['load_time'].value / params.timeUnit)",
            "params": {
              "timeUnit": 1000
            }
          }
        }
      },
      "aggs": {
        "load_time_ranks": {
          "percentile_ranks": {
            "values": [ 500, 600 ],
            "field": "load_time.seconds"
          }
        }
      }
    }

### HDRHistogram

HDR 直方图(高动态范围直方图)是一种替代实现，在计算延迟测量的百分位数排名时非常有用，因为它可能比 t 摘要实现更快，但代价是内存占用量更大。此实现维护固定的最坏情况百分比错误(指定为有效数字数)。这意味着，如果在直方图中记录的值从 1 微秒到 1 小时(3，600，000，000 微秒)设置为 3 位有效数字，则对于最多 1 毫秒的值，它将保持 1 微秒的值分辨率，对于最大跟踪值(1 小时)保持 3.6 秒(或更好)的值分辨率。

HDR 直方图可以通过在请求中指定"hdr"对象来使用：

    
    
    response = client.search(
      index: 'latency',
      body: {
        size: 0,
        aggregations: {
          load_time_ranks: {
            percentile_ranks: {
              field: 'load_time',
              values: [
                500,
                600
              ],
              hdr: {
                number_of_significant_value_digits: 3
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET latency/_search
    {
      "size": 0,
      "aggs": {
        "load_time_ranks": {
          "percentile_ranks": {
            "field": "load_time",
            "values": [ 500, 600 ],
            "hdr": {                                  __"number_of_significant_value_digits": 3 __}
          }
        }
      }
    }

__

|

'hdr' 对象表示应使用 HDR 直方图来计算百分位数，并且可以在对象内部指定此算法的特定设置---|--- __

|

"number_of_significant_value_digits"指定直方图值的分辨率(以有效位数为单位) HDRHistogram 仅支持正值，如果传递负值，则会出错。如果值范围未知，使用 HDRHistogram 也不是一个好主意，因为这可能会导致高内存使用率。

### 缺失值

"missing"参数定义应如何处理缺少值的文档。默认情况下，它们将被忽略，但也可以将它们视为具有值。

    
    
    response = client.search(
      index: 'latency',
      body: {
        size: 0,
        aggregations: {
          load_time_ranks: {
            percentile_ranks: {
              field: 'load_time',
              values: [
                500,
                600
              ],
              missing: 10
            }
          }
        }
      }
    )
    puts response
    
    
    GET latency/_search
    {
      "size": 0,
      "aggs": {
        "load_time_ranks": {
          "percentile_ranks": {
            "field": "load_time",
            "values": [ 500, 600 ],
            "missing": 10           __}
        }
      }
    }

__

|

"load_time"字段中没有值的文档将与值为"10"的文档属于同一存储桶。   ---|--- « 最小聚合百分位数聚合 »