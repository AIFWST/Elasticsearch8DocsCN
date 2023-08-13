

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
streams](data-streams.md) ›[Time series data stream (TSDS)](tsds.md)

[« Time series index settings](tsds-index-settings.md) [Run downsampling
with ILM »](downsampling-ilm.md)

## 对时序数据流进行降采样

缩减采样提供了一种减少时间序列数据占用空间的方法)，方法是以降低粒度存储时间序列数据。

指标解决方案收集大量随时间增长的时序数据。随着数据的老化，它与系统的当前状态的相关性会降低。缩减采样过程将固定时间间隔内的文档汇总到单个摘要文档中。每个摘要文档都包含原始数据的统计表示形式：每个指标的"最小值"、"最大值"、"总和"、"value_count"和"平均值"。数据流时间序列维度保持不变。

实际上，缩减采样允许您以数据分辨率和精度换取存储大小。您可以将其包含在索引生命周期管理 (ILM) 策略中，以自动管理指标数据的数量和相关成本。

查看以下部分以了解更多信息：

* 工作原理 * 对时间序列数据运行缩减采样 * 查询缩减采样索引 * 限制和限制 * 尝试一下

### 工作原理

时间序列是随时间推移对特定实体进行的观测序列。观察到的样本可以表示为连续函数，其中时间序列维度保持不变，时间序列指标随时间变化。

！时间序列函数

在 Elasticsearch 索引中，将为每个时间戳创建一个文档，其中包含不可变的时间序列维度，以及指标名称和不断变化的指标值。对于单个时间戳，可以存储多个时序维度和指标。

！时间序列度量解剖学

对于最新且最相关的数据，指标系列通常具有较低的采样时间间隔，因此针对需要高数据分辨率的查询进行了优化。

！时间序列原版

图2.原始指标系列

缩减采样适用于较旧、访问频率较低的数据，方法是将原始时间序列替换为采样间隔较高的数据流和该数据的统计表示形式。原始指标样本可能已采集，例如，每十秒一次，随着数据的老化，您可以选择将样本粒度降低到每小时或每天。您可以选择将"冷"存档数据的粒度减少到每月或更少。

！时间序列缩减采样

图3.缩减采样指标系列

### 对时间序列数据运行下采样

若要对时序索引进行下采样，请使用下采样 API 并将"fixed_interval"设置为所需的粒度级别：

    
    
    response = client.indices.downsample(
      index: 'my-time-series-index',
      target_index: 'my-downsampled-time-series-index',
      body: {
        fixed_interval: '1d'
      }
    )
    puts response
    
    
    POST /my-time-series-index/_downsample/my-downsampled-time-series-index
    {
        "fixed_interval": "1d"
    }

若要将时序数据作为 ILM 的一部分进行缩减采样，请在 ILM 策略中包含缩减采样操作，并将"fixed_interval"设置为所需的粒度级别：

    
    
    response = client.ilm.put_lifecycle(
      policy: 'my_policy',
      body: {
        policy: {
          phases: {
            warm: {
              actions: {
                downsample: {
                  fixed_interval: '1h'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT _ilm/policy/my_policy
    {
      "policy": {
        "phases": {
          "warm": {
            "actions": {
              "downsample" : {
                "fixed_interval": "1h"
              }
            }
          }
        }
      }
    }

### 查询缩减采样索引

可以使用"_search"和"_async_search"终结点查询缩减采样索引。可以在单个请求中查询多个原始数据和缩减采样索引，单个请求可以包含不同粒度(不同存储桶时间跨度)的缩减采样索引。也就是说，您可以查询包含具有多个缩减采样间隔(例如，"15m"、"1h"、"1d")的缩减采样索引的数据流。

基于时间的直方图聚合的结果采用统一的存储桶大小，每个缩减采样索引返回的数据忽略缩减采样时间间隔。例如，如果您在每小时分辨率("fixed_interval"： "1h")对已按小时分辨率下采样的缩减采样索引运行"fixed_interval date_histogram"聚合，其中包含所有数据，然后返回 59 个空存储桶，然后返回下一个小时的包含数据的存储桶。

#### 下采样查询注意事项

关于查询缩减采样索引，有几点需要注意：

* 当您在 Kibana 中和通过 Elastic 解决方案运行查询时，会返回正常响应，而不会通知某些查询的索引已缩减采样。  * 对于日期直方图聚合，仅支持"fixed_intervals"(不支持日历感知间隔)。  * 仅支持协调世界时 (UTC) 日期时间。

### 限制和限制

以下限制和限制适用于缩减采样：

* 仅支持时间序列数据流中的索引)。  * 数据仅根据时间维度进行缩减采样。所有其他维度将复制到新索引，无需进行任何修改。  * 在数据流中，缩减采样的索引将替换原始索引，并删除原始索引。在给定时间段内只能存在一个索引。  * 源索引必须处于只读模式，缩减采样过程才能成功。有关详细信息，请查看手动运行缩减采样示例。  * 支持多次对同一时间段的数据进行降采样(下采样索引的下采样)。下采样间隔必须是下采样索引间隔的倍数。  * 缩减像素采样作为 ILM 操作提供。请参见缩减采样。  * 新的缩减采样索引在原始索引的数据层上创建，并继承其设置(例如，分片和副本的数量)。  * 支持数字"仪表"和"计数器"指标类型。  * 下采样配置是从时间序列数据流索引映射中提取的。唯一需要的附加设置是缩减采样"fixed_interval"。

### 试试吧

要对测试运行进行缩减采样，请尝试手动运行缩减采样的示例。

缩减像素采样可以很容易地添加到您的 ILM 策略中。要了解如何操作，请尝试我们的使用 ILM运行缩减采样示例。

[« Time series index settings](tsds-index-settings.md) [Run downsampling
with ILM »](downsampling-ilm.md)
