

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning data frame analytics APIs](ml-df-
analytics-apis.md)

[« Stop data frame analytics jobs API](stop-dfanalytics.md) [Machine
learning trained model APIs »](ml-df-trained-models-apis.md)

## 更新数据帧分析作业API

更新现有数据框分析作业。

###Request

"发布_ml/data_frame/分析/<data_frame_analytics_id>/_update"

###Prerequisites

需要以下权限：

* 集群："manage_ml"("machine_learning_admin"内置角色授予此权限) * 源索引："读取"、"view_index_metadata" * 目标索引："读取"、"create_index"、"管理"和"索引"

数据框分析作业会记住更新它的用户在更新时具有哪些角色。启动作业时，它将使用相同的角色执行分析。如果提供辅助授权标头，则会改用这些凭据。

###Description

此 API 更新现有数据帧分析作业，该作业对源索引执行分析并将结果存储在目标索引中。

### 路径参数

`<data_frame_analytics_id>`

     (Required, string) Identifier for the data frame analytics job. This identifier can contain lowercase alphanumeric characters (a-z and 0-9), hyphens, and underscores. It must start and end with alphanumeric characters. 

### 请求正文

`allow_lazy_start`

     (Optional, Boolean) Specifies whether this job can start when there is insufficient machine learning node capacity for it to be immediately assigned to a node. The default is `false`; if a machine learning node with capacity to run the job cannot immediately be found, the API returns an error. However, this is also subject to the cluster-wide `xpack.ml.max_lazy_ml_nodes` setting. See [Advanced machine learning settings](ml-settings.html#advanced-ml-settings "Advanced machine learning settings"). If this option is set to `true`, the API does not return an error and the job waits in the `starting` state until sufficient machine learning node capacity is available. 
`description`

     (Optional, string) A description of the job. 
`max_num_threads`

     (Optional, integer) The maximum number of threads to be used by the analysis. The default value is `1`. Using more threads may decrease the time necessary to complete the analysis at the cost of using more CPU. Note that the process may use additional threads for operational functionality other than the analysis itself. 
`_meta`

     (Optional, object) Advanced configuration option. Contains custom metadata about the job. For example, it can contain custom URL information. 
`model_memory_limit`

     (Optional, string) The approximate maximum amount of memory resources that are permitted for analytical processing. The default value for data frame analytics jobs is `1gb`. If you specify a value for the `xpack.ml.max_model_memory_limit` setting, an error occurs when you try to create jobs that have `model_memory_limit` values greater than that setting value. For more information, see [Machine learning settings](ml-settings.html "Machine learning settings in Elasticsearch"). 

###Examples

#### 更新模型内存限制示例

以下示例显示如何更新现有数据框分析配置的模型内存限制。

    
    
    POST _ml/data_frame/analytics/loganalytics/_update
    {
      "model_memory_limit": "200mb"
    }

更新作业时，响应将包含其配置以及更新的值。例如：

    
    
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
      "model_memory_limit" : "200mb",
      "allow_lazy_start" : false,
      "max_num_threads" : 1
    }

[« Stop data frame analytics jobs API](stop-dfanalytics.md) [Machine
learning trained model APIs »](ml-df-trained-models-apis.md)
