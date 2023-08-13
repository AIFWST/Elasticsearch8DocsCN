

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat task management API](cat-tasks.md) [cat thread pool API »](cat-
thread-pool.md)

## 猫模板接口

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。对于应用程序使用，请使用获取索引模板 API。

返回有关群集中索引模板的信息。您可以使用索引模板在创建时将索引设置和字段映射应用于新索引。

###Request

'获取/_cat/模板/<template_name>'

"获取/_cat/模板"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

### 路径参数

`<template_name>`

     (Optional, string) The name of the template to return. Accepts wildcard expressions. If omitted, all templates are returned. 

### 查询参数

`format`

     (Optional, string) Short version of the [HTTP accept header](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html). Valid values include JSON, YAML, etc. 
`h`

     (Optional, string) Comma-separated list of column names to display. 
`help`

     (Optional, Boolean) If `true`, the response includes help information. Defaults to `false`. 
`local`

     (Optional, Boolean) If `true`, the request retrieves information from the local node only. Defaults to `false`, which means information is retrieved from the master node. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`s`

     (Optional, string) Comma-separated list of column names or column aliases used to sort the response. 
`v`

     (Optional, Boolean) If `true`, the response includes column headings. Defaults to `false`. 

###Examples

    
    
    response = client.cat.templates(
      name: 'my-template-*',
      v: true,
      s: 'name'
    )
    puts response
    
    
    GET _cat/templates/my-template-*?v=true&s=name

API 返回以下响应：

    
    
    name          index_patterns order version composed_of
    my-template-0 [te*]          500           []
    my-template-1 [tea*]         501           []
    my-template-2 [teak*]        502   7       []

[« cat task management API](cat-tasks.md) [cat thread pool API »](cat-
thread-pool.md)
