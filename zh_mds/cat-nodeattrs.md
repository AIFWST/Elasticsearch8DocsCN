

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat master API](cat-master.md) [cat nodes API »](cat-nodes.md)

## cat nodeattrsAPI

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。对于应用程序使用，请使用节点信息 API。

返回有关自定义节点属性的信息。

###Request

'GET /_cat/nodeattrs'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

### 查询参数

`format`

     (Optional, string) Short version of the [HTTP accept header](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html). Valid values include JSON, YAML, etc. 
`h`

    

(可选，字符串)要显示的列名称的逗号分隔列表。

如果未指定要包含的列，API 将按下面列出的顺序返回默认列。如果显式指定一个或多个列，则仅返回指定的列。

有效列为：

`node`,`name`

     (Default) Name of the node, such as `DKDM97B`. 
`host`, `h`

     (Default) Host name, such as `n1`. 
`ip`, `i`

     (Default) IP address, such as `127.0.1.1`. 
`attr`, `attr.name`

     (Default) Attribute name, such as `rack`. 
`value`, `attr.value`

     (Default) Attribute value, such as `rack123`. 
`id`, `nodeId`

     ID of the node, such as `k0zy`. 
`pid`, `p`

     Process ID, such as `13061`. 
`port`, `po`

     Bound transport port, such as `9300`. 

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

#### 默认列的示例

    
    
    response = client.cat.nodeattrs(
      v: true
    )
    puts response
    
    
    GET /_cat/nodeattrs?v=true

API 返回以下响应：

    
    
    node    host      ip        attr     value
    ...
    node-0 127.0.0.1 127.0.0.1 testattr test
    ...

"节点"、"主机"和"ip"列提供有关每个节点的基本信息。"attr"和"value"列返回自定义节点属性，每行一个。

#### 显式列的示例

以下 API 请求返回"名称"、"pid"、"attr"和"值"列。

    
    
    response = client.cat.nodeattrs(
      v: true,
      h: 'name,pid,attr,value'
    )
    puts response
    
    
    GET /_cat/nodeattrs?v=true&h=name,pid,attr,value

API 返回以下响应：

    
    
    name    pid   attr     value
    ...
    node-0 19566 testattr test
    ...

[« cat master API](cat-master.md) [cat nodes API »](cat-nodes.md)
