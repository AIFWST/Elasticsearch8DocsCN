

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning APIs](ml-apis.md)

[« Machine learning APIs](ml-apis.md) [Get machine learning memory stats API
»](get-ml-memory.md)

## 获取机器学习信息接口

返回机器学习使用的默认值和限制。

###Request

"获取_ml/信息"

###Prerequisites

需要"monitor_ml"群集权限。此权限包含在"machine_learning_user"内置角色中。

###Description

此终结点旨在由需要完全了解未指定某些选项的机器学习配置的用户界面使用，这意味着应使用默认值。此终结点可用于找出这些默认值是什么。它还提供有关可在当前群集配置中运行的机器学习作业的最大大小的信息。

###Examples

终结点不带任何参数：

    
    
    response = client.ml.info
    puts response
    
    
    GET _ml/info

这是一个可能的响应：

    
    
    {
      "defaults" : {
        "anomaly_detectors" : {
          "categorization_analyzer" : {
            "char_filter" : [
              "first_line_with_letters"
            ],
            "tokenizer" : "ml_standard",
            "filter" : [
              {
                "type" : "stop",
                "stopwords" : [
                  "Monday",
                  "Tuesday",
                  "Wednesday",
                  "Thursday",
                  "Friday",
                  "Saturday",
                  "Sunday",
                  "Mon",
                  "Tue",
                  "Wed",
                  "Thu",
                  "Fri",
                  "Sat",
                  "Sun",
                  "January",
                  "February",
                  "March",
                  "April",
                  "May",
                  "June",
                  "July",
                  "August",
                  "September",
                  "October",
                  "November",
                  "December",
                  "Jan",
                  "Feb",
                  "Mar",
                  "Apr",
                  "May",
                  "Jun",
                  "Jul",
                  "Aug",
                  "Sep",
                  "Oct",
                  "Nov",
                  "Dec",
                  "GMT",
                  "UTC"
                ]
              },
              {
                "type": "limit",
                "max_token_count": "100"
              }
            ]
          },
          "model_memory_limit" : "1gb",
          "categorization_examples_limit" : 4,
          "model_snapshot_retention_days" : 10,
          "daily_model_snapshot_retention_after_days" : 1
        },
        "datafeeds" : {
          "scroll_size" : 1000
        }
      },
      "upgrade_mode": false,
      "native_code" : {
        "version": "7.0.0",
        "build_hash": "99a07c016d5a73"
      },
      "limits" : {
        "effective_max_model_memory_limit": "28961mb",
        "total_ml_memory": "86883mb"
      }
    }

[« Machine learning APIs](ml-apis.md) [Get machine learning memory stats API
»](get-ml-memory.md)
