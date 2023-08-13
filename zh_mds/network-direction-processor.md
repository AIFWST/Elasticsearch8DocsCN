

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Lowercase processor](lowercase-processor.md) [Pipeline processor
»](pipeline-processor.md)

## 网络方向处理器

在给定源 IP 地址、目标 IP 地址和内部网络列表的情况下计算网络方向。

默认情况下，网络方向处理器从弹性通用架构 (ECS) 字段中读取 IP 地址。如果您使用的是弹性云服务器，则只需指定"internal_networks"选项。

**表 32.网络方向选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'source_ip'

|

no

|

`source.ip`

|

包含源 IP 地址的字段。   "destination_ip"

|

no

|

`destination.ip`

|

包含目标 IP 地址的字段。   "target_field"

|

no

|

`network.direction`

|

网络方向的输出字段。   "internal_networks"

|

是的*

|

|

内部网络列表。支持 IPv4 和 IPv6 地址和范围，采用 CIDR 表示法。还支持下面列出的命名范围。这些可以使用模板片段构建。* 必须仅指定"internal_networks"或"internal_networks_field"之一。   "internal_networks_field"

|

no

|

|

给定文档上的一个字段，用于读取"internal_networks"配置。   "ignore_missing"

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

处理器的标识符。对于调试和指标很有用。   必须指定"internal_networks"或"internal_networks_field"之一。如果指定了"internal_networks_field"，则它遵循由"ignore_missing"指定的行为。

##### 支持的命名网络范围

"internal_networks"选项支持的命名范围包括：

* "环回" \- 匹配"127.0.0.0/8"或"：：1/128"范围内的环回地址。  * "单播"或"global_unicast"\- 匹配 RFC 1122、RFC 4632 和 RFC 4291 中定义的全局单播地址，IPv4 广播地址 ('255.255.255.255') 除外。这包括专用地址范围。  * "多播" \- 匹配多播地址。  * "interface_local_multicast" \- 匹配 IPv6 接口本地组播地址。  * "link_local_unicast" \- 匹配链路本地单播地址。  * "link_local_multicast" \- 匹配链路本地多播地址。  * 'private' \- 匹配 RFC 1918 (IPv4) 和 RFC 4193 (IPv6) 中定义的专用地址范围。  * "public" \- 匹配非环回、未指定、IPv4 广播、链路本地单播、链路本地多播、接口本地多播或专用的地址。  * "未指定" \- 匹配未指定的地址(IPv4 地址"0.0.0.0"或 IPv6 地址"：：")。

#####Examples

以下示例说明了网络方向处理器的用法：

    
    
    response = client.ingest.simulate(
      body: {
        pipeline: {
          processors: [
            {
              network_direction: {
                internal_networks: [
                  'private'
                ]
              }
            }
          ]
        },
        docs: [
          {
            _source: {
              source: {
                ip: '128.232.110.120'
              },
              destination: {
                ip: '192.168.1.1'
              }
            }
          }
        ]
      }
    )
    puts response
    
    
    POST _ingest/pipeline/_simulate
    {
      "pipeline": {
        "processors": [
          {
            "network_direction": {
              "internal_networks": ["private"]
            }
          }
        ]
      },
      "docs": [
        {
          "_source": {
            "source": {
              "ip": "128.232.110.120"
            },
            "destination": {
              "ip": "192.168.1.1"
            }
          }
        }
      ]
    }

这将产生以下结果：

    
    
    {
      "docs": [
        {
          "doc": {
            ...
            "_source": {
              "destination": {
                "ip": "192.168.1.1"
              },
              "source": {
                "ip": "128.232.110.120"
              },
              "network": {
                "direction": "inbound"
              }
            }
          }
        }
      ]
    }

[« Lowercase processor](lowercase-processor.md) [Pipeline processor
»](pipeline-processor.md)
