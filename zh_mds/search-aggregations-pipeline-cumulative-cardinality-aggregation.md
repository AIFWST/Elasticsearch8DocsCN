

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Pipeline aggregations](search-
aggregations-pipeline.md)

[« Change point aggregation](search-aggregations-change-point-
aggregation.md) [Cumulative sum aggregation »](search-aggregations-pipeline-
cumulative-sum-aggregation.md)

## 累积基数聚合

父管道聚合，用于计算父直方图(或date_histogram)聚合中的累积基数。指定的指标必须是基数聚合，封闭直方图必须将"min_doc_count"设置为"0"("直方图"聚合的默认值)。

"cumulative_cardinality"agg 对于查找"新项目总数"很有用，例如每天您网站的新访问者数量。常规基数聚合将告诉您每天有多少唯一身份访问者，但不区分"新"或"重复"访问者。累积基数聚合可用于确定每天有多少唯一身份访问者是"新访客"。

###Syntax

"cumulative_cardinality"聚合单独如下所示：

    
    
    {
      "cumulative_cardinality": {
        "buckets_path": "my_cardinality_agg"
      }
    }

**表 57.'cumulative_cardinality' 参数**

参数名称 |描述 |必填 |默认值 ---|---|---|--- 'buckets_path'

|

我们希望找到累积基数的基数聚合路径(有关更多详细信息，请参阅"buckets_path"语法)

|

Required

|   "格式"

|

十进制格式模式的输出值。如果指定，则在聚合的"value_as_string"属性中返回格式化值

|

Optional

|

"null" 以下代码段计算每日"用户"总数的累积基数：

    
    
    response = client.search(
      index: 'user_hits',
      body: {
        size: 0,
        aggregations: {
          users_per_day: {
            date_histogram: {
              field: 'timestamp',
              calendar_interval: 'day'
            },
            aggregations: {
              distinct_users: {
                cardinality: {
                  field: 'user_id'
                }
              },
              total_new_users: {
                cumulative_cardinality: {
                  buckets_path: 'distinct_users'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /user_hits/_search
    {
      "size": 0,
      "aggs": {
        "users_per_day": {
          "date_histogram": {
            "field": "timestamp",
            "calendar_interval": "day"
          },
          "aggs": {
            "distinct_users": {
              "cardinality": {
                "field": "user_id"
              }
            },
            "total_new_users": {
              "cumulative_cardinality": {
                "buckets_path": "distinct_users" __}
            }
          }
        }
      }
    }

__

|

"buckets_path"指示此聚合将"distinct_users"聚合的输出用于累积基数---|--- 以下是响应：

    
    
    {
       "took": 11,
       "timed_out": false,
       "_shards": ...,
       "hits": ...,
       "aggregations": {
          "users_per_day": {
             "buckets": [
                {
                   "key_as_string": "2019-01-01T00:00:00.000Z",
                   "key": 1546300800000,
                   "doc_count": 2,
                   "distinct_users": {
                      "value": 2
                   },
                   "total_new_users": {
                      "value": 2
                   }
                },
                {
                   "key_as_string": "2019-01-02T00:00:00.000Z",
                   "key": 1546387200000,
                   "doc_count": 2,
                   "distinct_users": {
                      "value": 2
                   },
                   "total_new_users": {
                      "value": 3
                   }
                },
                {
                   "key_as_string": "2019-01-03T00:00:00.000Z",
                   "key": 1546473600000,
                   "doc_count": 3,
                   "distinct_users": {
                      "value": 3
                   },
                   "total_new_users": {
                      "value": 4
                   }
                }
             ]
          }
       }
    }

请注意，第二天"2019-01-02"有两个不同的用户，但累积管道 agg 生成的"total_new_users"指标仅递增到三个。这意味着当天的两个用户中只有一个没有出现，另一个在前一天已经见过。这种情况在第三天再次发生，其中三个用户中只有一个是全新的。

### 增量累积基数

"cumulative_cardinality"agg 将显示自查询时间段开始以来的总非重复计数。但是，有时查看"增量"计数很有用。这意味着每天添加的新用户数，而不是累积总数。

这可以通过在查询中添加"导数"聚合来实现：

    
    
    response = client.search(
      index: 'user_hits',
      body: {
        size: 0,
        aggregations: {
          users_per_day: {
            date_histogram: {
              field: 'timestamp',
              calendar_interval: 'day'
            },
            aggregations: {
              distinct_users: {
                cardinality: {
                  field: 'user_id'
                }
              },
              total_new_users: {
                cumulative_cardinality: {
                  buckets_path: 'distinct_users'
                }
              },
              incremental_new_users: {
                derivative: {
                  buckets_path: 'total_new_users'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /user_hits/_search
    {
      "size": 0,
      "aggs": {
        "users_per_day": {
          "date_histogram": {
            "field": "timestamp",
            "calendar_interval": "day"
          },
          "aggs": {
            "distinct_users": {
              "cardinality": {
                "field": "user_id"
              }
            },
            "total_new_users": {
              "cumulative_cardinality": {
                "buckets_path": "distinct_users"
              }
            },
            "incremental_new_users": {
              "derivative": {
                "buckets_path": "total_new_users"
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
          "users_per_day": {
             "buckets": [
                {
                   "key_as_string": "2019-01-01T00:00:00.000Z",
                   "key": 1546300800000,
                   "doc_count": 2,
                   "distinct_users": {
                      "value": 2
                   },
                   "total_new_users": {
                      "value": 2
                   }
                },
                {
                   "key_as_string": "2019-01-02T00:00:00.000Z",
                   "key": 1546387200000,
                   "doc_count": 2,
                   "distinct_users": {
                      "value": 2
                   },
                   "total_new_users": {
                      "value": 3
                   },
                   "incremental_new_users": {
                      "value": 1.0
                   }
                },
                {
                   "key_as_string": "2019-01-03T00:00:00.000Z",
                   "key": 1546473600000,
                   "doc_count": 3,
                   "distinct_users": {
                      "value": 3
                   },
                   "total_new_users": {
                      "value": 4
                   },
                   "incremental_new_users": {
                      "value": 1.0
                   }
                }
             ]
          }
       }
    }

[« Change point aggregation](search-aggregations-change-point-
aggregation.md) [Cumulative sum aggregation »](search-aggregations-pipeline-
cumulative-sum-aggregation.md)
