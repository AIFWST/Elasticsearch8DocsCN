

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« Scripted metric aggregation](search-aggregations-metrics-scripted-metric-
aggregation.md) [String stats aggregation »](search-aggregations-metrics-
string-stats-aggregation.md)

## 统计聚合

一种"多值"指标聚合，用于计算从聚合文档中提取的数值的统计信息。

返回的统计信息包括："最小"、"最大值"、"总和"、"计数"和"平均值"。

假设数据由代表学生考试成绩(0 到 100 之间)的文档组成

    
    
    response = client.search(
      index: 'exams',
      size: 0,
      body: {
        aggregations: {
          grades_stats: {
            stats: {
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
        "grades_stats": { "stats": { "field": "grade" } }
      }
    }

上述聚合计算所有文档的成绩统计信息。聚合类型为"统计信息"，"字段"设置定义将计算统计信息的文档的数值字段。以上将返回以下内容：

    
    
    {
      ...
    
      "aggregations": {
        "grades_stats": {
          "count": 2,
          "min": 50.0,
          "max": 100.0,
          "avg": 75.0,
          "sum": 150.0
        }
      }
    }

聚合的名称(上面的"grades_stats")也用作可以从返回的响应中检索聚合结果的键。

###Script

如果您需要获取比单个字段更复杂的内容的"统计信息"，请在运行时字段上运行聚合。

    
    
    response = client.search(
      index: 'exams',
      body: {
        size: 0,
        runtime_mappings: {
          "grade.weighted": {
            type: 'double',
            script: "\n        emit(doc['grade'].value * doc['weight'].value)\n      "
          }
        },
        aggregations: {
          grades_stats: {
            stats: {
              field: 'grade.weighted'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /exams/_search
    {
      "size": 0,
      "runtime_mappings": {
        "grade.weighted": {
          "type": "double",
          "script": """
            emit(doc['grade'].value * doc['weight'].value)
          """
        }
      },
      "aggs": {
        "grades_stats": {
          "stats": {
            "field": "grade.weighted"
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
          grades_stats: {
            stats: {
              field: 'grade',
              missing: 0
            }
          }
        }
      }
    )
    puts response
    
    
    POST /exams/_search?size=0
    {
      "aggs": {
        "grades_stats": {
          "stats": {
            "field": "grade",
            "missing": 0      __}
        }
      }
    }

__

|

"grade"字段中没有值的文档将与值为"0"的文档属于同一存储桶。   ---|--- « 脚本化指标聚合 字符串统计信息聚合 »