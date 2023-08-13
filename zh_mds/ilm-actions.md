

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md)

[« Lifecycle policy updates](update-lifecycle-policy.md) [Allocate »](ilm-
allocate.md)

## 索引生命周期操作

分配

     Move shards to nodes with different performance characteristics and reduce the number of replicas. 
[Delete](ilm-delete.html "Delete")

     Permanently remove the index. 
[Force merge](ilm-forcemerge.html "Force merge")

     Reduce the number of index segments and purge deleted documents. 
[Migrate](ilm-migrate.html "Migrate")

     Move the index shards to the [data tier](data-tiers.html "Data tiers") that corresponds to the current ILM phase. 
[Read only](ilm-readonly.html "Read only")

     Block write operations to the index. 
[Rollover](ilm-rollover.html "Rollover")

     Remove the index as the write index for the rollover alias and start indexing to a new index. 
[Downsample](ilm-downsample.html "Downsample")

     Aggregates an index's time series data and stores the results in a new read-only index. For example, you can downsample hourly data into daily or weekly summaries. 
[Searchable snapshot](ilm-searchable-snapshot.html "Searchable snapshot")

     Take a snapshot of the managed index in the configured repository and mount it as a searchable snapshot. 
[Set priority](ilm-set-priority.html "Set priority")

     Lower the priority of an index as it moves through the lifecycle to ensure that hot indices are recovered first. 
[Shrink](ilm-shrink.html "Shrink")

     Reduce the number of primary shards by shrinking the index into a new index. 
[Unfollow](ilm-unfollow.html "Unfollow")

     Convert a follower index to a regular index. Performed automatically before a rollover, shrink, or searchable snapshot action. 
[Wait for snapshot](ilm-wait-for-snapshot.html "Wait for snapshot")

     Ensure that a snapshot exists before deleting the index. 

[« Lifecycle policy updates](update-lifecycle-policy.md) [Allocate »](ilm-
allocate.md)
