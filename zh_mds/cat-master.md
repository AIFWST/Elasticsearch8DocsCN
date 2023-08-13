

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat indices API](cat-indices.md) [cat nodeattrs API »](cat-
nodeattrs.md)

## 猫咪大师API

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。对于应用程序使用，请使用节点信息 API。

返回主节点信息，包括 ID、绑定 IP 地址和名称。

###Request

"获取/_cat/主"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

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

    
    
    response = client.cat.master(
      v: true
    )
    puts response
    
    
    GET /_cat/master?v=true

API 返回以下响应：

    
    
    id                     host      ip        node
    YzWoH_2BT-6UjVGDyPdqYg 127.0.0.1 127.0.0.1 YzWoH_2

此信息也可以通过"nodes"命令获得，但是当您要做的只是验证所有节点是否同意主节点时，此信息会稍微短一些：

    
    
    % pssh -i -h list.of.cluster.hosts curl -s localhost:9200/_cat/master
    [1] 19:16:37 [SUCCESS] es3.vm
    Ntgn2DcuTjGuXlhKDUD4vA 192.168.56.30 H5dfFeA
    [2] 19:16:37 [SUCCESS] es2.vm
    Ntgn2DcuTjGuXlhKDUD4vA 192.168.56.30 H5dfFeA
    [3] 19:16:37 [SUCCESS] es1.vm
    Ntgn2DcuTjGuXlhKDUD4vA 192.168.56.30 H5dfFeA

[« cat indices API](cat-indices.md) [cat nodeattrs API »](cat-
nodeattrs.md)
