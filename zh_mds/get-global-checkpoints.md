

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Fleet APIs](fleet-apis.md)

[« Fleet APIs](fleet-apis.md) [Fleet search API »](fleet-search.md)

## 获取全局检查点API

获取全局检查点 API 的目的是返回索引的当前全局检查点。此 API 允许用户知道哪些序列号已安全地保留在 Elasticsearch 中。

## 轮询全局检查点提前

API 具有由"wait_for_advance"查询参数启用的可选轮询模式。在轮询模式下，API 仅在全局检查点通过提供的"检查点"后返回。默认情况下，"检查点"是一个空数组，这将导致 API 立即返回。

如果在全局检查点超过提供的"检查点"之前发生超时，Elasticsearch 将返回当前的全局检查点和 aboolean 指示请求超时。

目前，"wait_for_advance"参数仅支持一个分片索引。

## 在索引就绪上轮询

默认情况下，在轮询模式下，如果索引不存在或所有主分片都未处于活动状态，则会返回异常。在轮询模式下，"wait_for_index"参数可用于修改此行为。如果 'wait_for_index' 设置为 true，API 将等待创建索引并激活所有主分片。

如果在满足这些条件之前发生超时，将返回相关的异常。

目前，仅当"wait_for_advance"为真时，才支持"wait_for_index"参数。

###Request

"获取/<index>/_fleet/global_checkpoints"

### 路径参数

`<index>`

     (Required, string) A single index or index alias that resolves to a single index. 

### 查询参数

`wait_for_advance`

     (Optional, Boolean) A boolean value which controls whether to wait (until the `timeout`) for the global checkpoints to advance past the provided `checkpoints`. Defaults to `false`. 
`wait_for_index`

     (Optional, Boolean) A boolean value which controls whether to wait (until the `timeout`) for the target index to exist and all primary shards be active. Can only be `true` when `wait_for_advance` is `true`. Defaults to `false`. 
`checkpoints`

     (Optional, list) A comma separated list of previous global checkpoints. When used in combination with `wait_for_advance`, the API will only return once the global checkpoints advances past the `checkpoints`. Defaults to an empty list which will cause Elasticsearch to immediately return the current global checkpoints. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a global checkpoints to advance past `checkpoints`. Defaults to `30s`. 

### 响应正文

`global_checkpoints`

     (array of integers) The global checkpoints for the index. 
`timed_out`

     (Boolean) If `false` the global checkpoints did not advance past the `checkpoints` within the specified `timeout`. 

[« Fleet APIs](fleet-apis.md) [Fleet search API »](fleet-search.md)
