

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search Application APIs](search-application-apis.md)

[« Put Search Application](put-search-application.md) [List Search
Applications »](list-search-applications.md)

## 获取搜索应用程序

此功能处于测试阶段，可能会发生变化。设计和代码不如官方 GA 功能成熟，并且按原样提供，不提供任何保证。测试版功能不受官方 GA 功能的支持 SLA 的约束。

检索有关搜索应用程序的信息。

###Request

"得到_application/search_application<name>/"

###Prerequisites

需要"manage_search_application"群集权限。

### 路径参数

`<name>`

     (Required, string) 

### 响应码

`400`

     The `name` was not provided. 
`404` (Missing resources)

     No Search Application matching `name` could be found. 

###Examples

以下示例获取名为"my-app"的搜索应用程序：

    
    
    GET _application/search_application/my-app/

示例响应：

    
    
    {
        "name": "my-app",
        "indices": [ "index1", "index2" ],
        "updated_at_millis": 1682105622204,
        "template": {
          "script": {
            "source": {
              "query": {
                "query_string": {
                  "query": "{{query_string}}",
                  "default_field": "{{default_field}}"
                }
              }
            },
            "params": {
              "query_string": "*",
              "default_field": "*"
            }
          }
      }
    }

[« Put Search Application](put-search-application.md) [List Search
Applications »](list-search-applications.md)
