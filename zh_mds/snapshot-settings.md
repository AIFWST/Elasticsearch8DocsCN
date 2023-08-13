

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Shard request cache settings](shard-request-cache.md) [Transforms
settings in Elasticsearch »](transform-settings.md)

## 快照和还原设置

以下群集设置配置快照和还原。

`snapshot.max_concurrent_operations`

    

(动态，整数)最大并发快照操作数。默认为"1000"。

此限制总共适用于所有正在进行的快照创建、克隆和删除操作。Elasticsearch 将拒绝任何超过此限制的操作。

### SLM设置

以下群集设置配置快照生命周期管理 (SLM)。

`slm.history_index_enabled`

     ([Dynamic](settings.html#dynamic-cluster-setting), Boolean) Controls whether SLM records the history of actions taken as part of SLM policies to the `slm-history-*` indices. Defaults to `true`. 

`slm.retention_schedule`

     ([Dynamic](settings.html#dynamic-cluster-setting), [cron scheduler value](trigger-schedule.html#schedule-cron "Watcher cron schedule")) Controls when the [retention task](snapshots-take-snapshot.html#slm-retention-task "SLM retention") runs. Can be a periodic or absolute time schedule. Supports all values supported by the [cron scheduler](trigger-schedule.html#schedule-cron "Watcher cron schedule"). Defaults to daily at 1:30am UTC: `0 30 1 * * ?`. 

`slm.retention_duration`

     ([Dynamic](settings.html#dynamic-cluster-setting), [time value](api-conventions.html#time-units "Time units")) Limits how long SLM should spend deleting old snapshots. Defaults to one hour: `1h`. 

`slm.health.failed_snapshot_warn_threshold`

     ([Dynamic](settings.html#dynamic-cluster-setting), Long) The number of failed invocations since last successful snapshot that indicate a problem with the policy in the health api. Defaults to a health api warning after five repeated failures: `5L`. 

"repositories.url.allowed_urls"！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

     ([Static](settings.html#static-cluster-setting)) Specifies the [read-only URL repositories](snapshots-read-only-repository.html "Read-only URL repository") that snapshots can be restored from. 

[« Shard request cache settings](shard-request-cache.md) [Transforms
settings in Elasticsearch »](transform-settings.md)
