

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning data frame analytics APIs](ml-df-
analytics-apis.md)

[« Preview data frame analytics API](preview-dfanalytics.md) [Stop data
frame analytics jobs API »](stop-dfanalytics.md)

## 启动数据帧分析作业API

启动数据框分析作业。

###Request

"发布_ml/data_frame/分析/<data_frame_analytics_id>/_start"

###Prerequisites

需要以下权限：

* 集群："manage_ml"("machine_learning_admin"内置角色授予此权限) * 源索引："读取"、"view_index_metadata" * 目标索引："读取"、"create_index"、"管理"和"索引"

###Description

数据框分析作业在其整个生命周期中可以多次启动和停止。

如果目标索引不存在，则会在您首次启动数据框分析作业时自动创建该索引。目标索引的"index.number_of_shards"和"index.number_of_replicas"设置是从源索引复制的。如果有多个源索引，则目标索引将复制最高设置值。目标索引的映射也是从源索引复制的。如果存在任何映射冲突，作业将无法启动。

如果目标索引存在，则按原样使用。因此，您可以使用自定义设置和映射提前设置目标索引。

启用 Elasticsearch 安全功能后，数据帧分析作业会记住创建它的用户，并使用这些凭据运行作业。如果在创建作业时提供了辅助授权标头，则会使用这些凭据。

### 路径参数

`<data_frame_analytics_id>`

     (Required, string) Identifier for the data frame analytics job. This identifier can contain lowercase alphanumeric characters (a-z and 0-9), hyphens, and underscores. It must start and end with alphanumeric characters. 

### 查询参数

`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Controls the amount of time to wait until the data frame analytics job starts. Defaults to 20 seconds. 

### 响应正文

`acknowledged`

     (Boolean) For a successful response, this value is always `true`. On failure, an exception is returned instead. 
`node`

     (string) The ID of the node that the job was started on. If the job is allowed to open lazily and has not yet been assigned to a node, this value is an empty string. 

###Examples

以下示例启动"日志分析"数据帧分析作业：

    
    
    POST _ml/data_frame/analytics/loganalytics/_start

数据框分析作业启动时，您会收到以下结果：

    
    
    {
      "acknowledged" : true,
      "node" : "node-1"
    }

[« Preview data frame analytics API](preview-dfanalytics.md) [Stop data
frame analytics jobs API »](stop-dfanalytics.md)
