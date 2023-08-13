

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
streams](data-streams.md) ›[Time series data stream (TSDS)](tsds.md)

[« Run downsampling with ILM](downsampling-ilm.md) [Ingest pipelines
»](ingest.md)

## 手动运行缩减采样

对时序数据流 (TSDS) 进行下采样的建议方法是通过索引生命周期管理 (ILM)。但是，如果您不使用 ILM，则可以手动对 TSDS 进行缩减采样。本指南介绍如何使用典型的 Kubernetes 集群监控数据。

若要测试手动缩减采样，请执行以下步骤：

1. 检查先决条件。  2. 创建时间序列数据流。  3. 引入时序数据。  4. 对 TSDS 进行下采样。  5. 查看结果。

####Prerequisites

* 请参阅 TSDS 先决条件。  * 不能直接对数据流进行降采样，也不能一次对多个索引进行降采样。只能对一个时序索引(TSDS 后备索引)进行降采样。  * 为了对索引进行降采样，它必须是只读的。对于 TSDS 写入索引，这意味着需要先滚动更新并使其只读。  * 缩减采样使用 UTC 时间戳。  * 缩减采样需要至少一个指标字段才能存在于时间序列索引中。

#### 创建时序数据流

首先，您将创建一个 TSDS。为简单起见，在时间序列映射中，所有"time_series_metric"参数都设置为类型"gauge"，但也可以使用其他值，例如"计数器"和"直方图"。"time_series_metric"值确定在缩减采样期间使用的统计表示类型。

索引模板包含一组静态时间序列维度："主机"、"命名空间"、"节点"和"pod"。缩减采样过程不会更改时序维度。

    
    
    PUT _index_template/my-data-stream-template
    {
      "index_patterns": [
        "my-data-stream*"
      ],
      "data_stream": {},
      "template": {
        "settings": {
          "index": {
            "mode": "time_series",
            "routing_path": [
              "kubernetes.namespace",
              "kubernetes.host",
              "kubernetes.node",
              "kubernetes.pod"
            ],
            "number_of_replicas": 0,
            "number_of_shards": 2
          }
        },
        "mappings": {
          "properties": {
            "@timestamp": {
              "type": "date"
            },
            "kubernetes": {
              "properties": {
                "container": {
                  "properties": {
                    "cpu": {
                      "properties": {
                        "usage": {
                          "properties": {
                            "core": {
                              "properties": {
                                "ns": {
                                  "type": "long"
                                }
                              }
                            },
                            "limit": {
                              "properties": {
                                "pct": {
                                  "type": "float"
                                }
                              }
                            },
                            "nanocores": {
                              "type": "long",
                              "time_series_metric": "gauge"
                            },
                            "node": {
                              "properties": {
                                "pct": {
                                  "type": "float"
                                }
                              }
                            }
                          }
                        }
                      }
                    },
                    "memory": {
                      "properties": {
                        "available": {
                          "properties": {
                            "bytes": {
                              "type": "long",
                              "time_series_metric": "gauge"
                            }
                          }
                        },
                        "majorpagefaults": {
                          "type": "long"
                        },
                        "pagefaults": {
                          "type": "long",
                          "time_series_metric": "gauge"
                        },
                        "rss": {
                          "properties": {
                            "bytes": {
                              "type": "long",
                              "time_series_metric": "gauge"
                            }
                          }
                        },
                        "usage": {
                          "properties": {
                            "bytes": {
                              "type": "long",
                              "time_series_metric": "gauge"
                            },
                            "limit": {
                              "properties": {
                                "pct": {
                                  "type": "float"
                                }
                              }
                            },
                            "node": {
                              "properties": {
                                "pct": {
                                  "type": "float"
                                }
                              }
                            }
                          }
                        },
                        "workingset": {
                          "properties": {
                            "bytes": {
                              "type": "long",
                              "time_series_metric": "gauge"
                            }
                          }
                        }
                      }
                    },
                    "name": {
                      "type": "keyword"
                    },
                    "start_time": {
                      "type": "date"
                    }
                  }
                },
                "host": {
                  "type": "keyword",
                  "time_series_dimension": true
                },
                "namespace": {
                  "type": "keyword",
                  "time_series_dimension": true
                },
                "node": {
                  "type": "keyword",
                  "time_series_dimension": true
                },
                "pod": {
                  "type": "keyword",
                  "time_series_dimension": true
                }
              }
            }
          }
        }
      }
    }

#### 引入时间序列数据

由于时序数据流设计为仅接受最近数据，因此在此示例中，你将使用引入管道在编制索引时对数据进行时移。因此，索引数据将具有过去 15 分钟的"@timestamp"。

使用此请求创建管道：

    
    
    PUT _ingest/pipeline/my-timestamp-pipeline
    {
      "description": "Shifts the @timestamp to the last 15 minutes",
      "processors": [
        {
          "set": {
            "field": "ingest_time",
            "value": "{{_ingest.timestamp}}"
          }
        },
        {
          "script": {
            "lang": "painless",
            "source": """
              def delta = ChronoUnit.SECONDS.between(
                ZonedDateTime.parse("2022-06-21T15:49:00Z"),
                ZonedDateTime.parse(ctx["ingest_time"])
              );
              ctx["@timestamp"] = ZonedDateTime.parse(ctx["@timestamp"]).plus(delta,ChronoUnit.SECONDS).toString();
            """
          }
        }
      ]
    }

接下来，使用批量 API 请求自动创建 TSDS 并为一组十个文档编制索引：

    
    
    PUT /my-data-stream/_bulk?refresh&pipeline=my-timestamp-pipeline
    {"create": {}}
    {"@timestamp":"2022-06-21T15:49:00Z","kubernetes":{"host":"gke-apps-0","node":"gke-apps-0-0","pod":"gke-apps-0-0-0","container":{"cpu":{"usage":{"nanocores":91153,"core":{"ns":12828317850},"node":{"pct":2.77905e-05},"limit":{"pct":2.77905e-05}}},"memory":{"available":{"bytes":463314616},"usage":{"bytes":307007078,"node":{"pct":0.01770037710617187},"limit":{"pct":9.923134671484496e-05}},"workingset":{"bytes":585236},"rss":{"bytes":102728},"pagefaults":120901,"majorpagefaults":0},"start_time":"2021-03-30T07:59:06Z","name":"container-name-44"},"namespace":"namespace26"}}
    {"create": {}}
    {"@timestamp":"2022-06-21T15:45:50Z","kubernetes":{"host":"gke-apps-0","node":"gke-apps-0-0","pod":"gke-apps-0-0-0","container":{"cpu":{"usage":{"nanocores":124501,"core":{"ns":12828317850},"node":{"pct":2.77905e-05},"limit":{"pct":2.77905e-05}}},"memory":{"available":{"bytes":982546514},"usage":{"bytes":360035574,"node":{"pct":0.01770037710617187},"limit":{"pct":9.923134671484496e-05}},"workingset":{"bytes":1339884},"rss":{"bytes":381174},"pagefaults":178473,"majorpagefaults":0},"start_time":"2021-03-30T07:59:06Z","name":"container-name-44"},"namespace":"namespace26"}}
    {"create": {}}
    {"@timestamp":"2022-06-21T15:44:50Z","kubernetes":{"host":"gke-apps-0","node":"gke-apps-0-0","pod":"gke-apps-0-0-0","container":{"cpu":{"usage":{"nanocores":38907,"core":{"ns":12828317850},"node":{"pct":2.77905e-05},"limit":{"pct":2.77905e-05}}},"memory":{"available":{"bytes":862723768},"usage":{"bytes":379572388,"node":{"pct":0.01770037710617187},"limit":{"pct":9.923134671484496e-05}},"workingset":{"bytes":431227},"rss":{"bytes":386580},"pagefaults":233166,"majorpagefaults":0},"start_time":"2021-03-30T07:59:06Z","name":"container-name-44"},"namespace":"namespace26"}}
    {"create": {}}
    {"@timestamp":"2022-06-21T15:44:40Z","kubernetes":{"host":"gke-apps-0","node":"gke-apps-0-0","pod":"gke-apps-0-0-0","container":{"cpu":{"usage":{"nanocores":86706,"core":{"ns":12828317850},"node":{"pct":2.77905e-05},"limit":{"pct":2.77905e-05}}},"memory":{"available":{"bytes":567160996},"usage":{"bytes":103266017,"node":{"pct":0.01770037710617187},"limit":{"pct":9.923134671484496e-05}},"workingset":{"bytes":1724908},"rss":{"bytes":105431},"pagefaults":233166,"majorpagefaults":0},"start_time":"2021-03-30T07:59:06Z","name":"container-name-44"},"namespace":"namespace26"}}
    {"create": {}}
    {"@timestamp":"2022-06-21T15:44:00Z","kubernetes":{"host":"gke-apps-0","node":"gke-apps-0-0","pod":"gke-apps-0-0-0","container":{"cpu":{"usage":{"nanocores":150069,"core":{"ns":12828317850},"node":{"pct":2.77905e-05},"limit":{"pct":2.77905e-05}}},"memory":{"available":{"bytes":639054643},"usage":{"bytes":265142477,"node":{"pct":0.01770037710617187},"limit":{"pct":9.923134671484496e-05}},"workingset":{"bytes":1786511},"rss":{"bytes":189235},"pagefaults":138172,"majorpagefaults":0},"start_time":"2021-03-30T07:59:06Z","name":"container-name-44"},"namespace":"namespace26"}}
    {"create": {}}
    {"@timestamp":"2022-06-21T15:42:40Z","kubernetes":{"host":"gke-apps-0","node":"gke-apps-0-0","pod":"gke-apps-0-0-0","container":{"cpu":{"usage":{"nanocores":82260,"core":{"ns":12828317850},"node":{"pct":2.77905e-05},"limit":{"pct":2.77905e-05}}},"memory":{"available":{"bytes":854735585},"usage":{"bytes":309798052,"node":{"pct":0.01770037710617187},"limit":{"pct":9.923134671484496e-05}},"workingset":{"bytes":924058},"rss":{"bytes":110838},"pagefaults":259073,"majorpagefaults":0},"start_time":"2021-03-30T07:59:06Z","name":"container-name-44"},"namespace":"namespace26"}}
    {"create": {}}
    {"@timestamp":"2022-06-21T15:42:10Z","kubernetes":{"host":"gke-apps-0","node":"gke-apps-0-0","pod":"gke-apps-0-0-0","container":{"cpu":{"usage":{"nanocores":153404,"core":{"ns":12828317850},"node":{"pct":2.77905e-05},"limit":{"pct":2.77905e-05}}},"memory":{"available":{"bytes":279586406},"usage":{"bytes":214904955,"node":{"pct":0.01770037710617187},"limit":{"pct":9.923134671484496e-05}},"workingset":{"bytes":1047265},"rss":{"bytes":91914},"pagefaults":302252,"majorpagefaults":0},"start_time":"2021-03-30T07:59:06Z","name":"container-name-44"},"namespace":"namespace26"}}
    {"create": {}}
    {"@timestamp":"2022-06-21T15:40:20Z","kubernetes":{"host":"gke-apps-0","node":"gke-apps-0-0","pod":"gke-apps-0-0-0","container":{"cpu":{"usage":{"nanocores":125613,"core":{"ns":12828317850},"node":{"pct":2.77905e-05},"limit":{"pct":2.77905e-05}}},"memory":{"available":{"bytes":822782853},"usage":{"bytes":100475044,"node":{"pct":0.01770037710617187},"limit":{"pct":9.923134671484496e-05}},"workingset":{"bytes":2109932},"rss":{"bytes":278446},"pagefaults":74843,"majorpagefaults":0},"start_time":"2021-03-30T07:59:06Z","name":"container-name-44"},"namespace":"namespace26"}}
    {"create": {}}
    {"@timestamp":"2022-06-21T15:40:10Z","kubernetes":{"host":"gke-apps-0","node":"gke-apps-0-0","pod":"gke-apps-0-0-0","container":{"cpu":{"usage":{"nanocores":100046,"core":{"ns":12828317850},"node":{"pct":2.77905e-05},"limit":{"pct":2.77905e-05}}},"memory":{"available":{"bytes":567160996},"usage":{"bytes":362826547,"node":{"pct":0.01770037710617187},"limit":{"pct":9.923134671484496e-05}},"workingset":{"bytes":1986724},"rss":{"bytes":402801},"pagefaults":296495,"majorpagefaults":0},"start_time":"2021-03-30T07:59:06Z","name":"container-name-44"},"namespace":"namespace26"}}
    {"create": {}}
    {"@timestamp":"2022-06-21T15:38:30Z","kubernetes":{"host":"gke-apps-0","node":"gke-apps-0-0","pod":"gke-apps-0-0-0","container":{"cpu":{"usage":{"nanocores":40018,"core":{"ns":12828317850},"node":{"pct":2.77905e-05},"limit":{"pct":2.77905e-05}}},"memory":{"available":{"bytes":1062428344},"usage":{"bytes":265142477,"node":{"pct":0.01770037710617187},"limit":{"pct":9.923134671484496e-05}},"workingset":{"bytes":2294743},"rss":{"bytes":340623},"pagefaults":224530,"majorpagefaults":0},"start_time":"2021-03-30T07:59:06Z","name":"container-name-44"},"namespace":"namespace26"}}

您可以使用搜索 API 检查文档是否已正确编制索引：

    
    
    GET /my-data-stream/_search

对数据运行以下聚合以计算一些有趣的统计信息：

    
    
    GET /my-data-stream/_search
    {
        "size": 0,
        "aggs": {
            "tsid": {
                "terms": {
                    "field": "_tsid"
                },
                "aggs": {
                    "over_time": {
                        "date_histogram": {
                            "field": "@timestamp",
                            "fixed_interval": "1d"
                        },
                        "aggs": {
                            "min": {
                                "min": {
                                    "field": "kubernetes.container.memory.usage.bytes"
                                }
                            },
                            "max": {
                                "max": {
                                    "field": "kubernetes.container.memory.usage.bytes"
                                }
                            },
                            "avg": {
                                "avg": {
                                    "field": "kubernetes.container.memory.usage.bytes"
                                }
                            }
                        }
                    }
                }
            }
        }
    }

#### 下采样 TSDS

TSDS 不能直接缩减采样。您需要对其支持索引进行下采样。您可以通过以下方式查看数据流的支持索引：

    
    
    response = client.indices.get_data_stream(
      name: 'my-data-stream'
    )
    puts response
    
    
    GET /_data_stream/my-data-stream

这将返回：

    
    
    {
      "data_streams": [
        {
          "name": "my-data-stream",
          "timestamp_field": {
            "name": "@timestamp"
          },
          "indices": [
            {
              "index_name": ".ds-my-data-stream-2023.07.26-000001", __"index_uuid": "ltOJGmqgTVm4T-Buoe7Acg"
            }
          ],
          "generation": 1,
          "status": "GREEN",
          "template": "my-data-stream-template",
          "hidden": false,
          "system": false,
          "allow_custom_routing": false,
          "replicated": false,
          "time_series": {
            "temporal_ranges": [
              {
                "start": "2023-07-26T09:26:42.000Z",
                "end": "2023-07-26T13:26:42.000Z"
              }
            ]
          }
        }
      ]
    }

__

|

此数据流的支持索引。   ---|--- 在对后备索引进行缩减采样之前，需要滚动更新 TSDS，并且需要将旧索引设为只读。

使用滚动更新 API 滚动更新 TSDS：

    
    
    response = client.indices.rollover(
      alias: 'my-data-stream'
    )
    puts response
    
    
    POST /my-data-stream/_rollover/

从响应中复制"old_index"的名称。在以下步骤中，将索引名称替换为"old_index"的名称。

旧索引需要设置为只读模式。运行以下请求：

    
    
    PUT /.ds-my-data-stream-2023.07.26-000001/_block/write

接下来，使用下采样 API 对索引进行下采样，将时序间隔设置为 1 小时：

    
    
    POST /.ds-my-data-stream-2023.07.26-000001/_downsample/.ds-my-data-stream-2023.07.26-000001-downsample
    {
      "fixed_interval": "1h"
    }

现在，您可以修改数据流，并将原始索引替换为缩减采样的索引：

    
    
    POST _data_stream/_modify
    {
      "actions": [
        {
          "remove_backing_index": {
            "data_stream": "my-data-stream",
            "index": ".ds-my-data-stream-2023.07.26-000001"
          }
        },
        {
          "add_backing_index": {
            "data_stream": "my-data-stream",
            "index": ".ds-my-data-stream-2023.07.26-000001-downsample"
          }
        }
      ]
    }

现在可以删除旧的后备索引。但请注意，这将删除原始数据。如果将来可能需要原始数据，请不要删除索引。

#### 查看结果

重新运行较早的搜索查询(请注意，在查询缩减采样索引时，需要注意一些细微差别)：

    
    
    GET /my-data-stream/_search

具有新的缩减采样支持索引的 TSDS 仅包含一个文档。对于计数器，此文档将只有最后一个值。对于仪表，字段类型现在为"aggregate_metric_double"。您会看到基于原始抽样指标的"最小"、"最大值"、"总和"和"value_count"统计信息：

    
    
    {
      "took": 2,
      "timed_out": false,
      "_shards": {
        "total": 4,
        "successful": 4,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": {
          "value": 1,
          "relation": "eq"
        },
        "max_score": 1,
        "hits": [
          {
            "_index": ".ds-my-data-stream-2023.07.26-000001-downsample",
            "_id": "0eL0wC_4-45SnTNFAAABiZHbD4A",
            "_score": 1,
            "_source": {
              "@timestamp": "2023-07-26T11:00:00.000Z",
              "_doc_count": 10,
              "ingest_time": "2023-07-26T11:26:42.715Z",
              "kubernetes": {
                "container": {
                  "cpu": {
                    "usage": {
                      "core": {
                        "ns": 12828317850
                      },
                      "limit": {
                        "pct": 0.0000277905
                      },
                      "nanocores": {
                        "min": 38907,
                        "max": 153404,
                        "sum": 992677,
                        "value_count": 10
                      },
                      "node": {
                        "pct": 0.0000277905
                      }
                    }
                  },
                  "memory": {
                    "available": {
                      "bytes": {
                        "min": 279586406,
                        "max": 1062428344,
                        "sum": 7101494721,
                        "value_count": 10
                      }
                    },
                    "majorpagefaults": 0,
                    "pagefaults": {
                      "min": 74843,
                      "max": 302252,
                      "sum": 2061071,
                      "value_count": 10
                    },
                    "rss": {
                      "bytes": {
                        "min": 91914,
                        "max": 402801,
                        "sum": 2389770,
                        "value_count": 10
                      }
                    },
                    "usage": {
                      "bytes": {
                        "min": 100475044,
                        "max": 379572388,
                        "sum": 2668170609,
                        "value_count": 10
                      },
                      "limit": {
                        "pct": 0.00009923134
                      },
                      "node": {
                        "pct": 0.017700378
                      }
                    },
                    "workingset": {
                      "bytes": {
                        "min": 431227,
                        "max": 2294743,
                        "sum": 14230488,
                        "value_count": 10
                      }
                    }
                  },
                  "name": "container-name-44",
                  "start_time": "2021-03-30T07:59:06.000Z"
                },
                "host": "gke-apps-0",
                "namespace": "namespace26",
                "node": "gke-apps-0-0",
                "pod": "gke-apps-0-0-0"
              }
            }
          }
        ]
      }
    }

重新运行之前的聚合。即使聚合在仅包含 1 个文档的缩减采样 TSDS 上运行，它也返回与原始 TSDS 上的早期聚合相同的结果。

    
    
    GET /my-data-stream/_search
    {
        "size": 0,
        "aggs": {
            "tsid": {
                "terms": {
                    "field": "_tsid"
                },
                "aggs": {
                    "over_time": {
                        "date_histogram": {
                            "field": "@timestamp",
                            "fixed_interval": "1d"
                        },
                        "aggs": {
                            "min": {
                                "min": {
                                    "field": "kubernetes.container.memory.usage.bytes"
                                }
                            },
                            "max": {
                                "max": {
                                    "field": "kubernetes.container.memory.usage.bytes"
                                }
                            },
                            "avg": {
                                "avg": {
                                    "field": "kubernetes.container.memory.usage.bytes"
                                }
                            }
                        }
                    }
                }
            }
        }
    }

此示例演示了缩减像素采样如何在您选择的任何时间边界内显著减少为时序数据存储的文档数。还可以对已经缩减采样的数据执行缩减采样，以进一步降低存储和相关成本，因为时间序列数据时代和数据分辨率变得不那么重要。

对 TSDS 进行缩减采样的建议方法是使用 ILM。若要了解详细信息，请尝试使用 ILM运行缩减采样示例。

[« Run downsampling with ILM](downsampling-ilm.md) [Ingest pipelines
»](ingest.md)
