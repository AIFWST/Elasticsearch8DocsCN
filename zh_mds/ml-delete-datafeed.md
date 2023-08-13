

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Delete calendars API](ml-delete-calendar.md) [Delete events from calendar
API »](ml-delete-calendar-event.md)

## 删除数据馈送接口

删除现有数据馈送。

###Request

"删除_ml/数据馈送/<feed_id>"

###Prerequisites

* 需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。  * 除非使用"force"参数，否则必须先停止数据馈送，然后才能将其删除。

### 路径参数

`<feed_id>`

     (Required, string) A numerical character string that uniquely identifies the datafeed. This identifier can contain lowercase alphanumeric characters (a-z and 0-9), hyphens, and underscores. It must start and end with alphanumeric characters. 

### 查询参数

`force`

     (Optional, Boolean) Use to forcefully delete a started datafeed; this method is quicker than stopping and deleting the datafeed. 

###Examples

    
    
    response = client.ml.delete_datafeed(
      datafeed_id: 'datafeed-total-requests'
    )
    puts response
    
    
    DELETE _ml/datafeeds/datafeed-total-requests

删除数据馈送后，您会收到以下结果：

    
    
    {
      "acknowledged": true
    }

[« Delete calendars API](ml-delete-calendar.md) [Delete events from calendar
API »](ml-delete-calendar-event.md)
