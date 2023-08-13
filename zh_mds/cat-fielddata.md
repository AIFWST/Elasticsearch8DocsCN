

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat datafeeds API](cat-datafeeds.md) [cat health API »](cat-health.md)

## cat fielddataAPI

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。对于应用程序使用，请使用节点统计信息 API。

返回群集中每个数据节点上的字段数据缓存当前使用的堆内存量。

###Request

'获取/_cat/字段数据/<field>'

'获取/_cat/字段数据'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

### 路径参数

`<field>`

     (Optional, string) Comma-separated list of fields used to limit returned information. 

### 查询参数

`bytes`

     (Optional, [byte size units](api-conventions.html#byte-units "Byte size units")) Unit used to display byte values. 
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

#### 单个字段的示例

您可以在请求正文或 URL 路径中指定单个字段。以下"fieldata"API 请求检索"body"字段的堆内存大小信息。

    
    
    response = client.cat.fielddata(
      v: true,
      fields: 'body'
    )
    puts response
    
    
    GET /_cat/fielddata?v=true&fields=body

API 返回以下响应：

    
    
    id                     host      ip        node    field   size
    Nqk-6inXQq-OxUfOUI8jNQ 127.0.0.1 127.0.0.1 Nqk-6in body    544b

#### 字段列表示例

您可以在请求正文或 URL 路径中指定以逗号分隔的字段列表。以下"fieldata"API 请求检索"身体"和"灵魂"字段的堆内存大小信息。

    
    
    response = client.cat.fielddata(
      fields: 'body,soul',
      v: true
    )
    puts response
    
    
    GET /_cat/fielddata/body,soul?v=true

API 返回以下响应：

    
    
    id                     host      ip        node    field   size
    Nqk-6inXQq-OxUfOUI8jNQ 127.0.0.1 127.0.0.1 Nqk-6in body    544b
    Nqk-6inXQq-OxUfOUI8jNQ 127.0.0.1 127.0.0.1 Nqk-6in soul    480b

响应显示"身体"和"灵魂"字段的各个字段数据，每个节点每个字段一行。

#### 集群中所有字段的示例

以下"fieldata"API 请求检索堆内存大小信息所有字段。

    
    
    response = client.cat.fielddata(
      v: true
    )
    puts response
    
    
    GET /_cat/fielddata?v=true

API 返回以下响应：

    
    
    id                     host      ip        node    field   size
    Nqk-6inXQq-OxUfOUI8jNQ 127.0.0.1 127.0.0.1 Nqk-6in body    544b
    Nqk-6inXQq-OxUfOUI8jNQ 127.0.0.1 127.0.0.1 Nqk-6in mind    360b
    Nqk-6inXQq-OxUfOUI8jNQ 127.0.0.1 127.0.0.1 Nqk-6in soul    480b

[« cat datafeeds API](cat-datafeeds.md) [cat health API »](cat-health.md)
