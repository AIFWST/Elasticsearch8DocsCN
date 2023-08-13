

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md)

[« Weighted avg aggregation](search-aggregations-metrics-weight-avg-
aggregation.md) [Average bucket aggregation »](search-aggregations-pipeline-
avg-bucket-aggregation.md)

## 管道聚合

管道聚合处理从其他聚合而不是文档集生成的输出，从而将信息添加到输出树。有许多不同类型的管道聚合，每种聚合计算的信息都与其他聚合不同，但这些类型可以分为两个系列：

_Parent_

     A family of pipeline aggregations that is provided with the output of its parent aggregation and is able to compute new buckets or new aggregations to add to existing buckets. 
_Sibling_

     Pipeline aggregations that are provided with the output of a sibling aggregation and are able to compute a new aggregation which will be at the same level as the sibling aggregation. 

管道聚合可以使用"buckets_path"参数来指示所需指标的路径，从而引用执行计算所需的聚合。定义这些路径的语法可以在下面的"buckets_path"语法部分找到。

管道聚合不能有子聚合，但根据类型，它可以在"buckets_path"中引用另一个管道，从而允许管道聚合链接。例如，您可以将两个导数链接在一起以计算二阶导数(即辅助导数)。

由于管道聚合仅添加到输出中，因此在链接管道聚合时，每个管道聚合的输出将包含在最终输出中。

### 'buckets_path'语法

大多数管道聚合需要另一个聚合作为其输入。输入聚合通过"buckets_path"参数定义，该参数遵循特定格式：

    
    
    AGG_SEPARATOR       =  `>` ;
    METRIC_SEPARATOR    =  `.` ;
    AGG_NAME            =  <the name of the aggregation> ;
    METRIC              =  <the name of the metric (in case of multi-value metrics aggregation)> ;
    MULTIBUCKET_KEY     =  `[<KEY_NAME>]`
    PATH                =  <AGG_NAME><MULTIBUCKET_KEY>? (<AGG_SEPARATOR>, <AGG_NAME> )* ( <METRIC_SEPARATOR>, <METRIC> ) ;

例如，路径"my_bucket>my_stats.avg"将路径为"my_stats"指标中的"avg"值，该指标包含在"my_bucket"存储桶聚合中。

以下是更多示例：

* "multi_bucket["foo"]>single_bucket>multi_metric.avg' 将转到"multi_metric"AGG 中的""AGG 中的"平均值"指标，该指标位于"multi_bucket"多存储桶聚合的"foo"存储桶中的单个存储桶"single_bucket"下。  * 'agg1["foo"]._count' 将获取多存储桶聚合 "multi_bucket"中"foo"存储桶的"_count"指标

路径相对于管道聚合的位置;它们不是绝对路径，并且路径不能返回到聚合树的"向上"。例如，此导数嵌入在date_histogram中，并引用"同级"度量""the_sum"：

    
    
    response = client.search(
      body: {
        aggregations: {
          my_date_histo: {
            date_histogram: {
              field: 'timestamp',
              calendar_interval: 'day'
            },
            aggregations: {
              the_sum: {
                sum: {
                  field: 'lemmings'
                }
              },
              the_deriv: {
                derivative: {
                  buckets_path: 'the_sum'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /_search
    {
      "aggs": {
        "my_date_histo": {
          "date_histogram": {
            "field": "timestamp",
            "calendar_interval": "day"
          },
          "aggs": {
            "the_sum": {
              "sum": { "field": "lemmings" }              __},
            "the_deriv": {
              "derivative": { "buckets_path": "the_sum" } __}
          }
        }
      }
    }

__

|

该指标称为"the_sum"---|---__

|

"buckets_path"是指通过相对路径"the_sum"的指标 "buckets_path"也用于同级管道聚合，其中聚合是一系列存储桶的"下一个"，而不是嵌入"内部"。例如，"max_bucket"聚合使用"buckets_path"指定嵌入在同级聚合中的指标：

    
    
    response = client.search(
      body: {
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
              }
            }
          },
          max_monthly_sales: {
            max_bucket: {
              buckets_path: 'sales_per_month>sales'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /_search
    {
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
            }
          }
        },
        "max_monthly_sales": {
          "max_bucket": {
            "buckets_path": "sales_per_month>sales" __}
        }
      }
    }

__

|

"buckets_path"指示此max_bucket聚合，我们希望"sales_per_month"日期直方图中"销售"聚合的最大值。   ---|--- 如果同级管道 agg 引用多存储桶聚合(例如"terms"agg)，它还可以选择从多存储桶中选择特定键。例如，"bucket_script"可以选择两个特定的存储桶(通过其存储桶键)来执行计算：

    
    
    response = client.search(
      body: {
        aggregations: {
          sales_per_month: {
            date_histogram: {
              field: 'date',
              calendar_interval: 'month'
            },
            aggregations: {
              sale_type: {
                terms: {
                  field: 'type'
                },
                aggregations: {
                  sales: {
                    sum: {
                      field: 'price'
                    }
                  }
                }
              },
              hat_vs_bag_ratio: {
                bucket_script: {
                  buckets_path: {
                    hats: "sale_type['hat']>sales",
                    bags: "sale_type['bag']>sales"
                  },
                  script: 'params.hats / params.bags'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /_search
    {
      "aggs": {
        "sales_per_month": {
          "date_histogram": {
            "field": "date",
            "calendar_interval": "month"
          },
          "aggs": {
            "sale_type": {
              "terms": {
                "field": "type"
              },
              "aggs": {
                "sales": {
                  "sum": {
                    "field": "price"
                  }
                }
              }
            },
            "hat_vs_bag_ratio": {
              "bucket_script": {
                "buckets_path": {
                  "hats": "sale_type['hat']>sales",   __"bags": "sale_type['bag'] >sales"    __},
                "script": "params.hats / params.bags"
              }
            }
          }
        }
      }
    }

__

|

"buckets_path"专门选择要在脚本中使用的帽子和袋子桶(通过"帽子"]/"["袋子"]")，而不是从"sale_type"聚合中获取所有桶 ---|--- ### 特殊路径[编辑]

"buckets_path"可以使用特殊的"_count"路径，而不是路径到指标。这将指示管道聚合使用文档计数作为其输入。例如，可以根据每个存储桶的文档计数而不是特定指标计算导数：

    
    
    response = client.search(
      body: {
        aggregations: {
          my_date_histo: {
            date_histogram: {
              field: 'timestamp',
              calendar_interval: 'day'
            },
            aggregations: {
              the_deriv: {
                derivative: {
                  buckets_path: '_count'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /_search
    {
      "aggs": {
        "my_date_histo": {
          "date_histogram": {
            "field": "timestamp",
            "calendar_interval": "day"
          },
          "aggs": {
            "the_deriv": {
              "derivative": { "buckets_path": "_count" } __}
          }
        }
      }
    }

__

|

通过使用"_count"而不是指标名称，我们可以计算直方图中文档计数的导数 ---|--- "buckets_path"还可以使用"_bucket_count"和多存储桶聚合的路径，以使用该聚合在管道聚合中返回的存储桶数，而不是指标。例如，此处可以使用"bucket_selector"来过滤掉不包含内部术语聚合存储桶的存储桶：

    
    
    response = client.search(
      index: 'sales',
      body: {
        size: 0,
        aggregations: {
          histo: {
            date_histogram: {
              field: 'date',
              calendar_interval: 'day'
            },
            aggregations: {
              categories: {
                terms: {
                  field: 'category'
                }
              },
              min_bucket_selector: {
                bucket_selector: {
                  buckets_path: {
                    count: 'categories._bucket_count'
                  },
                  script: {
                    source: 'params.count != 0'
                  }
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
        "histo": {
          "date_histogram": {
            "field": "date",
            "calendar_interval": "day"
          },
          "aggs": {
            "categories": {
              "terms": {
                "field": "category"
              }
            },
            "min_bucket_selector": {
              "bucket_selector": {
                "buckets_path": {
                  "count": "categories._bucket_count" __},
                "script": {
                  "source": "params.count != 0"
                }
              }
            }
          }
        }
      }
    }

__

|

通过使用"_bucket_count"而不是指标名称，我们可以过滤掉不包含"类别"聚合---|--- ### 处理 agggnamesedit 中的点

支持另一种语法来处理名称中包含点的聚合或指标，例如第 99.9 个百分位数。此指标可称为：

    
    
    "buckets_path": "my_percentile[99.9]"

### 处理数据中的差距

现实世界中的数据通常是嘈杂的，有时包含**间隙** - 数据根本不存在的地方。发生这种情况的原因有多种，最常见的是：

* 落入存储桶的文档不包含必填字段 * 没有与一个或多个存储桶的查询匹配的文档 * 正在计算的指标无法生成值，可能是因为另一个依赖存储桶缺少值。一些管道聚合具有必须满足的特定要求(例如，导数无法计算第一个值的度量，因为没有先前的值，HoltWinters 移动平均线需要"预热"数据才能开始计算，等等)

间隙策略是一种机制，用于在遇到"gappy"或缺失数据时通知管道聚合所需的行为。所有管道聚合都接受"gap_policy"参数。目前有两种差距策略可供选择：

_skip_

     This option treats missing data as if the bucket does not exist. It will skip the bucket and continue calculating using the next available value. 
_insert_zeros_

     This option will replace missing values with a zero (`0`) and pipeline aggregation computation will proceed as normal. 
_keep_values_

     This option is similar to skip, except if the metric provides a non-null, non-NaN value this value is used, otherwise the empty bucket is skipped. 

[« Weighted avg aggregation](search-aggregations-metrics-weight-avg-
aggregation.md) [Average bucket aggregation »](search-aggregations-pipeline-
avg-bucket-aggregation.md)
