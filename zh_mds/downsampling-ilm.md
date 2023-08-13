

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
streams](data-streams.md) ›[Time series data stream (TSDS)](tsds.md)

[« Downsampling a time series data stream](downsampling.md) [Run
downsampling manually »](downsampling-manual.md)

## 使用 ILM 运行缩减采样

这是一个简化的示例，允许您快速了解下采样如何作为 ILM 策略的一部分来减少一组采样指标的存储大小。该示例使用典型的 Kubernetes 集群监控数据。若要使用 ILM 测试缩减像素采样，请执行以下步骤：

1. 检查先决条件。  2. 创建索引生命周期策略。  3. 创建索引模板。  4. 引入时序数据。  5. 查看结果。

####Prerequisites

请参阅时序数据流先决条件。

在运行此示例之前，您可能需要尝试手动运行缩减采样示例。

#### 创建索引生命周期策略

为时序数据创建 ILM 策略。虽然不是必需的，但建议使用 ILM策略来自动管理时序数据流索引。

要启用缩减采样，请添加缩减采样操作，并将"fixed_interval"设置为要聚合原始时间序列数据的缩减采样间隔。

在此示例中，ILM 策略配置为"热"阶段。下采样在初始索引滚动更新后进行，出于演示目的，设置为在五分钟后运行。

    
    
    response = client.ilm.put_lifecycle(
      policy: 'datastream_policy',
      body: {
        policy: {
          phases: {
            hot: {
              actions: {
                rollover: {
                  max_age: '5m'
                },
                downsample: {
                  fixed_interval: '1h'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT _ilm/policy/datastream_policy
    {
      "policy": {
        "phases": {
          "hot": {
            "actions": {
              "rollover" : {
                "max_age": "5m"
              },
              "downsample": {
      	        "fixed_interval": "1h"
      	      }
            }
          }
        }
      }
    }

#### 创建索引模板

这将为基本数据流创建索引模板。设置时序数据流中详细介绍了索引模板的可用参数。

为简单起见，在时间序列映射中，所有"time_series_metric"参数都设置为"gauge"类型，但也可以使用"计数器"指标类型。"time_series_metric"值确定在缩减采样期间使用的统计表示类型。

索引模板包含一组静态时间序列维度："主机"、"命名空间"、"节点"和"pod"。缩减采样过程不会更改时序维度。

    
    
    response = client.indices.put_index_template(
      name: 'datastream_template',
      body: {
        index_patterns: [
          'datastream*'
        ],
        data_stream: {},
        template: {
          settings: {
            index: {
              mode: 'time_series',
              number_of_replicas: 0,
              number_of_shards: 2
            },
            "index.lifecycle.name": 'datastream_policy'
          },
          mappings: {
            properties: {
              "@timestamp": {
                type: 'date'
              },
              kubernetes: {
                properties: {
                  container: {
                    properties: {
                      cpu: {
                        properties: {
                          usage: {
                            properties: {
                              core: {
                                properties: {
                                  ns: {
                                    type: 'long'
                                  }
                                }
                              },
                              limit: {
                                properties: {
                                  pct: {
                                    type: 'float'
                                  }
                                }
                              },
                              nanocores: {
                                type: 'long',
                                time_series_metric: 'gauge'
                              },
                              node: {
                                properties: {
                                  pct: {
                                    type: 'float'
                                  }
                                }
                              }
                            }
                          }
                        }
                      },
                      memory: {
                        properties: {
                          available: {
                            properties: {
                              bytes: {
                                type: 'long',
                                time_series_metric: 'gauge'
                              }
                            }
                          },
                          majorpagefaults: {
                            type: 'long'
                          },
                          pagefaults: {
                            type: 'long',
                            time_series_metric: 'gauge'
                          },
                          rss: {
                            properties: {
                              bytes: {
                                type: 'long',
                                time_series_metric: 'gauge'
                              }
                            }
                          },
                          usage: {
                            properties: {
                              bytes: {
                                type: 'long',
                                time_series_metric: 'gauge'
                              },
                              limit: {
                                properties: {
                                  pct: {
                                    type: 'float'
                                  }
                                }
                              },
                              node: {
                                properties: {
                                  pct: {
                                    type: 'float'
                                  }
                                }
                              }
                            }
                          },
                          workingset: {
                            properties: {
                              bytes: {
                                type: 'long',
                                time_series_metric: 'gauge'
                              }
                            }
                          }
                        }
                      },
                      name: {
                        type: 'keyword'
                      },
                      start_time: {
                        type: 'date'
                      }
                    }
                  },
                  host: {
                    type: 'keyword',
                    time_series_dimension: true
                  },
                  namespace: {
                    type: 'keyword',
                    time_series_dimension: true
                  },
                  node: {
                    type: 'keyword',
                    time_series_dimension: true
                  },
                  pod: {
                    type: 'keyword',
                    time_series_dimension: true
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT _index_template/datastream_template
    {
        "index_patterns": [
            "datastream*"
        ],
        "data_stream": {},
        "template": {
            "settings": {
                "index": {
                    "mode": "time_series",
                    "number_of_replicas": 0,
                    "number_of_shards": 2
                },
                "index.lifecycle.name": "datastream_policy"
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

使用批量 API 请求自动创建 TSDS 并索引一组经常使用的文档。

**重要提示：** 在运行此批量请求之前，您需要将时间戳更新为当前时间后的三到五小时内。也就是说，搜索"2022-06-21T15"并替换为您当前的日期，并将小时调整为当前时间加三个小时。

    
    
    response = client.bulk(
      index: 'datastream',
      refresh: true,
      body: [
        {
          create: {}
        },
        {
          "@timestamp": '2022-06-21T15:49:00Z',
          kubernetes: {
            host: 'gke-apps-0',
            node: 'gke-apps-0-0',
            pod: 'gke-apps-0-0-0',
            container: {
              cpu: {
                usage: {
                  nanocores: 91_153,
                  core: {
                    ns: 12_828_317_850
                  },
                  node: {
                    pct: 2.77905e-05
                  },
                  limit: {
                    pct: 2.77905e-05
                  }
                }
              },
              memory: {
                available: {
                  bytes: 463_314_616
                },
                usage: {
                  bytes: 307_007_078,
                  node: {
                    pct: 0.01770037710617187
                  },
                  limit: {
                    pct: 9.923134671484496e-05
                  }
                },
                workingset: {
                  bytes: 585_236
                },
                rss: {
                  bytes: 102_728
                },
                pagefaults: 120_901,
                majorpagefaults: 0
              },
              start_time: '2021-03-30T07:59:06Z',
              name: 'container-name-44'
            },
            namespace: 'namespace26'
          }
        },
        {
          create: {}
        },
        {
          "@timestamp": '2022-06-21T15:45:50Z',
          kubernetes: {
            host: 'gke-apps-0',
            node: 'gke-apps-0-0',
            pod: 'gke-apps-0-0-0',
            container: {
              cpu: {
                usage: {
                  nanocores: 124_501,
                  core: {
                    ns: 12_828_317_850
                  },
                  node: {
                    pct: 2.77905e-05
                  },
                  limit: {
                    pct: 2.77905e-05
                  }
                }
              },
              memory: {
                available: {
                  bytes: 982_546_514
                },
                usage: {
                  bytes: 360_035_574,
                  node: {
                    pct: 0.01770037710617187
                  },
                  limit: {
                    pct: 9.923134671484496e-05
                  }
                },
                workingset: {
                  bytes: 1_339_884
                },
                rss: {
                  bytes: 381_174
                },
                pagefaults: 178_473,
                majorpagefaults: 0
              },
              start_time: '2021-03-30T07:59:06Z',
              name: 'container-name-44'
            },
            namespace: 'namespace26'
          }
        },
        {
          create: {}
        },
        {
          "@timestamp": '2022-06-21T15:44:50Z',
          kubernetes: {
            host: 'gke-apps-0',
            node: 'gke-apps-0-0',
            pod: 'gke-apps-0-0-0',
            container: {
              cpu: {
                usage: {
                  nanocores: 38_907,
                  core: {
                    ns: 12_828_317_850
                  },
                  node: {
                    pct: 2.77905e-05
                  },
                  limit: {
                    pct: 2.77905e-05
                  }
                }
              },
              memory: {
                available: {
                  bytes: 862_723_768
                },
                usage: {
                  bytes: 379_572_388,
                  node: {
                    pct: 0.01770037710617187
                  },
                  limit: {
                    pct: 9.923134671484496e-05
                  }
                },
                workingset: {
                  bytes: 431_227
                },
                rss: {
                  bytes: 386_580
                },
                pagefaults: 233_166,
                majorpagefaults: 0
              },
              start_time: '2021-03-30T07:59:06Z',
              name: 'container-name-44'
            },
            namespace: 'namespace26'
          }
        },
        {
          create: {}
        },
        {
          "@timestamp": '2022-06-21T15:44:40Z',
          kubernetes: {
            host: 'gke-apps-0',
            node: 'gke-apps-0-0',
            pod: 'gke-apps-0-0-0',
            container: {
              cpu: {
                usage: {
                  nanocores: 86_706,
                  core: {
                    ns: 12_828_317_850
                  },
                  node: {
                    pct: 2.77905e-05
                  },
                  limit: {
                    pct: 2.77905e-05
                  }
                }
              },
              memory: {
                available: {
                  bytes: 567_160_996
                },
                usage: {
                  bytes: 103_266_017,
                  node: {
                    pct: 0.01770037710617187
                  },
                  limit: {
                    pct: 9.923134671484496e-05
                  }
                },
                workingset: {
                  bytes: 1_724_908
                },
                rss: {
                  bytes: 105_431
                },
                pagefaults: 233_166,
                majorpagefaults: 0
              },
              start_time: '2021-03-30T07:59:06Z',
              name: 'container-name-44'
            },
            namespace: 'namespace26'
          }
        },
        {
          create: {}
        },
        {
          "@timestamp": '2022-06-21T15:44:00Z',
          kubernetes: {
            host: 'gke-apps-0',
            node: 'gke-apps-0-0',
            pod: 'gke-apps-0-0-0',
            container: {
              cpu: {
                usage: {
                  nanocores: 150_069,
                  core: {
                    ns: 12_828_317_850
                  },
                  node: {
                    pct: 2.77905e-05
                  },
                  limit: {
                    pct: 2.77905e-05
                  }
                }
              },
              memory: {
                available: {
                  bytes: 639_054_643
                },
                usage: {
                  bytes: 265_142_477,
                  node: {
                    pct: 0.01770037710617187
                  },
                  limit: {
                    pct: 9.923134671484496e-05
                  }
                },
                workingset: {
                  bytes: 1_786_511
                },
                rss: {
                  bytes: 189_235
                },
                pagefaults: 138_172,
                majorpagefaults: 0
              },
              start_time: '2021-03-30T07:59:06Z',
              name: 'container-name-44'
            },
            namespace: 'namespace26'
          }
        },
        {
          create: {}
        },
        {
          "@timestamp": '2022-06-21T15:42:40Z',
          kubernetes: {
            host: 'gke-apps-0',
            node: 'gke-apps-0-0',
            pod: 'gke-apps-0-0-0',
            container: {
              cpu: {
                usage: {
                  nanocores: 82_260,
                  core: {
                    ns: 12_828_317_850
                  },
                  node: {
                    pct: 2.77905e-05
                  },
                  limit: {
                    pct: 2.77905e-05
                  }
                }
              },
              memory: {
                available: {
                  bytes: 854_735_585
                },
                usage: {
                  bytes: 309_798_052,
                  node: {
                    pct: 0.01770037710617187
                  },
                  limit: {
                    pct: 9.923134671484496e-05
                  }
                },
                workingset: {
                  bytes: 924_058
                },
                rss: {
                  bytes: 110_838
                },
                pagefaults: 259_073,
                majorpagefaults: 0
              },
              start_time: '2021-03-30T07:59:06Z',
              name: 'container-name-44'
            },
            namespace: 'namespace26'
          }
        },
        {
          create: {}
        },
        {
          "@timestamp": '2022-06-21T15:42:10Z',
          kubernetes: {
            host: 'gke-apps-0',
            node: 'gke-apps-0-0',
            pod: 'gke-apps-0-0-0',
            container: {
              cpu: {
                usage: {
                  nanocores: 153_404,
                  core: {
                    ns: 12_828_317_850
                  },
                  node: {
                    pct: 2.77905e-05
                  },
                  limit: {
                    pct: 2.77905e-05
                  }
                }
              },
              memory: {
                available: {
                  bytes: 279_586_406
                },
                usage: {
                  bytes: 214_904_955,
                  node: {
                    pct: 0.01770037710617187
                  },
                  limit: {
                    pct: 9.923134671484496e-05
                  }
                },
                workingset: {
                  bytes: 1_047_265
                },
                rss: {
                  bytes: 91_914
                },
                pagefaults: 302_252,
                majorpagefaults: 0
              },
              start_time: '2021-03-30T07:59:06Z',
              name: 'container-name-44'
            },
            namespace: 'namespace26'
          }
        },
        {
          create: {}
        },
        {
          "@timestamp": '2022-06-21T15:40:20Z',
          kubernetes: {
            host: 'gke-apps-0',
            node: 'gke-apps-0-0',
            pod: 'gke-apps-0-0-0',
            container: {
              cpu: {
                usage: {
                  nanocores: 125_613,
                  core: {
                    ns: 12_828_317_850
                  },
                  node: {
                    pct: 2.77905e-05
                  },
                  limit: {
                    pct: 2.77905e-05
                  }
                }
              },
              memory: {
                available: {
                  bytes: 822_782_853
                },
                usage: {
                  bytes: 100_475_044,
                  node: {
                    pct: 0.01770037710617187
                  },
                  limit: {
                    pct: 9.923134671484496e-05
                  }
                },
                workingset: {
                  bytes: 2_109_932
                },
                rss: {
                  bytes: 278_446
                },
                pagefaults: 74_843,
                majorpagefaults: 0
              },
              start_time: '2021-03-30T07:59:06Z',
              name: 'container-name-44'
            },
            namespace: 'namespace26'
          }
        },
        {
          create: {}
        },
        {
          "@timestamp": '2022-06-21T15:40:10Z',
          kubernetes: {
            host: 'gke-apps-0',
            node: 'gke-apps-0-0',
            pod: 'gke-apps-0-0-0',
            container: {
              cpu: {
                usage: {
                  nanocores: 100_046,
                  core: {
                    ns: 12_828_317_850
                  },
                  node: {
                    pct: 2.77905e-05
                  },
                  limit: {
                    pct: 2.77905e-05
                  }
                }
              },
              memory: {
                available: {
                  bytes: 567_160_996
                },
                usage: {
                  bytes: 362_826_547,
                  node: {
                    pct: 0.01770037710617187
                  },
                  limit: {
                    pct: 9.923134671484496e-05
                  }
                },
                workingset: {
                  bytes: 1_986_724
                },
                rss: {
                  bytes: 402_801
                },
                pagefaults: 296_495,
                majorpagefaults: 0
              },
              start_time: '2021-03-30T07:59:06Z',
              name: 'container-name-44'
            },
            namespace: 'namespace26'
          }
        },
        {
          create: {}
        },
        {
          "@timestamp": '2022-06-21T15:38:30Z',
          kubernetes: {
            host: 'gke-apps-0',
            node: 'gke-apps-0-0',
            pod: 'gke-apps-0-0-0',
            container: {
              cpu: {
                usage: {
                  nanocores: 40_018,
                  core: {
                    ns: 12_828_317_850
                  },
                  node: {
                    pct: 2.77905e-05
                  },
                  limit: {
                    pct: 2.77905e-05
                  }
                }
              },
              memory: {
                available: {
                  bytes: 1_062_428_344
                },
                usage: {
                  bytes: 265_142_477,
                  node: {
                    pct: 0.01770037710617187
                  },
                  limit: {
                    pct: 9.923134671484496e-05
                  }
                },
                workingset: {
                  bytes: 2_294_743
                },
                rss: {
                  bytes: 340_623
                },
                pagefaults: 224_530,
                majorpagefaults: 0
              },
              start_time: '2021-03-30T07:59:06Z',
              name: 'container-name-44'
            },
            namespace: 'namespace26'
          }
        }
      ]
    )
    puts response
    
    
    PUT /datastream/_bulk?refresh
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

#### 查看结果

创建文档并将其添加到数据流后，请检查以确认新索引的当前状态。

    
    
    response = client.indices.get_data_stream
    puts response
    
    
    GET _data_stream

如果尚未应用 ILM 策略，则结果将如下所示。请注意原始的"index_name"：".ds-datastream-<timestamp>-000001"。

    
    
    {
      "data_streams": [
        {
          "name": "datastream",
          "timestamp_field": {
            "name": "@timestamp"
          },
          "indices": [
            {
              "index_name": ".ds-datastream-2022.08.26-000001",
              "index_uuid": "5g-3HrfETga-5EFKBM6R-w"
            },
            {
              "index_name": ".ds-datastream-2022.08.26-000002",
              "index_uuid": "o0yRTdhWSo2pY8XMvfwy7Q"
            }
          ],
          "generation": 2,
          "status": "GREEN",
          "template": "datastream_template",
          "ilm_policy": "datastream_policy",
          "hidden": false,
          "system": false,
          "allow_custom_routing": false,
          "replicated": false,
          "time_series": {
            "temporal_ranges": [
              {
                "start": "2022-08-26T13:29:07.000Z",
                "end": "2022-08-26T19:29:07.000Z"
              }
            ]
          }
        }
      ]
    }

接下来，运行搜索查询：

    
    
    response = client.search(
      index: 'datastream'
    )
    puts response
    
    
    GET datastream/_search

该查询将返回十个新添加的文档。

    
    
    {
      "took": 17,
      "timed_out": false,
      "_shards": {
        "total": 4,
        "successful": 4,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": {
          "value": 10,
          "relation": "eq"
        },
    ...

默认情况下，索引生命周期管理每十分钟检查一次符合策略条件的索引。等待大约十分钟(也许冲泡一杯快咖啡或茶☕)，然后重新运行"获取_data_stream"请求。

    
    
    response = client.indices.get_data_stream
    puts response
    
    
    GET _data_stream

ILM 策略生效后，原始的".ds-datastream-2022.08.26-000001"索引将替换为新的缩减采样索引，在本例中为"downsample-6tkn-.ds-datastream-2022.08.26-000001"。

    
    
    {
      "data_streams": [
        {
          "name": "datastream",
          "timestamp_field": {
            "name": "@timestamp"
          },
          "indices": [
            {
              "index_name": "downsample-6tkn-.ds-datastream-2022.08.26-000001",
              "index_uuid": "qRane1fQQDCNgKQhXmTIvg"
            },
            {
              "index_name": ".ds-datastream-2022.08.26-000002",
              "index_uuid": "o0yRTdhWSo2pY8XMvfwy7Q"
            }
          ],
    ...

对数据流运行搜索查询(请注意，在查询缩减采样索引时，需要注意一些细微差别)。

    
    
    response = client.search(
      index: 'datastream'
    )
    puts response
    
    
    GET datastream/_search

新的缩减采样索引仅包含一个文档，其中包含基于原始采样度量的"最小"、"最大值"、"总和"和"value_count"统计信息。

    
    
    {
      "took": 6,
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
            "_index": "downsample-6tkn-.ds-datastream-2022.08.26-000001",
            "_id": "0eL0wC_4-45SnTNFAAABgtpz0wA",
            "_score": 1,
            "_source": {
              "@timestamp": "2022-08-26T14:00:00.000Z",
              "_doc_count": 10,
              "kubernetes.host": "gke-apps-0",
              "kubernetes.namespace": "namespace26",
              "kubernetes.node": "gke-apps-0-0",
              "kubernetes.pod": "gke-apps-0-0-0",
              "kubernetes.container.cpu.usage.nanocores": {
                "min": 38907,
                "max": 153404,
                "sum": 992677,
                "value_count": 10
              },
              "kubernetes.container.memory.available.bytes": {
                "min": 279586406,
                "max": 1062428344,
                "sum": 7101494721,
                "value_count": 10
              },
              "kubernetes.container.memory.pagefaults": {
                "min": 74843,
                "max": 302252,
                "sum": 2061071,
                "value_count": 10
              },
              "kubernetes.container.memory.rss.bytes": {
                "min": 91914,
                "max": 402801,
                "sum": 2389770,
                "value_count": 10
              },
              "kubernetes.container.memory.usage.bytes": {
                "min": 100475044,
                "max": 379572388,
                "sum": 2668170609,
                "value_count": 10
              },
              "kubernetes.container.memory.workingset.bytes": {
                "min": 431227,
                "max": 2294743,
                "sum": 14230488,
                "value_count": 10
              },
              "kubernetes.container.cpu.usage.core.ns": 12828317850,
              "kubernetes.container.cpu.usage.limit.pct": 0.000027790500098490156,
              "kubernetes.container.cpu.usage.node.pct": 0.000027790500098490156,
              "kubernetes.container.memory.majorpagefaults": 0,
              "kubernetes.container.memory.usage.limit.pct": 0.00009923134348355234,
              "kubernetes.container.memory.usage.node.pct": 0.017700377851724625,
              "kubernetes.container.name": "container-name-44",
              "kubernetes.container.start_time": "2021-03-30T07:59:06.000Z"
            }
          }
        ]
      }
    }

使用数据流统计信息 API 获取数据流的统计信息，包括存储大小。

    
    
    response = client.indices.data_streams_stats(
      name: 'datastream',
      human: true
    )
    puts response
    
    
    GET /_data_stream/datastream/_stats?human=true
    
    
    {
      "_shards": {
        "total": 4,
        "successful": 4,
        "failed": 0
      },
      "data_stream_count": 1,
      "backing_indices": 2,
      "total_store_size": "16.6kb",
      "total_store_size_bytes": 17059,
      "data_streams": [
        {
          "data_stream": "datastream",
          "backing_indices": 2,
          "store_size": "16.6kb",
          "store_size_bytes": 17059,
          "maximum_timestamp": 1661522400000
        }
      ]
    }

此示例演示了缩减采样作为 ILM 策略的一部分如何工作，以便在指标数据变得不那么最新且查询频率降低时减少指标数据的存储大小。

您还可以尝试我们的手动运行缩减像素采样示例，以了解缩减采样如何在 ILM 策略之外工作。

[« Downsampling a time series data stream](downsampling.md) [Run
downsampling manually »](downsampling-manual.md)
