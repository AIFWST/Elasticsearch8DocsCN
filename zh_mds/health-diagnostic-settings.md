

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Field data cache settings](modules-fielddata.md) [Index lifecycle
management settings in Elasticsearch »](ilm-settings.md)

## 弹性搜索中的健康诊断设置

以下是可用于配置内部诊断服务的_expert level_设置。此服务的输出当前通过运行状况 API 运行状况 API 公开。不建议更改其中任何一个默认值。

### 群集级别设置

`health.master_history.has_master_lookup_timeframe`

     ([Static](settings.html#static-cluster-setting)) The amount of time a node looks back to see if it has observed a master at all, before moving on with other checks. Defaults to `30s` (30 seconds). 
`master_history.max_age`

     ([Static](settings.html#static-cluster-setting)) The timeframe we record the master history to be used for diagnosing the cluster health. Master node changes older than this time will not be considered when diagnosing the cluster health. Defaults to `30m` (30 minutes). 
`health.master_history.identity_changes_threshold`

     ([Static](settings.html#static-cluster-setting)) The number of master identity changes witnessed by a node that indicates the cluster is not healthy. Defaults to `4`. 
`health.master_history.no_master_transitions_threshold`

     ([Static](settings.html#static-cluster-setting)) The number of transitions to no master witnessed by a node that indicates the cluster is not healthy. Defaults to `4`. 
`health.node.enabled`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API")) Enables the health node, which allows the health API to provide indications about cluster wide health aspects such as disk space. 
`health.reporting.local.monitor.interval`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API")) Determines the interval in which each node of the cluster monitors aspects that comprise its local health such as its disk usage. 
`health.ilm.max_time_on_action`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API")) The minimum amount of time an index has to be in an index lifecycle management (ILM) action before it is considered stagnant. Defaults to `1d` (1 day). 
`health.ilm.max_time_on_step`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API")) The minimum amount of time an index has to be in an ILM step before it is considered stagnant. Defaults to `1d` (1 day). 
`health.ilm.max_retries_per_step`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API")) The minimum amount of times an index has retried by an ILM step before it is considered stagnant. Defaults to `100`

[« Field data cache settings](modules-fielddata.md) [Index lifecycle
management settings in Elasticsearch »](ilm-settings.md)
