

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search Application APIs](search-application-apis.md)

[« Search Application APIs](search-application-apis.md) [Get Search
Application »](get-search-application.md)

## 放置搜索应用程序

此功能处于测试阶段，可能会发生变化。设计和代码不如官方 GA 功能成熟，并且按原样提供，不提供任何保证。测试版功能不受官方 GA 功能的支持 SLA 的约束。

创建或更新搜索应用程序。

###Request

"放_application/search_application<name>/"

###Prerequisites

需要"manage_search_application"群集权限。还需要对添加到搜索应用程序的所有索引的管理权限。

### 路径参数

`create`

     (Optional, Boolean) If `true`, this request cannot replace or update existing Search Applications. Defaults to `false`. 
`<body>`

    

(必填，对象)包含搜索应用程序的参数：

"<body>"对象的属性

`indices`

     (Required, array of strings) The [indices](indices.html "Index APIs") associated with this search application. All indices need to exist in order to be added to a search application. 
`template`

    

(可选，对象)与此搜索应用程序关联的搜索模板。搜索应用程序的模板只能通过搜索应用程序进行存储和访问。

* 此搜索模板必须是胡须模板。  * 模板必须包含胡须脚本和脚本源。  * 模板可能会随着后续的放置搜索应用程序请求进行修改。  * 如果在创建搜索应用程序时未指定模板，或者如果从搜索应用程序中删除了模板，我们将使用模板示例中定义的query_string作为默认值。  * 搜索应用程序搜索 API 将使用此模板来执行搜索。  * 该模板接受可选的"字典"参数，该参数定义用于验证发送到搜索应用程序搜索 API 的参数的 JSON 架构。

""的属性<template>

`script`

     (Required, object) The associated mustache template. 
`dictionary`

     (Optional, object) The dictionary used to validate the parameters used with the [search application search](search-application-search.html "Search Application Search") API. The dictionary must be a valid JSON schema. If `dictionary` is not specified, then the parameters will not be validated before being applied in the template. 

### 响应码

`404`

     Search Application `<name>` does not exist. 
`409`

     Search Application `<name>` exists and `create` is `true`. 

###Examples

下面的示例创建一个名为"my-app"的新搜索应用程序：

    
    
    PUT _application/search_application/my-app?create
    {
      "indices": [ "index1", "index2" ],
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
        },
        "dictionary": {
          "properties": {
            "query_string": {
              "type": "string"
            },
            "default_field": {
              "type": "string",
              "enum": [
                "title",
                "description"
              ]
            },
            "additionalProperties": false
          },
          "required": [
            "query_string"
          ]
        }
      }
    }

指定上述"字典"参数时，搜索应用程序搜索 API 将执行以下参数验证：

* 它只接受"query_string"和"default_field"参数 * 它验证"query_string"和"default_field"都是字符串 * 仅当它采用值"标题"或"描述"时，它才接受"default_field"

如果参数无效，搜索应用程序搜索 API 将返回错误。

    
    
    POST _application/search_application/my-app/_search
    {
      "params": {
        "default_field": "author",
        "query_string": "Jane"
      }
    }

在上面的例子中，'default_field' 参数的值无效，因此 Elasticsearch 会返回一个错误：

    
    
    {
      "error": {
        "root_cause": [
          {
            "type": "validation_exception",
            "reason": "Validation Failed: 1: $.default_field: does not have a value in the enumeration [title, description];"
          }
        ],
        "type": "validation_exception",
        "reason": "Validation Failed: 1: $.default_field: does not have a value in the enumeration [title, description];"
      },
      "status": 400
    }

以下示例创建或更新名为"my-app"的现有搜索应用程序：

    
    
    PUT _application/search_application/my-app
    {
      "indices": [ "index1", "index2", "index3" ],
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
        },
        "dictionary": {
          "properties": {
            "query_string": {
              "type": "string"
            },
            "default_field": {
              "type": "string",
              "enum": [
                "title",
                "description"
              ]
            },
            "additionalProperties": false
          },
          "required": [
            "query_string"
          ]
        }
      }
    }

[« Search Application APIs](search-application-apis.md) [Get Search
Application »](get-search-application.md)
