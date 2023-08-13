

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« Avg aggregation](search-aggregations-metrics-avg-aggregation.md)
[Cardinality aggregation »](search-aggregations-metrics-cardinality-
aggregation.md)

## 箱线聚合

一种"箱线图"指标聚合，用于计算从聚合文档中提取的数值的箱线图。这些值可以从文档中的特定数值或直方图字段生成。

"箱线图"聚合返回制作箱线图的基本信息：最小值、最大值、中位数、第一四分位数(第 25 个百分位数)和第三个四分位数(第 75 个百分位数)值。

###Syntax

"箱线图"聚合单独如下所示：

    
    
    {
      "boxplot": {
        "field": "load_time"
      }
    }

让我们看一个表示加载时间的箱线图：

    
    
    response = client.search(
      index: 'latency',
      body: {
        size: 0,
        aggregations: {
          load_time_boxplot: {
            boxplot: {
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
        "load_time_boxplot": {
          "boxplot": {
            "field": "load_time" __}
        }
      }
    }

__

|

字段"load_time"必须是数值字段 ---|--- 响应将如下所示：

    
    
    {
      ...
    
     "aggregations": {
        "load_time_boxplot": {
          "min": 0.0,
          "max": 990.0,
          "q1": 167.5,
          "q2": 445.0,
          "q3": 722.5,
          "lower": 0.0,
          "upper": 990.0
        }
      }
    }

在这种情况下，下须值和上须值等于最小值和最大值。通常，这些值是 1.5 * IQR 范围，即最接近"q1 - (1.5 * IQR)"和"q3 + (1.5 * IQR)"的值。由于这是近似值，因此给定的值实际上可能不是从数据中观察到的值，而应该在合理的误差范围内。虽然 Boxplotaggregation 不会直接返回异常值点，但您可以检查是"下>分钟"还是"上限<最大值"以查看两侧是否存在异常值，然后直接查询它们。

###Script

如果您需要为未完全索引的值创建箱线图，则应创建一个运行时字段并获取该字段的箱线图。例如，如果加载时间以毫秒为单位，但您希望以秒为单位计算值，请使用运行时字段对其进行转换：

    
    
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
          load_time_boxplot: {
            boxplot: {
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
        "load_time_boxplot": {
          "boxplot": { "field": "load_time.seconds" }
        }
      }
    }

### 箱线图值(通常)是近似值

"箱线图"指标使用的算法称为TDigest(由Ted Dunning在Computing Accurate Quantiles Using T-Digests中引入)。

箱线图作为其他百分位数聚合也是不确定的。这意味着使用相同的数据可以获得略有不同的结果。

###Compression

近似算法必须在内存利用率与估计精度之间取得平衡。可以使用"压缩"参数来控制此平衡：

    
    
    response = client.search(
      index: 'latency',
      body: {
        size: 0,
        aggregations: {
          load_time_boxplot: {
            boxplot: {
              field: 'load_time',
              compression: 200
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
        "load_time_boxplot": {
          "boxplot": {
            "field": "load_time",
            "compression": 200    __}
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
        "load_time_boxplot": {
          "boxplot": {
            "field": "load_time",
            "execution_hint": "high_accuracy"    __}
        }
      }
    }

__

|

优化 TDigest 的准确性，但牺牲性能 ---|--- 此选项可以提高准确性(在某些情况下，数百万个样本的相对误差接近 0.01%)，但百分位查询需要 2 倍到 10 倍的时间才能完成。

### 缺失值

"missing"参数定义应如何处理缺少值的文档。默认情况下，它们将被忽略，但也可以将它们视为具有值。

    
    
    response = client.search(
      index: 'latency',
      body: {
        size: 0,
        aggregations: {
          grade_boxplot: {
            boxplot: {
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
        "grade_boxplot": {
          "boxplot": {
            "field": "grade",
            "missing": 10     __}
        }
      }
    }

__

|

"grade"字段中没有值的文档将与值为"10"的文档属于同一存储桶。   ---|--- « 平均聚合基数聚合 »