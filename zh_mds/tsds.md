

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
streams](data-streams.md)

[« Modify a data stream](modify-data-streams.md) [Set up a time series data
stream (TSDS) »](set-up-tsds.md)

## 时间序列数据流

时序数据流 (TSDS) 将时间戳指标数据建模为一个或多个时序。

您可以使用 TSDS 更有效地存储指标数据。在我们的基准测试中，存储在 TSDS 中的指标数据使用的磁盘空间比常规数据流少 70%。确切的影响将因数据集而异。

### 何时使用 aTSDS

常规数据流和 TSDS 都可以存储带时间戳的指标数据。仅当您通常以近乎实时和"@timestamp"的顺序将指标数据添加到 Elasticsearch 时，才使用 TSDS。

TSDS 仅适用于指标数据。对于其他带时间戳的数据(例如日志或跟踪)，请使用常规数据流。

### 与常规数据流的区别

TSDS 的工作方式类似于常规数据流，但存在一些关键区别：

* TSDS 的匹配索引模板需要一个带有"index.mode： time_series"选项的"data_stream"对象。此选项启用大多数与 TSDS 相关的功能。  * 除了"@timestamp"之外，TSDS 中的每个文档都必须包含一个或多个维度字段。TSDS 的匹配索引模板必须包含至少一个"关键字"维度的映射。

TSDS 文档通常还包含一个或多个指标字段。

* Elasticsearch 为 TSDS 中的每个文档生成一个隐藏的"_tsid"元数据字段。  * TSDS 使用有时间限制的后备索引将同一时间段的数据存储在同一后备索引中。  * TSDS 的匹配索引模板必须包含"index.routing_path"索引设置。TSDS 使用此设置执行基于维度的路由。  * TSDS 使用内部索引排序按"_tsid"和"@timestamp"对分片段进行排序。  * TSDS 文档仅支持自动生成的文档"_id"值。对于 TSDS 文档，文档"_id"是文档尺寸和"@timestamp"的哈希。TSDS 不支持自定义文档"_id"值。  * TSDS使用合成的"_source"，因此受到许多限制。

### 什么是时间序列？

时间序列是特定实体的观测值序列。总之，这些观察结果可让您跟踪实体随时间推移的变化。例如，时序可以跟踪：

* 计算机的 CPU 和磁盘使用情况 * 股票价格 * 来自天气传感器的温度和湿度读数。

！时间序列图

图1.绘制为图形的天气传感器读数的时间序列

在 TSDS 中，每个 Elasticsearch 文档代表特定时间序列中的一个观测值或数据点。尽管 TSDS 可以包含多个时间序列，但一个文档只能属于一个时间序列。一个时序不能跨越多个数据流。

####Dimensions

维度是字段名称和值，它们组合在一起标识文档的时间序列。在大多数情况下，维度描述您正在测量的实体的某些方面。例如，与同一天气传感器相关的文档可能始终具有相同的"sensor_id"和"位置"值。

TSDS文档由其时间序列和时间戳唯一标识，这两者都用于生成文档"_id"。因此，具有相同尺寸和相同时间戳的两个文档被视为重复项。使用"_bulk"端点将文档添加到 TSDS 时，具有相同时间戳和维度的第二个文档将覆盖第一个文档。当您使用"PUT //<target>_create/<_id>"格式添加单个文档和已存在具有相同"_id"的文档时，将生成错误。

您可以使用布尔"time_series_dimension"映射参数将字段标记为维度。以下字段类型支持"time_series_dimension"参数：

* "关键字" * "IP" * "字节" * "短" * "整数" * "长" * "unsigned_long"

对于平展字段，请使用"time_series_dimensions"参数将字段数组配置为维度。有关详细信息，请参阅"扁平化"。

**尺寸限制**

在TSDS中，Elasticsearch使用维度来生成文档"_id"和"_tsid"值。生成的"_id"始终是短编码哈希。为了防止"_tsid"值过大，Elasticsearch 使用"index.mapping.dimension_fields.limit"索引设置来限制索引的维度数。虽然您可以增加此限制，但生成的文档"_tsid"值不能超过 32KB。此外，维度的字段名称不能超过 512 个字节，并且每个维度值不能超过 1kb。

####Metrics

指标是包含数值度量值以及基于这些度量值的聚合沙/或缩减采样值的字段。虽然不是必需的，但 TSDS 中的文档通常包含一个或多个指标字段。

指标与维度的不同之处在于，虽然维度通常保持不变，但指标预计会随着时间的推移而变化，即使很少或缓慢。

要将字段标记为指标，必须使用"time_series_metric"映射参数指定指标类型。以下字段类型支持"time_series_metric"参数：

* "aggregate_metric_double" * "直方图" * 所有数值字段类型

接受的指标类型因字段类型而异：

"time_series_metric"的有效值

`counter`

    

仅单调增加或重置为"0"(零)的累积指标。例如，错误或已完成任务的计数。

计数器字段具有额外的语义含义，因为它表示累积计数器。这适用于"速率"聚合，因为速率可以从累积单调递增的计数器中导出。但是，由于其累积性质，许多聚合(例如"sum")计算的结果对计数器字段没有意义。

只有数字和"aggregate_metric_double"字段支持"计数器"指标类型。

由于计数器字段的累积性质，支持以下聚合，并期望通过"计数器"字段提供有意义的结果："速率"、"直方图"、"范围"、"最小值"、"最大值"、"top_metrics"和"variable_width_histogram"。为了防止现有集成和自定义仪表板出现问题，我们还允许以下聚合，即使结果在计数器上可能毫无意义："平均"、"箱线图"、"基数"、"扩展统计"、"中位数绝对偏差"、"百分位数"、"百分位数"、"统计"、"总和"和"值计数"。

`gauge`

    

表示可以任意增加或减少的单个数值的指标。例如，温度或可用磁盘空间。

只有数字和"aggregate_metric_double"字段支持"仪表"指标类型。

"空"(默认值)

     Not a time series metric. 

### 时间序列模式

TSDS 的匹配索引模板必须包含带有"index_mode：time_series"选项的"data_stream"对象。此选项可确保 TSDS 创建具有"索引模式"设置为"time_series"的后备索引。此设置在后备索引中启用大多数与 TSDS 相关的功能。

如果将现有数据流转换为 TSDS，则只有在转换后创建的后备索引才具有"time_series"的"index.mode"。您无法更改现有后备索引的"index.mode"。

#### '_tsid' 元数据字段

当您将文档添加到 TSDS 时，Elasticsearch 会自动为该文档生成一个"_tsid"元数据字段。"_tsid"是包含文档尺寸的对象。具有相同"_tsid"的相同 TSDS 中的文档是同一时间序列的一部分。

"_tsid"字段不可查询或更新。您也不能使用获取文档请求检索文档的"_tsid"。但是，您可以在聚合中使用"_tsid"字段，并使用"fields"参数在搜索中检索"_tsid"值。

不应依赖"_tsid"字段的格式。它可能会因版本而异。

#### 时限索引

在 TSDS 中，每个后备索引(包括最新的后备索引)都有一系列可接受的"@timestamp"值。此范围由"index.time_series.start_time"和"index.time_series.end_time"索引设置定义。

当您将文档添加到 TSDS 时，Elasticsearch 会根据其"@timestamp"值将该文档添加到相应的支持索引中。因此，TSDS 可以将文档添加到任何可以接收写入操作的 TSDS 后备索引。即使索引不是最新的后备索引，这也适用。

！有时限的指数

某些 ILM 操作(如"强制合并"、"收缩"和"searchable_snapshot")使后备索引成为只读索引。不能将文档添加到只读索引。在为 TSDS 定义索引生命周期策略时，请记住这一点。

如果没有后备索引可以接受文档的"@timestamp"值，Elasticsearch将拒绝该文档。

Elasticsearch 会自动配置"index.time_series.start_time"和"index.time_series.end_time"设置，作为索引创建和滚动更新过程的一部分。

#### 提前展望

使用"index.look_ahead_time"索引设置来配置将来可以将文档添加到索引的时间。当您为 TSDS 创建新的写入索引时，Elasticsearch 会将索引的 'index.time_series.end_time' 值计算为：

"现在+index.look_ahead_time"

在时间序列轮询间隔(通过"time_series.poll_interval"设置控制)时，Elasticsearch 会检查写入索引是否满足其索引生命周期策略中的滚动更新条件。如果没有，Elasticsearch 会刷新 'now' 值，并将写入索引的 'index.time_series.end_time' 更新为：

'now + index.look_ahead_time + time_series.poll_interval'

此过程一直持续到写入索引滚动更新。当索引滚动更新时，Elasticsearch 会为索引设置一个最终的 'index.time_series.end_time' 值。此值与新写入索引的"index.time_series.start_time"接壤。这可确保相邻支持索引的"@timestamp"范围始终边界但不重叠。

#### 添加数据的接受时间范围

TSDS 旨在引入当前指标数据。首次创建 TSDS 时，初始支持索引具有：

* "index.time_series.start_time"值设置为"now - index.look_ahead_time" * "index.time_series.end_time"值设置为"now + index.look_ahead_time"

只能为该范围内的数据编制索引。

在我们的 TSDS 示例中，"index.look_ahead_time"设置为三小时，因此只有当前时间之前或之后三小时内值为"@timestamp"的文档才会被接受用于索引。

可以使用获取数据流 API 检查写入任何 TSDS 的接受时间范围。

#### 基于维度的路由

在每个TSDS支持索引中，Elasticsearch使用"index.routing_path"索引设置将具有相同维度的文档路由到相同的分片。

为 TSDS 创建匹配的索引模板时，必须在"index.routing_path"设置中指定一个或多个维度。aTSDS 中的每个文档都必须包含一个或多个与"index.routing_path"设置匹配的维度。

"index.routing_path"设置中的维度必须是普通的"关键字"字段。"index.routing_path"设置接受通配符模式(例如"dim.*")，并且可以动态匹配新字段。但是，Elasticsearch 将拒绝任何添加脚本化、运行时或与"index.routing_path"值匹配的非维度、非"关键字"字段的映射更新。

TSDS 文档不支持自定义"_routing"值。同样，不能在 TSDS 的映射中要求"_routing"值。

#### 索引排序

Elasticsearch使用压缩算法来压缩重复的值。当重复值彼此靠近还原时，此压缩效果最佳 — 在同一索引中、同一分片上以及在同一分片段中并排恢复。

大多数时间序列数据都包含重复值。维度在同一时间序列中跨文档重复。时序的指标值也可能随时间缓慢变化。

在内部，每个 TSDS 后备索引使用索引排序按"_tsid"和"@timestamp"对其分片段进行排序。这使得这些重复值更有可能彼此靠近存储，以便更好地压缩。TSDS 不支持任何 'index.sort.*' indexsettings。

### 下一步是什么？

现在您已经了解了基础知识，可以创建 TSDS")或将现有数据流转换为 TSDS")。

[« Modify a data stream](modify-data-streams.md) [Set up a time series data
stream (TSDS) »](set-up-tsds.md)
