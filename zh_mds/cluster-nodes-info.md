

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cluster APIs](cluster.md)

[« Nodes hot threads API](cluster-nodes-hot-threads.md) [Prevalidate node
removal API »](prevalidate-node-removal-api.md)

## 节点信息接口

返回群集节点信息。

###Request

"获取/_nodes"

"获取/_nodes/<node_id>"

"获取/_nodes/<metric>"

'获取/_nodes/<node_id>/<metric>'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

###Description

群集节点信息 API 允许检索一个或多个(或所有)群集节点信息。此处介绍了所有节点的选择性选项。

默认情况下，它返回节点的所有属性和核心设置。

### 路径参数

`<metric>`

    

(可选，字符串)将返回的信息限制为特定指标。支持逗号分隔的列表，例如"http，ingest"。

""的有效值<metric>

`aggregations`

     Information about the available types of aggregation. 
`http`

     Information about the HTTP interface of this node. 
`indices`

    

与索引相关的节点级配置：

* "total_indexing_buffer"：此节点上索引缓冲区的最大大小。

`ingest`

     Information about ingest pipelines and processors. 
`jvm`

     JVM information, including its name, its version, and its configuration. 
`os`

     Operating system information, including its name and version. 
`plugins`

    

有关每个节点安装的插件和模块的详细信息。以下信息可用于每个插件和模块：

* "name"：插件名称 * "版本"：插件构建的 Elasticsearch 版本 * "描述"：插件用途的简短描述 * "类名"：插件入口点的完全限定类名 * "has_native_controller"：插件是否具有本机控制器进程

`process`

     Process information, including the numeric process ID. 
`settings`

     Lists all node settings in use as defined in the `elasticsearch.yml` file. 
`thread_pool`

     Information about the configuration of each thread pool. 
`transport`

     Information about the transport interface of the node. 

如果您使用此 API 的完整"GET /_nodes//"形式，则还可以请求指标"_all"来检索所有指标<node_id><metric>，也可以请求指标"_none"来抑制所有指标并仅检索节点的身份。

`<node_id>`

     (Optional, string) Comma-separated list of node IDs or names used to limit returned information. 

### 响应正文

`build_hash`

     Short hash of the last git commit in this release. 
`host`

     The node's host name. 
`ip`

     The node's IP address. 
`name`

     The node's name. 
`total_indexing_buffer`

     Total heap allowed to be used to hold recently indexed documents before they must be written to disk. This size is a shared pool across all shards on this node, and is controlled by [Indexing Buffer settings](indexing-buffer.html "Indexing buffer settings"). 
`total_indexing_buffer_in_bytes`

     Same as `total_indexing_buffer`, but expressed in bytes. 
`transport_address`

     Host and port where transport HTTP connections are accepted. 
`version`

     Elasticsearch version running on this node. 
`transport_version`

     The most recent transport version that this node can communicate with. 

可以设置"os"标志以检索与操作系统有关的信息：

`os.refresh_interval_in_millis`

     Refresh interval for the OS statistics 
`os.name`

     Name of the operating system (ex: Linux, Windows, Mac OS X) 
`os.arch`

     Name of the JVM architecture (ex: amd64, x86) 
`os.version`

     Version of the operating system 
`os.available_processors`

     Number of processors available to the Java virtual machine 
`os.allocated_processors`

     The number of processors actually used to calculate thread pool size. This number can be set with the [`node.processors`](modules-threadpool.html#node.processors "Allocated processors setting") setting of a node and defaults to the number of processors reported by the OS. 

可以设置"进程"标志来检索与当前正在运行的进程有关的信息：

`process.refresh_interval_in_millis`

     Refresh interval for the process statistics 
`process.id`

     Process identifier (PID) 
`process.mlockall`

     Indicates if the process address space has been successfully locked in memory 

### 查询参数

`flat_settings`

     (Optional, Boolean) If `true`, returns settings in flat format. Defaults to `false`. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

    
    
    response = client.nodes.info(
      node_id: 'process'
    )
    puts response
    
    response = client.nodes.info(
      node_id: '_all',
      metric: 'process'
    )
    puts response
    
    response = client.nodes.info(
      node_id: 'nodeId1,nodeId2',
      metric: 'jvm,process'
    )
    puts response
    
    response = client.nodes.info(
      node_id: 'nodeId1,nodeId2',
      metric: '_all'
    )
    puts response
    
    
    # return just process
    GET /_nodes/process
    
    # same as above
    GET /_nodes/_all/process
    
    # return just jvm and process of only nodeId1 and nodeId2
    GET /_nodes/nodeId1,nodeId2/jvm,process
    
    # same as above
    GET /_nodes/nodeId1,nodeId2/info/jvm,process
    
    # return all the information of only nodeId1 and nodeId2
    GET /_nodes/nodeId1,nodeId2/_all

可以将"_all"标志设置为返回所有信息 - 也可以省略它。

#### 插件度量示例

如果指定了"插件"，则结果将包含有关已安装的插件和模块的详细信息：

    
    
    response = client.nodes.info(
      node_id: 'plugins'
    )
    puts response
    
    
    GET /_nodes/plugins

API 返回以下响应：

    
    
    {
      "_nodes": ...
      "cluster_name": "elasticsearch",
      "nodes": {
        "USpTGYaBSIKbgSUJR2Z9lg": {
          "name": "node-0",
          "transport_address": "192.168.17:9300",
          "host": "node-0.elastic.co",
          "ip": "192.168.17",
          "version": "{version}",
          "transport_version": 100000298,
          "build_flavor": "default",
          "build_type": "{build_type}",
          "build_hash": "587409e",
          "roles": [
            "master",
            "data",
            "ingest"
          ],
          "attributes": {},
          "plugins": [
            {
              "name": "analysis-icu",
              "version": "{version}",
              "description": "The ICU Analysis plugin integrates Lucene ICU module into elasticsearch, adding ICU relates analysis components.",
              "classname": "org.elasticsearch.plugin.analysis.icu.AnalysisICUPlugin",
              "has_native_controller": false
            }
          ],
          "modules": [
            {
              "name": "lang-painless",
              "version": "{version}",
              "description": "An easy, safe and fast scripting language for Elasticsearch",
              "classname": "org.elasticsearch.painless.PainlessPlugin",
              "has_native_controller": false
            }
          ]
        }
      }
    }

#### 引入度量的示例

如果指定了"摄取"，则响应将包含有关每个节点的可用处理器的详细信息：

    
    
    response = client.nodes.info(
      node_id: 'ingest'
    )
    puts response
    
    
    GET /_nodes/ingest

API 返回以下响应：

    
    
    {
      "_nodes": ...
      "cluster_name": "elasticsearch",
      "nodes": {
        "USpTGYaBSIKbgSUJR2Z9lg": {
          "name": "node-0",
          "transport_address": "192.168.17:9300",
          "host": "node-0.elastic.co",
          "ip": "192.168.17",
          "version": "{version}",
          "transport_version": 100000298,
          "build_flavor": "default",
          "build_type": "{build_type}",
          "build_hash": "587409e",
          "roles": [],
          "attributes": {},
          "ingest": {
            "processors": [
              {
                "type": "date"
              },
              {
                "type": "uppercase"
              },
              {
                "type": "set"
              },
              {
                "type": "lowercase"
              },
              {
                "type": "gsub"
              },
              {
                "type": "convert"
              },
              {
                "type": "remove"
              },
              {
                "type": "fail"
              },
              {
                "type": "foreach"
              },
              {
                "type": "split"
              },
              {
                "type": "trim"
              },
              {
                "type": "rename"
              },
              {
                "type": "join"
              },
              {
                "type": "append"
              }
            ]
          }
        }
      }
    }

[« Nodes hot threads API](cluster-nodes-hot-threads.md) [Prevalidate node
removal API »](prevalidate-node-removal-api.md)
