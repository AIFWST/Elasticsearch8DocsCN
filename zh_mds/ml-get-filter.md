

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Get scheduled events API](ml-get-calendar-event.md) [Get records API
»](ml-get-record.md)

## 获取过滤器接口

检索筛选器。

###Request

"获取_ml/过滤器/<filter_id>"

"获取_ml/过滤器/"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

您可以获得单个过滤器或所有过滤器。有关详细信息，请参阅自定义规则。

### 路径参数

`<filter_id>`

     (Optional, string) A string that uniquely identifies a filter. 

### 查询参数

`from`

     (Optional, integer) Skips the specified number of filters. Defaults to `0`. 
`size`

     (Optional, integer) Specifies the maximum number of filters to obtain. Defaults to `100`. 

### 响应正文

API 返回筛选器资源数组，这些资源具有以下属性：

`description`

     (string) A description of the filter. 
`filter_id`

     (string) A string that uniquely identifies a filter. 
`items`

     (array of strings) An array of strings which is the filter item list. 

###Examples

    
    
    response = client.ml.get_filters(
      filter_id: 'safe_domains'
    )
    puts response
    
    
    GET _ml/filters/safe_domains

API 返回以下结果：

    
    
    {
      "count": 1,
      "filters": [
        {
          "filter_id": "safe_domains",
          "description": "A list of safe domains",
          "items": [
            "*.google.com",
            "wikipedia.org"
          ]
        }
      ]
    }

[« Get scheduled events API](ml-get-calendar-event.md) [Get records API
»](ml-get-record.md)
