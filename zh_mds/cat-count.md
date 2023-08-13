

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat component templates API](cat-component-templates.md) [cat data frame
analytics API »](cat-dfanalytics.md)

## 猫计数API

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。对于应用程序使用，请使用计数 API。

提供对数据流、索引或整个群集的文档计数的快速访问。

文档计数仅包括活动文档，不包括尚未通过合并过程删除的已删除文档。

###Request

'获取/_cat/计数/<target>"

"获取/_cat/计数"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对检索到的任何数据流、索引或别名具有"读取"索引权限。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases used to limit the request. Supports wildcards (`*`). To target all data streams and indices, omit this parameter or use `*` or `_all`. 

### 查询参数

`format`

     (Optional, string) Short version of the [HTTP accept header](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html). Valid values include JSON, YAML, etc. 
`h`

     (Optional, string) Comma-separated list of column names to display. 
`help`

     (Optional, Boolean) If `true`, the response includes help information. Defaults to `false`. 
`s`

     (Optional, string) Comma-separated list of column names or column aliases used to sort the response. 
`v`

     (Optional, Boolean) If `true`, the response includes column headings. Defaults to `false`. 

###Examples

#### 具有单个数据流或索引的示例

以下"计数"API 请求检索"my-index-000001"数据流或索引的文档计数。

    
    
    response = client.cat.count(
      index: 'my-index-000001',
      v: true
    )
    puts response
    
    
    GET /_cat/count/my-index-000001?v=true

API 返回以下响应：

    
    
    epoch      timestamp count
    1475868259 15:24:20  120

#### 集群中所有数据流和索引的示例

以下"计数"API 请求检索集群中所有数据流和索引的文档计数。

    
    
    response = client.cat.count(
      v: true
    )
    puts response
    
    
    GET /_cat/count?v=true

API 返回以下响应：

    
    
    epoch      timestamp count
    1475868259 15:24:20  121

[« cat component templates API](cat-component-templates.md) [cat data frame
analytics API »](cat-dfanalytics.md)
