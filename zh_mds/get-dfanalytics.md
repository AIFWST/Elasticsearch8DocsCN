

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning data frame analytics APIs](ml-df-
analytics-apis.md)

[« Explain data frame analytics API](explain-dfanalytics.md) [Get data frame
analytics jobs statistics API »](get-dfanalytics-stats.md)

## 获取数据帧分析作业API

检索数据框分析作业的配置信息。

###Request

"获取_ml/data_frame/分析/<data_frame_analytics_id>"

'GET_ml/data_frame/分析/<data_frame_analytics_id><data_frame_analytics_id>，'

"获取_ml/data_frame/分析/"

"获取_ml/data_frame/分析/_all"

###Prerequisites

需要"monitor_ml"群集权限。此权限包含在"machine_learning_user"内置角色中。

###Description

您可以使用以逗号分隔的数据帧分析作业列表或通配符表达式在单个 APIrequest 中获取多个数据框分析作业的信息。

### 路径参数

`<data_frame_analytics_id>`

    

(可选，字符串)数据框分析作业的标识符。如果未指定此选项，API 将返回前一百个数据帧分析作业的信息。

您可以通过使用 _all、将"*"指定为"<data_frame_analytics_id>"或省略"来获取所有数据框分析作业的信息<data_frame_analytics_id>。

### 查询参数

`allow_no_match`

    

(可选，布尔值)指定在请求时要执行的操作：

* 包含通配符表达式，并且没有匹配的数据框分析作业。  * 包含"_all"字符串或不包含标识符，并且没有匹配项。  * 包含通配符表达式，并且只有部分匹配。

默认值为"true"，当没有匹配项时返回空的"data_frame_analytics"数组，当存在部分匹配时返回结果子集。如果此参数为"false"，则当没有匹配项或只有部分匹配项时，请求将返回"404"状态代码。

`exclude_generated`

     (Optional, Boolean) Indicates if certain fields should be removed from the configuration on retrieval. This allows the configuration to be in an acceptable format to be retrieved and then added to another cluster. Default is false. 
`from`

     (Optional, integer) Skips the specified number of data frame analytics jobs. The default value is `0`. 
`size`

     (Optional, integer) Specifies the maximum number of data frame analytics jobs to obtain. The default value is `100`. 

### 响应正文

`data_frame_analytics`

    

(阵列)数据帧分析作业资源的数组，按"id"值升序排序。

数据框分析作业资源的属性

`analysis`

     (object) The type of analysis that is performed on the `source`. 

`analyzed_fields`

    

(对象)包含"包含"和/或"排除"模式，用于选择分析中包含的字段。

"analyzed_fields"的属性

`excludes`

     (Optional, array) An array of strings that defines the fields that are excluded from the analysis. 
`includes`

     (Optional, array) An array of strings that defines the fields that are included in the analysis. 

`authorization`

    

(对象)作业用于运行其查询的安全特权。如果在最近更新作业时禁用了 Elastic Stack 安全功能，则省略此属性。

"授权"的属性

`api_key`

    

(对象)如果 API 密钥用于作业的最新更新，则响应中会列出其名称和标识符。

"api_key"的属性

`id`

     (string) The identifier for the API key. 
`name`

     (string) The name of the API key. 

`roles`

     (array of strings) If a user ID was used for the most recent update to the job, its roles at the time of the update are listed in the response. 
`service_account`

     (string) If a service account was used for the most recent update to the job, the account name is listed in the response. 

`dest`

    

(字符串)分析的目标配置。

"目标"的属性

`index`

     (string) The _destination index_ that stores the results of the data frame analytics job. 
`results_field`

     (string) The name of the field that stores the results of the analysis. Defaults to `ml`. 

`id`

     (string) The unique identifier of the data frame analytics job. 
`model_memory_limit`

     (string) The `model_memory_limit` that has been set for the data frame analytics job. 
`source`

    

(对象)分析数据来源方式的配置。它有一个"索引"参数，可以选择一个"查询"和一个"_source"。

"源"的属性

`index`

     (array) Index or indices on which to perform the analysis. It can be a single index or index pattern as well as an array of indices or patterns. 
`query`

     (object) The query that has been specified for the data frame analytics job. The Elasticsearch query domain-specific language ([DSL](query-dsl.html "Query DSL")). This value corresponds to the query object in an Elasticsearch search POST body. By default, this property has the following value: `{"match_all": {}}`. 
`_source`

    

(对象)包含指定的"包含"和/或"排除"模式，用于选择目标中存在的字段。排除的字段不能包含在分析中。

"_source"的属性

`excludes`

     (array) An array of strings that defines the fields that are excluded from the destination. 
`includes`

     (array) An array of strings that defines the fields that are included in the destination. 

### 响应码

"404"(缺少资源)

     If `allow_no_match` is `false`, this code indicates that there are no resources that match the request or only partial matches for the request. 

###Examples

以下示例获取"日志分析"数据帧分析作业的配置信息：

    
    
    response = client.ml.get_data_frame_analytics(
      id: 'loganalytics'
    )
    puts response
    
    
    GET _ml/data_frame/analytics/loganalytics

API 返回以下结果：

    
    
    {
      "count" : 1,
      "data_frame_analytics" : [
        {
          "id" : "loganalytics",
          "create_time" : 1656364565517,
          "version" : "8.4.0",
          "authorization" : {
            "roles" : [
              "superuser"
            ]
          },
          "description" : "Outlier detection on log data",
          "source" : {
            "index" : [
              "logdata"
            ],
            "query" : {
              "match_all" : { }
            }
          },
          "dest" : {
            "index" : "logdata_out",
            "results_field" : "ml"
          },
          "analysis" : {
            "outlier_detection" : {
              "compute_feature_influence" : true,
              "outlier_fraction" : 0.05,
              "standardization_enabled" : true
            }
          },
          "model_memory_limit" : "1gb",
          "allow_lazy_start" : false,
          "max_num_threads" : 1
        }
      ]
    }

[« Explain data frame analytics API](explain-dfanalytics.md) [Get data frame
analytics jobs statistics API »](get-dfanalytics-stats.md)
