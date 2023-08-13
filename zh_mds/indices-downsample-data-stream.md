

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Data stream APIs](data-stream-apis.md)

[« Modify data streams API](modify-data-streams-api.md) [Document APIs
»](docs.md)

## 下采样索引接口

聚合时间序列 (TSDS) 索引，并存储按配置的时间间隔分组的每个指标字段的预先计算的统计摘要("最小"、"最大值"、"总和"、"value_count"和"平均值")。例如，包含每 10 秒采样一次的指标的 TSDS 索引可以缩减采样为每小时索引。一小时间隔内的所有文档都将汇总并作为单个文档存储在缩减采样索引中。

    
    
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

###Request

'发布 /<source-index>/_downsample<output-downsampled-index>/'

###Prerequisites

* 仅支持时间序列数据流中的索引)。  * 如果启用了 Elasticsearch 安全功能，您必须对数据流具有"全部"或"管理"索引权限。  * 无法在源索引上定义字段级和文档级安全性。  * 源索引必须是只读的('index.blocks.write： true')。

### 路径参数

`<source-index>`

     (Optional, string) Name of the time series index to downsample. 
`<output-downsampled_index>`

    

(必需，字符串)要创建的索引的名称。

索引名称必须满足以下条件：

* 仅限小写 * 不能包含 '\'， '/'， '*'， '？''， '<'， '>'， '|'， ' ' (空格字符)， '，'， '#' * 7.0 之前的索引可能包含冒号 ('：')，但该冒号已被弃用，在 7.0+ 中不受支持 * 不能以 '-'、'_'、'+' 开头 * 不能是 '." 或 '..' * 不能超过 255 字节(注意是字节，因此多字节字符将更快地计入 255 限制) * 不推荐使用以 '." 开头的名称，隐藏索引和插件管理的内部索引除外

### 查询参数

`fixed_interval`

    

(必需，时间单位)聚合原始时序索引的时间间隔。例如，"60m"每 60 分钟(每小时)生成一个文档。这遵循了 Elasticsearch 中其他地方使用的标准时间格式语法。

更小、更精细的间隔按比例占用更多空间。

### 缩减采样过程

缩减采样操作遍历源 TSDS 索引并执行以下步骤：

1. 为"_tsid"字段的每个值和每个"@timestamp"值创建一个新文档，四舍五入到缩减采样配置中定义的"fixed_interval"。  2. 对于每个新文档，将所有时间序列维度从源索引复制到目标索引。TSDS 中的维度是恒定的，因此每个存储桶仅执行一次。  3. 对于每个时间序列指标字段，计算存储桶中所有文档的聚合。根据每个指标字段的指标类型，将存储一组不同的预聚合结果：

    * `gauge`: The `min`, `max`, `sum`, and `value_count` are stored; `value_count` is stored as type `aggregate_metric_double`. 
    * `counter`: The `last_value` is stored. 

4. 对于所有其他字段，最新值将复制到目标索引。

### 源索引和目标索引字段映射

目标缩减采样索引中的字段基于原始源索引中的字段创建，如下所示：

1. 使用"时间序列维度"参数映射的所有字段都在目标下采样索引中创建，其映射与源索引中的映射相同。  2. 使用 'time_series_metric' 参数映射的所有字段都在目标下采样索引中创建，其映射与源索引中的映射相同。一个例外是，对于映射为"time_series_metric：gauge"的字段，字段类型更改为"aggregate_metric_double"。  3. 所有其他既不是维度也不是指标的字段(即标签字段)都是在目标缩减采样索引中创建的，其映射与源索引中的映射相同。

查看缩减采样文档，了解手动运行缩减采样和作为 ILM 策略的一部分运行的概述和示例。

[« Modify data streams API](modify-data-streams-api.md) [Document APIs
»](docs.md)
