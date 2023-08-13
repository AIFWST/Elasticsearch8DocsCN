

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Get categories API](ml-get-category.md) [Get datafeed statistics API
»](ml-get-datafeed-stats.md)

## 获取数据馈送接口

检索数据馈送的配置信息。

###Request

"获取_ml/数据馈送/<feed_id>"

"获取_ml/数据馈送/<feed_id><feed_id>"，""

"获取_ml/数据馈送/"

"获取_ml/数据馈送/_all"

###Prerequisites

需要"monitor_ml"群集权限。此权限包含在"machine_learning_user"内置角色中。

###Description

此 API 最多返回 10，000 个数据馈送。

### 路径参数

`<feed_id>`

    

(可选，字符串)数据馈送的标识符。它可以是数据馈送标识符或通配符表达式。

您可以使用逗号分隔的数据馈送列表或通配符表达式在单个 API 请求中获取多个数据馈送的信息。您可以通过使用"_all"、指定"*"作为数据馈送标识符或省略标识符来获取所有数据馈送的信息。

### 查询参数

`allow_no_match`

    

(可选，布尔值)指定在请求时要执行的操作：

* 包含通配符表达式，并且没有匹配的数据馈送。  * 包含"_all"字符串或不包含标识符，并且没有匹配项。  * 包含通配符表达式，并且只有部分匹配。

默认值为"true"，当没有匹配项时返回一个空的"数据馈送"数组，当存在部分匹配时返回结果子集。如果此参数为"false"，则当没有匹配项或只有部分匹配项时，请求将返回"404"状态代码。

`exclude_generated`

     (Optional, Boolean) Indicates if certain fields should be removed from the configuration on retrieval. This allows the configuration to be in an acceptable format to be retrieved and then added to another cluster. Default is false. 

### 响应正文

API 返回数据馈送资源数组。有关属性的完整列表，请参阅创建数据馈送 API。

### 响应码

"404"(缺少资源)

     If `allow_no_match` is `false`, this code indicates that there are no resources that match the request or only partial matches for the request. 

###Examples

    
    
    response = client.ml.get_datafeeds(
      datafeed_id: 'datafeed-high_sum_total_sales'
    )
    puts response
    
    
    GET _ml/datafeeds/datafeed-high_sum_total_sales

API 返回以下结果：

    
    
    {
      "count" : 1,
      "datafeeds" : [
        {
          "datafeed_id" : "datafeed-high_sum_total_sales",
          "job_id" : "high_sum_total_sales",
          "authorization" : {
            "roles" : [
              "superuser"
            ]
          },
          "query_delay" : "93169ms",
          "chunking_config" : {
            "mode" : "auto"
          },
          "indices_options" : {
            "expand_wildcards" : [
              "open"
            ],
            "ignore_unavailable" : false,
            "allow_no_indices" : true,
            "ignore_throttled" : true
          },
          "query" : {
            "bool" : {
              "filter" : [
                {
                  "term" : {
                    "event.dataset" : "sample_ecommerce"
                  }
                }
              ]
            }
          },
          "indices" : [
            "kibana_sample_data_ecommerce"
          ],
          "scroll_size" : 1000,
          "delayed_data_check_config" : {
            "enabled" : true
          }
        }
      ]
    }

[« Get categories API](ml-get-category.md) [Get datafeed statistics API
»](ml-get-datafeed-stats.md)
