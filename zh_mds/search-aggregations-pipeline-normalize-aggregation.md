

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Pipeline aggregations](search-
aggregations-pipeline.md)

[« Moving percentiles aggregation](search-aggregations-pipeline-moving-
percentiles-aggregation.md) [Percentiles bucket aggregation »](search-
aggregations-pipeline-percentiles-bucket-aggregation.md)

## 规范化聚合

父管道聚合，用于计算特定存储桶值的特定规范化/重新扩展值。无法使用跳过间隙策略跳过无法规范化的值。

###Syntax

"规范化"聚合孤立地如下所示：

    
    
    {
      "normalize": {
        "buckets_path": "normalized",
        "method": "percent_of_sum"
      }
    }

**表 75.'normalize_pipeline' 参数**

参数名称 |描述 |必填 |默认值 ---|---|---|--- 'buckets_path'

|

我们希望规范化的存储桶的路径(有关更多详细信息，请参阅 'buckets_path'语法)

|

Required

|   "方法"

|

具体申请方法

|

Required

|   "格式"

|

十进制格式模式的输出值。如果指定，则在聚合的"value_as_string"属性中返回格式化值

|

Optional

|

"空" ###Methodsedit

规范化聚合支持多种方法来转换存储桶值。每个方法定义都将使用以下原始存储桶值集作为示例："[5， 5， 10， 50， 10， 20]"。

_rescale_0_1_

    

此方法重新缩放数据，使最小数量为零，最大数量为 1，其余数字在两者之间线性规范化。

    
    
    x' = (x - min_x) / (max_x - min_x)
    
    
    [0, 0, .1111, 1, .1111, .3333]

_rescale_0_100_

    

此方法重新缩放数据，使最小数量为零，最大数量为 100，其余数字在两者之间线性规范化。

    
    
    x' = 100 * (x - min_x) / (max_x - min_x)
    
    
    [0, 0, 11.11, 100, 11.11, 33.33]

_percent_of_sum_

    

此方法对每个值进行规范化，以便它表示其属性到的总和的百分比。

    
    
    x' = x / sum_x
    
    
    [5%, 5%, 10%, 50%, 10%, 20%]

_mean_

    

此方法进行归一化，使每个值按其与平均值的差异程度进行归一化。

    
    
    x' = (x - mean_x) / (max_x - min_x)
    
    
    [4.63, 4.63, 9.63, 49.63, 9.63, 9.63, 19.63]

_z-score_

    

此方法进行归一化，使得每个值表示它与主题的距离相对于标准偏差

    
    
    x' = (x - mean_x) / stdev_x
    
    
    [-0.68, -0.68, -0.39, 1.94, -0.39, 0.19]

_softmax_

    

此方法进行规范化，使每个值都相对于原始值的指数之和进行指数化。

    
    
    x' = e^x / sum_e_x
    
    
    [2.862E-20, 2.862E-20, 4.248E-18, 0.999, 9.357E-14, 4.248E-18]

###Example

以下代码片段计算每月总销售额的百分比：

    
    
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
              percent_of_total_sales: {
                normalize: {
                  buckets_path: 'sales',
                  method: 'percent_of_sum',
                  format: '00.00%'
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
            "percent_of_total_sales": {
              "normalize": {
                "buckets_path": "sales",          __"method": "percent_of_sum", __"format": "00.00%" __}
            }
          }
        }
      }
    }

__

|

"buckets_path"指示此规范化聚合使用"sales"聚合的输出重新缩放---|--- __

|

"方法"设置要应用的重新缩放。在这种情况下，"percent_of_sum"将以父存储桶中所有销售额的百分比计算销售额 __

|

"format"影响如何使用Java的"DecimalFormat"模式将指标格式化为字符串。在这种情况下，乘以 100 并添加一个 _%_ 以下是响应：

    
    
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
                   "percent_of_total_sales": {
                      "value": 0.5583756345177665,
                      "value_as_string": "55.84%"
                   }
                },
                {
                   "key_as_string": "2015/02/01 00:00:00",
                   "key": 1422748800000,
                   "doc_count": 2,
                   "sales": {
                      "value": 60.0
                   },
                   "percent_of_total_sales": {
                      "value": 0.06091370558375635,
                      "value_as_string": "06.09%"
                   }
                },
                {
                   "key_as_string": "2015/03/01 00:00:00",
                   "key": 1425168000000,
                   "doc_count": 2,
                   "sales": {
                      "value": 375.0
                   },
                   "percent_of_total_sales": {
                      "value": 0.38071065989847713,
                      "value_as_string": "38.07%"
                   }
                }
             ]
          }
       }
    }

[« Moving percentiles aggregation](search-aggregations-pipeline-moving-
percentiles-aggregation.md) [Percentiles bucket aggregation »](search-
aggregations-pipeline-percentiles-bucket-aggregation.md)
