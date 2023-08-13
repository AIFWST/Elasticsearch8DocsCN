

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Transform APIs](transform-apis.md)

[« Delete transform API](delete-transform.md) [Get transform statistics API
»](get-transform-stats.md)

## 获取转换接口

检索转换的配置信息。

###Request

"得到_transform/<transform_id>"

"得到_transform/<transform_id><transform_id>，"

"得到_transform/"

"得到_transform/_all"

"得到_transform/*"

###Prerequisites

需要"monitor_transform"群集权限。此权限包含在"transform_user"内置角色中。

###Description

您可以使用逗号分隔的标识符列表或通配符表达式在单个 API 请求中获取多个转换的信息。可以通过使用"_all"、将"*"指定为"<transform_id>"或省略"来获取所有转换的信息<transform_id>。

### 路径参数

`<transform_id>`

     (Optional, string) Identifier for the transform. It can be a transform identifier or a wildcard expression. If you do not specify one of these options, the API returns information for all transforms. 

### 查询参数

`allow_no_match`

    

(可选，布尔值)指定在请求时要执行的操作：

* 包含通配符表达式，并且没有匹配的转换。  * 包含"_all"字符串或不包含标识符，并且没有匹配项。  * 包含通配符表达式，并且只有部分匹配。

默认值为"true"，当没有匹配项时返回一个空的"转换"数组，当存在部分匹配时返回结果的子集。

如果此参数为"false"，则当没有匹配项或只有部分匹配项时，请求将返回"404"状态代码。

`exclude_generated`

     (Optional, Boolean) Excludes fields that were automatically added when creating the transform. This allows the configuration to be in an acceptable format to be retrieved and then added to another cluster. Default is false. 
`from`

     (Optional, integer) Skips the specified number of transforms. The default value is `0`. 
`size`

     (Optional, integer) Specifies the maximum number of transforms to obtain. The default value is `100`. 

### 响应正文

API 返回一个转换资源数组，这些资源按"id"值升序排序。有关属性的完整列表，请参阅创建转换 API。

`create_time`

     (string) The time the transform was created. For example, `1576094542936`. This property is informational; you cannot change its value. 
`version`

     (string) The version of Elasticsearch that existed on the node when the transform was created. 

### 响应码

"404"(缺少资源)

     If `allow_no_match` is `false`, this code indicates that there are no resources that match the request or only partial matches for the request. 

###Examples

以下示例检索有关最多十个转换的信息：

    
    
    response = client.transform.get_transform(
      size: 10
    )
    puts response
    
    
    GET _transform?size=10

以下示例获取"ecommerce_transform1"转换的配置信息：

    
    
    response = client.transform.get_transform(
      transform_id: 'ecommerce_transform1'
    )
    puts response
    
    
    GET _transform/ecommerce_transform1

API 返回以下结果：

    
    
    {
      "count" : 1,
      "transforms" : [
        {
          "id" : "ecommerce_transform1",
          "authorization" : {
            "roles" : [
              "superuser"
            ]
          },
          "version" : "8.4.0",
          "create_time" : 1656023416565,
          "source" : {
            "index" : [
              "kibana_sample_data_ecommerce"
            ],
            "query" : {
              "term" : {
                "geoip.continent_name" : {
                  "value" : "Asia"
                }
              }
            }
          },
          "dest" : {
            "index" : "kibana_sample_data_ecommerce_transform1",
            "pipeline" : "add_timestamp_pipeline"
          },
          "frequency" : "5m",
          "sync" : {
            "time" : {
              "field" : "order_date",
              "delay" : "60s"
            }
          },
          "pivot" : {
            "group_by" : {
              "customer_id" : {
                "terms" : {
                  "field" : "customer_id"
                }
              }
            },
            "aggregations" : {
              "max_price" : {
                "max" : {
                  "field" : "taxful_total_price"
                }
              }
            }
          },
          "description" : "Maximum priced ecommerce data by customer_id in Asia",
          "settings" : { },
          "retention_policy" : {
            "time" : {
              "field" : "order_date",
              "max_age" : "30d"
            }
          }
        }
      ]
    }

[« Delete transform API](delete-transform.md) [Get transform statistics API
»](get-transform-stats.md)
