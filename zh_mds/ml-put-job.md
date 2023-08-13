

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Close anomaly detection jobs API](ml-close-job.md) [Create calendars API
»](ml-put-calendar.md)

## 创建异常检测作业API

实例化异常情况检测作业。

###Request

"放_ml/anomaly_detectors/<job_id>"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

如果包含"datafeed_config"，则还必须具有源索引的"读取"索引权限。

###Description

* 您必须使用 Kibana 或此 API 来创建异常检测作业。不要使用 Elasticsearch index API 将作业直接放入 '.ml-config' 索引。如果启用了 Elasticsearch 安全功能，请不要授予用户对".ml-config"索引的"写入"权限。  * 如果您包含"datafeed_config"并且启用了 Elasticsearch 安全功能，则您的数据馈送会记住创建它的用户在创建时具有哪些角色，并使用这些相同的角色运行查询。如果提供辅助授权标头，则改用这些凭据。

### 路径参数

`<job_id>`

     (Required, string) Identifier for the anomaly detection job. This identifier can contain lowercase alphanumeric characters (a-z and 0-9), hyphens, and underscores. It must start and end with alphanumeric characters. 

### 请求正文

`allow_lazy_open`

     (Optional, Boolean) Advanced configuration option. Specifies whether this job can open when there is insufficient machine learning node capacity for it to be immediately assigned to a node. The default value is `false`; if a machine learning node with capacity to run the job cannot immediately be found, the [open anomaly detection jobs API](ml-open-job.html "Open anomaly detection jobs API") returns an error. However, this is also subject to the cluster-wide `xpack.ml.max_lazy_ml_nodes` setting; see [Advanced machine learning settings](ml-settings.html#advanced-ml-settings "Advanced machine learning settings"). If this option is set to `true`, the [open anomaly detection jobs API](ml-open-job.html "Open anomaly detection jobs API") does not return an error and the job waits in the `opening` state until sufficient machine learning node capacity is available. 

`analysis_config`

    

(必填，对象)分析配置，指定如何分析数据。创建作业后，无法更改分析配置;所有属性都是信息性的。

"analysis_config"的属性

`bucket_span`

     ([time units](api-conventions.html#time-units "Time units")) The size of the interval that the analysis is aggregated into, typically between `5m` and `1h`. This value should be either a whole number of days or equate to a whole number of buckets in one day;  [8.1]  Deprecated in 8.1. Values that do not meet these recommendations are deprecated and will be disallowed in a future version  . If the anomaly detection job uses a datafeed with [aggregations](/guide/en/machine-learning/8.9/ml-configuring-aggregation.html), this value must also be divisible by the interval of the date histogram aggregation. The default value is `5m`. For more information, see [Bucket span](/guide/en/machine-learning/8.9/ml-ad-run-jobs.html#ml-ad-bucket-span). 
`categorization_analyzer`

    

(对象或字符串)如果指定了"categorization_field_name"，则还可以定义用于解释分类字段的分析器。此属性不能与"categorization_filters"同时使用。分类分析器指定分类过程如何解释"categorization_field"。语法与用于在分析终结点中定义"分析器"的语法非常相似。有关更多信息，请参阅对日志消息进行分类。

"categorization_analyzer"字段可以指定为字符串或 asan 对象。如果它是一个字符串，它必须引用内置分析器或另一个插件添加的分析器。如果它是一个对象，则它具有以下属性：

"categorization_analyzer"的属性

`char_filter`

     (array of strings or objects) One or more [character filters](analysis-charfilters.html "Character filters reference"). In addition to the built-in character filters, other plugins can provide more character filters. This property is optional. If it is not specified, no character filters are applied prior to categorization. If you are customizing some other aspect of the analyzer and you need to achieve the equivalent of `categorization_filters` (which are not permitted when some other aspect of the analyzer is customized), add them here as [pattern replace character filters](analysis-pattern-replace-charfilter.html "Pattern replace character filter"). 
`tokenizer`

     (string or object) The name or definition of the [tokenizer](analysis-tokenizers.html "Tokenizer reference") to use after character filters are applied. This property is compulsory if `categorization_analyzer` is specified as an object. Machine learning provides a tokenizer called `ml_standard` that tokenizes in a way that has been determined to produce good categorization results on a variety of log file formats for logs in English. If you want to use that tokenizer but change the character or token filters, specify `"tokenizer": "ml_standard"` in your `categorization_analyzer`. Additionally, the `ml_classic` tokenizer is available, which tokenizes in the same way as the non-customizable tokenizer in old versions of the product (before 6.2). `ml_classic` was the default categorization tokenizer in versions 6.2 to 7.13, so if you need categorization identical to the default for jobs created in these versions, specify `"tokenizer": "ml_classic"` in your `categorization_analyzer`. 
`filter`

     (array of strings or objects) One or more [token filters](analysis-tokenfilters.html "Token filter reference"). In addition to the built-in token filters, other plugins can provide more token filters. This property is optional. If it is not specified, no token filters are applied prior to categorization. 

`categorization_field_name`

     (string) If this property is specified, the values of the specified field will be categorized. The resulting categories must be used in a detector by setting `by_field_name`, `over_field_name`, or `partition_field_name` to the keyword `mlcategory`. For more information, see [Categorizing log messages](/guide/en/machine-learning/8.9/ml-configuring-categories.html). 
`categorization_filters`

     (array of strings) If `categorization_field_name` is specified, you can also define optional filters. This property expects an array of regular expressions. The expressions are used to filter out matching sequences from the categorization field values. You can use this functionality to fine tune the categorization by excluding sequences from consideration when categories are defined. For example, you can exclude SQL statements that appear in your log files. For more information, see [Categorizing log messages](/guide/en/machine-learning/8.9/ml-configuring-categories.html). This property cannot be used at the same time as `categorization_analyzer`. If you only want to define simple regular expression filters that are applied prior to tokenization, setting this property is the easiest method. If you also want to customize the tokenizer or post-tokenization filtering, use the `categorization_analyzer` property instead and include the filters as `pattern_replace` character filters. The effect is exactly the same. 

`detectors`

    

(阵列)检测器配置对象的数组。检测器配置对象指定作业分析的数据字段。它们还指定使用哪些分析函数。您可以为一个作业指定多个检测器。

如果"检测器"阵列不包含至少一个检测器，则不会发生分析并返回错误。

"探测器"的特性

`by_field_name`

     (string) The field used to split the data. In particular, this property is used for analyzing the splits with respect to their own history. It is used for finding unusual values in the context of the split. 

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

`detector_description`

     (string) A description of the detector. For example, `Low event rate`. 
`detector_index`

    

(整数)检测器的唯一标识符。此标识符基于"analysis_config"中探测器的顺序，从零开始。

如果为此属性指定值，则会忽略该值。

`exclude_frequent`

     (string) Contains one of the following values: `all`, `none`, `by`, or `over`. If set, frequent entities are excluded from influencing the anomaly results. Entities can be considered frequent over time or frequent in a population. If you are working with both over and by fields, then you can set `exclude_frequent` to `all` for both fields, or to `by` or `over` for those specific fields. 
`field_name`

    

(字符串)检测器在函数中使用的字段。如果使用事件率函数(如"计数"或"稀有")，请不要指定此字段。

"field_name"不能包含双引号或反斜杠。

`function`

     (string) The analysis function that is used. For example, `count`, `rare`, `mean`, `min`, `max`, and `sum`. For more information, see [Function reference](/guide/en/machine-learning/8.9/ml-functions.html). 
`over_field_name`

     (string) The field used to split the data. In particular, this property is used for analyzing the splits with respect to the history of all splits. It is used for finding unusual values in the population of all splits. For more information, see [Performing population analysis](/guide/en/machine-learning/8.9/ml-configuring-populations.html). 
`partition_field_name`

     (string) The field used to segment the analysis. When you use this property, you have completely independent baselines for each value of this field. 
`use_null`

     (Boolean) Defines whether a new series is used as the null series when there is no value for the by or partition fields. The default value is `false`. 

`influencers`

     (array of strings) A comma separated list of influencer field names. Typically these can be the by, over, or partition fields that are used in the detector configuration. You might also want to use a field name that is not specifically named in a detector, but is available as part of the input data. When you use multiple detectors, the use of influencers is recommended as it aggregates results for each influencer entity. 
`latency`

    

(时间单位)预期数据超出时间顺序的窗口的大小。默认值为 0(无延迟)。如果指定非零值，则该值必须大于或等于 1 秒。有关时间单位的详细信息，请参阅时间单位。

延迟仅在使用后数据 API 发送数据时适用。

`model_prune_window`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Advanced configuration option. Affects the pruning of models that have not been updated for the given time duration. The value must be set to a multiple of the `bucket_span`. If set too low, important information may be removed from the model. Typically, set to `30d` or longer. If not set, model pruning only occurs if the model memory status reaches the soft limit or the hard limit. For jobs created in 8.1 and later, the default value is the greater of `30d` or 20 times `bucket_span`. 
`multivariate_by_fields`

    

(布尔值)此功能保留供内部使用。它不支持在客户环境中使用，并且不受官方 GA 功能的 SLA 支持的约束。

如果设置为"true"，分析将自动查找给定"by"字段值的度量之间的相关性，并在这些相关性不再成立时报告异常。例如，假设主机 A 上的 CPU 和内存使用情况通常与主机 B 上的相同指标高度相关。也许出现这种相关性是因为它们正在运行负载平衡的应用程序。如果启用此属性，则当主机 A 上的 CPU 使用率较高而主机 B 上的 CPU 使用率值较低时，将报告异常。也就是说，当主机 A 的 CPU 异常给定主机 B 的 CPU 时，您将看到异常。

要使用"multivariate_by_fields"属性，还必须在检测器中指定"by_field_name"。

`per_partition_categorization`

    

(可选，对象)与分类如何与分区字段交互相关的设置。

"per_partition_categorization"的属性

`enabled`

     (Boolean) To enable this setting, you must also set the partition_field_name property to the same value in every detector that uses the keyword mlcategory. Otherwise, job creation fails. 
`stop_on_warn`

     (Boolean) This setting can be set to true only if per-partition categorization is enabled. If true, both categorization and subsequent anomaly detection stops for partitions where the categorization status changes to `warn`. This setting makes it viable to have a job where it is expected that categorization works well for some partitions but not others; you do not pay the cost of bad categorization forever in the partitions where it works badly. 

`summary_count_field_name`

    

(字符串)如果指定此属性，则应预先汇总提供给作业的数据。此属性值是包含已汇总的原始数据点计数的字段的名称。相同的"summary_count_field_name"适用于作业中的所有探测器。

"summary_count_field_name"属性不能与"度量"函数一起使用。

`analysis_limits`

    

(可选，对象)可以对将数学模型保存在内存中所需的资源应用限制。这些限制是近似值，可以按作业设置。它们不控制其他进程使用的内存，例如Elasticsearch Java进程。

"analysis_limits"的属性

`categorization_examples_limit`

    

(长)内存和结果数据存储中每个类别存储的最大示例数。默认值为 4。如果增加此值，则有更多示例可用，但它要求您具有更多可用存储空间。如果将此值设置为"0"，则不会存储任何示例。

"categorization_examples_limit"仅适用于使用分类的分析。有关更多信息，请参阅对日志消息进行分类。

`model_memory_limit`

    

(长或字符串)分析处理所需的近似最大内存资源量。一旦接近此限制，数据修剪就会变得更加激进。超过此限制时，不会对新实体进行建模。在版本 6.1 及更高版本中创建的作业的默认值为"1024mb"。但是，如果"xpack.ml.max_model_memory_limit"设置的值大于"0"且小于"1024mb"，则会改用该值。如果未设置"xpack.ml.max_model_memory_limit"，但设置了"xpack.ml.use_auto_machine_memory_percent"，则默认值"model_memory_limit"将设置为群集中可以分配的最大大小，上限为"1024mb"。默认值相对较小，以确保高资源使用率是有意识的决定。如果您的作业需要分析高基数字段，则可能需要使用更高的值。

如果指定数字而不是字符串，则假定单位为 MiB。为清楚起见，建议指定字符串。如果指定字节大小单位"b"或"kb"，并且该数字不等于离散的兆字节数，则会将其向下舍入到最接近的 MiB。最小有效值为 1MiB。如果指定的值小于 1 MiB，则会发生错误。有关支持的字节大小单位的详细信息，请参阅字节大小单位。

如果为"xpack.ml.max_model_memory_limit"设置指定值，则当您尝试创建具有大于该设置值的"model_memory_limit"值的作业时，会发生错误。有关详细信息，请参阅机器学习设置。

`background_persist_interval`

    

(可选，时间单位)高级配置选项。模型的每个周期持久性之间的时间。默认值是介于 3 到 4 小时之间的随机值，可避免所有作业在同一时间持续存在。最小允许值为 1 小时。

对于非常大的模型(几GB)，持久性可能需要 10-20 分钟，因此不要将"background_persist_interval"值设置得太低。

`custom_settings`

     (Optional, object) Advanced configuration option. Contains custom metadata about the job. For example, it can contain custom URL information as shown in [Adding custom URLs to machine learning results](/guide/en/machine-learning/8.9/ml-configuring-url.html). 
`daily_model_snapshot_retention_after_days`

     (Optional, long) Advanced configuration option, which affects the automatic removal of old model snapshots for this job. It specifies a period of time (in days) after which only the first snapshot per day is retained. This period is relative to the timestamp of the most recent snapshot for this job. Valid values range from `0` to `model_snapshot_retention_days`. For new jobs, the default value is `1`. For jobs created before version 7.8.0, the default value matches `model_snapshot_retention_days`. For more information, refer to [Model snapshots](/guide/en/machine-learning/8.9/ml-ad-run-jobs.html#ml-ad-model-snapshots). 

`data_description`

    

(必填，对象)数据描述定义了使用后数据 API 将数据发送到作业时输入数据的格式。请注意，配置数据馈送时，会自动设置这些属性。当通过发布数据 API 接收数据时，它不会存储在 Elasticsearch 中，仅保留异常检测的结果。

"data_description"的属性

`format`

     (string) Only `JSON` format is supported at this time. 
`time_field`

     (string) The name of the field that contains the timestamp. The default value is `time`. 
`time_format`

    

(字符串)时间格式，可以是"纪元"、"epoch_ms"或自定义模式。默认值为"epoch"，表示 UNIX 或纪元时间(自 1970 年 1 月 1 日以来的秒数)。值"epoch_ms"表示时间以自纪元以来的毫秒为单位。"纪元"和"epoch_ms"时间格式接受整数或实数值。 

自定义模式必须符合 Java 'DateTimeFormatter' 类。使用日期时间格式模式时，建议您提供完整日期、时间和时区。例如："yyyy-MM-dd'T'HH：mm：ssX'。如果指定的模式不足以生成完整的时间戳，则作业创建将失败。

`datafeed_config`

    

(可选，对象)数据馈送，它从 Elasticsearch 中检索数据以供作业分析。只能将一个数据馈送与每个异常情况检测作业关联。

"数据馈送"的属性

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

`datafeed_id`

    

(可选，字符串)唯一标识数据馈送的数字字符串。此标识符可以包含小写字母数字字符 (a-zand 0-9)、连字符和下划线。它必须以字母数字字符开头和结尾。

默认为与异常情况检测作业相同的 ID。

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

`description`

     (Optional, string) A description of the job. 
`groups`

     (Optional, array of strings) A list of job groups. A job can belong to no groups or many. 

`model_plot_config`

    

(可选，对象)此高级配置选项存储模型信息以及结果。它提供了异常检测的更详细视图。

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

`model_snapshot_retention_days`

     (Optional, long) Advanced configuration option, which affects the automatic removal of old model snapshots for this job. It specifies the maximum period of time (in days) that snapshots are retained. This period is relative to the timestamp of the most recent snapshot for this job. The default value is `10`, which means snapshots ten days older than the newest snapshot are deleted. For more information, refer to [Model snapshots](/guide/en/machine-learning/8.9/ml-ad-run-jobs.html#ml-ad-model-snapshots). 
`renormalization_window_days`

     (Optional, long) Advanced configuration option. The period over which adjustments to the score are applied, as new data is seen. The default value is the longer of 30 days or 100 `bucket_spans`. 
`results_index_name`

     (Optional, string) A text string that affects the name of the machine learning results index. The default value is `shared`, which generates an index named `.ml-anomalies-shared`. 
`results_retention_days`

     (Optional, long) Advanced configuration option. The period of time (in days) that results are retained. Age is calculated relative to the timestamp of the latest bucket result. If this property has a non-null value, once per day at 00:30 (server time), results that are the specified number of days older than the latest bucket result are deleted from Elasticsearch. The default value is null, which means all results are retained. Annotations generated by the system also count as results for retention purposes; they are deleted after the same number of days as results. Annotations added by users are retained forever. 

###Examples

创建异常情况检测作业和数据馈送：

    
    
    PUT _ml/anomaly_detectors/test-job1?pretty
    {
      "analysis_config": {
        "bucket_span": "15m",
        "detectors": [
          {
            "detector_description": "Sum of bytes",
            "function": "sum",
            "field_name": "bytes"
          }
        ]
      },
      "data_description": {
        "time_field": "timestamp",
        "time_format": "epoch_ms"
      },
      "analysis_limits": {
        "model_memory_limit": "11MB"
      },
      "model_plot_config": {
        "enabled": true,
        "annotations_enabled": true
      },
      "results_index_name": "test-job1",
      "datafeed_config":
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
        "runtime_mappings": {
          "hour_of_day": {
            "type": "long",
            "script": {
              "source": "emit(doc['timestamp'].value.getHour());"
            }
          }
        },
        "datafeed_id": "datafeed-test-job1"
      }
    }

API 返回以下结果：

    
    
    {
      "job_id" : "test-job1",
      "job_type" : "anomaly_detector",
      "job_version" : "8.4.0",
      "create_time" : 1656087283340,
      "datafeed_config" : {
        "datafeed_id" : "datafeed-test-job1",
        "job_id" : "test-job1",
        "authorization" : {
          "roles" : [
            "superuser"
          ]
        },
        "query_delay" : "61499ms",
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
        },
        "runtime_mappings" : {
          "hour_of_day" : {
            "type" : "long",
            "script" : {
              "source" : "emit(doc['timestamp'].value.getHour());"
            }
          }
        }
      },
      "analysis_config" : {
        "bucket_span" : "15m",
        "detectors" : [
          {
            "detector_description" : "Sum of bytes",
            "function" : "sum",
            "field_name" : "bytes",
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
      "model_snapshot_retention_days" : 10,
      "daily_model_snapshot_retention_after_days" : 1,
      "results_index_name" : "custom-test-job1",
      "allow_lazy_open" : false
    }

[« Close anomaly detection jobs API](ml-close-job.md) [Create calendars API
»](ml-put-calendar.md)
