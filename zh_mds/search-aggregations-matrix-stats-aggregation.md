

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« Cartesian-centroid aggregation](search-aggregations-metrics-cartesian-
centroid-aggregation.md) [Max aggregation »](search-aggregations-metrics-
max-aggregation.md)

## 矩阵统计聚合

"matrix_stats"聚合是一个数字聚合，用于计算一组文档字段的以下统计信息：

`count`

|

计算中包含的每个字段样本数。   ---|--- "意思"

|

每个字段的平均值。   "差异"

|

每个字段 测量样本与平均值的分布程度。   "偏度"

|

每个场测量量化平均值周围的不对称分布。   "峰度"

|

每个字段测量量化分布的形状。   "协方差"

|

定量描述一个字段中的变化如何与另一个字段相关联的矩阵。   "相关性"

|

协方差矩阵缩放到 -1 到 1 的范围(包括 -1 和 1)。描述字段分布之间的关系。   与其他指标聚合不同，"matrix_stats"聚合不支持脚本。

以下示例演示了如何使用矩阵统计信息来描述收入与贫困之间的关系。

    
    
    response = client.search(
      body: {
        aggregations: {
          statistics: {
            matrix_stats: {
              fields: [
                'poverty',
                'income'
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "aggs": {
        "statistics": {
          "matrix_stats": {
            "fields": [ "poverty", "income" ]
          }
        }
      }
    }

聚合类型为"matrix_stats"，"字段"设置定义用于计算统计信息的字段集(作为数组)。上述请求返回以下响应：

    
    
    {
      ...
      "aggregations": {
        "statistics": {
          "doc_count": 50,
          "fields": [ {
              "name": "income",
              "count": 50,
              "mean": 51985.1,
              "variance": 7.383377037755103E7,
              "skewness": 0.5595114003506483,
              "kurtosis": 2.5692365287787124,
              "covariance": {
                "income": 7.383377037755103E7,
                "poverty": -21093.65836734694
              },
              "correlation": {
                "income": 1.0,
                "poverty": -0.8352655256272504
              }
            }, {
              "name": "poverty",
              "count": 50,
              "mean": 12.732000000000001,
              "variance": 8.637730612244896,
              "skewness": 0.4516049811903419,
              "kurtosis": 2.8615929677997767,
              "covariance": {
                "income": -21093.65836734694,
                "poverty": 8.637730612244896
              },
              "correlation": {
                "income": -0.8352655256272504,
                "poverty": 1.0
              }
            } ]
        }
      }
    }

"doc_count"字段表示统计数据计算中涉及的文档数量。

### 多值字段

"matrix_stats"聚合将每个文档字段视为独立样本。"mode"参数控制聚合将用于数组或多值字段的数组值。此参数可以采用以下方法之一：

`avg`

|

(默认)使用所有值的平均值。   ---|--- "分钟"

|

选择最低值。   "最大"

|

选择最高值。   "总和"

|

使用所有值的总和。   "中位数"

|

使用所有值的中位数。   ### 缺失值编辑

"missing"参数定义应如何处理缺少值的文档。默认情况下，它们将被忽略，但也可以将它们视为具有值。这是通过添加一组字段名称：值映射来指定每个字段的默认值来完成的。

    
    
    GET /_search
    {
      "aggs": {
        "matrixstats": {
          "matrix_stats": {
            "fields": [ "poverty", "income" ],
            "missing": { "income": 50000 }      __}
        }
      }
    }

__

|

"收入"字段中没有值的文档将具有默认值"50000"。   ---|--- « 笛卡尔质心聚合 最大聚合 »