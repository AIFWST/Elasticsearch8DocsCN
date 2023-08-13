

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Create calendars API](ml-put-calendar.md) [Create filters API »](ml-put-
filter.md)

## 创建数据馈送接口

实例化数据馈送。

###Request

"放置_ml/数据馈送/<feed_id>"

###Prerequisites

* 必须先创建异常情况检测作业，然后才能创建数据馈送。  * 需要以下权限：

    * cluster: `manage_ml` (the `machine_learning_admin` built-in role grants this privilege) 
    * source index configured in the datafeed: `read`

###Description

数据馈送从 Elasticsearch 检索数据，以便通过异常检测作业进行分析。只能将一个数据馈送关联到每个异常情况检测作业。

数据馈送包含按定义的间隔("频率")运行的查询。如果您担心数据延迟，可以在每个时间间隔添加延迟("query_delay")。请参阅处理延迟数据。

* 您必须使用 Kibana、此 API 或创建异常情况检测作业 API 来创建数据馈送。不要使用 Elasticsearch 索引 API 将数据馈送到 '.ml-config' 索引中。如果启用了 Elasticsearch 安全功能，请不要授予用户对".ml-config"索引的"写入"权限。  * 启用 Elasticsearch 安全功能后，您的数据馈送会记住创建它的用户在创建时具有哪些角色，并使用这些相同的角色运行查询。如果提供辅助授权标头，则改用这些凭据。

### 路径参数

`<feed_id>`

     (Required, string) A numerical character string that uniquely identifies the datafeed. This identifier can contain lowercase alphanumeric characters (a-z and 0-9), hyphens, and underscores. It must start and end with alphanumeric characters. 

### 查询参数

`allow_no_indices`

     (Optional, Boolean) If `true`, wildcard indices expressions that resolve into no concrete indices are ignored. This includes the `_all` string or when no indices are specified. Defaults to `true`. 
`expand_wildcards`

    

(可选，字符串)通配符模式可以匹配的索引类型。如果请求可以以数据流为目标，则此参数确定通配符表达式是否与隐藏的数据流匹配。支持逗号分隔的值，例如"打开，隐藏"。有效值为：

`all`

     Match any data stream or index, including [hidden](api-conventions.html#multi-hidden "Hidden data streams and indices") ones. 
`open`

     Match open, non-hidden indices. Also matches any non-hidden data stream. 
`closed`

     Match closed, non-hidden indices. Also matches any non-hidden data stream. Data streams cannot be closed. 
`hidden`

     Match hidden data streams and hidden indices. Must be combined with `open`, `closed`, or both. 
`none`

     Wildcard patterns are not accepted. 

默认为"打开"。

`ignore_throttled`

    

(可选，布尔值)如果为"true"，则在冻结时将忽略具体索引、扩展索引或别名索引。默认为"真"。

[7.16.0] 在 7.16.0 中已弃用。

`ignore_unavailable`

     (Optional, Boolean) If `true`, unavailable indices (missing or closed) are ignored. Defaults to `false`. 

### 请求正文

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

###Examples

为异常情况检测作业("测试作业")创建数据馈送：

    
    
    PUT _ml/datafeeds/datafeed-test-job?pretty
    {
      "indices": [
        "kibana_sample_data_logs"
      ],
      "query": {
        "bool": {
          "must": [
            {
              "match_all": {}
            }
          ]
        }
      },
      "job_id": "test-job"
    }

创建数据馈送后，您会收到以下结果：

    
    
    {
      "datafeed_id" : "datafeed-test-job",
      "job_id" : "test-job",
      "authorization" : {
        "roles" : [
          "superuser"
        ]
      },
      "query_delay" : "91820ms",
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
          "must" : [
            {
              "match_all" : { }
            }
          ]
        }
      },
      "indices" : [
        "kibana_sample_data_logs"
      ],
      "scroll_size" : 1000,
      "delayed_data_check_config" : {
        "enabled" : true
      }
    }

[« Create calendars API](ml-put-calendar.md) [Create filters API »](ml-put-
filter.md)
