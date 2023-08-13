

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Pipeline aggregations](search-
aggregations-pipeline.md)

[« Bucket selector aggregation](search-aggregations-pipeline-bucket-selector-
aggregation.md) [Change point aggregation »](search-aggregations-change-
point-aggregation.md)

## 桶排序聚合

父管道聚合，用于对其父多存储桶聚合的存储桶进行排序。可以将零个或多个排序字段与相应的排序顺序一起指定。每个存储桶可以根据其"_key"、"_count"或其子聚合进行排序。此外，可以设置参数"from"和"size"以截断结果存储桶。

与所有管道聚合一样，"bucket_sort"聚合在所有其他非管道聚合之后执行。这意味着排序仅适用于已从父聚合返回的任何存储桶。例如，如果父聚合为"术语"，并且其"大小"设置为"10"，则"bucket_sort"将仅对这 10 个返回的术语存储桶进行排序。

###Syntax

"bucket_sort"聚合单独如下所示：

    
    
    {
      "bucket_sort": {
        "sort": [
          { "sort_field_1": { "order": "asc" } },   __{ "sort_field_2": { "order": "desc" } },
          "sort_field_3"
        ],
        "from": 1,
        "size": 3
      }
    }

__

|

在这里，"sort_field_1"是要用作主排序的变量的存储桶路径，其顺序是升序。   ---|--- **表 56.'bucket_sort' 参数**

参数名称 |描述 |必填 |默认值---|---|---|---"排序"

|

要作为排序依据的字段列表。有关更多详细信息，请参阅"排序"。

|

Optional

|   "从"

|

位于设定值之前的位置的存储桶将被截断。

|

Optional

|

"0""大小"

|

要返回的存储桶数。默认为父聚合的所有存储桶。

|

Optional

|   "gap_policy"

|

在数据中发现差距时要应用的策略(有关更多详细信息，请参阅处理数据中的差距)

|

Optional

|

"跳过" 以下代码片段按降序返回与总销售额最高的 3 个月对应的存储桶：

    
    
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
              sales_bucket_sort: {
                bucket_sort: {
                  sort: [
                    {
                      total_sales: {
                        order: 'desc'
                      }
                    }
                  ],
                  size: 3
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
            "sales_bucket_sort": {
              "bucket_sort": {
                "sort": [
                  { "total_sales": { "order": "desc" } } __],
                "size": 3 __}
            }
          }
        }
      }
    }

__

|

"sort"设置为按降序使用"total_sales"的值---|---__

|

"大小"设置为"3"，表示将仅返回"total_sales"中的前 3 个月 以下是响应：

    
    
    {
       "took": 82,
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
                },
                {
                   "key_as_string": "2015/03/01 00:00:00",
                   "key": 1425168000000,
                   "doc_count": 2,
                   "total_sales": {
                       "value": 375.0
                   }
                },
                {
                   "key_as_string": "2015/02/01 00:00:00",
                   "key": 1422748800000,
                   "doc_count": 2,
                   "total_sales": {
                       "value": 60.0
                   }
                }
             ]
          }
       }
    }

### 截断而不排序

也可以使用此聚合来截断结果桶，而无需执行任何排序。为此，只需使用"from"和/或"size"参数，而无需指定"sort"。

以下示例只是截断结果，以便仅返回第二个存储桶：

    
    
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
              bucket_truncate: {
                bucket_sort: {
                  from: 1,
                  size: 1
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
            "bucket_truncate": {
              "bucket_sort": {
                "from": 1,
                "size": 1
              }
            }
          }
        }
      }
    }

Response:

    
    
    {
       "took": 11,
       "timed_out": false,
       "_shards": ...,
       "hits": ...,
       "aggregations": {
          "sales_per_month": {
             "buckets": [
                {
                   "key_as_string": "2015/02/01 00:00:00",
                   "key": 1422748800000,
                   "doc_count": 2
                }
             ]
          }
       }
    }

[« Bucket selector aggregation](search-aggregations-pipeline-bucket-selector-
aggregation.md) [Change point aggregation »](search-aggregations-change-
point-aggregation.md)
