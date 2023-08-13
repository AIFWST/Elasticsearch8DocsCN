

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« Metrics aggregations](search-aggregations-metrics.md) [Boxplot
aggregation »](search-aggregations-metrics-boxplot-aggregation.md)

## 平均聚合

一种"单值"指标聚合，用于计算从聚合文档中提取的数字值的平均值。可以从文档中的特定数值或直方图字段中提取这些值。

假设数据由代表学生考试成绩(0 到 100 之间)的文档组成，我们可以将他们的分数平均为：

    
    
    response = client.search(
      index: 'exams',
      size: 0,
      body: {
        aggregations: {
          avg_grade: {
            avg: {
              field: 'grade'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /exams/_search?size=0
    {
      "aggs": {
        "avg_grade": { "avg": { "field": "grade" } }
      }
    }

上述聚合计算所有文档的平均成绩。聚合类型为"avg"，"字段"设置定义将计算平均值的文档的数值字段。以上将返回以下内容：

    
    
    {
      ...
      "aggregations": {
        "avg_grade": {
          "value": 75.0
        }
      }
    }

聚合的名称(上面的"avg_grade")也用作从返回的响应中检索聚合结果的键。

###Script

假设考试非常困难，您需要进行成绩更正。对运行时字段求平均值以获得更正的平均值：

    
    
    response = client.search(
      index: 'exams',
      size: 0,
      body: {
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
          avg_corrected_grade: {
            avg: {
              field: 'grade.corrected'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /exams/_search?size=0
    {
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
        "avg_corrected_grade": {
          "avg": {
            "field": "grade.corrected"
          }
        }
      }
    }

### 缺失值

"missing"参数定义应如何处理缺少值的文档。默认情况下，它们将被忽略，但也可以将它们视为具有值。

    
    
    response = client.search(
      index: 'exams',
      size: 0,
      body: {
        aggregations: {
          grade_avg: {
            avg: {
              field: 'grade',
              missing: 10
            }
          }
        }
      }
    )
    puts response
    
    
    POST /exams/_search?size=0
    {
      "aggs": {
        "grade_avg": {
          "avg": {
            "field": "grade",
            "missing": 10     __}
        }
      }
    }

__

|

"grade"字段中没有值的文档将与值为"10"的文档属于同一存储桶。   ---|--- ### 直方图字段编辑

在直方图字段上计算平均值时，聚合的结果是"值"数组中所有元素的加权平均值，同时考虑了"计数"数组中相同位置的数字。

例如，对于以下索引，该索引存储了预聚合的直方图以及不同网络的延迟指标：

    
    
    response = client.index(
      index: 'metrics_index',
      id: 1,
      body: {
        "network.name": 'net-1',
        latency_histo: {
          values: [
            0.1,
            0.2,
            0.3,
            0.4,
            0.5
          ],
          counts: [
            3,
            7,
            23,
            12,
            6
          ]
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'metrics_index',
      id: 2,
      body: {
        "network.name": 'net-2',
        latency_histo: {
          values: [
            0.1,
            0.2,
            0.3,
            0.4,
            0.5
          ],
          counts: [
            8,
            17,
            8,
            7,
            6
          ]
        }
      }
    )
    puts response
    
    response = client.search(
      index: 'metrics_index',
      size: 0,
      body: {
        aggregations: {
          avg_latency: {
            avg: {
              field: 'latency_histo'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT metrics_index/_doc/1
    {
      "network.name" : "net-1",
      "latency_histo" : {
          "values" : [0.1, 0.2, 0.3, 0.4, 0.5], __"counts" : [3, 7, 23, 12, 6] __}
    }
    
    PUT metrics_index/_doc/2
    {
      "network.name" : "net-2",
      "latency_histo" : {
          "values" :  [0.1, 0.2, 0.3, 0.4, 0.5], __"counts" : [8, 17, 8, 7, 6] __}
    }
    
    POST /metrics_index/_search?size=0
    {
      "aggs": {
        "avg_latency":
          { "avg": { "field": "latency_histo" }
        }
      }
    }

对于每个直方图字段，"avg"聚合将"values"数组<1>中的每个数字乘以"counts"数组中的关联计数<2>。最终，它将计算所有直方图的这些值的平均值，并返回以下结果：

    
    
    {
      ...
      "aggregations": {
        "avg_latency": {
          "value": 0.29690721649
        }
      }
    }

[« Metrics aggregations](search-aggregations-metrics.md) [Boxplot
aggregation »](search-aggregations-metrics-boxplot-aggregation.md)
