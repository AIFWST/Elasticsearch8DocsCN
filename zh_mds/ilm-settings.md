

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Health diagnostic settings in Elasticsearch](health-diagnostic-
settings.md) [Index management settings »](index-management-settings.md)

## 弹性搜索中的索引生命周期管理设置

这些是可用于配置索引生命周期管理 (ILM) 的设置。

### 群集级别设置

`xpack.ilm.enabled`

     ([Static](settings.html#static-cluster-setting), Boolean)  [7.8.0]  Deprecated in 7.8.0. Basic License features are always enabled    
This deprecated setting has no effect and will be removed in Elasticsearch
8.0.

`indices.lifecycle.history_index_enabled`

     ([Dynamic](settings.html#dynamic-cluster-setting), Boolean) Whether ILM's history index is enabled. If enabled, ILM will record the history of actions taken as part of ILM policies to the `ilm-history-*` indices. Defaults to `true`. 

`indices.lifecycle.poll_interval`

     ([Dynamic](settings.html#dynamic-cluster-setting), [time unit value](api-conventions.html#time-units "Time units")) How often index lifecycle management checks for indices that meet policy criteria. Defaults to `10m`. 

`indices.lifecycle.rollover.only_if_has_documents`

     ([Dynamic](settings.html#dynamic-cluster-setting), Boolean) Whether ILM will only roll over non-empty indices. If enabled, ILM will only roll over indices as long as they contain at least one document. Defaults to `true`. 

### 索引级别设置

这些索引级 ILM 设置通常通过索引模板进行配置。具体操作，请参见创建生命周期策略。

`index.lifecycle.indexing_complete`

     ([Dynamic](indices-update-settings.html "Update index settings API"), Boolean) Indicates whether or not the index has been rolled over. Automatically set to `true` when ILM completes the rollover action. You can explicitly set it to [skip rollover](skipping-rollover.html "Skip rollover"). Defaults to `false`. 

`index.lifecycle.name`

     ([Dynamic](indices-update-settings.html "Update index settings API"), string) The name of the policy to use to manage the index. For information about how Elasticsearch applies policy changes, see [Policy updates](update-lifecycle-policy.html "Lifecycle policy updates"). If you are restoring an index from snapshot that was previously managed by index lifecycle management, you can override this setting to null during the restore operation to disable further management of the index. See also [Index level settings](ilm-settings.html#index-lifecycle-rollover-alias). 

`index.lifecycle.origination_date`

     ([Dynamic](indices-update-settings.html "Update index settings API"), long) If specified, this is the timestamp used to calculate the index age for its phase transitions. Use this setting if you create a new index that contains old data and want to use the original creation date to calculate the index age. Specified as a Unix epoch value in milliseconds. 

`index.lifecycle.parse_origination_date`

     ([Dynamic](indices-update-settings.html "Update index settings API"), Boolean) Set to `true` to parse the origination date from the index name. This origination date is used to calculate the index age for its phase transitions. The index name must match the pattern `^.*-{date_format}-\\d+`, where the `date_format` is `yyyy.MM.dd` and the trailing digits are optional. An index that was rolled over would normally match the full format, for example `logs-2016.10.31-000002`). If the index name doesn't match the pattern, index creation fails. 

`index.lifecycle.step.wait_time_threshold`

     ([Dynamic](indices-update-settings.html "Update index settings API"), [time value](api-conventions.html#time-units "Time units")) Time to wait for the cluster to resolve allocation issues during an ILM [`shrink`](ilm-shrink.html "Shrink") action. Must be greater than `1h` (1 hour). Defaults to `12h` (12 hours). See [Shard allocation for shrink](ilm-shrink.html#ilm-shrink-shard-allocation "Shard allocation for shrink"). 

`index.lifecycle.rollover_alias`

     ([Dynamic](indices-update-settings.html "Update index settings API"), string) The index alias to update when the index rolls over. Specify when using a policy that contains a rollover action. When the index rolls over, the alias is updated to reflect that the index is no longer the write index. For more information about rolling indices, see [Rollover](index-rollover.html "Rollover"). If you are restoring an index from snapshot that was previously managed by index lifecycle management, you can override this setting to null during the restore operation to disable further management of future indices. See also [Index level settings](ilm-settings.html#index-lifecycle-name). 

[« Health diagnostic settings in Elasticsearch](health-diagnostic-
settings.md) [Index management settings »](index-management-settings.md)
