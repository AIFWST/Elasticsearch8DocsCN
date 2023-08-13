

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search Application APIs](search-application-apis.md)

[« Search Application Search](search-application-search.md) [Searchable
snapshots APIs »](searchable-snapshots-apis.md)

## 呈现搜索应用程序查询

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

给定指定的查询参数，创建要运行的 Elasticsearch 查询。如果适用，将为任何未指定的模板参数分配其默认值。返回将通过调用搜索应用程序搜索生成和运行的特定 Elasticsearch 查询。

###Request

"发布_application/search_application/<name>/_render_query"

###Prerequisites

需要对搜索应用程序的后备别名具有读取权限。

### 请求正文

`params`

     (Optional, map of strings to objects) Query parameters specific to this request, which will override any defaults specified in the template. 

### 响应码

`404`

     Search Application `<name>` does not exist. 

###Examples

下面的示例呈现名为"my-app"的搜索应用程序的查询。在这种情况下，不指定"from"和"size"参数，从搜索应用程序模板中提取默认值。

    
    
    POST _application/search_application/my-app/_render_query
    {
      "params": {
        "value": "my first query",
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

示例响应：

    
    
    {
        "size": 10,
        "from": 0,
        "query": {
            "multi_match": {
                "query": "my first query",
                "fields": [
                    "title^10",
                    "text^1"
                ]
            }
        }
    }

[« Search Application Search](search-application-search.md) [Searchable
snapshots APIs »](searchable-snapshots-apis.md)
