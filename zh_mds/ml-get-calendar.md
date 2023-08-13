

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Get buckets API](ml-get-bucket.md) [Get categories API »](ml-get-
category.md)

## 获取日历接口

检索日历的配置信息。

###Request

"获取_ml/日历/<calendar_id>"

"获取_ml/日历/_all"

###Prerequisites

需要"monitor_ml"群集权限。此权限包含在"machine_learning_user"内置角色中。

###Description

有关详细信息，请参阅日历和计划事件。

### 路径参数

`<calendar_id>`

    

(必需，字符串)唯一标识日历的字符串。

您可以使用逗号分隔的 id 列表或通配符表达式在单个 API 请求中获取多个日历的信息。您可以通过使用"_all"、指定"*"作为日历标识符或省略标识符来获取所有日历的信息。

### 查询参数

`from`

     (Optional, integer) Skips the specified number of calendars. This parameter is supported only when you omit the `<calendar_id>`. Defaults to `0`. 
`size`

     (Optional, integer) Specifies the maximum number of calendars to obtain. This parameter is supported only when you omit the `<calendar_id>`. Defaults to `100`. 

### 请求正文

`page`

     Properties of `page`

`from`

     (Optional, integer) Skips the specified number of calendars. This object is supported only when you omit the `<calendar_id>`. Defaults to `0`. 
`size`

     (Optional, integer) Specifies the maximum number of calendars to obtain. This object is supported only when you omit the `<calendar_id>`. Defaults to `100`. 

### 响应正文

API 返回日历资源数组，这些资源具有以下属性：

`calendar_id`

     (string) A string that uniquely identifies a calendar. 
`job_ids`

     (array) An array of anomaly detection job identifiers. For example: `["total-requests"]`. 

###Examples

    
    
    response = client.ml.get_calendars(
      calendar_id: 'planned-outages'
    )
    puts response
    
    
    GET _ml/calendars/planned-outages

API 返回以下结果：

    
    
    {
      "count": 1,
      "calendars": [
        {
          "calendar_id": "planned-outages",
          "job_ids": [
            "total-requests"
          ]
        }
      ]
    }

[« Get buckets API](ml-get-bucket.md) [Get categories API »](ml-get-
category.md)
