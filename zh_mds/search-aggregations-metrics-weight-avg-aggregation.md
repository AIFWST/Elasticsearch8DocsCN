

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« Value count aggregation](search-aggregations-metrics-valuecount-
aggregation.md) [Pipeline aggregations »](search-aggregations-pipeline.md)

## 加权平均聚合

一种"单值"指标聚合，用于计算从聚合文档中提取的数字值的加权平均值。这些值可以从文档中的特定数值字段中提取。

在计算常规平均值时，每个数据点具有相等的"权重"......它对最终价值的贡献相等。另一方面，加权平均值对每个数据点的权重不同。从文档中提取每个数据点对最终值的贡献量。

作为公式，加权平均值是"∑(值 * 权重)/∑(权重)"

可以将常规平均值视为加权平均值，其中每个值的隐式权重为"1"。

**表 51.'weighted_avg' 参数**

参数名称 |描述 |必填 |默认值 ---|---|---|--- 'value'

|

提供值的字段或脚本的配置

|

Required

|   "重量"

|

提供权重的字段或脚本的配置

|

Required

|   "格式"

|

数值响应格式化程序

|

Optional

|   "值"和"权重"对象具有特定于字段的配置：

**表 52."值"参数**

参数名称 |描述 |必填 |默认值 ---|---|---|--- 'field'

|

应从中提取值的字段

|

Required

|   "失踪"

|

字段完全缺失时要使用的值

|

Optional

|   **表 53."重量"参数**

参数名称 |描述 |必填 |默认值 ---|---|---|--- 'field'

|

应从中提取权重的字段

|

Required

|   "失踪"

|

字段完全缺失时要使用的权重

|

Optional

|   ###Examplesedit

如果我们的文档有一个包含 0-100 数字分数的"grade"字段和一个包含任意数字权重的""权重"字段，我们可以使用以下方法计算加权平均值：

    
    
    response = client.search(
      index: 'exams',
      body: {
        size: 0,
        aggregations: {
          weighted_grade: {
            weighted_avg: {
              value: {
                field: 'grade'
              },
              weight: {
                field: 'weight'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /exams/_search
    {
      "size": 0,
      "aggs": {
        "weighted_grade": {
          "weighted_avg": {
            "value": {
              "field": "grade"
            },
            "weight": {
              "field": "weight"
            }
          }
        }
      }
    }

这会产生如下响应：

    
    
    {
      ...
      "aggregations": {
        "weighted_grade": {
          "value": 70.0
        }
      }
    }

虽然每个字段允许多个值，但只允许一个权重。如果聚合遇到具有多个权重的文档(例如，权重字段是多值字段)，它将中止搜索。如果遇到这种情况，则应生成一个运行时字段，将这些值合并为单个权重。

此单个权重将独立应用于从"值"字段提取的每个值。

此示例显示如何使用单个权重对具有多个值的单个文档求平均值：

    
    
    response = client.index(
      index: 'exams',
      refresh: true,
      body: {
        grade: [
          1,
          2,
          3
        ],
        weight: 2
      }
    )
    puts response
    
    response = client.search(
      index: 'exams',
      body: {
        size: 0,
        aggregations: {
          weighted_grade: {
            weighted_avg: {
              value: {
                field: 'grade'
              },
              weight: {
                field: 'weight'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /exams/_doc?refresh
    {
      "grade": [1, 2, 3],
      "weight": 2
    }
    
    POST /exams/_search
    {
      "size": 0,
      "aggs": {
        "weighted_grade": {
          "weighted_avg": {
            "value": {
              "field": "grade"
            },
            "weight": {
              "field": "weight"
            }
          }
        }
      }
    }

三个值("1"、"2"和"3")将作为独立值包含在内，所有值的权重均为"2"：

    
    
    {
      ...
      "aggregations": {
        "weighted_grade": {
          "value": 2.0
        }
      }
    }

聚合返回 '2.0' 作为结果，这与我们在手动计算时所期望的相匹配："((1*2) + (2*2) + (3*2)) / (2+2+2) == 2'

### 运行时字段

如果必须对与索引值不完全一致的值求和或加权，请在运行时字段上运行聚合。

    
    
    response = client.index(
      index: 'exams',
      refresh: true,
      body: {
        grade: 100,
        weight: [
          2,
          3
        ]
      }
    )
    puts response
    
    response = client.index(
      index: 'exams',
      refresh: true,
      body: {
        grade: 80,
        weight: 3
      }
    )
    puts response
    
    response = client.search(
      index: 'exams',
      filter_path: 'aggregations',
      body: {
        size: 0,
        runtime_mappings: {
          "weight.combined": {
            type: 'double',
            script: "\n        double s = 0;\n        for (double w : doc['weight']) {\n          s += w;\n        }\n        emit(s);\n      "
          }
        },
        aggregations: {
          weighted_grade: {
            weighted_avg: {
              value: {
                script: 'doc.grade.value + 1'
              },
              weight: {
                field: 'weight.combined'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /exams/_doc?refresh
    {
      "grade": 100,
      "weight": [2, 3]
    }
    POST /exams/_doc?refresh
    {
      "grade": 80,
      "weight": 3
    }
    
    POST /exams/_search?filter_path=aggregations
    {
      "size": 0,
      "runtime_mappings": {
        "weight.combined": {
          "type": "double",
          "script": """
            double s = 0;
            for (double w : doc['weight']) {
              s += w;
            }
            emit(s);
          """
        }
      },
      "aggs": {
        "weighted_grade": {
          "weighted_avg": {
            "value": {
              "script": "doc.grade.value + 1"
            },
            "weight": {
              "field": "weight.combined"
            }
          }
        }
      }
    }

它应该看起来像：

    
    
    {
      "aggregations": {
        "weighted_grade": {
          "value": 93.5
        }
      }
    }

### 缺失值

默认情况下，聚合排除"值"或"权重"字段缺少值或"null"值的文档。改用"missing"参数为这些文档指定默认值。

    
    
    POST /exams/_search
    {
      "size": 0,
      "aggs": {
        "weighted_grade": {
          "weighted_avg": {
            "value": {
              "field": "grade",
              "missing": 2
            },
            "weight": {
              "field": "weight",
              "missing": 3
            }
          }
        }
      }
    }

[« Value count aggregation](search-aggregations-metrics-valuecount-
aggregation.md) [Pipeline aggregations »](search-aggregations-pipeline.md)
