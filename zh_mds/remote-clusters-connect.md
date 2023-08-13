

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Remote clusters](remote-clusters.md)

[« Configure remote clusters with security](remote-clusters-security.md)
[Configure roles and users for remote clusters »](remote-clusters-
privileges.md)

## 连接到远程群集

本地群集使用传输接口与远程群集建立通信。本地群集中的协调节点与远程群集中的特定节点建立长期 TCP 连接。Elasticsearch 要求这些连接保持打开状态，即使连接长时间处于空闲状态。

您必须具有"管理"群集权限才能连接远程群集。

要从 Kibana 中的堆栈管理添加远程集群，请执行以下操作：

1. 从侧面导航栏中选择**远程群集**。  2. 指定 Elasticsearch 终端节点 URL，或远程集群的 IP 地址或主机名，后跟传输端口(默认为 '9300')。例如，"cluster.es.eastus2.staging.azure.foundit.no:9400"或"192.168.1.1：9300"。

或者，使用群集更新设置 API 添加远程群集。您还可以使用此 API 为本地群集中的 _every_ 节点动态配置远程群集。要在本地集群中的单个节点上配置远程集群，请在"elasticsearch.yml"中为每个节点定义静态设置。

连接远程群集后，为远程群集配置角色和用户。

以下请求添加别名为"cluster_one"的远程群集。此_cluster alias_是表示与远程群集的连接的唯一标识符，用于区分本地索引和远程索引。

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          cluster: {
            remote: {
              cluster_one: {
                seeds: [
                  '127.0.0.1:9300'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /_cluster/settings
    {
      "persistent" : {
        "cluster" : {
          "remote" : {
            "cluster_one" : {    __"seeds" : [
                "127.0.0.1:9300" __]
            }
          }
        }
      }
    }

__

|

此远程群集的群集别名为"cluster_one"。   ---|---    __

|

指定远程群集中种子节点的主机名和传输端口。   可以使用远程群集信息 API 验证本地群集是否已成功连接到远程群集：

    
    
    response = client.cluster.remote_info
    puts response
    
    
    GET /_remote/info

API 响应指示本地集群已连接到集群别名为"cluster_one"的远程集群：

    
    
    {
      "cluster_one" : {
        "seeds" : [
          "127.0.0.1:9300"
        ],
        "connected" : true,
        "num_nodes_connected" : 1,  __"max_connections_per_cluster" : 3,
        "initial_connect_timeout" : "30s",
        "skip_unavailable" : false, __"mode" : "sniff"
      }
    }

__

|

本地群集连接到的远程群集中的节点数。   ---|---    __

|

指示如果通过跨群集搜索进行搜索但没有可用的节点，是否跳过远程群集。   ### 动态配置远程群集编辑

使用群集更新设置 API 在群集中的每个节点上动态配置远程设置。以下请求添加三个远程群集："cluster_one"、"cluster_two"和"cluster_three"。

"seeds"参数指定远程群集中种子节点的主机名和传输端口(默认值为"9300")。

"mode"参数确定配置的连接模式，默认为"sniff"。因为"cluster_one"没有指定"模式"，所以它使用默认值。"cluster_two"和"cluster_three"都明确使用不同的模式。

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          cluster: {
            remote: {
              cluster_one: {
                seeds: [
                  '127.0.0.1:9300'
                ]
              },
              cluster_two: {
                mode: 'sniff',
                seeds: [
                  '127.0.0.1:9301'
                ],
                "transport.compress": true,
                skip_unavailable: true
              },
              cluster_three: {
                mode: 'proxy',
                proxy_address: '127.0.0.1:9302'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT _cluster/settings
    {
      "persistent": {
        "cluster": {
          "remote": {
            "cluster_one": {
              "seeds": [
                "127.0.0.1:9300"
              ]
            },
            "cluster_two": {
              "mode": "sniff",
              "seeds": [
                "127.0.0.1:9301"
              ],
              "transport.compress": true,
              "skip_unavailable": true
            },
            "cluster_three": {
              "mode": "proxy",
              "proxy_address": "127.0.0.1:9302"
            }
          }
        }
      }
    }

您可以在初始配置后动态更新远程群集的设置。以下请求更新"cluster_two"的压缩设置，以及"cluster_three"的压缩和 ping 计划设置。

当压缩或 ping 计划设置更改时，所有现有节点连接必须关闭并重新打开，这可能会导致正在进行的请求失败。

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          cluster: {
            remote: {
              cluster_two: {
                "transport.compress": false
              },
              cluster_three: {
                "transport.compress": true,
                "transport.ping_schedule": '60s'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT _cluster/settings
    {
      "persistent": {
        "cluster": {
          "remote": {
            "cluster_two": {
              "transport.compress": false
            },
            "cluster_three": {
              "transport.compress": true,
              "transport.ping_schedule": "60s"
            }
          }
        }
      }
    }

您可以通过为每个远程群集设置传递"null"值，从群集设置中删除远程群集。以下请求从群集设置中删除"cluster_two"，保留"cluster_one"和"cluster_three"不变：

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          cluster: {
            remote: {
              cluster_two: {
                mode: nil,
                seeds: nil,
                skip_unavailable: nil,
                "transport.compress": nil
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT _cluster/settings
    {
      "persistent": {
        "cluster": {
          "remote": {
            "cluster_two": {
              "mode": null,
              "seeds": null,
              "skip_unavailable": null,
              "transport.compress": null
            }
          }
        }
      }
    }

### 静态配置远程群集

如果在"elasticsearch.yml"中指定设置，则只有具有这些设置的节点才能连接到远程群集并为远程群集请求提供服务。

使用集群更新设置API指定的远程集群设置优先于您在"elasticsearch.yml"中为单个节点指定的设置。

在以下示例中，"cluster_one"、"cluster_two"和"cluster_three"是表示与每个集群连接的任意集群别名。这些名称随后用于区分本地索引和远程索引。

    
    
    cluster:
        remote:
            cluster_one:
                seeds: 127.0.0.1:9300
            cluster_two:
                mode: sniff
                seeds: 127.0.0.1:9301
                transport.compress: true      __skip_unavailable: true __cluster_three:
                mode: proxy
                proxy_address: 127.0.0.1:9302 __

__

|

为"cluster_two"请求显式启用压缩。   ---|---    __

|

对于"cluster_two"，断开连接的远程群集是可选的。   __

|

用于连接到"cluster_three"的代理终结点的地址。   « 配置远程群集具有安全性配置远程群集的角色和用户 »