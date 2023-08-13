

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Cross-cluster replication settings](ccr-settings.md) [Field data cache
settings »](modules-fielddata.md)

## 发现和集群形成设置

发现和群集形成受以下设置的影响：

`discovery.seed_hosts`

    

(静态)提供群集中符合主节点条件的地址列表。也可以是包含逗号分隔的地址的单个字符串。每个地址的格式为"host：port"或"host"。"主机"是要由 DNS 解析的主机名、IPv4 地址或 IPv6 地址。IPv6 地址必须括在方括号中。如果一个主机名通过DNS解析到多个地址，Elasticsearch会使用所有这些地址。DNS 查找受 JVM DNS 缓存的约束。如果未给出"端口"，则通过按顺序检查以下设置来确定：

1. "传输.配置文件.默认.端口" 2."运输港"

如果这两个都未设置，则默认端口为"9300"。"discovery.seed_hosts"的默认值为"127.0.0.1"、"[：：1]"]"。请参阅['discovery.seed_hosts'。

`discovery.seed_providers`

     ([Static](settings.html#static-cluster-setting)) Specifies which types of [seed hosts provider](discovery-hosts-providers.html#built-in-hosts-providers "Seed hosts providers") to use to obtain the addresses of the seed nodes used to start the discovery process. By default, it is the [settings-based seed hosts provider](discovery-hosts-providers.html#settings-based-hosts-provider "Settings-based seed hosts provider") which obtains the seed node addresses from the `discovery.seed_hosts` setting. 
`discovery.type`

     ([Static](settings.html#static-cluster-setting)) Specifies whether Elasticsearch should form a multiple-node cluster. Defaults to `multi-node`, which means that Elasticsearch discovers other nodes when forming a cluster and allows other nodes to join the cluster later. If set to `single-node`, Elasticsearch forms a single-node cluster and suppresses the timeout set by `cluster.publish.timeout`. For more information about when you might use this setting, see [Single-node discovery](bootstrap-checks.html#single-node-discovery "Single-node discovery"). 
`cluster.initial_master_nodes`

     ([Static](settings.html#static-cluster-setting)) Sets the initial set of master-eligible nodes in a brand-new cluster. By default this list is empty, meaning that this node expects to join a cluster that has already been bootstrapped. Remove this setting once the cluster has formed. Do not use this setting when restarting nodes or when adding new nodes to an existing cluster. See [`cluster.initial_master_nodes`](important-settings.html#initial_master_nodes "cluster.initial_master_nodes"). 

#### 专家设置

发现和群集形成也受以下 _expert level_设置的影响，但不建议更改其中任何默认值。

如果调整这些设置，则群集可能无法正确形成，或者可能变得不稳定或不能容忍某些故障。

`discovery.cluster_formation_warning_timeout`

     ([Static](settings.html#static-cluster-setting)) Sets how long a node will try to form a cluster before logging a warning that the cluster did not form. Defaults to `10s`. If a cluster has not formed after `discovery.cluster_formation_warning_timeout` has elapsed then the node will log a warning message that starts with the phrase `master not discovered` which describes the current state of the discovery process. 
`discovery.find_peers_interval`

     ([Static](settings.html#static-cluster-setting)) Sets how long a node will wait before attempting another discovery round. Defaults to `1s`. 
`discovery.probe.connect_timeout`

     ([Static](settings.html#static-cluster-setting)) Sets how long to wait when attempting to connect to each address. Defaults to `30s`. 
`discovery.probe.handshake_timeout`

     ([Static](settings.html#static-cluster-setting)) Sets how long to wait when attempting to identify the remote node via a handshake. Defaults to `30s`. 
`discovery.request_peers_timeout`

     ([Static](settings.html#static-cluster-setting)) Sets how long a node will wait after asking its peers again before considering the request to have failed. Defaults to `3s`. 
`discovery.find_peers_warning_timeout`

     ([Static](settings.html#static-cluster-setting)) Sets how long a node will attempt to discover its peers before it starts to log verbose messages describing why the connection attempts are failing. Defaults to `3m`. 
`discovery.seed_resolver.max_concurrent_resolvers`

     ([Static](settings.html#static-cluster-setting)) Specifies how many concurrent DNS lookups to perform when resolving the addresses of seed nodes. Defaults to `10`. 
`discovery.seed_resolver.timeout`

     ([Static](settings.html#static-cluster-setting)) Specifies how long to wait for each DNS lookup performed when resolving the addresses of seed nodes. Defaults to `5s`. 
`cluster.auto_shrink_voting_configuration`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Controls whether the [voting configuration](modules-discovery-voting.html "Voting configurations") sheds departed nodes automatically, as long as it still contains at least 3 nodes. The default value is `true`. If set to `false`, the voting configuration never shrinks automatically and you must remove departed nodes manually with the [voting configuration exclusions API](voting-config-exclusions.html "Voting configuration exclusions API"). 
`cluster.election.back_off_time`

     ([Static](settings.html#static-cluster-setting)) Sets the amount to increase the upper bound on the wait before an election on each election failure. Note that this is _linear_ backoff. This defaults to `100ms`. Changing this setting from the default may cause your cluster to fail to elect a master node. 
`cluster.election.duration`

     ([Static](settings.html#static-cluster-setting)) Sets how long each election is allowed to take before a node considers it to have failed and schedules a retry. This defaults to `500ms`. Changing this setting from the default may cause your cluster to fail to elect a master node. 
`cluster.election.initial_timeout`

     ([Static](settings.html#static-cluster-setting)) Sets the upper bound on how long a node will wait initially, or after the elected master fails, before attempting its first election. This defaults to `100ms`. Changing this setting from the default may cause your cluster to fail to elect a master node. 
`cluster.election.max_timeout`

     ([Static](settings.html#static-cluster-setting)) Sets the maximum upper bound on how long a node will wait before attempting an first election, so that an network partition that lasts for a long time does not result in excessively sparse elections. This defaults to `10s`. Changing this setting from the default may cause your cluster to fail to elect a master node. 
`cluster.fault_detection.follower_check.interval`

     ([Static](settings.html#static-cluster-setting)) Sets how long the elected master waits between follower checks to each other node in the cluster. Defaults to `1s`. Changing this setting from the default may cause your cluster to become unstable. 
`cluster.fault_detection.follower_check.timeout`

     ([Static](settings.html#static-cluster-setting)) Sets how long the elected master waits for a response to a follower check before considering it to have failed. Defaults to `10s`. Changing this setting from the default may cause your cluster to become unstable. 
`cluster.fault_detection.follower_check.retry_count`

     ([Static](settings.html#static-cluster-setting)) Sets how many consecutive follower check failures must occur to each node before the elected master considers that node to be faulty and removes it from the cluster. Defaults to `3`. Changing this setting from the default may cause your cluster to become unstable. 
`cluster.fault_detection.leader_check.interval`

     ([Static](settings.html#static-cluster-setting)) Sets how long each node waits between checks of the elected master. Defaults to `1s`. Changing this setting from the default may cause your cluster to become unstable. 
`cluster.fault_detection.leader_check.timeout`

     ([Static](settings.html#static-cluster-setting)) Sets how long each node waits for a response to a leader check from the elected master before considering it to have failed. Defaults to `10s`. Changing this setting from the default may cause your cluster to become unstable. 
`cluster.fault_detection.leader_check.retry_count`

     ([Static](settings.html#static-cluster-setting)) Sets how many consecutive leader check failures must occur before a node considers the elected master to be faulty and attempts to find or elect a new master. Defaults to `3`. Changing this setting from the default may cause your cluster to become unstable. 
`cluster.follower_lag.timeout`

     ([Static](settings.html#static-cluster-setting)) Sets how long the master node waits to receive acknowledgements for cluster state updates from lagging nodes. The default value is `90s`. If a node does not successfully apply the cluster state update within this period of time, it is considered to have failed and is removed from the cluster. See [Publishing the cluster state](cluster-state-publishing.html "Publishing the cluster state"). 
`cluster.max_voting_config_exclusions`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Sets a limit on the number of voting configuration exclusions at any one time. The default value is `10`. See [_Add and remove nodes in your cluster_](add-elasticsearch-nodes.html "Add and remove nodes in your cluster"). 
`cluster.publish.info_timeout`

     ([Static](settings.html#static-cluster-setting)) Sets how long the master node waits for each cluster state update to be completely published to all nodes before logging a message indicating that some nodes are responding slowly. The default value is `10s`. 
`cluster.publish.timeout`

     ([Static](settings.html#static-cluster-setting)) Sets how long the master node waits for each cluster state update to be completely published to all nodes, unless `discovery.type` is set to `single-node`. The default value is `30s`. See [Publishing the cluster state](cluster-state-publishing.html "Publishing the cluster state"). 
`cluster.discovery_configuration_check.interval`

     ([Static](settings.html#static-cluster-setting)) Sets the interval of some checks that will log warnings about an incorrect discovery configuration. The default value is `30s`. 
`cluster.join_validation.cache_timeout`

     ([Static](settings.html#static-cluster-setting)) When a node requests to join the cluster, the elected master node sends it a copy of a recent cluster state to detect certain problems which might prevent the new node from joining the cluster. The master caches the state it sends and uses the cached state if another node joins the cluster soon after. This setting controls how long the master waits until it clears this cache. Defaults to `60s`. 

`cluster.no_master_block`

    

(动态)指定当集群中没有活动主服务器时拒绝哪些操作。此设置有三个有效值：

`all`

     All operations on the node (both read and write operations) are rejected. This also applies for API cluster state read or write operations, like the get index settings, update mapping, and cluster state API. 
`write`

     (default) Write operations are rejected. Read operations succeed, based on the last known cluster configuration. This situation may result in partial reads of stale data as this node may be isolated from the rest of the cluster. 
`metadata_write`

     Only metadata write operations (e.g. mapping updates, routing table changes) are rejected but regular indexing operations continue to work. Read and write operations succeed, based on the last known cluster configuration. This situation may result in partial reads of stale data as this node may be isolated from the rest of the cluster. 

* "cluster.no_master_block"设置不适用于基于节点的 API(例如，集群统计信息、节点信息和节点统计信息 API)。对这些 API 的请求不会被阻止，并且可以在任何可用节点上运行。  * 要使集群完全正常运行，它必须具有活动主服务器。

`monitor.fs.health.enabled`

     ([Dynamic](settings.html#dynamic-cluster-setting)) If `true`, the node runs periodic [filesystem health checks](cluster-fault-detection.html#cluster-fault-detection-filesystem-health). Defaults to `true`. 
`monitor.fs.health.refresh_interval`

     ([Static](settings.html#static-cluster-setting)) Interval between successive [filesystem health checks](cluster-fault-detection.html#cluster-fault-detection-filesystem-health). Defaults to `2m`. 
`monitor.fs.health.slow_path_logging_threshold`

     ([Dynamic](settings.html#dynamic-cluster-setting)) If a [filesystem health checks](cluster-fault-detection.html#cluster-fault-detection-filesystem-health) takes longer than this threshold then Elasticsearch logs a warning. Defaults to `5s`. 

[« Cross-cluster replication settings](ccr-settings.md) [Field data cache
settings »](modules-fielddata.md)
