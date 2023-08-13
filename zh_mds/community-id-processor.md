

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Circle processor](ingest-circle-processor.md) [Convert processor
»](convert-processor.md)

## 社区 ID 处理器

计算社区 ID 规范中定义的网络流数据的社区 ID。您可以使用社区 ID 关联与单个流相关的网络事件。

默认情况下，社区 ID 处理器从相关的 ElasticCommon Schema (ECS) 字段中读取网络流数据。如果您使用的是弹性云服务器，则无需进行任何配置。

**表 8.社区 ID 选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'source_ip'

|

no

|

`source.ip`

|

包含源 IP 地址的字段。   "source_port"

|

no

|

`source.port`

|

包含源端口的字段。   "destination_ip"

|

no

|

`destination.ip`

|

包含目标 IP 地址的字段。   "destination_port"

|

no

|

`destination.port`

|

包含目标端口的字段。   "iana_number"

|

no

|

`network.iana_number`

|

包含 IANA 编号的字段。当前支持以下协议编号："1"ICMP，"2"IGMP，"6"TCP，"17"UDP，"47"GRE，"58"ICMP IPv6，"88"EIGRP，"89"OSPF，"103"PIM和"132"SCTP。   "icmp_type"

|

no

|

`icmp.type`

|

包含 ICMP 类型的字段。   "icmp_code"

|

no

|

`icmp.code`

|

包含 ICMP 代码的字段。   "运输"

|

no

|

`network.transport`

|

包含传输协议的字段。仅在"iana_number"字段不存在时使用。   "target_field"

|

no

|

`network.community_id`

|

社区 ID 的输出字段。   "种子"

|

no

|

`0`

|

社区 ID 哈希的种子。必须介于 0 和 65535(含)之间。这些可以防止网络域之间的哈希冲突，例如使用相同寻址方案的暂存网络和生产网络。   "ignore_missing"

|

no

|

`true`

|

如果缺少"true"并且缺少任何必填字段，处理器将静默退出而不修改文档。   "说明"

|

no

|

-

|

处理器的说明。用于描述处理器的目的或其配置。   "如果"

|

no

|

-

|

有条件地执行处理器。请参阅有条件运行处理器。   "ignore_failure"

|

no

|

`false`

|

忽略处理器的故障。请参阅处理管道故障。   "on_failure"

|

no

|

-

|

处理处理器的故障。请参阅处理管道故障。   "标签"

|

no

|

-

|

处理器的标识符。对于调试和指标很有用。   下面是社区 ID 处理器的示例定义：

    
    
    {
      "description" : "...",
      "processors" : [
        {
          "community_id": {
          }
        }
      ]
    }

当上述处理器在以下文档上执行时：

    
    
    {
      "_source": {
        "source": {
          "ip": "123.124.125.126",
          "port": 12345
        },
        "destination": {
          "ip": "55.56.57.58",
          "port": 80
        },
        "network": {
          "transport": "TCP"
        }
      }
    }

它产生以下结果：

    
    
    "_source" : {
      "destination" : {
        "port" : 80,
        "ip" : "55.56.57.58"
      },
      "source" : {
        "port" : 12345,
        "ip" : "123.124.125.126"
      },
      "network" : {
        "community_id" : "1:9qr9Z1LViXcNwtLVOHZ3CL8MlyM=",
        "transport" : "TCP"
      }
    }

[« Circle processor](ingest-circle-processor.md) [Convert processor
»](convert-processor.md)
