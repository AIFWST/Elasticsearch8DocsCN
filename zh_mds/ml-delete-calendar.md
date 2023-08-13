

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Create filters API](ml-put-filter.md) [Delete datafeeds API »](ml-delete-
datafeed.md)

## 删除日历接口

删除日历。

###Request

"删除_ml/日历/<calendar_id>"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

此 API 从日历中删除所有计划事件，然后删除日历。

### 路径参数

`<calendar_id>`

     (Required, string) A string that uniquely identifies a calendar. 

###Examples

    
    
    response = client.ml.delete_calendar(
      calendar_id: 'planned-outages'
    )
    puts response
    
    
    DELETE _ml/calendars/planned-outages

删除日历后，您会收到以下结果：

    
    
    {
      "acknowledged": true
    }

[« Create filters API](ml-put-filter.md) [Delete datafeeds API »](ml-delete-
datafeed.md)
