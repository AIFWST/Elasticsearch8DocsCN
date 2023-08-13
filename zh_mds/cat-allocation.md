

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat aliases API](cat-alias.md) [cat anomaly detectors API »](cat-anomaly-
detectors.md)

## 猫分配API

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。

提供分配给每个数据节点的分片数及其磁盘空间的快照。

###Request

'获取/_cat/分配/<node_id>"

'获取/_cat/分配'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

### 路径参数

`<node_id>`

     (Optional, string) Comma-separated list of node IDs or names used to limit returned information. 

### 查询参数

`bytes`

     (Optional, [byte size units](api-conventions.html#byte-units "Byte size units")) Unit used to display byte values. 
`format`

     (Optional, string) Short version of the [HTTP accept header](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html). Valid values include JSON, YAML, etc. 
`local`

     (Optional, Boolean) If `true`, the request retrieves information from the local node only. Defaults to `false`, which means information is retrieved from the master node. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`h`

     (Optional, string) Comma-separated list of column names to display. 
`help`

     (Optional, Boolean) If `true`, the response includes help information. Defaults to `false`. 
`s`

     (Optional, string) Comma-separated list of column names or column aliases used to sort the response. 
`v`

     (Optional, Boolean) If `true`, the response includes column headings. Defaults to `false`. 

### 响应正文

`shards`

     Number of primary and replica shards assigned to the node. 
`disk.indices`

    

节点分片使用的磁盘空间。不包括用于传输日志或未分配分片的磁盘空间。

此指标重复计算硬链接文件的磁盘空间，例如在收缩、拆分或克隆索引时创建的磁盘空间。

`disk.used`

    

使用的总磁盘空间。Elasticsearch 从节点的操作系统 (OS) 中检索此指标。该指标包括以下各项的磁盘空间：

* Elasticsearch，包括 translog 和未分配的分片 * 节点的操作系统 * 节点上的任何其他应用程序或文件

与"disk.index"不同，此指标不会重复计算硬链接文件的磁盘空间。

`disk.avail`

     Free disk space available to Elasticsearch. Elasticsearch retrieves this metric from the node's OS. [Disk-based shard allocation](modules-cluster.html#disk-based-shard-allocation "Disk-based shard allocation settings") uses this metric to assign shards to nodes based on available disk space. 
`disk.total`

     Total disk space for the node, including in-use and available space. 
`disk.percent`

     Total percentage of disk space in use. Calculated as `disk.used` / `disk.total`. 
`host`

     Network host for the node. Set using [`network.host`](important-settings.html#network.host "Network host setting"). 
`ip`

     IP address and port for the node. 
`node`

     Name for the node. Set using [`node.name`](important-settings.html#node-name "Node name setting"). 

###Examples

    
    
    response = client.cat.allocation(
      v: true
    )
    puts response
    
    
    GET /_cat/allocation?v=true

API 返回以下响应：

    
    
    shards disk.indices disk.used disk.avail disk.total disk.percent host      ip        node
         1         260b    47.3gb     43.4gb    100.7gb           46 127.0.0.1 127.0.0.1 CSUXak2

此响应显示将单个分片分配给一个可用节点。

[« cat aliases API](cat-alias.md) [cat anomaly detectors API »](cat-anomaly-
detectors.md)
