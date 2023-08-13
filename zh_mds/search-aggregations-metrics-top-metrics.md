

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« Top hits aggregation](search-aggregations-metrics-top-hits-
aggregation.md) [Value count aggregation »](search-aggregations-metrics-
valuecount-aggregation.md)

## 顶级指标聚合

"top_metrics"聚合从文档中选择具有最大或最小"排序"值的指标。例如，这将获取文档中最大值为 's' 的 'm' 字段的值：

    
    
    response = client.bulk(
      index: 'test',
      refresh: true,
      body: [
        {
          index: {}
        },
        {
          s: 1,
          m: 3.1415
        },
        {
          index: {}
        },
        {
          s: 2,
          m: 1
        },
        {
          index: {}
        },
        {
          s: 3,
          m: 2.71828
        }
      ]
    )
    puts response
    
    response = client.search(
      index: 'test',
      filter_path: 'aggregations',
      body: {
        aggregations: {
          tm: {
            top_metrics: {
              metrics: {
                field: 'm'
              },
              sort: {
                s: 'desc'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /test/_bulk?refresh
    {"index": {}}
    {"s": 1, "m": 3.1415}
    {"index": {}}
    {"s": 2, "m": 1.0}
    {"index": {}}
    {"s": 3, "m": 2.71828}
    POST /test/_search?filter_path=aggregations
    {
      "aggs": {
        "tm": {
          "top_metrics": {
            "metrics": {"field": "m"},
            "sort": {"s": "desc"}
          }
        }
      }
    }

其中返回：

    
    
    {
      "aggregations": {
        "tm": {
          "top": [ {"sort": [3], "metrics": {"m": 2.718280076980591 } } ]
        }
      }
    }

"top_metrics"在精神上与"top_hits"非常相似，但由于它更有限，因此它能够使用更少的内存来完成其工作，并且通常更快。

###'排序'

指标请求中的"排序"字段与搜索请求中的"排序"字段的功能完全相同，但以下情况除外：

* 它不能用于二进制、平展、ip、关键字或文本字段。  * 它仅支持单个排序值，因此未指定哪个文档赢得领带。

聚合返回的指标是搜索请求返回的第一个匹配。所以

'"sort"： {"s"： "desc"}'

     gets metrics from the document with the highest `s`
`"sort": {"s": "asc"}`

     gets the metrics from the document with the lowest `s`
`"sort": {"_geo_distance": {"location": "POINT (-78.6382 35.7796)"}}`

     gets metrics from the documents with `location` **closest** to `35.7796, -78.6382`
`"sort": "_score"`

     gets metrics from the document with the highest score 

###'指标'

"指标"选择要返回的"顶部"文档的字段。您可以通过请求诸如"指标"：[{"字段"： "m"}，{"字段"： "i"} 之类的指标列表来请求单个指标，也可以请求多个指标，例如 "指标"： [{"字段"： "m"}，{"字段"： "i"}"。

"metrics.field"支持以下字段类型：

* "布尔值" * "IP" * 关键字 * 数字

除关键字外，还支持相应类型的运行时字段。"metrics.field"不支持具有数组值的字段。数组值上的"top_metric"聚合可能会返回不一致的结果。

以下示例对多个字段类型运行"top_metrics"聚合。

    
    
    response = client.indices.create(
      index: 'test',
      body: {
        mappings: {
          properties: {
            d: {
              type: 'date'
            }
          }
        }
      }
    )
    puts response
    
    response = client.bulk(
      index: 'test',
      refresh: true,
      body: [
        {
          index: {}
        },
        {
          s: 1,
          m: 3.1415,
          i: 1,
          d: '2020-01-01T00:12:12Z',
          t: 'cat'
        },
        {
          index: {}
        },
        {
          s: 2,
          m: 1,
          i: 6,
          d: '2020-01-02T00:12:12Z',
          t: 'dog'
        },
        {
          index: {}
        },
        {
          s: 3,
          m: 2.71828,
          i: -12,
          d: '2019-12-31T00:12:12Z',
          t: 'chicken'
        }
      ]
    )
    puts response
    
    response = client.search(
      index: 'test',
      filter_path: 'aggregations',
      body: {
        aggregations: {
          tm: {
            top_metrics: {
              metrics: [
                {
                  field: 'm'
                },
                {
                  field: 'i'
                },
                {
                  field: 'd'
                },
                {
                  field: 't.keyword'
                }
              ],
              sort: {
                s: 'desc'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /test
    {
      "mappings": {
        "properties": {
          "d": {"type": "date"}
        }
      }
    }
    POST /test/_bulk?refresh
    {"index": {}}
    {"s": 1, "m": 3.1415, "i": 1, "d": "2020-01-01T00:12:12Z", "t": "cat"}
    {"index": {}}
    {"s": 2, "m": 1.0, "i": 6, "d": "2020-01-02T00:12:12Z", "t": "dog"}
    {"index": {}}
    {"s": 3, "m": 2.71828, "i": -12, "d": "2019-12-31T00:12:12Z", "t": "chicken"}
    POST /test/_search?filter_path=aggregations
    {
      "aggs": {
        "tm": {
          "top_metrics": {
            "metrics": [
              {"field": "m"},
              {"field": "i"},
              {"field": "d"},
              {"field": "t.keyword"}
            ],
            "sort": {"s": "desc"}
          }
        }
      }
    }

其中返回：

    
    
    {
      "aggregations": {
        "tm": {
          "top": [ {
            "sort": [3],
            "metrics": {
              "m": 2.718280076980591,
              "i": -12,
              "d": "2019-12-31T00:12:12.000Z",
              "t.keyword": "chicken"
            }
          } ]
        }
      }
    }

###'失踪'

"missing"参数定义如何处理具有缺失值的文档。默认情况下，如果缺少任何关键组件，则忽略整个文档。通过使用"missing"参数，可以将缺少的组件视为具有值。

    
    
    PUT /my-index
    {
      "mappings": {
        "properties": {
          "nr":    { "type": "integer" },
          "state":  { "type": "keyword"  } __}
      }
    }
    POST /my-index/_bulk?refresh
    {"index": {}}
    {"nr": 1, "state": "started"}
    {"index": {}}
    {"nr": 2, "state": "stopped"}
    {"index": {}}
    {"nr": 3, "state": "N/A"}
    {"index": {}}
    {"nr": 4} __POST /my-index/_search?filter_path=aggregations
    {
      "aggs": {
        "my_top_metrics": {
          "top_metrics": {
            "metrics": {
              "field": "state",
              "missing": "N/A"}, __"sort": {"nr": "desc"}
          }
        }
      }
    }

__

|

如果要对文本内容使用聚合，它必须是"关键字"类型字段，或者必须在该字段上启用字段数据。   ---|---    __

|

此文档缺少"状态"字段值。   __

|

"missing"参数定义，如果"state"字段具有缺失值，则应将其视为具有"N/A"值。   该请求将产生以下响应：

    
    
    {
      "aggregations": {
        "my_top_metrics": {
          "top": [
            {
              "sort": [
                4
              ],
              "metrics": {
                "state": "N/A"
              }
            }
          ]
        }
      }
    }

###'大小'

"top_metrics"可以使用 size 参数返回前几个文档的指标：

    
    
    response = client.bulk(
      index: 'test',
      refresh: true,
      body: [
        {
          index: {}
        },
        {
          s: 1,
          m: 3.1415
        },
        {
          index: {}
        },
        {
          s: 2,
          m: 1
        },
        {
          index: {}
        },
        {
          s: 3,
          m: 2.71828
        }
      ]
    )
    puts response
    
    response = client.search(
      index: 'test',
      filter_path: 'aggregations',
      body: {
        aggregations: {
          tm: {
            top_metrics: {
              metrics: {
                field: 'm'
              },
              sort: {
                s: 'desc'
              },
              size: 3
            }
          }
        }
      }
    )
    puts response
    
    
    POST /test/_bulk?refresh
    {"index": {}}
    {"s": 1, "m": 3.1415}
    {"index": {}}
    {"s": 2, "m": 1.0}
    {"index": {}}
    {"s": 3, "m": 2.71828}
    POST /test/_search?filter_path=aggregations
    {
      "aggs": {
        "tm": {
          "top_metrics": {
            "metrics": {"field": "m"},
            "sort": {"s": "desc"},
            "size": 3
          }
        }
      }
    }

其中返回：

    
    
    {
      "aggregations": {
        "tm": {
          "top": [
            {"sort": [3], "metrics": {"m": 2.718280076980591 } },
            {"sort": [2], "metrics": {"m": 1.0 } },
            {"sort": [1], "metrics": {"m": 3.1414999961853027 } }
          ]
        }
      }
    }

默认"大小"为 1。最大默认大小为"10"，因为聚合的工作存储是"密集的"，这意味着我们为每个存储桶分配"大小"插槽。"10"是**非常**保守的默认最大值，如果需要，您可以通过更改"top_metrics_max_size"索引设置来提高它。但是要知道，大尺寸可能会占用相当多的内存，特别是如果它们位于聚合中，这使得许多钱像大型术语聚合一样。如果你一直想提高它，请使用这样的东西：

    
    
    response = client.indices.put_settings(
      index: 'test',
      body: {
        top_metrics_max_size: 100
      }
    )
    puts response
    
    
    PUT /test/_settings
    {
      "top_metrics_max_size": 100
    }

如果"size"大于"1"，则"top_metrics"聚合不能是某种类型的目标。

###Examples

#### 与术语一起使用

这种聚合在"terms"聚合中应该非常有用，例如，找到每个服务器报告的最后一个值。

    
    
    response = client.indices.create(
      index: 'node',
      body: {
        mappings: {
          properties: {
            ip: {
              type: 'ip'
            },
            date: {
              type: 'date'
            }
          }
        }
      }
    )
    puts response
    
    response = client.bulk(
      index: 'node',
      refresh: true,
      body: [
        {
          index: {}
        },
        {
          ip: '192.168.0.1',
          date: '2020-01-01T01:01:01',
          m: 1
        },
        {
          index: {}
        },
        {
          ip: '192.168.0.1',
          date: '2020-01-01T02:01:01',
          m: 2
        },
        {
          index: {}
        },
        {
          ip: '192.168.0.2',
          date: '2020-01-01T02:01:01',
          m: 3
        }
      ]
    )
    puts response
    
    response = client.search(
      index: 'node',
      filter_path: 'aggregations',
      body: {
        aggregations: {
          ip: {
            terms: {
              field: 'ip'
            },
            aggregations: {
              tm: {
                top_metrics: {
                  metrics: {
                    field: 'm'
                  },
                  sort: {
                    date: 'desc'
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /node
    {
      "mappings": {
        "properties": {
          "ip": {"type": "ip"},
          "date": {"type": "date"}
        }
      }
    }
    POST /node/_bulk?refresh
    {"index": {}}
    {"ip": "192.168.0.1", "date": "2020-01-01T01:01:01", "m": 1}
    {"index": {}}
    {"ip": "192.168.0.1", "date": "2020-01-01T02:01:01", "m": 2}
    {"index": {}}
    {"ip": "192.168.0.2", "date": "2020-01-01T02:01:01", "m": 3}
    POST /node/_search?filter_path=aggregations
    {
      "aggs": {
        "ip": {
          "terms": {
            "field": "ip"
          },
          "aggs": {
            "tm": {
              "top_metrics": {
                "metrics": {"field": "m"},
                "sort": {"date": "desc"}
              }
            }
          }
        }
      }
    }

其中返回：

    
    
    {
      "aggregations": {
        "ip": {
          "buckets": [
            {
              "key": "192.168.0.1",
              "doc_count": 2,
              "tm": {
                "top": [ {"sort": ["2020-01-01T02:01:01.000Z"], "metrics": {"m": 2 } } ]
              }
            },
            {
              "key": "192.168.0.2",
              "doc_count": 1,
              "tm": {
                "top": [ {"sort": ["2020-01-01T02:01:01.000Z"], "metrics": {"m": 3 } } ]
              }
            }
          ],
          "doc_count_error_upper_bound": 0,
          "sum_other_doc_count": 0
        }
      }
    }

与"top_hits"不同，您可以按此指标的结果对存储桶进行排序：

    
    
    response = client.search(
      index: 'node',
      filter_path: 'aggregations',
      body: {
        aggregations: {
          ip: {
            terms: {
              field: 'ip',
              order: {
                "tm.m": 'desc'
              }
            },
            aggregations: {
              tm: {
                top_metrics: {
                  metrics: {
                    field: 'm'
                  },
                  sort: {
                    date: 'desc'
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /node/_search?filter_path=aggregations
    {
      "aggs": {
        "ip": {
          "terms": {
            "field": "ip",
            "order": {"tm.m": "desc"}
          },
          "aggs": {
            "tm": {
              "top_metrics": {
                "metrics": {"field": "m"},
                "sort": {"date": "desc"}
              }
            }
          }
        }
      }
    }

其中返回：

    
    
    {
      "aggregations": {
        "ip": {
          "buckets": [
            {
              "key": "192.168.0.2",
              "doc_count": 1,
              "tm": {
                "top": [ {"sort": ["2020-01-01T02:01:01.000Z"], "metrics": {"m": 3 } } ]
              }
            },
            {
              "key": "192.168.0.1",
              "doc_count": 2,
              "tm": {
                "top": [ {"sort": ["2020-01-01T02:01:01.000Z"], "metrics": {"m": 2 } } ]
              }
            }
          ],
          "doc_count_error_upper_bound": 0,
          "sum_other_doc_count": 0
        }
      }
    }

#### 混合排序类型

按在不同索引中具有不同类型的字段对"top_metrics"进行排序会产生一些令人惊讶的结果：浮点字段始终独立于整个编号字段进行排序。

    
    
    response = client.bulk(
      index: 'test',
      refresh: true,
      body: [
        {
          index: {
            _index: 'test1'
          }
        },
        {
          s: 1,
          m: 3.1415
        },
        {
          index: {
            _index: 'test1'
          }
        },
        {
          s: 2,
          m: 1
        },
        {
          index: {
            _index: 'test2'
          }
        },
        {
          s: 3.1,
          m: 2.71828
        }
      ]
    )
    puts response
    
    response = client.search(
      index: 'test*',
      filter_path: 'aggregations',
      body: {
        aggregations: {
          tm: {
            top_metrics: {
              metrics: {
                field: 'm'
              },
              sort: {
                s: 'asc'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /test/_bulk?refresh
    {"index": {"_index": "test1"}}
    {"s": 1, "m": 3.1415}
    {"index": {"_index": "test1"}}
    {"s": 2, "m": 1}
    {"index": {"_index": "test2"}}
    {"s": 3.1, "m": 2.71828}
    POST /test*/_search?filter_path=aggregations
    {
      "aggs": {
        "tm": {
          "top_metrics": {
            "metrics": {"field": "m"},
            "sort": {"s": "asc"}
          }
        }
      }
    }

其中返回：

    
    
    {
      "aggregations": {
        "tm": {
          "top": [ {"sort": [3.0999999046325684], "metrics": {"m": 2.718280076980591 } } ]
        }
      }
    }

虽然这比错误要好，但它**可能**不是你想要的。虽然它确实会失去一些精度，但您可以使用如下所示将整数字段显式转换为浮点数：

    
    
    response = client.search(
      index: 'test*',
      filter_path: 'aggregations',
      body: {
        aggregations: {
          tm: {
            top_metrics: {
              metrics: {
                field: 'm'
              },
              sort: {
                s: {
                  order: 'asc',
                  numeric_type: 'double'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /test*/_search?filter_path=aggregations
    {
      "aggs": {
        "tm": {
          "top_metrics": {
            "metrics": {"field": "m"},
            "sort": {"s": {"order": "asc", "numeric_type": "double"}}
          }
        }
      }
    }

这返回了更预期的：

    
    
    {
      "aggregations": {
        "tm": {
          "top": [ {"sort": [1.0], "metrics": {"m": 3.1414999961853027 } } ]
        }
      }
    }

#### 在管道聚合中使用

"top_metrics"可用于使用每个存储桶单个值的管道聚合，例如应用于每个存储桶筛选的"bucket_selector"，类似于在 SQL 中使用 HAVING 子句。这需要将"size"设置为 1，并为要传递到包装聚合器的(单个)指标指定正确的路径。例如：

    
    
    POST /test*/_search?filter_path=aggregations
    {
      "aggs": {
        "ip": {
          "terms": {
            "field": "ip"
          },
          "aggs": {
            "tm": {
              "top_metrics": {
                "metrics": {"field": "m"},
                "sort": {"s": "desc"},
                "size": 1
              }
            },
            "having_tm": {
              "bucket_selector": {
                "buckets_path": {
                  "top_m": "tm[m]"
                },
                "script": "params.top_m < 1000"
              }
            }
          }
        }
      }
    }

"bucket_path"使用"top_metrics"名称"tm"和提供聚合值的度量关键字，即"m"。

[« Top hits aggregation](search-aggregations-metrics-top-hits-
aggregation.md) [Value count aggregation »](search-aggregations-metrics-
valuecount-aggregation.md)
