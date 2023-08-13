

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md) ›[Index lifecycle actions](ilm-actions.md)

[« Set priority](ilm-set-priority.md) [Unfollow »](ilm-unfollow.md)

##Shrink

允许的阶段：热，暖。

将源索引设置为只读，并将其收缩为主分片较少的新索引。生成的索引的名称是"shrink-<random-uuid>-<original-index-name>"。此操作对应于收缩 API。

在"收缩"操作之后，指向源索引的任何别名都指向新的收缩索引。如果 ILM 对数据流的支持索引执行"收缩"操作，则收缩的索引将替换流中的源索引。不能对写入索引执行"收缩"操作。

要在"热"阶段使用"收缩"操作，必须存在"翻转"操作。如果未配置滚动更新操作，ILM 将拒绝该策略。

收缩操作将取消设置索引sindex.routing.allocation.total_shards_per_node设置，这意味着没有限制。这是为了确保索引的所有分片都可以复制到单个节点。即使在步骤完成后，此设置更改仍将保留在索引上。

如果对追随者索引使用收缩操作，则策略执行将等待，直到领导者索引滚动更新(否则标记为完成)，然后在执行收缩操作之前，将追随者索引转换为具有取消关注操作的常规索引。

### 收缩选项

`number_of_shards`

     (Optional, integer) Number of shards to shrink to. Must be a factor of the number of shards in the source index. This parameter conflicts with `max_primary_shard_size`, only one of them may be set. 
`max_primary_shard_size`

     (Optional, [byte units](api-conventions.html#byte-units "Byte size units")) The max primary shard size for the target index. Used to find the optimum number of shards for the target index. When this parameter is set, each shard's storage in the target index will not be greater than the parameter. The shards count of the target index will still be a factor of the source index's shards count, but if the parameter is less than the single shard size in the source index, the shards count for the target index will be equal to the source index's shards count. For example, when this parameter is set to 50gb, if the source index has 60 primary shards with totaling 100gb, then the target index will have 2 primary shards, with each shard size of 50gb; if the source index has 60 primary shards with totaling 1000gb, then the target index will have 20 primary shards; if the source index has 60 primary shards with totaling 4000gb, then the target index will still have 60 primary shards. This parameter conflicts with `number_of_shards` in the `settings`, only one of them may be set. 

###Example

#### 显式设置新收缩索引的分片数

    
    
    response = client.ilm.put_lifecycle(
      policy: 'my_policy',
      body: {
        policy: {
          phases: {
            warm: {
              actions: {
                shrink: {
                  number_of_shards: 1
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT _ilm/policy/my_policy
    {
      "policy": {
        "phases": {
          "warm": {
            "actions": {
              "shrink" : {
                "number_of_shards": 1
              }
            }
          }
        }
      }
    }

#### 计算收缩索引的最佳主分片数

以下策略使用"max_primary_shard_size"参数根据源索引的存储大小自动计算新缩减索引的主分片计数。

    
    
    response = client.ilm.put_lifecycle(
      policy: 'my_policy',
      body: {
        policy: {
          phases: {
            warm: {
              actions: {
                shrink: {
                  max_primary_shard_size: '50gb'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT _ilm/policy/my_policy
    {
      "policy": {
        "phases": {
          "warm": {
            "actions": {
              "shrink" : {
                "max_primary_shard_size": "50gb"
              }
            }
          }
        }
      }
    }

### 分片分配收缩

在"收缩"操作期间，ILM 将源索引的主分片分配给一个节点。收缩索引后，ILM 会根据您的分配规则将缩减的索引的分片重新分配到相应的节点。

这些分配步骤可能由于多种原因而失败，包括：

* 在"收缩"操作期间删除节点。  * 没有节点有足够的磁盘空间来托管源索引的分片。  * 由于分配规则冲突，Elasticsearch 无法重新分配收缩的索引。

当其中一个分配步骤失败时，ILM 将等待在"index.lifecycle.step.wait_time_threshold"中设置的时间段，该时间段默认为 12 小时。此阈值期限允许群集解决导致分配失败的任何问题。

如果阈值周期已过，并且 ILM 尚未收缩索引，则 ILM 会尝试将源索引的主分片分配给另一个节点。如果 ILM 收缩了索引，但在阈值期间无法重新分配收缩索引的分片，则 ILM 将删除收缩的索引并重新尝试整个"收缩"操作。

[« Set priority](ilm-set-priority.md) [Unfollow »](ilm-unfollow.md)
