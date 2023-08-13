

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Roll up or
transform your data](data-rollup-transform.md) ›[Rolling up historical
data](xpack-rollup.md)

[« Rollup aggregation limitations](rollup-agg-limitations.md) [Transforming
data »](transforms.md)

## 汇总搜索限制

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

对于版本 8.5 及更高版本，我们建议对汇总进行缩减采样，以降低时序数据的存储成本。

虽然我们认为汇总功能非常灵活，但汇总数据的性质意味着会有一些限制。一旦实时数据被丢弃，您将始终失去一些灵活性。

本页重点介绍主要限制，以便您了解这些限制。

#### 每次搜索只有一个汇总索引

使用汇总搜索终结点时，"index"参数接受一个或多个索引。这些索引可以是常规、非汇总索引和汇总索引的混合。但是，只能指定一个汇总索引。"index"参数的确切规则列表如下：

* 必须至少指定一个索引/索引模式。这可以是汇总索引或非汇总索引。不允许省略索引参数或使用"_all" * 可以指定多个非汇总索引 * 只能指定一个汇总索引。如果提供了多个索引，则会引发异常 * 可以使用索引模式，但如果它们与多个汇总索引匹配，则会引发异常。

此限制由确定哪些作业对于任何给定查询的"最佳"逻辑驱动。如果在单个索引中存储了十个作业，这些索引覆盖了具有不同完整性和不同间隔的源数据，则查询需要确定要实际搜索的作业集。不正确的决策可能会导致聚合结果不准确(例如，过度计算文档计数或指标错误)。不用说，这是一段技术上具有挑战性的代码。

为了帮助简化问题，我们将搜索限制为一次只有一个汇总索引(可能包含多个作业)。将来，我们也许能够将其开放到多个汇总作业。

#### 只能聚合已存储的内容

这可能是一个明显的限制，但汇总只能聚合已存储在汇总中的数据。如果未将汇总作业配置为存储有关"价格"字段的指标，则无法在任何查询或聚合中使用"价格"字段。

例如，以下查询中的"温度"字段已存储在汇总作业中...但不是使用"平均"指标。这意味着不允许使用"avg"here：

    
    
    response = client.rollup.rollup_search(
      index: 'sensor_rollup',
      body: {
        size: 0,
        aggregations: {
          avg_temperature: {
            avg: {
              field: 'temperature'
            }
          }
        }
      }
    )
    puts response
    
    
    GET sensor_rollup/_rollup_search
    {
      "size": 0,
      "aggregations": {
        "avg_temperature": {
          "avg": {
            "field": "temperature"
          }
        }
      }
    }

响应将告诉您字段和聚合是不可能的，因为找不到包含它们的汇总作业：

    
    
    {
      "error": {
        "root_cause": [
          {
            "type": "illegal_argument_exception",
            "reason": "There is not a rollup job that has a [avg] agg with name [avg_temperature] which also satisfies all requirements of query.",
            "stack_trace": ...
          }
        ],
        "type": "illegal_argument_exception",
        "reason": "There is not a rollup job that has a [avg] agg with name [avg_temperature] which also satisfies all requirements of query.",
        "stack_trace": ...
      },
      "status": 400
    }

#### 间隔粒度

汇总以特定粒度存储，由配置中的"date_histogram"组定义。这意味着您只能搜索/聚合间隔大于或等于配置的汇总间隔的汇总数据。

例如，如果数据按每小时汇总一次，则 Rollupsearch API 可以按每小时或更长时间的任何时间间隔进行聚合。小于一小时的间隔将引发异常，因为对于更精细的粒度根本不存在数据。

**请求必须是配置的倍数**

也许不是很明显，但聚合请求中指定的间隔必须是配置间隔的整数倍。如果作业配置为按"3d"间隔汇总，则只能查询和聚合三个("3d"、"6d"、"9d"等)的倍数。

非倍数不起作用，因为汇总的数据不会与聚合生成的存储桶完全"重叠"，从而导致结果不正确。

因此，如果未找到配置间隔的整数倍，则会引发错误。

由于 RollupSearch 终结点可以"上采样"间隔，因此无需配置具有多个间隔(每小时、每天等)的作业。建议仅配置具有所需最小粒度的单个作业，并允许搜索终结点根据需要上采样。

也就是说，如果单个汇总索引中存在多个具有不同间隔的作业，则搜索终结点将识别并使用间隔最大的作业来满足搜索请求。

#### 有限的查询组件

汇总功能允许在搜索请求中使用"查询"，但组件子集有限。当前允许的查询包括：

* 术语查询 * 术语查询 * 范围查询 * 匹配所有查询 * 任何复合查询(布尔、提升、常量分数等)

此外，这些查询只能使用在汇总作业中也作为"组"保存的字段。如果要筛选关键字"主机名"字段，则必须已在汇总作业中的"术语"分组下配置该字段。

如果尝试使用不受支持的查询，或者查询引用了汇总作业中未配置的字段，则会引发异常。我们预计，随着更多查询的实施，支持查询列表将随着时间的推移而增长。

####Timezones

汇总文档存储在作业中"date_histogram"组配置的时区中。如果未指定时区，则默认值为以"UTC"为单位的汇总时间戳。

[« Rollup aggregation limitations](rollup-agg-limitations.md) [Transforming
data »](transforms.md)
