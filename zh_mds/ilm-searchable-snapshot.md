

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md) ›[Index lifecycle actions](ilm-actions.md)

[« Downsample](ilm-downsample.md) [Set priority »](ilm-set-priority.md)

## 可搜索快照

允许的阶段：热，冷，冷冻。

在配置的存储库中拍摄托管索引的快照，并将其装载为可搜索的快照。如果索引是数据流的一部分，则挂载的索引将替换流中的原始索引。

"searchable_snapshot"操作需要数据层。该操作使用"index.routing.allocation.include._tier_preference"设置将索引直接装载到阶段的相应数据层。在冻结阶段，该操作将前缀为"部分-"的部分挂载的索引挂载到冻结层。在其他阶段，该操作将一个以"还原-"为前缀的完全挂载的索引挂载到相应的数据层。

在冻结层中，操作将忽略设置"index.routing.allocation.total_shards_per_node"(如果它存在于原始索引中)，以说明冻结层和其他层之间的节点数差异。

不要在热相和冷相中都包含"searchable_snapshot"操作。这可能会导致索引无法在冷阶段自动迁移到冷层。

如果在热阶段使用"searchable_snapshot"操作，则后续阶段不能包含"收缩"或"强制合并"操作。

无法对数据流的写入索引执行此操作。尝试这样做将失败。要将索引转换为可搜索快照，请先手动滚动数据流。这将创建一个新的写入索引。由于索引不再是流的写入索引，因此操作随后可以将其转换为可搜索的快照。使用在热阶段使用滚动更新操作的策略将避免这种情况，并且需要对将来的托管索引进行手动滚动更新。

挂载和重新定位可搜索快照索引的分片涉及从快照存储库复制分片内容。这可能会产生与常规索引在节点之间复制不同的成本。这些成本通常较低，但在某些环境中可能更高。有关更多详细信息，请参阅使用可搜索快照降低成本。

默认情况下，此快照由删除阶段的删除操作删除。要保留快照，请在删除操作中将"delete_searchable_snapshot"设置为"false"。此快照保留在索引生命周期管理 (ILM) 策略之外运行，不受快照生命周期管理 (SLM) 策略的影响。

###Options

`snapshot_repository`

     (Required, string) [Repository](snapshots-register-repository.html "Register a snapshot repository") used to store the snapshot. 
`force_merge_index`

     (Optional, Boolean) Force merges the managed index to one segment. Defaults to `true`. If the managed index was already force merged using the [force merge action](ilm-forcemerge.html "Force merge") in a previous action the `searchable snapshot` action force merge step will be a no-op. 

"强制合并"操作是尽力而为。可能会发生某些分片正在重新定位的情况，在这种情况下，它们将不会合并。"searchable_snapshot"操作将继续执行，即使并非所有分片都强制合并。

此强制合并发生在索引处于"searchable_snapshot"操作的**先于**的阶段。例如，如果在"热"阶段使用"searchable_snapshot"操作，则将在热节点上执行强制合并。如果在"冷"阶段使用"searchable_snapshot"操作，则强制合并将在索引"冷"阶段("热"或"暖")之前的任何层执行。

###Examples

    
    
    PUT _ilm/policy/my_policy
    {
      "policy": {
        "phases": {
          "cold": {
            "actions": {
              "searchable_snapshot" : {
                "snapshot_repository" : "backing_repo"
              }
            }
          }
        }
      }
    }

[« Downsample](ilm-downsample.md) [Set priority »](ilm-set-priority.md)
