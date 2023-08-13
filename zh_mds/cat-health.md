

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat fielddata API](cat-fielddata.md) [cat indices API »](cat-
indices.md)

## 猫咪健康接口

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。对于应用程序使用，请使用群集运行状况 API。

返回群集的运行状况，类似于群集运行状况 API。

###Request

"获取/_cat/生命值"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

###Description

您可以使用猫健康 API 获取集群的健康状态。

此 API 通常用于检查故障群集。为了帮助您跟踪群集运行状况以及日志文件和警报系统，API 以两种格式返回时间戳：

* "HH：MM：SS"，这是人类可读的，但不包含日期信息。  * Unix"纪元"时间，可进行机器排序并包含日期信息。这对于需要多天的群集恢复非常有用。

您可以使用 cat 运行状况 API 跨多个节点验证群集运行状况。请参阅跨节点的示例。

您还可以使用 API 跟踪大型集群在较长时间内的恢复情况。请参阅大型集群的示例。

### 查询参数

`format`

     (Optional, string) Short version of the [HTTP accept header](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html). Valid values include JSON, YAML, etc. 
`h`

     (Optional, string) Comma-separated list of column names to display. 
`help`

     (Optional, Boolean) If `true`, the response includes help information. Defaults to `false`. 
`s`

     (Optional, string) Comma-separated list of column names or column aliases used to sort the response. 
`time`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Unit used to display time values. 
`ts` (timestamps)

     (Optional, Boolean) If `true`, returns `HH:MM:SS` and [Unix `epoch`](https://en.wikipedia.org/wiki/Unix_time) timestamps. Defaults to `true`. 
`v`

     (Optional, Boolean) If `true`, the response includes column headings. Defaults to `false`. 

###Examples

#### 带有时间戳的示例

默认情况下，cat health API 返回"HH：MM：SS"和 Unix'epoch' 时间戳。例如：

    
    
    response = client.cat.health(
      v: true
    )
    puts response
    
    
    GET /_cat/health?v=true

API 返回以下响应：

    
    
    epoch      timestamp cluster       status node.total node.data shards pri relo init unassign pending_tasks max_task_wait_time active_shards_percent
    1475871424 16:17:04  elasticsearch green           1         1      1   1    0    0        0             0                  -                100.0%

#### 不带时间戳的示例

您可以使用"ts"(时间戳)参数来禁用时间戳。例如：

    
    
    response = client.cat.health(
      v: true,
      ts: false
    )
    puts response
    
    
    GET /_cat/health?v=true&ts=false

API 返回以下响应：

    
    
    cluster       status node.total node.data shards pri relo init unassign pending_tasks max_task_wait_time active_shards_percent
    elasticsearch green           1         1      1   1    0    0        0             0                  -                100.0%

#### 跨节点示例

您可以使用 cat 运行状况 API 跨节点验证集群的运行状况。例如：

    
    
    % pssh -i -h list.of.cluster.hosts curl -s localhost:9200/_cat/health
    [1] 20:20:52 [SUCCESS] es3.vm
    1384309218 18:20:18 foo green 3 3 3 3 0 0 0 0
    [2] 20:20:52 [SUCCESS] es1.vm
    1384309218 18:20:18 foo green 3 3 3 3 0 0 0 0
    [3] 20:20:52 [SUCCESS] es2.vm
    1384309218 18:20:18 foo green 3 3 3 3 0 0 0 0

#### 大型集群示例

您可以使用 cat 运行状况 API 跟踪大型集群在较长时间内的恢复情况。您可以通过在延迟循环中包含猫健康 API 请求来执行此操作。例如：

    
    
    % while true; do curl localhost:9200/_cat/health; sleep 120; done
    1384309446 18:24:06 foo red 3 3 20 20 0 0 1812 0
    1384309566 18:26:06 foo yellow 3 3 950 916 0 12 870 0
    1384309686 18:28:06 foo yellow 3 3 1328 916 0 12 492 0
    1384309806 18:30:06 foo green 3 3 1832 916 4 0 0
    ^C

在此示例中，恢复大约需要六分钟，从"18：24：06"到"18：30：06"。如果此恢复需要数小时，您可以继续监视"未分配"分片的数量，该数量应该会下降。如果"未分配"分片的数量保持不变，则表明集群恢复存在问题。

[« cat fielddata API](cat-fielddata.md) [cat indices API »](cat-
indices.md)
