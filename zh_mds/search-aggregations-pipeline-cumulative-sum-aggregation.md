

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Pipeline aggregations](search-
aggregations-pipeline.md)

[« Cumulative cardinality aggregation](search-aggregations-pipeline-
cumulative-cardinality-aggregation.md) [Derivative aggregation »](search-
aggregations-pipeline-derivative-aggregation.md)

## 累积总和聚合

父管道聚合，用于计算父直方图(或date_histogram)聚合中指定指标的累积总和。指定的指标必须是数字，并且封闭直方图必须将"min_doc_count"设置为"0"("直方图"聚合的默认值)。

###Syntax

"cumulative_sum"聚合单独如下所示：

    
    
    {
      "cumulative_sum": {
        "buckets_path": "the_sum"
      }
    }

**表 58.'cumulative_sum' 参数**

参数名称 |描述 |必填 |默认值 ---|---|---|--- 'buckets_path'

|

我们希望找到其累积总和的存储桶的路径(有关更多详细信息，请参阅"buckets_path"语法)

|

Required

|   "格式"

|

十进制格式模式的输出值。如果指定，则在聚合的"value_as_string"属性中返回格式化值

|

Optional

|

"null" 以下代码片段计算每月总销售额的累计总和：

    
    
    response = client.search(
      index: 'sales',
      body: {
        size: 0,
        aggregations: {
          sales_per_month: {
            date_histogram: {
              field: 'date',
              calendar_interval: 'month'
            },
            aggregations: {
              sales: {
                sum: {
                  field: 'price'
                }
              },
              cumulative_sales: {
                cumulative_sum: {
                  buckets_path: 'sales'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search
    {
      "size": 0,
      "aggs": {
        "sales_per_month": {
          "date_histogram": {
            "field": "date",
            "calendar_interval": "month"
          },
          "aggs": {
            "sales": {
              "sum": {
                "field": "price"
              }
            },
            "cumulative_sales": {
              "cumulative_sum": {
                "buckets_path": "sales" __}
            }
          }
        }
      }
    }

__

|

"buckets_path"指示此累积总和聚合将"sales"聚合的输出用于累积总和---|--- 以下可能是响应：

    
    
    {
       "took": 11,
       "timed_out": false,
       "_shards": ...,
       "hits": ...,
       "aggregations": {
          "sales_per_month": {
             "buckets": [
                {
                   "key_as_string": "2015/01/01 00:00:00",
                   "key": 1420070400000,
                   "doc_count": 3,
                   "sales": {
                      "value": 550.0
                   },
                   "cumulative_sales": {
                      "value": 550.0
                   }
                },
                {
                   "key_as_string": "2015/02/01 00:00:00",
                   "key": 1422748800000,
                   "doc_count": 2,
                   "sales": {
                      "value": 60.0
                   },
                   "cumulative_sales": {
                      "value": 610.0
                   }
                },
                {
                   "key_as_string": "2015/03/01 00:00:00",
                   "key": 1425168000000,
                   "doc_count": 2,
                   "sales": {
                      "value": 375.0
                   },
                   "cumulative_sales": {
                      "value": 985.0
                   }
                }
             ]
          }
       }
    }

[« Cumulative cardinality aggregation](search-aggregations-pipeline-
cumulative-cardinality-aggregation.md) [Derivative aggregation »](search-
aggregations-pipeline-derivative-aggregation.md)
