

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search Application APIs](search-application-apis.md)

[« Delete Search Application](delete-search-application.md) [Render Search
Application Query »](search-application-render-query.md)

## 搜索应用程序搜索

此功能处于测试阶段，可能会发生变化。设计和代码不如官方 GA 功能成熟，并且按原样提供，不提供任何保证。测试版功能不受官方 GA 功能的支持 SLA 的约束。

给定指定的查询参数，创建要运行的 Elasticsearch 查询。如果适用，将为任何未指定的模板参数分配其默认值。

###Request

"发布_application/search_application<name>//_search"

###Prerequisites

需要对搜索应用程序的后备别名具有读取权限。

### 请求正文

`params`

     (Optional, map of strings to objects) Query parameters specific to this request, which will override any defaults specified in the template. 

### 响应码

`404`

     Search Application `<name>` does not exist. 

###Examples

下面的示例对名为"my-app"的搜索应用程序执行搜索：

    
    
    POST _application/search_application/my-app/_search
    {
      "params": {
        "value": "my first query",
        "size": 10,
        "from": 0,
        "text_fields": [
            {
                "name": "title",
                "boost": 10
            },
            {
                "name": "text",
                "boost": 1
            }
        ]
      }
    }

预期结果是已运行的查询的搜索结果。

[« Delete Search Application](delete-search-application.md) [Render Search
Application Query »](search-application-render-query.md)
