

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cluster APIs](cluster.md)

[« Prevalidate node removal API](prevalidate-node-removal-api.md) [Nodes
stats API »](cluster-nodes-stats.md)

## 节点重新加载安全设置API

在集群中的节点上重新装入密钥库。

###Request

"发布/_nodes/reload_secure_settings" "发布/_nodes/<node_id>/reload_secure_settings"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。

###Description

安全设置存储在磁盘上的密钥库中。其中一些设置是可重新加载的。也就是说，您可以在磁盘上更改它们并重新加载它们，而无需重新启动群集中的任何节点。更新密钥库中的可重新加载安全设置后，可以使用此 API 在每个节点上重新加载这些设置。

当 Elasticsearch 密钥库受密码保护且未简单地混淆时，您必须在重新加载安全设置时提供密钥库的密码。重新加载整个集群的设置假定所有节点的密钥库使用相同的密码进行保护;仅当节点间通信已加密时，才允许使用此方法。或者，您可以通过本地访问 API 并传递特定于节点的 Elasticsearch 密钥库密码来重新加载每个节点上的安全设置。

### 路径参数

`<node_id>`

     (Optional, string) The names of particular nodes in the cluster to target. For example, `nodeId1,nodeId2`. For node selection options, see [Node specification](cluster.html#cluster-nodes "Node specification"). 

Elasticsearch 要求跨集群节点进行一致的安全设置，但这种一致性并未强制执行。因此，重新加载特定节点是不标准的。仅当重试失败的重新加载操作时，才有理由这样做。

### 请求正文

`secure_settings_password`

     (Optional, string) The password for the Elasticsearch keystore. 

###Examples

以下示例假定集群的每个节点上的 Elasticsearch 密钥库都有一个通用密码：

    
    
    POST _nodes/reload_secure_settings
    {
      "secure_settings_password":"keystore-password"
    }
    POST _nodes/nodeId1,nodeId2/reload_secure_settings
    {
      "secure_settings_password":"keystore-password"
    }

响应包含"节点"对象，这是一个映射，由节点 id 键控。每个值都有节点"名称"和一个可选的"reload_exception"字段。"reload_exception"字段是在重新加载过程中引发的异常(如果有)的序列化。

    
    
    {
      "_nodes": {
        "total": 1,
        "successful": 1,
        "failed": 0
      },
      "cluster_name": "my_cluster",
      "nodes": {
        "pQHNt5rXTTWNvUgOrdynKg": {
          "name": "node-0"
        }
      }
    }

[« Prevalidate node removal API](prevalidate-node-removal-api.md) [Nodes
stats API »](cluster-nodes-stats.md)
