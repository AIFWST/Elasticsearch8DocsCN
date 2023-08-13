

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat anomaly detectors API](cat-anomaly-detectors.md) [cat count API
»](cat-count.md)

## 猫组件模板API

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。对于应用程序使用，请使用获取组件模板 API。

返回有关群集中组件模板的信息。组件模板是用于构造指定索引映射、设置和别名的索引模板的构建基块。

###Request

'获取/_cat/component_templates/<template_name>'

"获取/_cat/component_templates"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

### 路径参数

`<template_name>`

     (Optional, string) The name of the component template to return. Accepts wildcard expressions. If omitted, all component templates are returned. 

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

    
    
    response = client.cat.component_templates(
      name: 'my-template-*',
      v: true,
      s: 'name'
    )
    puts response
    
    
    GET _cat/component_templates/my-template-*?v=true&s=name

API 返回以下响应：

    
    
    name          version alias_count mapping_count settings_count metadata_count included_in
    my-template-1         0           0             1              0              [my-index-template]
    my-template-2         0           3             0              0              [my-index-template]

[« cat anomaly detectors API](cat-anomaly-detectors.md) [cat count API
»](cat-count.md)
