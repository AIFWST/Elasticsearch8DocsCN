

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Pipeline aggregations](search-
aggregations-pipeline.md)

[« Bucket correlation aggregation](search-aggregations-bucket-correlation-
aggregation.md) [Bucket sort aggregation »](search-aggregations-pipeline-
bucket-sort-aggregation.md)

## 存储桶选择器聚合

父管道聚合，执行一个脚本，该脚本确定当前存储桶是否将保留在父多存储桶聚合中。指定的指标必须是数字，并且脚本必须返回布尔值。如果脚本语言是"表达式"，则允许使用数字返回值。在这种情况下，0.0 将被评估为"false"，所有其他值的计算结果将为 true。

与所有管道聚合一样，bucket_selector聚合在所有其他同级聚合之后执行。这意味着使用thebucket_selector聚合筛选响应中返回的存储桶不会节省运行聚合的执行时间。

###Syntax

"bucket_selector"聚合单独如下所示：

    
    
    {
      "bucket_selector": {
        "buckets_path": {
          "my_var1": "the_sum",                     __"my_var2": "the_value_count"
        },
        "script": "params.my_var1 > params.my_var2"
      }
    }

__

|

此处，"my_var1"是要在脚本中使用的此存储桶路径的变量名称，"the_sum"是要用于该变量的指标的路径。   ---|--- **表 55.'bucket_selector' 参数**

参数名称 |描述 |必填 |默认值 ---|---|---|--- 'script'

|

要为此聚合运行的脚本。脚本可以是内联的、文件或索引的。(有关更多详细信息，请参阅脚本)

|

Required

|   "buckets_path"

|

脚本变量及其关联路径的映射，指向我们希望用于变量的存储桶(有关更多详细信息，请参阅"buckets_path"语法)

|

Required

|   "gap_policy"

|

在数据中发现差距时要应用的策略(有关更多详细信息，请参阅处理数据中的差距)

|

Optional

|

"跳过" 以下代码段仅保留当月总销售额超过 200 的存储桶：

    
    
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
              total_sales: {
                sum: {
                  field: 'price'
                }
              },
              sales_bucket_filter: {
                bucket_selector: {
                  buckets_path: {
                    "totalSales": 'total_sales'
                  },
                  script: 'params.totalSales > 200'
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
            "total_sales": {
              "sum": {
                "field": "price"
              }
            },
            "sales_bucket_filter": {
              "bucket_selector": {
                "buckets_path": {
                  "totalSales": "total_sales"
                },
                "script": "params.totalSales > 200"
              }
            }
          }
        }
      }
    }

以下是可能的响应：

    
    
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
                   "total_sales": {
                       "value": 550.0
                   }
                }, __{
                   "key_as_string": "2015/03/01 00:00:00",
                   "key": 1425168000000,
                   "doc_count": 2,
                   "total_sales": {
                       "value": 375.0
                   }
                }
             ]
          }
       }
    }

__

|

"2015/02/01 00：00：00"的存储桶已被删除，因为其总销售额低于 200 ---|--- « 桶相关聚合 桶排序聚合 »