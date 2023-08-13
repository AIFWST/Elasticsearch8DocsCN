

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Create datafeeds API](ml-put-datafeed.md) [Delete calendars API »](ml-
delete-calendar.md)

## 创建过滤器API

实例化筛选器。

###Request

"放置_ml/过滤器/<filter_id>"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

筛选器包含字符串列表。它可以由一个或多个作业使用。具体而言，过滤器在检测器配置对象的"custom_rules"属性中引用。有关详细信息，请参阅自定义规则。

### 路径参数

`<filter_id>`

     (Required, string) A string that uniquely identifies a filter. 

### 请求正文

`description`

     (Optional, string) A description of the filter. 
`items`

     (Required, array of strings) The items of the filter. A wildcard `*` can be used at the beginning or the end of an item. Up to 10000 items are allowed in each filter. 

###Examples

    
    
    response = client.ml.put_filter(
      filter_id: 'safe_domains',
      body: {
        description: 'A list of safe domains',
        items: [
          '*.google.com',
          'wikipedia.org'
        ]
      }
    )
    puts response
    
    
    PUT _ml/filters/safe_domains
    {
      "description": "A list of safe domains",
      "items": ["*.google.com", "wikipedia.org"]
    }

创建筛选器时，您会收到以下响应：

    
    
    {
      "filter_id": "safe_domains",
      "description": "A list of safe domains",
      "items": ["*.google.com", "wikipedia.org"]
    }

[« Create datafeeds API](ml-put-datafeed.md) [Delete calendars API »](ml-
delete-calendar.md)
