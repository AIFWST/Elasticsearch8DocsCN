

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search Application APIs](search-application-apis.md)

[« Get Search Application](get-search-application.md) [Delete Search
Application »](delete-search-application.md)

## 列表搜索应用程序

此功能处于测试阶段，可能会发生变化。设计和代码不如官方 GA 功能成熟，并且按原样提供，不提供任何保证。测试版功能不受官方 GA 功能的支持 SLA 的约束。

返回有关搜索应用程序的信息。

###Request

"得到_application/search_application/"

###Prerequisites

需要"manage_search_application"群集权限。

### 路径参数

`q`

     (Optional, string) Query in the Lucene query string syntax, to return only search applications matching the query. 
`size`

     (Optional, integer) Maximum number of results to retrieve. 
`from`

     (Optional, integer) The offset from the first result to fetch. 

### 响应码

###Examples

以下示例列出了所有已配置的搜索应用程序：

    
    
    GET _application/search_application/

以下示例列出了名称与查询字符串"app"匹配的前三个搜索应用程序：

    
    
    GET _application/search_application/?from=0&size=3&q=app

示例响应：

    
    
    {
      "count": 2,
      "results": [
        {
          "name": "app-1",
          "indices": [ "index1", "index2" ]
        },
        {
          "name": "app-2",
          "indices": [ "index3", "index4" ]
        }
      ],
      "updated_at_millis": 1682105622204
    }

[« Get Search Application](get-search-application.md) [Delete Search
Application »](delete-search-application.md)
