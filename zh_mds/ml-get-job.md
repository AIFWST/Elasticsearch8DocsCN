

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Get influencers API](ml-get-influencer.md) [Get anomaly detection job
statistics API »](ml-get-job-stats.md)

## 获取异常情况检测作业API

检索异常情况检测作业的配置信息。

###Request

"得到_ml/anomaly_detectors<job_id>/"

"得到_ml/anomaly_detectors/<job_id><job_id>，"

"得到_ml/anomaly_detectors/"

"得到_ml/anomaly_detectors/_all"

###Prerequisites

需要"monitor_ml"群集权限。此权限包含在"machine_learning_user"内置角色中。

###Description

此 API 最多返回 10，000 个作业。

### 路径参数

`<job_id>`

     (Optional, string) Identifier for the anomaly detection job. It can be a job identifier, a group name, or a wildcard expression. You can get information for multiple anomaly detection jobs in a single API request by using a group name, a comma-separated list of jobs, or a wildcard expression. You can get information for all anomaly detection jobs by using `_all`, by specifying `*` as the job identifier, or by omitting the identifier. 

### 查询参数

`allow_no_match`

    

(可选，布尔值)指定在请求时要执行的操作：

* 包含通配符表达式，并且没有匹配的作业。  * 包含"_all"字符串或不包含标识符，并且没有匹配项。  * 包含通配符表达式，并且只有部分匹配。

默认值为"true"，当没有匹配项时，它将返回一个空的"jobs"数组，当存在部分匹配时，它将返回结果的子集。如果此参数为"false"，则当没有匹配项或只有部分匹配项时，请求将返回"404"状态代码。

`exclude_generated`

     (Optional, Boolean) Indicates if certain fields should be removed from the configuration on retrieval. This allows the configuration to be in an acceptable format to be retrieved and then added to another cluster. Default is false. 

### 响应正文

API 返回异常情况检测作业资源数组。有关属性的完整列表，请参阅创建异常情况检测作业 API。

`blocked`

    

(对象)如果存在，它说明在阻止其打开的作业上执行了任务。

"已阻止"的属性

`reason`

     (string) The reason the job is blocked. Values may be `delete`, `reset`, `revert`. Each value means the corresponding action is being executed. 
`task_id`

     (string) The task id of the blocking action. You can use the [Task management](tasks.html "Task management API") API to monitor progress. 

`create_time`

     (string) The time the job was created. For example, `1491007356077`. This property is informational; you cannot change its value. 
`datafeed_config`

    

(对象)为当前异常情况检测作业配置的数据馈送。

"datafeed_config"的属性

`authorization`

    

(可选，对象)数据馈送用于运行其查询的安全特权。如果在最近更新数据馈送时禁用了 Elastic Stack 安全功能，则省略此属性。

"授权"的属性

`api_key`

    

(对象)如果 API 密钥用于数据馈送的最新更新，则响应中会列出其名称和标识符。

"api_key"的属性

`id`

     (string) The identifier for the API key. 
`name`

     (string) The name of the API key. 

`roles`

     (array of strings) If a user ID was used for the most recent update to the datafeed, its roles at the time of the update are listed in the response. 
`service_account`

     (string) If a service account was used for the most recent update to the datafeed, the account name is listed in the response. 

`datafeed_id`

     (Optional, string) A numerical character string that uniquely identifies the datafeed. This identifier can contain lowercase alphanumeric characters (a-z and 0-9), hyphens, and underscores. It must start and end with alphanumeric characters. 
`aggregations`

     (Optional, object) If set, the datafeed performs aggregation searches. Support for aggregations is limited and should be used only with low cardinality data. For more information, see [Aggregating data for faster performance](/guide/en/machine-learning/8.9/ml-configuring-aggregation.html). 
`chunking_config`

    

(可选，对象)可能需要数据馈送在很长一段时间内搜索，持续数月或数年。此搜索被拆分为时间块，以确保 Elasticsearch 上的负载得到管理。分块配置控制如何计算这些时间块的大小，并且是一个高级配置选项。

"chunking_config"的属性

`mode`

    

(字符串)有三种可用的模式：

* "auto"：块大小是动态计算的。这是数据馈送不使用聚合时的默认值和建议值。  * "手动"：根据指定的"time_span"应用分块。当数据馈送使用聚合时，使用此模式。  * "关闭"：不应用分块。

`time_span`

     ([time units](api-conventions.html#time-units "Time units")) The time span that each search will be querying. This setting is only applicable when the mode is set to `manual`. For example: `3h`. 

`delayed_data_check_config`

    

(可选，对象)指定数据馈送是否检查缺失的数据以及窗口的大小。例如："{"enabled"： true， "check_window"："1h"}'。

数据馈送可以选择搜索已读取的索引，以确定随后是否将任何数据添加到索引中。如果发现缺少数据，则表明"query_delay"选项设置得太低，并且在数据馈送通过该时刻后正在索引数据。请参阅使用延迟数据。

此检查仅在实时数据馈送上运行。

"delayed_data_check_config"的属性

`check_window`

     ([time units](api-conventions.html#time-units "Time units")) The window of time that is searched for late data. This window of time ends with the latest finalized bucket. It defaults to `null`, which causes an appropriate `check_window` to be calculated when the real-time datafeed runs. In particular, the default `check_window` span calculation is based on the maximum of `2h` or `8 * bucket_span`. 
`enabled`

     (Boolean) Specifies whether the datafeed periodically checks for delayed data. Defaults to `true`. 

`frequency`

     (Optional, [time units](api-conventions.html#time-units "Time units")) The interval at which scheduled queries are made while the datafeed runs in real time. The default value is either the bucket span for short bucket spans, or, for longer bucket spans, a sensible fraction of the bucket span. For example: `150s`. When `frequency` is shorter than the bucket span, interim results for the last (partial) bucket are written then eventually overwritten by the full bucket results. If the datafeed uses aggregations, this value must be divisible by the interval of the date histogram aggregation. 
`indices`

    

(必需，阵列)索引名称的数组。支持通配符。例如："["it_ops_metrics"、"服务器*"]"。

如果任何索引位于远程集群中，则机器学习节点需要具有"remote_cluster_client"角色。

`indices_options`

    

(可选，对象)指定在搜索期间使用的索引扩展选项。

例如：

    
    
    {
       "expand_wildcards": ["all"],
       "ignore_unavailable": true,
       "allow_no_indices": "false",
       "ignore_throttled": true
    }

有关这些选项的详细信息，请参阅多目标语法。

`job_id`

     (Required, string) Identifier for the anomaly detection job. 
`max_empty_searches`

     (Optional,integer) If a real-time datafeed has never seen any data (including during any initial training period) then it will automatically stop itself and close its associated job after this many real-time searches that return no documents. In other words, it will stop after `frequency` times `max_empty_searches` of real-time operation. If not set then a datafeed with no end time that sees no data will remain started until it is explicitly stopped. By default this setting is not set. 
`query`

     (Optional, object) The Elasticsearch query domain-specific language (DSL). This value corresponds to the query object in an Elasticsearch search POST body. All the options that are supported by Elasticsearch can be used, as this object is passed verbatim to Elasticsearch. By default, this property has the following value: `{"match_all": {"boost": 1}}`. 
`query_delay`

     (Optional, [time units](api-conventions.html#time-units "Time units")) The number of seconds behind real time that data is queried. For example, if data from 10:04 a.m. might not be searchable in Elasticsearch until 10:06 a.m., set this property to 120 seconds. The default value is randomly selected between `60s` and `120s`. This randomness improves the query performance when there are multiple jobs running on the same node. For more information, see [Handling delayed data](/guide/en/machine-learning/8.9/ml-delayed-data-detection.html). 
`runtime_mappings`

    

(可选，对象)指定数据馈送搜索的运行时字段。

例如：

    
    
    {
      "day_of_week": {
        "type": "keyword",
        "script": {
          "source": "emit(doc['@timestamp'].value.dayOfWeekEnum.getDisplayName(TextStyle.FULL, Locale.ROOT))"
        }
      }
    }

`script_fields`

     (Optional, object) Specifies scripts that evaluate custom expressions and returns script fields to the datafeed. The detector configuration objects in a job can contain functions that use these script fields. For more information, see [Transforming data with script fields](/guide/en/machine-learning/8.9/ml-configuring-transform.html) and [Script fields](search-fields.html#script-fields "Script fields"). 
`scroll_size`

     (Optional, unsigned integer) The `size` parameter that is used in Elasticsearch searches when the datafeed does not use aggregations. The default value is `1000`. The maximum value is the value of `index.max_result_window` which is 10,000 by default. 

`finished_time`

     (string) If the job closed or failed, this is the time the job finished, otherwise it is `null`. This property is informational; you cannot change its value. 
`job_type`

     (string) Reserved for future use, currently set to `anomaly_detector`. 
`job_version`

     (string) The version of Elasticsearch that existed on the node when the job was created. 
`model_snapshot_id`

     (string) A numerical character string that uniquely identifies the model snapshot. For example, `1575402236000`. 

### 响应码

"404"(缺少资源)

     If `allow_no_match` is `false`, this code indicates that there are no resources that match the request or only partial matches for the request. 

###Examples

    
    
    response = client.ml.get_jobs(
      job_id: 'high_sum_total_sales'
    )
    puts response
    
    
    GET _ml/anomaly_detectors/high_sum_total_sales

API 返回以下结果：

    
    
    {
      "count": 1,
      "jobs": [
        {
          "job_id" : "high_sum_total_sales",
          "job_type" : "anomaly_detector",
          "job_version" : "8.4.0",
          "create_time" : 1655852735889,
          "finished_time" : 1655852745980,
          "model_snapshot_id" : "1575402237",
          "custom_settings" : {
            "created_by" : "ml-module-sample",
            ...
          },
          "datafeed_config" : {
            "datafeed_id" : "datafeed-high_sum_total_sales",
            "job_id" : "high_sum_total_sales",
            "authorization" : {
              "roles" : [
                "superuser"
              ]
            },
            "query_delay" : "93169ms",
            "chunking_config" : {
              "mode" : "auto"
            },
            "indices_options" : {
              "expand_wildcards" : [
                "open"
              ],
              "ignore_unavailable" : false,
              "allow_no_indices" : true,
              "ignore_throttled" : true
            },
            "query" : {
              "bool" : {
                "filter" : [
                  {
                    "term" : {
                      "event.dataset" : "sample_ecommerce"
                    }
                  }
                ]
              }
            },
            "indices" : [
              "kibana_sample_data_ecommerce"
            ],
            "scroll_size" : 1000,
            "delayed_data_check_config" : {
              "enabled" : true
            }
          },
          "groups" : [
            "kibana_sample_data",
            "kibana_sample_ecommerce"
          ],
          "description" : "Find customers spending an unusually high amount in an hour",
          "analysis_config" : {
            "bucket_span" : "1h",
            "detectors" : [
              {
                "detector_description" : "High total sales",
                "function" : "high_sum",
                "field_name" : "taxful_total_price",
                "over_field_name" : "customer_full_name.keyword",
                "detector_index" : 0
              }
            ],
            "influencers" : [
              "customer_full_name.keyword",
              "category.keyword"
            ],
            "model_prune_window": "30d"
          },
          "analysis_limits" : {
            "model_memory_limit" : "13mb",
            "categorization_examples_limit" : 4
          },
          "data_description" : {
            "time_field" : "order_date",
            "time_format" : "epoch_ms"
          },
          "model_plot_config" : {
            "enabled" : true,
            "annotations_enabled" : true
          },
          "model_snapshot_retention_days" : 10,
          "daily_model_snapshot_retention_after_days" : 1,
          "results_index_name" : "shared",
          "allow_lazy_open" : false
        }
      ]
    }

[« Get influencers API](ml-get-influencer.md) [Get anomaly detection job
statistics API »](ml-get-job-stats.md)
