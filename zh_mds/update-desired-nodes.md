

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cluster APIs](cluster.md)

[« Voting configuration exclusions API](voting-config-exclusions.md) [Get
desired nodes API »](get-desired-nodes.md)

## 创建或更新所需的节点API

此功能专为 ElasticsearchService、Elastic Cloud Enterprise 和 Kubernetes 上的 ElasticCloud 间接使用而设计。不支持直接使用。

创建或更新所需的节点。

###Request

    
    
    PUT /_internal/desired_nodes/<history_id>/<version>
    {
        "nodes" : [
            {
                "settings" : {
                     "node.name" : "instance-000187",
                     "node.external_id": "instance-000187",
                     "node.roles" : ["data_hot", "master"],
                     "node.attr.data" : "hot",
                     "node.attr.logical_availability_zone" : "zone-0"
                },
                "processors" : 8.0,
                "memory" : "58gb",
                "storage" : "2tb",
                "node_version" : "{version}"
            }
        ]
    }

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`dry_run`

     (Optional, Boolean) If `true`, then the request simulates the update and returns a response with `dry_run` field set to `true`. 

###Description

此 API 创建或更新所需的节点。外部编排器可以使用此 API 让 Elasticsearch 了解集群拓扑，包括未来的更改，例如添加或删除节点。利用这些信息，系统能够做出更好的决策。

可以通过添加"？dry_run"查询参数在"试运行"模式下运行更新。这将验证请求结果，但实际上不会执行更新。

###Examples

在此示例中，为具有历史记录"Ywkh3INLQcuPT49f6kcppA"的所需节点创建了一个新版本。此 API 仅接受单调递增的版本。

    
    
    PUT /_internal/desired_nodes/Ywkh3INLQcuPT49f6kcppA/100
    {
        "nodes" : [
            {
                "settings" : {
                     "node.name" : "instance-000187",
                     "node.external_id": "instance-000187",
                     "node.roles" : ["data_hot", "master"],
                     "node.attr.data" : "hot",
                     "node.attr.logical_availability_zone" : "zone-0"
                },
                "processors" : 8.0,
                "memory" : "58gb",
                "storage" : "2tb",
                "node_version" : "{version}"
            }
        ]
    }

API 返回以下结果：

    
    
    {
      "replaced_existing_history_id": false,
      "dry_run": false
    }

此外，还可以指定处理器范围。这在 Elasticsearch 节点可以部署在主机中的环境中非常有用，在这些主机中，Elasticsearch 进程可以使用的处理器数量保证至少为下限范围，最高可达上限范围。这是使用 cgroups 的 Linux 部署中的常见方案。

    
    
    PUT /_internal/desired_nodes/Ywkh3INLQcuPT49f6kcppA/101
    {
        "nodes" : [
            {
                "settings" : {
                     "node.name" : "instance-000187",
                     "node.external_id": "instance-000187",
                     "node.roles" : ["data_hot", "master"],
                     "node.attr.data" : "hot",
                     "node.attr.logical_availability_zone" : "zone-0"
                },
                "processors_range" : {"min": 8.0, "max": 10.0},
                "memory" : "58gb",
                "storage" : "2tb",
                "node_version" : "{version}"
            }
        ]
    }

[« Voting configuration exclusions API](voting-config-exclusions.md) [Get
desired nodes API »](get-desired-nodes.md)
