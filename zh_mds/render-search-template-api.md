

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search APIs](search.md)

[« Multi search template API](multi-search-template.md) [Search shards API
»](search-shards.md)

## 渲染搜索模板API

将搜索模板呈现为搜索请求正文。

    
    
    response = client.render_search_template(
      body: {
        id: 'my-search-template',
        params: {
          query_string: 'hello world',
          from: 20,
          size: 10
        }
      }
    )
    puts response
    
    
    POST _render/template
    {
      "id": "my-search-template",
      "params": {
        "query_string": "hello world",
        "from": 20,
        "size": 10
      }
    }

###Request

"获取_render/模板"

"获取_render/模板/<template-id>"

"发布_render/模板"

"发布_render/模板/<template-id>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对至少一个索引模式具有"读取"索引权限。

### 路径参数

`<template-id>`

     (Required*, string) ID of the search template to render. If no `source` is specified, this or the `id` request body parameter is required. 

### 请求正文

`id`

     (Required*, string) ID of the search template to render. If no `source` is specified, this or the `<template-id>` request path parameter is required. If you specify both this parameter and the `<template-id>` parameter, the API uses only `<template-id>`. 
`params`

     (Optional, object) Key-value pairs used to replace Mustache variables in the template. The key is the variable name. The value is the variable value. 
`source`

     (Required*, object) An inline search template. Supports the same parameters as the [search API](search-search.html "Search API")'s request body. These parameters also support [Mustache](https://mustache.github.io/) variables. If no `id` or `<templated-id>` is specified, this parameter is required. 

[« Multi search template API](multi-search-template.md) [Search shards API
»](search-shards.md)
