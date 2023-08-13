

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cluster APIs](cluster.md)

[« Health API](health-api.md) [Cluster state API »](cluster-state.md)

## 集群重新路由API

更改集群中分片的分配。

###Request

"POST /_cluster/reroute？metric=none"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。

###Description

reroute 命令允许手动更改集群中单个分片的分配。例如，可以将分片从一个节点显式移动到另一个节点，可以取消分配，并且可以将未分配的分片显式分配给特定节点。

需要注意的是，在处理任何重新路由命令后，Elasticsearch 将正常执行重新平衡(遵循诸如"cluster.routeting.rebalance.enable"之类的设置的值)，以保持不平衡状态。例如，如果请求的分配包括将分片从"node1"移动到"node2"，那么这可能会导致分片从"node2"移回"node1"以平衡事情。

可以使用"cluster.routing.allocation.enable"设置将群集设置为禁用分配。如果分配被禁用，那么将执行的唯一分配是使用"reroute"命令给出的显式分配，以及由于重新平衡而引起的后续分配。

可以使用"？dry_run"URI 查询参数或在请求正文中传递"dry_run"：true，在"试运行"模式下运行"重新路由"命令。这将计算将命令应用于当前群集状态的结果，并在应用命令(andre-balancing)后返回生成的群集状态，但实际上不会执行请求的更改。

如果包含"？explain"URI 查询参数，则响应中包含有关命令可以或无法执行的原因的详细说明。

集群将尝试连续最多分配"index.allocation.max_retries"次数(默认为"5")，然后放弃并保留未分配的分片。这种情况可能是由结构问题引起的，例如分析器引用并非在所有节点上都存在的非索引字文件。

纠正问题后，可以通过使用"？retry_failed"URI 查询参数调用"重新路由"API 来手动重试分配，该参数将尝试对这些分片进行一次重试。

### 查询参数

`dry_run`

     (Optional, Boolean) If `true`, then the request simulates the operation only and returns the resulting state. 
`explain`

     (Optional, Boolean) If `true`, then the response contains an explanation of why the commands can or cannot be executed. 
`metric`

    

(可选，字符串)将返回的信息限制为指定的指标。除"none"之外的所有选项均已弃用，应避免使用此参数。默认为除元数据之外的所有内容。以下选项可用：

"公制"选项

`_all`

     Shows all metrics. 
`blocks`

     Shows the `blocks` part of the response. 
`master_node`

     Shows the elected `master_node` part of the response. 
`metadata`

     Shows the `metadata` part of the response. If you supply a comma separated list of indices, the returned output will only contain metadata for these indices. 
`nodes`

     Shows the `nodes` part of the response. 
`none`

     Excludes the entire `state` field from the response. 
`routing_table`

     Shows the `routing_table` part of the response. 
`version`

     Shows the cluster state version. 

`retry_failed`

     (Optional, Boolean) If `true`, then retries allocation of shards that are blocked due to too many subsequent allocation failures. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 请求正文

`commands`

    

(必需，对象数组)定义要执行的命令。支持的命令包括：

"命令"的属性

`move`

     Move a started shard from one node to another node. Accepts `index` and `shard` for index name and shard number, `from_node` for the node to move the shard from, and `to_node` for the node to move the shard to. 
`cancel`

     Cancel allocation of a shard (or recovery). Accepts `index` and `shard` for index name and shard number, and `node` for the node to cancel the shard allocation on. This can be used to force resynchronization of existing replicas from the primary shard by cancelling them and allowing them to be reinitialized through the standard recovery process. By default only replica shard allocations can be cancelled. If it is necessary to cancel the allocation of a primary shard then the `allow_primary` flag must also be included in the request. 
`allocate_replica`

     Allocate an unassigned replica shard to a node. Accepts `index` and `shard` for index name and shard number, and `node` to allocate the shard to. Takes [allocation deciders](modules-cluster.html "Cluster-level shard allocation and routing settings") into account. 

还有两个命令可用，允许将主分片分配给节点。但是，使用这些命令时应格外小心，因为主分片分配通常由 Elasticsearch 完全自动处理。无法自动分配主分片的原因包括：

* 已创建一个新索引，但没有满足分配决策程序的节点。  * 在集群中的当前数据节点上找不到数据的最新分片副本。为防止数据丢失，系统不会自动将过时的分片副本提升为主副本。

以下两个命令很危险，可能会导致数据丢失。它们旨在用于无法恢复原始数据且群集管理员接受丢失的情况。如果您遇到了可以修复的临时问题，请参阅上述"retry_failed"标志。强调：如果执行了这些命令，然后节点加入了包含受影响分片副本的集群，则新加入的节点上的副本将被删除或覆盖。

`allocate_stale_primary`

     Allocate a primary shard to a node that holds a stale copy. Accepts the `index` and `shard` for index name and shard number, and `node` to allocate the shard to. Using this command may lead to data loss for the provided shard id. If a node which has the good copy of the data rejoins the cluster later on, that data will be deleted or overwritten with the data of the stale copy that was forcefully allocated with this command. To ensure that these implications are well-understood, this command requires the flag `accept_data_loss` to be explicitly set to `true`. 
`allocate_empty_primary`

     Allocate an empty primary shard to a node. Accepts the `index` and `shard` for index name and shard number, and `node` to allocate the shard to. Using this command leads to a complete loss of all data that was indexed into this shard, if it was previously started. If a node which has a copy of the data rejoins the cluster later on, that data will be deleted. To ensure that these implications are well-understood, this command requires the flag `accept_data_loss` to be explicitly set to `true`. 

###Examples

这是简单重新路由 API 调用的简短示例：

    
    
    POST /_cluster/reroute?metric=none
    {
      "commands": [
        {
          "move": {
            "index": "test", "shard": 0,
            "from_node": "node1", "to_node": "node2"
          }
        },
        {
          "allocate_replica": {
            "index": "test", "shard": 1,
            "node": "node3"
          }
        }
      ]
    }

[« Health API](health-api.md) [Cluster state API »](cluster-state.md)
