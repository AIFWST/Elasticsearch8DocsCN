

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Update datafeeds API](ml-update-datafeed.md) [Update anomaly detection
jobs API »](ml-update-job.md)

## 更新过滤器接口

更新筛选器的说明、添加项目或删除项目。

###Request

"开机自检_ml/过滤器/<filter_id>/_update"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

### 路径参数

`<filter_id>`

     (Required, string) A string that uniquely identifies a filter. 

### 请求正文

`add_items`

     (Optional, array of strings) The items to add to the filter. 
`description`

     (Optional, string) A description for the filter. 
`remove_items`

     (Optional, array of strings) The items to remove from the filter. 

###Examples

    
    
    response = client.ml.update_filter(
      filter_id: 'safe_domains',
      body: {
        description: 'Updated list of domains',
        add_items: [
          '*.myorg.com'
        ],
        remove_items: [
          'wikipedia.org'
        ]
      }
    )
    puts response
    
    
    POST _ml/filters/safe_domains/_update
    {
      "description": "Updated list of domains",
      "add_items": ["*.myorg.com"],
      "remove_items": ["wikipedia.org"]
    }

API 返回以下结果：

    
    
    {
      "filter_id": "safe_domains",
      "description": "Updated list of domains",
      "items": ["*.google.com", "*.myorg.com"]
    }

[« Update datafeeds API](ml-update-datafeed.md) [Update anomaly detection
jobs API »](ml-update-job.md)
