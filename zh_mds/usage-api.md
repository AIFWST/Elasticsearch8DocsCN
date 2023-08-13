

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md)

[« Upgrade transforms API](upgrade-transforms.md) [Watcher APIs »](watcher-
api.md)

## 用法接口

提供有关已安装的 X-Pack 功能的使用信息。

###Request

"获取/_xpack/使用情况"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

###Description

此 API 提供有关当前许可证下已启用和可用的功能的信息，以及一些使用情况统计信息。

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

    
    
    response = client.xpack.usage
    puts response
    
    
    GET /_xpack/usage
    
    
    {
      "security" : {
        "available" : true,
        "enabled" : false
      },
      "monitoring" : {
        "available" : true,
        "enabled" : true,
        "collection_enabled" : false,
        "enabled_exporters" : {
          "local" : 1
        }
      },
      "watcher" : {
          "available" : true,
          "enabled" : true,
          "execution" : {
            "actions" : {
              "_all" : {
                "total" : 0,
                "total_time_in_ms" : 0
              }
            }
          },
        "watch" : {
          "input" : {
            "_all" : {
              "total" : 0,
              "active" : 0
            }
          },
          "trigger" : {
            "_all" : {
              "total" : 0,
              "active" : 0
            }
          }
        },
        "count" : {
          "total" : 0,
          "active" : 0
        }
      },
      "graph" : {
        "available" : true,
        "enabled" : true
      },
      "ml" : {
        "available" : true,
        "enabled" : true,
        "jobs" : {
          "_all" : {
            "count" : 0,
            "detectors" : {
              ...
            },
            "created_by" : { },
            "model_size" : {
              ...
            },
            "forecasts" : {
              "total" : 0,
              "forecasted_jobs" : 0
            }
          }
        },
        "datafeeds" : {
          "_all" : {
            "count" : 0
          }
        },
        "data_frame_analytics_jobs" : {
          "_all" : {
            "count" : 0
          },
          "analysis_counts": { },
          "memory_usage": {
            "peak_usage_bytes": {
              "min": 0.0,
              "max": 0.0,
              "avg": 0.0,
              "total": 0.0
            }
          }
        },
        "inference" : {
          "ingest_processors" : {
            "_all" : {
              "num_docs_processed" : {
                "max" : 0,
                "sum" : 0,
                "min" : 0
              },
              "pipelines" : {
                "count" : 0
              },
              "num_failures" : {
                "max" : 0,
                "sum" : 0,
                "min" : 0
              },
              "time_ms" : {
                "max" : 0,
                "sum" : 0,
                "min" : 0
              }
            }
          },
          "trained_models" : {
            "_all" : {
              "count": 1
            },
            "count": {
              "total": 1,
              "prepackaged": 1,
              "other": 0
            },
            "model_size_bytes": {
              "min": 0.0,
              "max": 0.0,
              "avg": 0.0,
              "total": 0.0
            },
            "estimated_operations": {
              "min": 0.0,
              "max": 0.0,
              "avg": 0.0,
              "total": 0.0
            }
          },
          "deployments": {
            "count": 0,
            "inference_counts": {
              "total": 0.0,
              "min": 0.0,
              "avg": 0.0,
              "max": 0.0
            },
            "model_sizes_bytes": {
              "total": 0.0,
              "min": 0.0,
              "avg": 0.0,
              "max": 0.0
            },
            "time_ms": {
              "avg": 0.0
            }
          }
        },
        "node_count" : 1
      },
      "logstash" : {
        "available" : true,
        "enabled" : true
      },
      "eql" : {
        "available" : true,
        "enabled" : true
      },
      "sql" : {
        "available" : true,
        "enabled" : true,
        "features" : {
          "having" : 0,
          "subselect" : 0,
          "limit" : 0,
          "orderby" : 0,
          "where" : 0,
          "join" : 0,
          "groupby" : 0,
          "command" : 0,
          "local" : 0
        },
        "queries" : {
          "rest" : {
            "total" : 0,
            "paging" : 0,
            "failed" : 0
          },
          "cli" : {
            "total" : 0,
            "paging" : 0,
            "failed" : 0
          },
          "canvas" : {
            "total" : 0,
            "paging" : 0,
            "failed" : 0
          },
          "odbc" : {
            "total" : 0,
            "paging" : 0,
            "failed" : 0
          },
          "jdbc" : {
            "total" : 0,
            "paging" : 0,
            "failed" : 0
          },
          "odbc32" : {
            "total" : 0,
            "paging" : 0,
            "failed" : 0
          },
          "odbc64" : {
            "total" : 0,
            "paging" : 0,
            "failed" : 0
          },
          "_all" : {
            "total" : 0,
            "paging" : 0,
            "failed" : 0
          },
          "translate" : {
            "count" : 0
          }
        }
      },
      "rollup" : {
        "available" : true,
        "enabled" : true
      },
      "ilm" : {
        "policy_count" : 3,
        "policy_stats" : [
          ...
        ]
      },
      "slm" : {
        "available" : true,
        "enabled" : true
      },
      "ccr" : {
        "available" : true,
        "enabled" : true,
        "follower_indices_count" : 0,
        "auto_follow_patterns_count" : 0
      },
      "transform" : {
        "available" : true,
        "enabled" : true
      },
      "voting_only" : {
        "available" : true,
        "enabled" : true
      },
      "searchable_snapshots" : {
        "available" : true,
        "enabled" : true,
        "indices_count" : 0,
        "full_copy_indices_count" : 0,
        "shared_cache_indices_count" : 0
      },
      "frozen_indices" : {
        "available" : true,
        "enabled" : true,
        "indices_count" : 0
      },
      "spatial" : {
        "available" : true,
        "enabled" : true
      },
      "analytics" : {
        "available" : true,
        "enabled" : true,
        "stats": {
          "boxplot_usage" : 0,
          "top_metrics_usage" : 0,
          "normalize_usage" : 0,
          "cumulative_cardinality_usage" : 0,
          "t_test_usage" : 0,
          "rate_usage" : 0,
          "string_stats_usage" : 0,
          "moving_percentiles_usage" : 0,
          "multi_terms_usage" : 0
        }
      },
      "data_streams" : {
        "available" : true,
        "enabled" : true,
        "data_streams" : 0,
        "indices_count" : 0
      },
      "data_lifecycle" : {
        "available": true,
        "enabled": true,
        "count": 0,
        "default_rollover_used": true,
        "retention": {
            "minimum_millis": 0,
            "maximum_millis": 0,
            "average_millis": 0.0
        }
      },
      "data_tiers" : {
        "available" : true,
        "enabled" : true,
        "data_warm" : {
          "node_count" : 0,
          "index_count" : 0,
          "total_shard_count" : 0,
          "primary_shard_count" : 0,
          "doc_count" : 0,
          "total_size_bytes" : 0,
          "primary_size_bytes" : 0,
          "primary_shard_size_avg_bytes" : 0,
          "primary_shard_size_median_bytes" : 0,
          "primary_shard_size_mad_bytes" : 0
        },
        "data_frozen" : {
          "node_count" : 1,
          "index_count" : 0,
          "total_shard_count" : 0,
          "primary_shard_count" : 0,
          "doc_count" : 0,
          "total_size_bytes" : 0,
          "primary_size_bytes" : 0,
          "primary_shard_size_avg_bytes" : 0,
          "primary_shard_size_median_bytes" : 0,
          "primary_shard_size_mad_bytes" : 0
        },
        "data_cold" : {
          "node_count" : 0,
          "index_count" : 0,
          "total_shard_count" : 0,
          "primary_shard_count" : 0,
          "doc_count" : 0,
          "total_size_bytes" : 0,
          "primary_size_bytes" : 0,
          "primary_shard_size_avg_bytes" : 0,
          "primary_shard_size_median_bytes" : 0,
          "primary_shard_size_mad_bytes" : 0
        },
        "data_content" : {
          "node_count" : 0,
          "index_count" : 0,
          "total_shard_count" : 0,
          "primary_shard_count" : 0,
          "doc_count" : 0,
          "total_size_bytes" : 0,
          "primary_size_bytes" : 0,
          "primary_shard_size_avg_bytes" : 0,
          "primary_shard_size_median_bytes" : 0,
          "primary_shard_size_mad_bytes" : 0
        },
        "data_hot" : {
          "node_count" : 0,
          "index_count" : 0,
          "total_shard_count" : 0,
          "primary_shard_count" : 0,
          "doc_count" : 0,
          "total_size_bytes" : 0,
          "primary_size_bytes" : 0,
          "primary_shard_size_avg_bytes" : 0,
          "primary_shard_size_median_bytes" : 0,
          "primary_shard_size_mad_bytes" : 0
        }
      },
      "aggregate_metric" : {
        "available" : true,
        "enabled" : true
      },
      "archive" : {
        "available" : true,
        "enabled" : true,
        "indices_count" : 0
      },
      "health_api" : {
        "available" : true,
        "enabled" : true,
        "invocations": {
          "total": 0
        }
      },
      "enterprise_search" : {
        "available": true,
        "enabled": true,
        "search_applications" : {
          "count": 0
        },
        "analytics_collections": {
          "count": 0
        }
      }
    }

[« Upgrade transforms API](upgrade-transforms.md) [Watcher APIs »](watcher-
api.md)
