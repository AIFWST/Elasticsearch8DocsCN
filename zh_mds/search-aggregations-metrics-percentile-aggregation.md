

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« Percentile ranks aggregation](search-aggregations-metrics-percentile-rank-
aggregation.md) [Rate aggregation »](search-aggregations-metrics-rate-
aggregation.md)

## 百分位数聚合

一种"多值"指标聚合，用于计算从聚合文档中提取的数值上的一个或多个百分位数。可以从文档中的特定数值或直方图字段中提取这些值。

百分位数显示一定百分比的观测值出现的点。例如，第 95 个百分位数是大于观测值的 95% 的值。

百分位数通常用于查找异常值。在正态分布中，第 0.13 个和第 99.87 个百分位数表示与 themean 的三个标准差。任何超出三个标准差的数据通常都被视为异常。

检索一系列百分位数时，它们可用于估计数据分布并确定数据是否偏斜、双峰等。

假设您的数据由网站加载时间组成。平均和中位数加载时间对管理员来说并不过分有用。最大值可能很有趣，但它很容易被单个慢响应所扭曲。

让我们看一下表示加载时间的百分位数范围：

    
    
    response = client.search(
      index: 'latency',
      body: {
        size: 0,
        aggregations: {
          load_time_outlier: {
            percentiles: {
              field: 'load_time'
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
        "load_time_outlier": {
          "percentiles": {
            "field": "load_time" __}
        }
      }
    }

__

|

字段"load_time"必须是数值字段 ---|--- 默认情况下，"百分位数"指标将生成一系列百分位数："[1， 5， 25， 50， 75， 95， 99 ]"。响应将如下所示：

    
    
    {
      ...
    
     "aggregations": {
        "load_time_outlier": {
          "values": {
            "1.0": 10.0,
            "5.0": 30.0,
            "25.0": 170.0,
            "50.0": 445.0,
            "75.0": 720.0,
            "95.0": 940.0,
            "99.0": 980.0
          }
        }
      }
    }

如您所见，聚合将返回默认范围内每个百分位数的计算值。如果我们假设响应时间为毫秒，很明显网页通常加载时间为 10-725 毫秒，但偶尔会飙升至 945-985 毫秒。

通常，管理员只对异常值(极值百分位数)感兴趣。我们可以只指定我们感兴趣的百分比(请求的百分位数必须是介于 0-100 之间的值(包括 0-100)：

    
    
    response = client.search(
      index: 'latency',
      body: {
        size: 0,
        aggregations: {
          load_time_outlier: {
            percentiles: {
              field: 'load_time',
              percents: [
                95,
                99,
                99.9
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
        "load_time_outlier": {
          "percentiles": {
            "field": "load_time",
            "percents": [ 95, 99, 99.9 ] __}
        }
      }
    }

__

|

使用"百分比"参数指定特定的百分位数来计算---|--- ### 键控响应编辑

默认情况下，"keyed"标志设置为"true"，它将唯一的字符串键与每个存储桶相关联，并将范围作为哈希而不是数组返回。将"键控"标志设置为"false"将禁用此行为：

    
    
    response = client.search(
      index: 'latency',
      body: {
        size: 0,
        aggregations: {
          load_time_outlier: {
            percentiles: {
              field: 'load_time',
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
        "load_time_outlier": {
          "percentiles": {
            "field": "load_time",
            "keyed": false
          }
        }
      }
    }

Response:

    
    
    {
      ...
    
      "aggregations": {
        "load_time_outlier": {
          "values": [
            {
              "key": 1.0,
              "value": 10.0
            },
            {
              "key": 5.0,
              "value": 30.0
            },
            {
              "key": 25.0,
              "value": 170.0
            },
            {
              "key": 50.0,
              "value": 445.0
            },
            {
              "key": 75.0,
              "value": 720.0
            },
            {
              "key": 95.0,
              "value": 940.0
            },
            {
              "key": 99.0,
              "value": 980.0
            }
          ]
        }
      }
    }

###Script

如果需要针对未编制索引的值运行聚合，请使用运行时字段。例如，如果我们的加载时间以毫秒为单位，但您希望以秒为单位计算百分位数：

    
    
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
          load_time_outlier: {
            percentiles: {
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
        "load_time_outlier": {
          "percentiles": {
            "field": "load_time.seconds"
          }
        }
      }
    }

### 百分位数(通常)是近似值

有许多不同的算法来计算百分位数。朴素实现只是将所有值存储在排序数组中。要找到第 50 个百分位数，您只需找到位于 'my_array[count(my_array) * 0.5]' 的值。

显然，朴素的实现不会缩放 - 排序数组随着数据集中的值数量线性增长。为了计算 Elasticsearch 集群中可能数十亿个值的百分位数，需要计算_近似_百分位数。

"百分位数"指标使用的算法称为TDigest(由Ted Dunning在Computing Accurate Quantiles Using T-Digests中引入)。

使用此指标时，需要牢记以下几条准则：

* 精度与"q(1-q)"成正比。这意味着极端百分位数(例如 99%)比不太极端的百分位数更准确，例如中位数 * 对于较小的值集，百分位数非常准确(如果数据足够小，则可能是 100% 准确)。  * 随着存储桶中值数量的增加，算法开始近似百分位数。它有效地用准确性换取了内存节省。确切的不准确性水平很难一概而论，因为它取决于您的数据分布和要聚合的数据量

下图显示了均匀分布上的相对误差，具体取决于收集的值的数量和请求的百分位数：

百分位数错误

它显示了极端百分位数的精度如何更好。大量值误差减小的原因是大数定律使值的分布越来越均匀，t-digest 树可以更好地总结它。在更偏斜的分布上，情况并非如此。

百分位聚合也是不确定的。这意味着使用相同的数据可以获得略有不同的结果。

###Compression

近似算法必须在内存利用率与估计精度之间取得平衡。可以使用"压缩"参数来控制此平衡：

    
    
    response = client.search(
      index: 'latency',
      body: {
        size: 0,
        aggregations: {
          load_time_outlier: {
            percentiles: {
              field: 'load_time',
              tdigest: {
                compression: 200
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
        "load_time_outlier": {
          "percentiles": {
            "field": "load_time",
            "tdigest": {
              "compression": 200    __}
          }
        }
      }
    }

__

|

压缩控制内存使用和近似误差 ---|--- TDigest 算法使用许多"节点"来近似百分位数 - 可用的节点越多，与数据量成正比的精度(和较大的内存占用)就越高。"压缩"参数将最大节点数限制为"20 * 压缩"。

因此，通过增加压缩值，可以以增加内存为代价来提高百分位数的准确性。较大的压缩值也会使算法变慢，因为基础树数据结构的大小会变小，从而导致操作成本更高。默认压缩值为"100"。

一个"节点"使用大约 32 字节的内存，因此在最坏的情况下(大量数据按排序和顺序到达)，默认设置将产生大约 64KB 大小的 TDigest。在实践中，数据往往更加随机，并且 TDigest 将使用更少的内存。

### 执行提示

TDigest 的默认实现针对性能进行了优化，可扩展到数百万甚至数十亿个样本值，同时保持可接受的准确度水平(在某些情况下，数百万个样本的相对误差接近 1%)。有一个选项可以使用针对准确性优化的实现，方法是将参数"execution_hint"设置为值"high_accuracy"：

    
    
    GET latency/_search
    {
      "size": 0,
      "aggs": {
        "load_time_outlier": {
          "percentiles": {
            "field": "load_time",
            "tdigest": {
              "execution_hint": "high_accuracy"    __}
          }
        }
      }
    }

__

|

优化 TDigest 的准确性，但牺牲性能 ---|--- 此选项可以提高准确性(在某些情况下，数百万个样本的相对误差接近 0.01%)，但百分位查询需要 2 倍到 10 倍的时间才能完成。

### HD直方图

HDR 直方图(高动态范围直方图)是一种替代实现，在计算延迟测量的百分位数时非常有用，因为它可以比摘要实现更快，但需要权衡更大的内存占用。此实现维护固定的最坏情况百分比错误(指定为有效数字数)。这意味着，如果使用直方图中的值从 1 微秒到 1 小时(3，600，000，000 微秒)记录数据，设置为 3 位有效数字，则对于最多 1 毫秒的值，它将保持 1 微秒的值分辨率，对于最大跟踪值(1 小时)保持 3.6 秒(或更好)的值分辨率。

HDR 直方图可以通过在请求中指定 'hdr' 参数来使用：

    
    
    response = client.search(
      index: 'latency',
      body: {
        size: 0,
        aggregations: {
          load_time_outlier: {
            percentiles: {
              field: 'load_time',
              percents: [
                95,
                99,
                99.9
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
        "load_time_outlier": {
          "percentiles": {
            "field": "load_time",
            "percents": [ 95, 99, 99.9 ],
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
          grade_percentiles: {
            percentiles: {
              field: 'grade',
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
        "grade_percentiles": {
          "percentiles": {
            "field": "grade",
            "missing": 10       __}
        }
      }
    }

__

|

"grade"字段中没有值的文档将与值为"10"的文档属于同一存储桶。   ---|--- « 百分位排名聚合 速率聚合 »