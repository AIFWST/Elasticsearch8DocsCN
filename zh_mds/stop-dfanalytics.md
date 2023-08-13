

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning data frame analytics APIs](ml-df-
analytics-apis.md)

[« Start data frame analytics jobs API](start-dfanalytics.md) [Update data
frame analytics jobs API »](update-dfanalytics.md)

## 停止数据帧分析作业API

停止一个或多个数据框分析作业。

###Request

"发布_ml/data_frame/分析/<data_frame_analytics_id>/_stop"

'POST_ml/data_frame/analytics/<data_frame_analytics_id>，<data_frame_analytics_id>/_stop'

"发布_ml/data_frame/分析/_all/_stop"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

数据框分析作业在其整个生命周期中可以多次启动和停止。

您可以使用以逗号分隔的数据框分析作业列表或通配符表达式在单个 API 请求中停止多个数据框分析作业。您可以通过使用 _all 或将 * 指定为 <data_frame_analytics_id>.

### 路径参数

`<data_frame_analytics_id>`

     (Required, string) Identifier for the data frame analytics job. This identifier can contain lowercase alphanumeric characters (a-z and 0-9), hyphens, and underscores. It must start and end with alphanumeric characters. 

### 查询参数

`allow_no_match`

    

(可选，布尔值)指定在请求时要执行的操作：

* 包含通配符表达式，并且没有匹配的数据框分析作业。  * 包含"_all"字符串或不包含标识符，并且没有匹配项。  * 包含通配符表达式，并且只有部分匹配。

默认值为"true"，当没有匹配项时返回空的"data_frame_analytics"数组，当存在部分匹配时返回结果子集。如果此参数为"false"，则当没有匹配项或只有部分匹配项时，请求将返回"404"状态代码。

`force`

     (Optional, Boolean) If true, the data frame analytics job is stopped forcefully. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Controls the amount of time to wait until the data frame analytics job stops. Defaults to 20 seconds. 

###Examples

以下示例停止"日志分析"数据帧分析作业：

    
    
    response = client.ml.stop_data_frame_analytics(
      id: 'loganalytics'
    )
    puts response
    
    
    POST _ml/data_frame/analytics/loganalytics/_stop

当数据框分析作业停止时，您会收到以下结果：

    
    
    {
      "stopped" : true
    }

[« Start data frame analytics jobs API](start-dfanalytics.md) [Update data
frame analytics jobs API »](update-dfanalytics.md)
