

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Delete events from calendar API](ml-delete-calendar-event.md) [Delete
forecasts API »](ml-delete-forecast.md)

## 删除过滤器接口

删除筛选器。

###Request

"删除_ml/过滤器/<filter_id>"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

此 API 删除筛选器。如果异常情况检测作业引用筛选器，则无法删除筛选器。必须先更新或删除作业，然后才能删除筛选器。更多信息，请参见自定义规则。

### 路径参数

`<filter_id>`

     (Required, string) A string that uniquely identifies a filter. 

###Examples

    
    
    response = client.ml.delete_filter(
      filter_id: 'safe_domains'
    )
    puts response
    
    
    DELETE _ml/filters/safe_domains

删除筛选器后，您会收到以下结果：

    
    
    {
      "acknowledged": true
    }

[« Delete events from calendar API](ml-delete-calendar-event.md) [Delete
forecasts API »](ml-delete-forecast.md)
