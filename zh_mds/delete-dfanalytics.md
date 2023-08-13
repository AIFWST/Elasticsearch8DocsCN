

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning data frame analytics APIs](ml-df-
analytics-apis.md)

[« Create data frame analytics jobs API](put-dfanalytics.md) [Evaluate data
frame analytics API »](evaluate-dfanalytics.md)

## 删除数据帧分析作业API

删除现有数据框分析作业。

###Request

"删除_ml/data_frame/分析/<data_frame_analytics_id>"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

### 路径参数

`<data_frame_analytics_id>`

     (Required, string) Identifier for the data frame analytics job. 

### 查询参数

`force`

     (Optional, Boolean) If `true`, it deletes a job that is not stopped; this method is quicker than stopping and deleting the job. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) The time to wait for the job to be deleted. Defaults to 1 minute. 

###Examples

以下示例删除"日志分析"数据帧分析作业：

    
    
    response = client.ml.delete_data_frame_analytics(
      id: 'loganalytics'
    )
    puts response
    
    
    DELETE _ml/data_frame/analytics/loganalytics

API 返回以下结果：

    
    
    {
      "acknowledged" : true
    }

[« Create data frame analytics jobs API](put-dfanalytics.md) [Evaluate data
frame analytics API »](evaluate-dfanalytics.md)
