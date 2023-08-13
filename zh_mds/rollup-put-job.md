

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Rollup APIs](rollup-apis.md)

[« Rollup APIs](rollup-apis.md) [Delete rollup jobs API »](rollup-delete-
job.md)

## 创建汇总作业API

创建汇总作业。

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

对于版本 8.5 及更高版本，我们建议对汇总进行缩减采样，以降低时序数据的存储成本。

###Request

"把_rollup/工作/<job_id>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"或"manage_rollup"集群权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

汇总作业配置包含有关作业应如何运行、何时为文档编制索引以及将来能够针对汇总索引执行哪些查询的所有详细信息。

作业配置有三个主要部分：有关作业的后勤详细信息(cron 计划等)、用于分组的字段以及要为每个组收集的指标。

作业在"已停止"状态下创建。可以使用启动汇总作业 API 启动它们。

### 路径参数

`<job_id>`

     (Required, string) Identifier for the rollup job. This can be any alphanumeric string and uniquely identifies the data that is associated with the rollup job. The ID is persistent; it is stored with the rolled up data. If you create a job, let it run for a while, then delete the job, the data that the job rolled up is still be associated with this job ID. You cannot create a new job with the same ID since that could lead to problems with mismatched job configurations. 

### 请求正文

`cron`

     (Required, string) A cron string which defines the intervals when the rollup job should be executed. When the interval triggers, the indexer attempts to rollup the data in the index pattern. The cron pattern is unrelated to the time interval of the data being rolled up. For example, you may wish to create hourly rollups of your document but to only run the indexer on a daily basis at midnight, as defined by the cron. The cron pattern is defined just like a Watcher cron schedule. 

`groups`

    

(必填，对象)定义为此汇总作业定义的分组字段和聚合。然后，这些字段将在以后聚合到存储桶中可用。

这些 agg 和字段可以任意组合使用。将"组"配置视为定义一组工具，这些工具以后可用于聚合对数据进行分区。与原始数据不同，我们必须提前考虑可以使用哪些字段和聚合。汇总提供了足够的灵活性，您只需确定需要 _哪些_ 字段，not_in需要哪些order_字段。

目前有三种类型的分组可用："date_histogram"、"直方图"和"术语"。

"组"的属性

`date_histogram`

    

(必填，对象)日期直方图组将"日期"字段聚合到基于时间的存储桶中。该组是**强制性的**;您当前无法汇总没有时间戳和"date_histogram"组的文档。"date_histogram"组有几个参数：

"date_histogram"的性质

"calendar_interval"或"fixed_interval"

    

(必需，时间单位)汇总时要生成的时间段的间隔。例如，"60m"生成 60 分钟(每小时)汇总。这遵循了 Elasticsearch 其他地方使用的标准时间格式语法。间隔定义只能聚合的_minimum_interval。如果配置了每小时("60m")间隔，则汇总搜索可以执行间隔为 60m 或更长(每周、每月等)的聚合。因此，将间隔定义为您希望稍后查询的最小单位。有关日历和固定时间间隔之间的差异的详细信息，请参阅日历和固定时间间隔。

更小、更精细的间隔按比例占用更多空间。

`delay`

    

(可选，时间单位)在汇总新文档之前等待多长时间。默认情况下，索引器尝试汇总所有可用的数据。但是，数据无序到达的情况并不少见，有时甚至晚了几天。索引器无法处理在汇总时间跨度后到达的数据。也就是说，没有更新现有汇总的规定。

相反，您应该指定一个"延迟"，该"延迟"与您预计无序数据到达的最长时间相匹配。例如，"1d"的"延迟"指示索引器将文档汇总到"现在 - 1d"，这为无序文档的到达提供了一天的缓冲时间。

`field`

     (Required, string) The date field that is to be rolled up. 
`time_zone`

     (Optional, string) Defines what time_zone the rollup documents are stored as. Unlike raw data, which can shift timezones on the fly, rolled documents have to be stored with a specific timezone. By default, rollup documents are stored in `UTC`. 

`histogram`

    

(可选，对象)直方图组将一个或多个数值字段聚合为数值直方图间隔。

"直方图"的属性

`fields`

     (Required, array) The set of fields that you wish to build histograms for. All fields specified must be some kind of numeric. Order does not matter. 
`interval`

     (Required, integer) The interval of histogram buckets to be generated when rolling up. For example, a value of `5` creates buckets that are five units wide (`0-5`, `5-10`, etc). Note that only one interval can be specified in the `histogram` group, meaning that all fields being grouped via the histogram must share the same interval. 

`terms`

    

(可选，对象)术语组可用于"关键字"或数字字段，以允许稍后通过"术语"聚合进行分桶。索引枚举并存储每个时间段的字段的 _all_ 值。对于高基数组(如 IP 地址)，这可能会造成潜在的成本，尤其是在时间段特别稀疏的情况下。

虽然汇总的大小不太可能大于原始数据，但在多个高基数字段上定义"术语"组可以在很大程度上有效地减少汇总的压缩。因此，您应该明智地考虑包含哪些高基数字段。

"术语"的属性

`fields`

     (Required, string) The set of fields that you wish to collect terms for. This array can contain fields that are both `keyword` and numerics. Order does not matter. 

`index_pattern`

    

(必需，字符串)要汇总的索引或索引模式。支持通配符样式模式("logstash-*")。作业尝试汇总整个索引或索引模式。

"index_pattern"不能是与目的地"rollup_index"匹配的模式。例如，模式"foo-*"将与汇总索引"foo-rollup"匹配。这种情况会导致问题，因为汇总作业会尝试在运行时汇总自己的数据。如果尝试配置与"rollup_index"匹配的模式，则会发生异常以防止此行为。

`metrics`

    

(可选，对象)定义要为每个分组元组收集的指标。默认情况下，仅收集每个组的doc_counts。为了使汇总有用，您通常会添加平均值、最小值、最大值等指标。指标基于每个字段定义，您可以为每个字段配置应收集的指标。

"指标"配置接受一个对象数组，其中每个对象有两个参数。

度量对象的属性

`field`

     (Required, string) The field to collect metrics for. This must be a numeric of some kind. 
`metrics`

     (Required, array) An array of metrics to collect for the field. At least one metric must be configured. Acceptable metrics are `min`,`max`,`sum`,`avg`, and `value_count`. 

`page_size`

     (Required, integer) The number of bucket results that are processed on each iteration of the rollup indexer. A larger value tends to execute faster, but requires more memory during processing. This value has no effect on how the data is rolled up; it is merely used for tweaking the speed or memory cost of the indexer. 
`rollup_index`

     (Required, string) The index that contains the rollup results. The index can be shared with other rollup jobs. The data is stored so that it doesn't interfere with unrelated jobs. 
`timeout`

     (Optional, [time value](api-conventions.html#time-units "Time units")) Time to wait for the request to complete. Defaults to `20s` (20 seconds). 

###Example

下面的示例创建一个名为"sensor"的汇总作业，以"sensor-*"索引模式为目标：

    
    
    PUT _rollup/job/sensor
    {
      "index_pattern": "sensor-*",
      "rollup_index": "sensor_rollup",
      "cron": "*/30 * * * * ?",
      "page_size": 1000,
      "groups": { __"date_histogram": {
          "field": "timestamp",
          "fixed_interval": "1h",
          "delay": "7d"
        },
        "terms": {
          "fields": [ "node" ]
        }
      },
      "metrics": [ __{
          "field": "temperature",
          "metrics": [ "min", "max", "sum" ]
        },
        {
          "field": "voltage",
          "metrics": [ "avg" ]
        }
      ]
    }

__

|

此配置允许在"时间戳"字段上使用日期直方图，并在"节点"字段上使用"术语"聚合。   ---|---    __

|

此配置通过两个字段定义指标："温度"和"电压"。对于"温度"字段，我们正在收集温度的最小值、最大值和总和。对于"电压"，我们正在收集平均值。   创建作业时，您会收到以下结果：

    
    
    {
      "acknowledged": true
    }

[« Rollup APIs](rollup-apis.md) [Delete rollup jobs API »](rollup-delete-
job.md)
