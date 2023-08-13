

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Start datafeeds API](ml-start-datafeed.md) [Update datafeeds API »](ml-
update-datafeed.md)

## 停止数据馈送API

停止一个或多个数据馈送。

###Request

"发布_ml/数据馈送/<feed_id>/_stop"

'POST _ml/datafeeds/<feed_id>，<feed_id>/_stop'

"发布_ml/数据馈送/_all/_stop"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

停止的数据馈送将停止从 Elasticsearch 检索数据。Adatafeed 在其整个生命周期中可以多次启动和停止。

### 路径参数

`<feed_id>`

     (Required, string) Identifier for the datafeed. You can stop multiple datafeeds in a single API request by using a comma-separated list of datafeeds or a wildcard expression. You can close all datafeeds by using `_all` or by specifying `*` as the identifier. 

### 查询参数

`allow_no_match`

    

(可选，布尔值)指定在请求时要执行的操作：

* 包含通配符表达式，并且没有匹配的数据馈送。  * 包含"_all"字符串或不包含标识符，并且没有匹配项。  * 包含通配符表达式，并且只有部分匹配。

默认值为"true"，当没有匹配项时返回一个空的"数据馈送"数组，当存在部分匹配时返回结果子集。如果此参数为"false"，则当没有匹配项或只有部分匹配项时，请求将返回"404"状态代码。

`force`

     (Optional, Boolean) If true, the datafeed is stopped forcefully. 
`timeout`

     (Optional, time) Specifies the amount of time to wait until a datafeed stops. The default value is 20 seconds. 

### 请求正文

您还可以在请求正文中指定查询参数(例如"allow_no_match"和"force")。

### 响应码

"404"(缺少资源)

     If `allow_no_match` is `false`, this code indicates that there are no resources that match the request or only partial matches for the request. 

###Examples

    
    
    response = client.ml.stop_datafeed(
      datafeed_id: 'datafeed-low_request_rate',
      body: {
        timeout: '30s'
      }
    )
    puts response
    
    
    POST _ml/datafeeds/datafeed-low_request_rate/_stop
    {
      "timeout": "30s"
    }

当数据馈送停止时，您会收到以下结果：

    
    
    {
      "stopped": true
    }

[« Start datafeeds API](ml-start-datafeed.md) [Update datafeeds API »](ml-
update-datafeed.md)
