

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cluster APIs](cluster.md)

[« Task management API](tasks.md) [Create or update desired nodes API
»](update-desired-nodes.md)

## 投票配置排除项API

在投票配置排除列表中添加或删除符合主节点条件的节点。

###Request

'POST /_cluster/voting_config_exclusions？node_names=<node_names>'

'POST /_cluster/voting_config_exclusions？node_ids=<node_ids>'

"删除/_cluster/voting_config_exclusions"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。  * 如果启用了操作员权限功能，则只有操作员用户才能使用此 API。

###Description

默认情况下，如果群集中有三个以上的主节点，并且您一次删除了集群中符合主节点条件的节点的一半以上，则投票配置会自动收缩。

如果要收缩投票配置以包含少于三个节点，或者一次性删除集群中一半或更多符合主节点条件的节点，请使用此 API 手动从投票配置中删除离开节点。API 将每个指定节点的条目添加到群集的投票配置排除列表中。然后，它会等待，直到群集重新配置其投票配置以排除指定的节点。

在正常操作中，群集不应具有投票配置排除项。排除的节点停止后，使用"DELETE /_cluster/voting_config_exclusions"清除投票配置排除项。此 API 等待节点从群集中完全删除，然后再返回。如果您的集群对您不再打算删除的节点具有投票配置排除项，请使用"DELETE/_cluster/voting_config_exclusions？wait_for_removal=false"清除投票配置排除项，而无需等待节点离开集群。

如果 API 失败，您可以安全地重试它。只有成功的响应才能保证节点已从投票配置中删除，并且不会恢复。

仅当您在短时间内从集群中删除至少一半的符合主节点条件的节点时，才需要投票排除。删除不符合主节点条件的节点或少于一半符合主节点条件的节点时，不需要它们。

有关更多信息，请参阅 删除符合主节点条件的节点。

### 查询参数

`node_names`

     A comma-separated list of the names of the nodes to exclude from the voting configuration. If specified, you may not also specify `?node_ids`. Only applies to the `POST` form of this API. 
`node_ids`

     A comma-separated list of the persistent ids of the nodes to exclude from the voting configuration. If specified, you may not also specify `?node_names`. Only applies to the `POST` form of this API. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) When adding a voting configuration exclusion, the API waits for the specified nodes to be excluded from the voting configuration before returning. The period of time to wait is specified by the `?timeout` query parameter. If the timeout expires before the appropriate condition is satisfied, the request fails and returns an error. Defaults to `30s`. Only applies to the `POST` form of this API. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Defines how long to wait while trying to route the request to the current master node in the cluster. Defaults to `30s`. Applies to both `POST` and `DELETE` forms of this API. 
`wait_for_removal`

     (Optional, Boolean) Specifies whether to wait for all excluded nodes to be removed from the cluster before clearing the voting configuration exclusions list. Defaults to `true`, meaning that all excluded nodes must be removed from the cluster before this API takes any action. If set to `false` then the voting configuration exclusions list is cleared even if some excluded nodes are still in the cluster. Only applies to the `DELETE` form of this API. 

###Examples

将名为"nodeName1"和"nodeName2"的节点添加到投票配置排除列表中：

    
    
    POST /_cluster/voting_config_exclusions?node_names=nodeName1,nodeName2

从列表中删除所有排除项：

    
    
    DELETE /_cluster/voting_config_exclusions

[« Task management API](tasks.md) [Create or update desired nodes API
»](update-desired-nodes.md)
