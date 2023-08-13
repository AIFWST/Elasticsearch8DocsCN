

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat plugins API](cat-plugins.md) [cat repositories API »](cat-
repositories.md)

## 猫恢复接口

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。对于应用程序使用，请使用索引恢复 API。

返回有关正在进行和已完成的分片恢复的信息，类似于索引恢复 API。

对于数据流，API 返回有关流的支持索引的信息。

###Request

'获取/_cat/恢复/<target>"

"获取/_cat/恢复"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。您还必须对检索到的任何数据流、索引或别名具有"监视"或"管理"索引权限。

###Description

cat 恢复 API 返回有关分片恢复的信息，包括正在进行的和已完成的。它是 JSON 索引恢复 API 的更紧凑视图。

分片恢复是初始化分片副本的过程，例如从快照恢复主分片或从主分片同步副本分片。分片恢复完成后，恢复的分片可用于搜索和索引。

恢复在以下过程中自动发生：

* 节点启动。这种类型的恢复称为本地存储恢复。  * 主分片复制。  * 将分片重新定位到同一集群中的不同节点。  * 快照还原操作。  * 克隆、收缩或拆分操作。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases used to limit the request. Supports wildcards (`*`). To target all data streams and indices, omit this parameter or use `*` or `_all`. 

### 查询参数

`active_only`

     (Optional, Boolean) If `true`, the response only includes ongoing shard recoveries. Defaults to `false`. 
`bytes`

     (Optional, [byte size units](api-conventions.html#byte-units "Byte size units")) Unit used to display byte values. 
`detailed`

     (Optional, Boolean) If `true`, the response includes detailed information about shard recoveries. Defaults to `false`. 
`format`

     (Optional, string) Short version of the [HTTP accept header](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html). Valid values include JSON, YAML, etc. 
`h`

     (Optional, string) Comma-separated list of column names to display. 
`help`

     (Optional, Boolean) If `true`, the response includes help information. Defaults to `false`. 
`index`

     (Optional, string) Comma-separated list or wildcard expression of index names used to limit the request. 
`s`

     (Optional, string) Comma-separated list of column names or column aliases used to sort the response. 
`time`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Unit used to display time values. 
`v`

     (Optional, Boolean) If `true`, the response includes column headings. Defaults to `false`. 

###Examples

#### 没有持续恢复的示例

    
    
    response = client.cat.recovery(
      v: true
    )
    puts response
    
    
    GET _cat/recovery?v=true

API 返回以下响应：

    
    
    index             shard time type  stage source_host source_node target_host target_node repository snapshot files files_recovered files_percent files_total bytes bytes_recovered bytes_percent bytes_total translog_ops translog_ops_recovered translog_ops_percent
    my-index-000001   0     13ms store done  n/a         n/a         127.0.0.1   node-0      n/a        n/a      0     0               100%          13          0b    0b              100%          9928b       0            0                      100.0%

在此示例响应中，源节点和目标节点相同，因为恢复类型为"store"，这意味着它们是在 nodestart 上从本地存储读取的。

#### 实时分片恢复示例

通过增加索引的副本计数并使另一个节点联机以托管副本，您可以检索有关正在进行的恢复的信息。

    
    
    response = client.cat.recovery(
      v: true,
      h: 'i,s,t,ty,st,shost,thost,f,fp,b,bp'
    )
    puts response
    
    
    GET _cat/recovery?v=true&h=i,s,t,ty,st,shost,thost,f,fp,b,bp

API 返回以下响应：

    
    
    i               s t      ty   st    shost       thost       f     fp      b  bp
    my-index-000001 0 1252ms peer done  192.168.1.1 192.168.1.2 0     100.0%  0b 100.0%

在此示例响应中，恢复类型为"对等"，表示从另一个节点恢复的分片。返回的文件和字节是实时测量值。

#### 快照恢复示例

您可以使用快照和还原 API 还原索引的备份。您可以使用 cat 恢复 API 检索有关快照恢复的信息。

    
    
    response = client.cat.recovery(
      v: true,
      h: 'i,s,t,ty,st,rep,snap,f,fp,b,bp'
    )
    puts response
    
    
    GET _cat/recovery?v=true&h=i,s,t,ty,st,rep,snap,f,fp,b,bp

API 返回以下响应，恢复类型为"快照"：

    
    
    i               s t      ty       st    rep     snap   f  fp   b     bp
    my-index-000001 0 1978ms snapshot done  my-repo snap-1 79 8.0% 12086 9.0%

[« cat plugins API](cat-plugins.md) [cat repositories API »](cat-
repositories.md)
