

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« Cardinality aggregation](search-aggregations-metrics-cardinality-
aggregation.md) [Geo-bounds aggregation »](search-aggregations-metrics-
geobounds-aggregation.md)

## 扩展统计聚合

一种"多值"指标聚合，用于计算从聚合文档中提取的数值的统计信息。

"extended_stats"聚合是"统计信息"聚合的扩展版本，其中添加了其他指标，例如"sum_of_squares"、"方差"、"std_deviation"和"std_deviation_bounds"。

假设数据由代表学生考试成绩(0 到 100 之间)的文档组成

    
    
    response = client.search(
      index: 'exams',
      body: {
        size: 0,
        aggregations: {
          grades_stats: {
            extended_stats: {
              field: 'grade'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /exams/_search
    {
      "size": 0,
      "aggs": {
        "grades_stats": { "extended_stats": { "field": "grade" } }
      }
    }

上述聚合计算所有文档的成绩统计信息。聚合类型为"extended_stats"，"字段"设置定义将计算统计信息的文档的数字字段。以上将返回以下内容：

"std_deviation"和"方差"作为总体指标计算，因此它们始终分别与"std_deviation_population"和"variance_population"相同。

    
    
    {
      ...
    
      "aggregations": {
        "grades_stats": {
          "count": 2,
          "min": 50.0,
          "max": 100.0,
          "avg": 75.0,
          "sum": 150.0,
          "sum_of_squares": 12500.0,
          "variance": 625.0,
          "variance_population": 625.0,
          "variance_sampling": 1250.0,
          "std_deviation": 25.0,
          "std_deviation_population": 25.0,
          "std_deviation_sampling": 35.35533905932738,
          "std_deviation_bounds": {
            "upper": 125.0,
            "lower": 25.0,
            "upper_population": 125.0,
            "lower_population": 25.0,
            "upper_sampling": 145.71067811865476,
            "lower_sampling": 4.289321881345245
          }
        }
      }
    }

聚合的名称(上面的"grades_stats")也用作可以从返回的响应中检索聚合结果的键。

### 标准偏差边界

默认情况下，"extended_stats"指标将返回一个名为"std_deviation_bounds"的对象，该对象提供与平均值正负两个标准差的区间。这是可视化数据方差的有用方法。如果你想要一个不同的边界，例如三个标准差，你可以在请求中设置"sigma"：

    
    
    response = client.search(
      index: 'exams',
      body: {
        size: 0,
        aggregations: {
          grades_stats: {
            extended_stats: {
              field: 'grade',
              sigma: 3
            }
          }
        }
      }
    )
    puts response
    
    
    GET /exams/_search
    {
      "size": 0,
      "aggs": {
        "grades_stats": {
          "extended_stats": {
            "field": "grade",
            "sigma": 3          __}
        }
      }
    }

__

|

"sigma"控制应在------|显示多少个标准差+/-，"sigma"可以是任何非负双精度，这意味着您可以请求非整数值，例如"1.5"。值"0"有效，但只会返回"上限"和"下限"的平均值。

"上限"和"下限"作为人口指标计算，因此它们始终分别与"upper_population"和"lower_population"相同。

### 标准差和边界需要正态性

默认情况下显示标准差及其边界，但它们并不总是适用于所有数据集。您的数据必须呈正态分布，指标才有意义。标准差背后的统计数据假定数据呈正态分布，因此，如果数据严重偏左或偏右，则返回的值将具有误导性。

###Script

如果需要对未编制索引的值进行聚合，请使用运行时字段。假设我们发现我们一直在努力的成绩是针对高于学生水平的考试，我们想"纠正"它：

    
    
    response = client.search(
      index: 'exams',
      body: {
        size: 0,
        runtime_mappings: {
          "grade.corrected": {
            type: 'double',
            script: {
              source: "emit(Math.min(100, doc['grade'].value * params.correction))",
              params: {
                correction: 1.2
              }
            }
          }
        },
        aggregations: {
          grades_stats: {
            extended_stats: {
              field: 'grade.corrected'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /exams/_search
    {
      "size": 0,
      "runtime_mappings": {
        "grade.corrected": {
          "type": "double",
          "script": {
            "source": "emit(Math.min(100, doc['grade'].value * params.correction))",
            "params": {
              "correction": 1.2
            }
          }
        }
      },
      "aggs": {
        "grades_stats": {
          "extended_stats": { "field": "grade.corrected" }
        }
      }
    }

### 缺失值

"missing"参数定义应如何处理缺少值的文档。默认情况下，它们将被忽略，但也可以将它们视为具有值。

    
    
    response = client.search(
      index: 'exams',
      body: {
        size: 0,
        aggregations: {
          grades_stats: {
            extended_stats: {
              field: 'grade',
              missing: 0
            }
          }
        }
      }
    )
    puts response
    
    
    GET /exams/_search
    {
      "size": 0,
      "aggs": {
        "grades_stats": {
          "extended_stats": {
            "field": "grade",
            "missing": 0        __}
        }
      }
    }

__

|

"grade"字段中没有值的文档将与值为"0"的文档属于同一存储桶。   ---|--- « 基数聚合 地理边界聚合 »