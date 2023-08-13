

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Miscellaneous cluster settings](misc-cluster-settings.md) [Discovery and
cluster formation settings »](modules-discovery-settings.md)

## 跨集群复制设置

可以使用群集更新设置 API 在实时群集上动态更新这些跨群集复制设置。

#### 远程恢复设置

以下设置可用于对远程恢复期间传输的数据进行速率限制：

'ccr.indices.recovery.max_bytes_per_sec' (动态)

     Limits the total inbound and outbound remote recovery traffic on each node. Since this limit applies on each node, but there may be many nodes performing remote recoveries concurrently, the total amount of remote recovery bytes may be much higher than this limit. If you set this limit too high then there is a risk that ongoing remote recoveries will consume an excess of bandwidth (or other resources) which could destabilize the cluster. This setting is used by both the leader and follower clusters. For example if it is set to `20mb` on a leader, the leader will only send `20mb/s` to the follower even if the follower is requesting and can accept `60mb/s`. Defaults to `40mb`. 

#### 高级远程恢复设置

可以设置以下 _expert_ 设置来管理远程恢复消耗的资源：

'ccr.indices.recovery.max_concurrent_file_chunks' (Dynamic)

     Controls the number of file chunk requests that can be sent in parallel per recovery. As multiple remote recoveries might already running in parallel, increasing this expert-level setting might only help in situations where remote recovery of a single shard is not reaching the total inbound and outbound remote recovery traffic as configured by `ccr.indices.recovery.max_bytes_per_sec`. Defaults to `5`. The maximum allowed value is `10`. 
`ccr.indices.recovery.chunk_size`([Dynamic](cluster-update-settings.html
"Cluster update settings API"))

     Controls the chunk size requested by the follower during file transfer. Defaults to `1mb`. 
`ccr.indices.recovery.recovery_activity_timeout`([Dynamic](cluster-update-
settings.html "Cluster update settings API"))

     Controls the timeout for recovery activity. This timeout primarily applies on the leader cluster. The leader cluster must open resources in-memory to supply data to the follower during the recovery process. If the leader does not receive recovery requests from the follower for this period of time, it will close the resources. Defaults to 60 seconds. 
`ccr.indices.recovery.internal_action_timeout` ([Dynamic](cluster-update-
settings.html "Cluster update settings API"))

     Controls the timeout for individual network requests during the remote recovery process. An individual action timing out can fail the recovery. Defaults to 60 seconds. 

[« Miscellaneous cluster settings](misc-cluster-settings.md) [Discovery and
cluster formation settings »](modules-discovery-settings.md)
