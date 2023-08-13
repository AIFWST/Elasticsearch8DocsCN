

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Pipeline aggregations](search-
aggregations-pipeline.md)

[« Extended stats bucket aggregation](search-aggregations-pipeline-extended-
stats-bucket-aggregation.md) [Max bucket aggregation »](search-aggregations-
pipeline-max-bucket-aggregation.md)

## 推理桶聚合

父管道聚合，用于加载预先训练的模型，并对父存储桶聚合中的整理结果字段执行推理。

要使用推理存储桶聚合，您需要具有使用获取训练模型 API 所需的相同安全权限。

###Syntax

"推理"聚合孤立地如下所示：

    
    
    {
      "inference": {
        "model_id": "a_model_for_inference", __"inference_config": { __"regression_config": {
            "num_top_feature_importance_values": 2
          }
        },
        "buckets_path": {
          "avg_cost": "avg_agg", __"max_cost": "max_agg"
        }
      }
    }

__

|

已训练模型的唯一标识符或别名。   ---|---    __

|

覆盖模型默认设置的可选推理配置 __

|

将"avg_agg"的值映射到模型的输入字段"avg_cost" **表 61."推理" 参数**

参数名称 |描述 |必填 |默认值 ---|---|---|--- 'model_id'

|

已训练模型的 ID 或别名。

|

Required

|

- "inference_config"

|

包含推理类型及其选项。有两种类型："回归"和"分类"

|

Optional

|

- "buckets_path"

|

定义输入聚合的路径，并将聚合名称映射到模型所需的字段名称。有关更多详细信息，请参阅"buckets_path"语法

|

Required

|

- ### 推理模型编辑的配置选项

"inference_config"设置是可选的，通常不是必需的，因为预先训练的模型配备了合理的默认值。在聚合的上下文中，可以为两种类型的模型中的每一种覆盖某些选项。

##### 回归模型的配置选项

`num_top_feature_importance_values`

     (Optional, integer) Specifies the maximum number of [feature importance](/guide/en/machine-learning/8.9/ml-feature-importance.html) values per document. By default, it is zero and no feature importance calculation occurs. 

##### 分类模型的配置选项

`num_top_classes`

     (Optional, integer) Specifies the number of top class predictions to return. Defaults to 0. 
`num_top_feature_importance_values`

     (Optional, integer) Specifies the maximum number of [feature importance](/guide/en/machine-learning/8.9/ml-feature-importance.html) values per document. Defaults to 0 which means no feature importance calculation occurs. 
`prediction_field_type`

     (Optional, string) Specifies the type of the predicted field to write. Valid values are: `string`, `number`, `boolean`. When `boolean` is provided `1.0` is transformed to `true` and `0.0` to `false`. 

###Example

以下代码片段按"client_ip"聚合 Web 日志，并通过指标和存储桶子聚合提取许多特征，作为推理聚合的输入，该推理聚合配置了经过训练以识别可疑客户端 IP 的模型：

    
    
    response = client.search(
      index: 'kibana_sample_data_logs',
      body: {
        size: 0,
        aggregations: {
          client_ip: {
            composite: {
              sources: [
                {
                  client_ip: {
                    terms: {
                      field: 'clientip'
                    }
                  }
                }
              ]
            },
            aggregations: {
              url_dc: {
                cardinality: {
                  field: 'url.keyword'
                }
              },
              bytes_sum: {
                sum: {
                  field: 'bytes'
                }
              },
              geo_src_dc: {
                cardinality: {
                  field: 'geo.src'
                }
              },
              geo_dest_dc: {
                cardinality: {
                  field: 'geo.dest'
                }
              },
              responses_total: {
                value_count: {
                  field: 'timestamp'
                }
              },
              success: {
                filter: {
                  term: {
                    response: '200'
                  }
                }
              },
              "error404": {
                filter: {
                  term: {
                    response: '404'
                  }
                }
              },
              "error503": {
                filter: {
                  term: {
                    response: '503'
                  }
                }
              },
              malicious_client_ip: {
                inference: {
                  model_id: 'malicious_clients_model',
                  buckets_path: {
                    response_count: 'responses_total',
                    url_dc: 'url_dc',
                    bytes_sum: 'bytes_sum',
                    geo_src_dc: 'geo_src_dc',
                    geo_dest_dc: 'geo_dest_dc',
                    success: 'success._count',
                    "error404": 'error404._count',
                    "error503": 'error503._count'
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET kibana_sample_data_logs/_search
    {
      "size": 0,
      "aggs": {
        "client_ip": { __"composite": {
            "sources": [
              {
                "client_ip": {
                  "terms": {
                    "field": "clientip"
                  }
                }
              }
            ]
          },
          "aggs": { __"url_dc": {
              "cardinality": {
                "field": "url.keyword"
              }
            },
            "bytes_sum": {
              "sum": {
                "field": "bytes"
              }
            },
            "geo_src_dc": {
              "cardinality": {
                "field": "geo.src"
              }
            },
            "geo_dest_dc": {
              "cardinality": {
                "field": "geo.dest"
              }
            },
            "responses_total": {
              "value_count": {
                "field": "timestamp"
              }
            },
            "success": {
              "filter": {
                "term": {
                  "response": "200"
                }
              }
            },
            "error404": {
              "filter": {
                "term": {
                  "response": "404"
                }
              }
            },
            "error503": {
              "filter": {
                "term": {
                  "response": "503"
                }
              }
            },
            "malicious_client_ip": { __"inference": {
                "model_id": "malicious_clients_model",
                "buckets_path": {
                  "response_count": "responses_total",
                  "url_dc": "url_dc",
                  "bytes_sum": "bytes_sum",
                  "geo_src_dc": "geo_src_dc",
                  "geo_dest_dc": "geo_dest_dc",
                  "success": "success._count",
                  "error404": "error404._count",
                  "error503": "error503._count"
                }
              }
            }
          }
        }
      }
    }

__

|

按"client_ip"聚合数据的复合存储桶聚合。   ---|---    __

|

一系列指标和存储桶子聚合。   __

|

推理存储桶聚合，用于指定经过训练的模型并将聚合名称映射到模型的输入字段。   « 扩展统计信息存储桶聚合 最大存储桶聚合 »