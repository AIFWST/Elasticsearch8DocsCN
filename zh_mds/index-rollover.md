

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md) ›[ILM concepts](ilm-concepts.md)

[« Index lifecycle](ilm-index-lifecycle.md) [Lifecycle policy updates
»](update-lifecycle-policy.md)

##Rollover

为日志或指标等时序数据编制索引时，不能无限期地写入单个索引。若要满足索引和搜索性能要求并管理资源使用情况，请写入索引，直到达到某个阈值，然后创建新索引并开始写入该索引。使用滚动索引可以：

* 优化活动索引，以实现高性能 _hot_ 节点上的高摄取率。  * 优化 _warm_ 节点上的搜索性能。  * 将较旧的、访问频率较低的数据转移到成本较低的 _cold_ 节点， * 通过删除整个索引来根据您的保留策略删除数据。

我们建议使用数据流来管理时序数据。数据流自动跟踪写入索引，同时将配置保持在最低限度。

每个数据流都需要一个索引模板，其中包含：

* 数据流的名称或通配符 ('*') 模式。  * 数据流的时间戳字段。此字段必须映射为"日期"或"date_nanos"字段数据类型，并且必须包含在索引到数据流的每个文档中。  * 创建每个后备索引时应用于该索引的映射和设置。

数据流专为仅追加数据而设计，其中数据流名称可用作操作(读取、写入、滚动更新、收缩等)目标。如果您的用例需要就地更新数据，则可以改用索引别名管理您的时间序列数据。但是，还有一些配置步骤和概念：

* 指定系列中每个新索引的设置的_index template_。您可以针对引入优化此配置，通常使用与热节点一样多的分片。  * 引用整组索引的_index alias_。  * 指定为_write index_的单个索引。这是处理所有写入请求的活动索引。每次滚动更新时，新索引将成为写入索引。

### 自动展期

ILM 和数据流生命周期(在 [预览版] 此功能是非技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持约束。 ]) 使您能够根据索引大小、文档计数或期限等条件自动滚动到新索引。触发滚动更新时，将创建一个新索引，更新写别名以指向新索引，并将所有后续更新写入新索引。

根据大小、文档计数或期限滚动更新到新索引比基于时间的滚动更新更可取。在任意时间滚动更新通常会导致许多小索引，这可能会对性能和资源使用情况产生负面影响。

[« Index lifecycle](ilm-index-lifecycle.md) [Lifecycle policy updates
»](update-lifecycle-policy.md)