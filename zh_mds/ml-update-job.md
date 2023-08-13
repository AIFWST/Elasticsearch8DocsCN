

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Update filters API](ml-update-filter.md) [Update model snapshots API
»](ml-update-snapshot.md)

## 更新异常检测作业API

更新异常情况检测作业的某些属性。

###Request

"发布_ml/anomaly_detectors<job_id>//_update"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

### 路径参数

`<job_id>`

     (Required, string) Identifier for the anomaly detection job. 

### 请求正文

创建作业后，可以更新以下属性：

`allow_lazy_open`

    

(布尔值)高级配置选项。指定当机器学习节点容量不足时，此作业是否可以打开，无法立即将其分配给节点。默认值为"假";如果无法立即找到具有运行作业能力的机器学习节点，则开放异常情况检测作业 API 将返回错误。但是，这也受集群范围的"xpack.ml.max_lazy_ml_nodes"设置的约束;请参阅高级机器学习设置。如果此选项设置为"true"，则打开异常情况检测作业 API 不会返回错误，作业将处于"打开"状态，直到有足够的机器学习节点容量可用。

如果在进行更新时作业处于打开状态，则必须停止数据馈送，关闭作业，然后重新打开作业并重新启动数据馈送以使更改生效。

`analysis_limits`

    

(可选，对象)可以对将数学模型保存在内存中所需的资源应用限制。这些限制是近似值，可以按作业设置。它们不控制其他进程使用的内存，例如Elasticsearch Java进程。

您只能在作业关闭时更新"analysis_limits"。

"analysis_limits"的属性

`model_memory_limit`

    

(长或字符串)分析处理所需的近似最大内存资源量。一旦接近此限制，数据修剪就会变得更加激进。超过此限制时，不会对新实体进行建模。在版本 6.1 及更高版本中创建的作业的默认值为"1024mb"。但是，如果"xpack.ml.max_model_memory_limit"设置的值大于"0"且小于"1024mb"，则会改用该值。如果未设置"xpack.ml.max_model_memory_limit"，但设置了"xpack.ml.use_auto_machine_memory_percent"，则默认值"model_memory_limit"将设置为群集中可以分配的最大大小，上限为"1024mb"。默认值相对较小，以确保高资源使用率是有意识的决定。如果您的作业需要分析高基数字段，则可能需要使用更高的值。

如果指定数字而不是字符串，则假定单位为 MiB。为清楚起见，建议指定字符串。如果指定字节大小单位"b"或"kb"，并且该数字不等于离散的兆字节数，则会将其向下舍入到最接近的 MiB。最小有效值为 1MiB。如果指定的值小于 1 MiB，则会发生错误。有关支持的字节大小单位的详细信息，请参阅字节大小单位。

如果为"xpack.ml.max_model_memory_limit"设置指定值，则当您尝试创建具有大于该设置值的"model_memory_limit"值的作业时，会发生错误。有关详细信息，请参阅机器学习设置。

* 您不能将"model_memory_limit"值降低到当前使用情况以下。若要确定当前使用情况，请参阅获取作业统计信息 API 中的"model_bytes"值。  * 如果 'model_size_stats' 对象中的 'memory_status' 属性的值为 'hard_limit'，这意味着它无法处理某些数据。您可能希望使用增加的"model_memory_limit"重新运行作业。

`background_persist_interval`

    

(时间单位)高级配置选项。模型的每个周期持久性之间的时间。默认值是介于 3 到 4 小时之间的随机值，可避免所有作业在同一时间持续存在。允许的最小值为 1 小时。

对于非常大的模型(几GB)，持久性可能需要 10-20 分钟，因此不要将"background_persist_interval"值设置得太低。

如果在进行更新时作业处于打开状态，则必须停止数据馈送，关闭作业，然后重新打开作业并重新启动数据馈送以使更改生效。

`custom_settings`

     (object) Advanced configuration option. Contains custom metadata about the job. For example, it can contain custom URL information as shown in [Adding custom URLs to machine learning results](/guide/en/machine-learning/8.9/ml-configuring-url.html). 
`daily_model_snapshot_retention_after_days`

     (long) Advanced configuration option, which affects the automatic removal of old model snapshots for this job. It specifies a period of time (in days) after which only the first snapshot per day is retained. This period is relative to the timestamp of the most recent snapshot for this job. Valid values range from `0` to `model_snapshot_retention_days`. For new jobs, the default value is `1`. For jobs created before version 7.8.0, the default value matches `model_snapshot_retention_days`. For more information, refer to [Model snapshots](/guide/en/machine-learning/8.9/ml-ad-run-jobs.html#ml-ad-model-snapshots). 
`description`

     (string) A description of the job. 

`detectors`

    

(阵列)检测器更新对象的数组。

"探测器"的特性

`custom_rules`

    

(阵列)自定义规则对象的数组，使您能够自定义路检测器的操作。例如，规则可以规定应跳过结果的检测器条件。Kibana 将自定义规则称为 _jobrules_。有关更多示例，请参阅使用自定义规则自定义检测器。

"custom_rules"的属性

`actions`

    

(阵列)应用规则时要触发的操作集。如果指定了多个操作，则会合并所有操作的效果。可用的操作包括：

* "skip_result"：不会创建结果。这是默认值。除非您还指定"skip_model_update"，否则模型将像往常一样使用相应的序列值进行更新。  * "skip_model_update"：该序列的值不会用于更新模型。除非您还指定"skip_result"，否则结果将照常创建。当某些值预计始终异常并且它们以对其余结果产生负面影响的方式影响模型时，此操作适用。

`conditions`

    

(阵列)应用规则时的可选数值条件数组。规则必须具有非空范围或至少一个条件。多个条件与逻辑"AND"组合在一起。条件具有以下属性：

"条件"的属性

`applies_to`

     (string) Specifies the result property to which the condition applies. The available options are `actual`, `typical`, `diff_from_typical`, `time`. If your detector uses `lat_long`, `metric`, `rare`, or `freq_rare` functions, you can only specify conditions that apply to `time`. 
`operator`

     (string) Specifies the condition operator. The available options are `gt` (greater than), `gte` (greater than or equals), `lt` (less than) and `lte` (less than or equals). 
`value`

     (double) The value that is compared against the `applies_to` field using the `operator`. 

`scope`

    

(对象)应用规则的可选系列范围。规则必须具有非空范围或至少一个条件。默认情况下，示波器包括所有系列。允许对在"by_field_name"、"over_field_name"或"partition_field_name"中指定的任何字段限定范围。若要为字段添加范围，请将字段名称添加为范围对象中的键，并将其值设置为具有以下属性的对象：

"范围"的属性

`filter_id`

     (string) The id of the filter to be used. 
`filter_type`

     (string) Either `include` (the rule applies for values in the filter) or `exclude` (the rule applies for values not in the filter). Defaults to `include`. 

`description`

     (string) A description of the detector. For example, `Low event rate`. 
`detector_index`

    

(整数)检测器的唯一标识符。此标识符基于"analysis_config"中探测器的顺序，从零开始。

如果要更新特定检测器，则必须使用此标识符。但是，您无法更改检测器的"detector_index"值。

`groups`

     (array of strings) A list of job groups. A job can belong to no groups or many. 

`model_plot_config`

    

(对象)此高级配置选项将模型信息与结果一起存储。它提供了异常检测的更详细视图。

如果启用模型图，可能会给系统性能增加相当大的开销;对于具有许多实体的工作，这是不可行的。

模型图提供了模型及其边界的简化和指示性视图。它不显示复杂特征，例如多元相关性或多模态数据。因此，偶尔可能会报告在模型图中看不到的异常。

可以在以后创建或更新作业时配置模型绘图配置。如果遇到性能问题，则必须禁用它。

"model_plot_config"的属性

`annotations_enabled`

     (Boolean) If true, enables calculation and storage of the model change annotations for each entity that is being analyzed. Defaults to `enabled`. 
`enabled`

     (Boolean) If true, enables calculation and storage of the model bounds for each entity that is being analyzed. By default, this is not enabled. 
`terms`

     [preview]  This functionality is in technical preview and may be changed or removed in a future release. Elastic will apply best effort to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.  (string) Limits data collection to this comma separated list of partition or by field values. If terms are not specified or it is an empty string, no filtering is applied. For example, "CPU,NetworkIn,DiskWrites". Wildcards are not supported. Only the specified `terms` can be viewed when using the Single Metric Viewer. 

`model_prune_window`

     ([time units](api-conventions.html#time-units "Time units")) Advanced configuration option. Affects the pruning of models that have not been updated for the given time duration. The value must be set to a multiple of the `bucket_span`. If set too low, important information may be removed from the model. Typically, set to `30d` or longer. If not set, model pruning only occurs if the model memory status reaches the soft limit or the hard limit. For jobs created in 8.1 and later, the default value is the greater of `30d` or 20 times `bucket_span`. 
`model_snapshot_retention_days`

     (long) Advanced configuration option, which affects the automatic removal of old model snapshots for this job. It specifies the maximum period of time (in days) that snapshots are retained. This period is relative to the timestamp of the most recent snapshot for this job. The default value is `10`, which means snapshots ten days older than the newest snapshot are deleted. For more information, refer to [Model snapshots](/guide/en/machine-learning/8.9/ml-ad-run-jobs.html#ml-ad-model-snapshots). 

`per_partition_categorization`

    

(对象)与分类如何与分区字段交互相关的设置。

"per_partition_categorization"的属性

`enabled`

     (Boolean) To enable this setting, you must also set the partition_field_name property to the same value in every detector that uses the keyword mlcategory. Otherwise, job creation fails. 
`stop_on_warn`

     (Boolean) This setting can be set to true only if per-partition categorization is enabled. If true, both categorization and subsequent anomaly detection stops for partitions where the categorization status changes to `warn`. This setting makes it viable to have a job where it is expected that categorization works well for some partitions but not others; you do not pay the cost of bad categorization forever in the partitions where it works badly. 

`renormalization_window_days`

     (long) Advanced configuration option. The period over which adjustments to the score are applied, as new data is seen. The default value is the longer of 30 days or 100 `bucket_spans`. 

如果在进行更新时作业处于打开状态，则必须停止数据馈送，关闭作业，然后重新打开作业并重新启动数据馈送以使更改生效。

`results_retention_days`

     (long) Advanced configuration option. The period of time (in days) that results are retained. Age is calculated relative to the timestamp of the latest bucket result. If this property has a non-null value, once per day at 00:30 (server time), results that are the specified number of days older than the latest bucket result are deleted from Elasticsearch. The default value is null, which means all results are retained. Annotations generated by the system also count as results for retention purposes; they are deleted after the same number of days as results. Annotations added by users are retained forever. 

###Examples

    
    
    response = client.ml.update_job(
      job_id: 'low_request_rate',
      body: {
        description: 'An updated job',
        detectors: {
          detector_index: 0,
          description: 'An updated detector description'
        },
        groups: [
          'kibana_sample_data',
          'kibana_sample_web_logs'
        ],
        model_plot_config: {
          enabled: true
        },
        renormalization_window_days: 30,
        background_persist_interval: '2h',
        model_snapshot_retention_days: 7,
        results_retention_days: 60
      }
    )
    puts response
    
    
    POST _ml/anomaly_detectors/low_request_rate/_update
    {
      "description":"An updated job",
      "detectors": {
        "detector_index": 0,
        "description": "An updated detector description"
      },
      "groups": ["kibana_sample_data","kibana_sample_web_logs"],
      "model_plot_config": {
        "enabled": true
      },
      "renormalization_window_days": 30,
      "background_persist_interval": "2h",
      "model_snapshot_retention_days": 7,
      "results_retention_days": 60
    }

更新异常情况检测作业时，您将收到作业配置信息的摘要，包括更新的属性值。例如：

    
    
    {
      "job_id" : "low_request_rate",
      "job_type" : "anomaly_detector",
      "job_version" : "8.4.0",
      "create_time" : 1656105950893,
      "finished_time" : 1656105965744,
      "model_snapshot_id" : "1656105964",
      "custom_settings" : {
        "created_by" : "ml-module-sample",
        "custom_urls" : [
          {
            "url_name" : "Raw data",
            "url_value" : "discover#/?_g=(time:(from:'$earliest$',mode:absolute,to:'$latest$'))&_a=(index:'90943e30-9a47-11e8-b64d-95841ca0b247')"
          },
          {
            "url_name" : "Data dashboard",
            "url_value" : "dashboards#/view/edf84fe0-e1a0-11e7-b6d5-4dc382ef7f5b?_g=(time:(from:'$earliest$',mode:absolute,to:'$latest$'))&_a=(filters:!(),query:(language:kuery,query:''))"
          }
        ]
      },
      "groups" : [
        "kibana_sample_data",
        "kibana_sample_web_logs"
      ],
      "description" : "An updated job",
      "analysis_config" : {
        "bucket_span" : "1h",
        "summary_count_field_name" : "doc_count",
        "detectors" : [
          {
            "detector_description" : "An updated detector description",
            "function" : "low_count",
            "detector_index" : 0
          }
        ],
        "influencers" : [ ],
        "model_prune_window" : "30d"
      },
      "analysis_limits" : {
        "model_memory_limit" : "11mb",
        "categorization_examples_limit" : 4
      },
      "data_description" : {
        "time_field" : "timestamp",
        "time_format" : "epoch_ms"
      },
      "model_plot_config" : {
        "enabled" : true,
        "annotations_enabled" : true
      },
      "renormalization_window_days" : 30,
      "background_persist_interval" : "2h",
      "model_snapshot_retention_days" : 7,
      "daily_model_snapshot_retention_after_days" : 1,
      "results_retention_days" : 60,
      "results_index_name" : "custom-low_request_rate",
      "allow_lazy_open" : false
    }

[« Update filters API](ml-update-filter.md) [Update model snapshots API
»](ml-update-snapshot.md)
