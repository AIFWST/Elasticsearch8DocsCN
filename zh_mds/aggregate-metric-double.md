

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Field data types](mapping-types.md) [Alias field type »](field-
alias.md)

## 聚合指标字段类型

存储指标聚合的预聚合数值。"aggregate_metric_double"字段是包含以下一个或多个指标子字段的对象："最小值"、"最大值"、"总和"和"value_count"。

当您在"aggregate_metric_double"字段上运行某些指标聚合时，聚合将使用相关子字段的值。例如，"aggregate_metric_double"字段上的"min"聚合返回所有"min"子字段的最小值。

"aggregate_metric_double"字段为每个指标子字段存储一个数字文档值。不支持数组值。"最小值"、"最大值"和"总和"值是"双精度"数字。"value_count"是一个正的"长"数。

    
    
    response = client.indices.create(
      index: 'my-index',
      body: {
        mappings: {
          properties: {
            "my-agg-metric-field": {
              type: 'aggregate_metric_double',
              metrics: [
                'min',
                'max',
                'sum',
                'value_count'
              ],
              default_metric: 'max'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index
    {
      "mappings": {
        "properties": {
          "my-agg-metric-field": {
            "type": "aggregate_metric_double",
            "metrics": [ "min", "max", "sum", "value_count" ],
            "default_metric": "max"
          }
        }
      }
    }

### "aggregate_metric_double"字段的参数

`metrics`

     (Required, array of strings) Array of metric sub-fields to store. Each value corresponds to a [metric aggregation](search-aggregations-metrics.html "Metrics aggregations"). Valid values are [`min`](search-aggregations-metrics-min-aggregation.html "Min aggregation"), [`max`](search-aggregations-metrics-max-aggregation.html "Max aggregation"), [`sum`](search-aggregations-metrics-sum-aggregation.html "Sum aggregation"), and [`value_count`](search-aggregations-metrics-valuecount-aggregation.html "Value count aggregation"). You must specify at least one value. 
`default_metric`

     (Required, string) Default metric sub-field to use for queries, scripts, and aggregations that don't use a sub-field. Must be a value from the `metrics` array. 
`time_series_metric`

    

(可选，字符串)将字段标记为时序指标。该值是指标类型。您无法更新现有字段的此参数。

"aggregate_metric_double"字段的有效"time_series_metric"值

`gauge`

     A metric that represents a single numeric that can arbitrarily increase or decrease. For example, a temperature or available disk space. 
`null` (Default)

     Not a time series metric. 

###Uses

我们设计了"aggregate_metric_double"字段以用于以下聚合：

* "min"聚合返回所有"min"子字段的最小值。  * "max"聚合返回所有"max"子字段的最大值。  * "sum"聚合返回所有"sum"子字段的值的总和。  * "value_count"聚合返回所有"value_count"子字段的值之和。  * "平均"聚合。没有"平均"子字段;"AVG"聚合的结果是使用"总和"和"value_count"指标计算的。要运行"avg"聚合，该字段必须同时包含"总和"和"value_count"指标子字段。

在"aggregate_metric_double"字段上运行任何其他聚合将失败，并显示"不支持的聚合"错误。

最后，"aggregate_metric_double"字段支持以下查询，它通过将行为委托给其"default_metric"子字段来表现为"双精度"：

* "存在" * "范围" * "术语" * "术语"

###Examples

以下创建索引 APIrequest 使用名为"agg_metric"的"aggregate_metric_double"字段创建一个索引。请求将"max"设置为字段的"default_metric"。

    
    
    response = client.indices.create(
      index: 'stats-index',
      body: {
        mappings: {
          properties: {
            agg_metric: {
              type: 'aggregate_metric_double',
              metrics: [
                'min',
                'max',
                'sum',
                'value_count'
              ],
              default_metric: 'max'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT stats-index
    {
      "mappings": {
        "properties": {
          "agg_metric": {
            "type": "aggregate_metric_double",
            "metrics": [ "min", "max", "sum", "value_count" ],
            "default_metric": "max"
          }
        }
      }
    }

以下索引 API 请求在"agg_metric"字段中添加具有预聚合数据的文档。

    
    
    response = client.index(
      index: 'stats-index',
      id: 1,
      body: {
        agg_metric: {
          min: -302.5,
          max: 702.3,
          sum: 200,
          value_count: 25
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'stats-index',
      id: 2,
      body: {
        agg_metric: {
          min: -93,
          max: 1702.3,
          sum: 300,
          value_count: 25
        }
      }
    )
    puts response
    
    
    PUT stats-index/_doc/1
    {
      "agg_metric": {
        "min": -302.50,
        "max": 702.30,
        "sum": 200.0,
        "value_count": 25
      }
    }
    
    PUT stats-index/_doc/2
    {
      "agg_metric": {
        "min": -93.00,
        "max": 1702.30,
        "sum": 300.00,
        "value_count": 25
      }
    }

您可以在"agg_metric"字段上运行"最小"、"最大值"、"总和"、"value_count"和"平均值"聚合。

    
    
    response = client.search(
      index: 'stats-index',
      size: 0,
      body: {
        aggregations: {
          metric_min: {
            min: {
              field: 'agg_metric'
            }
          },
          metric_max: {
            max: {
              field: 'agg_metric'
            }
          },
          metric_value_count: {
            value_count: {
              field: 'agg_metric'
            }
          },
          metric_sum: {
            sum: {
              field: 'agg_metric'
            }
          },
          metric_avg: {
            avg: {
              field: 'agg_metric'
            }
          }
        }
      }
    )
    puts response
    
    
    POST stats-index/_search?size=0
    {
      "aggs": {
        "metric_min": { "min": { "field": "agg_metric" } },
        "metric_max": { "max": { "field": "agg_metric" } },
        "metric_value_count": { "value_count": { "field": "agg_metric" } },
        "metric_sum": { "sum": { "field": "agg_metric" } },
        "metric_avg": { "avg": { "field": "agg_metric" } }
      }
    }

聚合结果基于相关的指标子字段值。

    
    
    {
    ...
      "aggregations": {
        "metric_min": {
          "value": -302.5
        },
        "metric_max": {
          "value": 1702.3
        },
        "metric_value_count": {
          "value": 50
        },
        "metric_sum": {
          "value": 500.0
        },
        "metric_avg": {
          "value": 10.0
        }
      }
    }

对"aggregate_metric_double"字段的查询使用"default_metric"值。

    
    
    response = client.search(
      index: 'stats-index',
      body: {
        query: {
          term: {
            agg_metric: {
              value: 702.3
            }
          }
        }
      }
    )
    puts response
    
    
    GET stats-index/_search
    {
      "query": {
        "term": {
          "agg_metric": {
            "value": 702.30
          }
        }
      }
    }

搜索将返回以下命中。"default_metric"字段"max"的值与查询值匹配。

    
    
    {
      ...
        "hits": {
        "total": {
          "value": 1,
          "relation": "eq"
        },
        "max_score": 1.0,
        "hits": [
          {
            "_index": "stats-index",
            "_id": "1",
            "_score": 1.0,
            "_source": {
              "agg_metric": {
                "min": -302.5,
                "max": 702.3,
                "sum": 200.0,
                "value_count": 25
              }
            }
          }
        ]
      }
    }

### 合成的"_source"

合成"_source"仅对 TSDB 索引(将"index.mode"设置为"time_series"的索引)正式发布。对于其他指数，合成"_source"处于技术预览状态。技术预览版中的功能可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

"aggregate_metric-double"字段在其默认配置中支持合成"_source"。合成"_source"不能与"ignore_malformed"一起使用。

例如：

    
    
    response = client.indices.create(
      index: 'idx',
      body: {
        mappings: {
          _source: {
            mode: 'synthetic'
          },
          properties: {
            agg_metric: {
              type: 'aggregate_metric_double',
              metrics: [
                'min',
                'max',
                'sum',
                'value_count'
              ],
              default_metric: 'max'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'idx',
      id: 1,
      body: {
        agg_metric: {
          min: -302.5,
          max: 702.3,
          sum: 200,
          value_count: 25
        }
      }
    )
    puts response
    
    
    PUT idx
    {
      "mappings": {
        "_source": { "mode": "synthetic" },
        "properties": {
          "agg_metric": {
            "type": "aggregate_metric_double",
            "metrics": [ "min", "max", "sum", "value_count" ],
            "default_metric": "max"
          }
        }
      }
    }
    
    PUT idx/_doc/1
    {
      "agg_metric": {
        "min": -302.50,
        "max": 702.30,
        "sum": 200.0,
        "value_count": 25
      }
    }

将成为：

    
    
    {
      "agg_metric": {
        "min": -302.50,
        "max": 702.30,
        "sum": 200.0,
        "value_count": 25
      }
    }

[« Field data types](mapping-types.md) [Alias field type »](field-
alias.md)
