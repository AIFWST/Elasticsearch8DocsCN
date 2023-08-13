

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md) ›[Index lifecycle actions](ilm-actions.md)

[« Shrink](ilm-shrink.md) [Wait for snapshot »](ilm-wait-for-snapshot.md)

##Unfollow

允许的阶段：热，温，冷，冷冻。

将 CCR 追随者索引转换为常规索引。这使得收缩、滚动更新和可搜索快照操作能够在追随者索引上安全地执行。在生命周期中移动关注者索引时，您也可以直接使用取消关注。对不是追随者的索引没有影响，阶段执行只是移动到下一个操作。

此操作在应用于关注者索引时由滚动更新、收缩和可搜索快照操作自动触发。

此操作会等到可以将关注者索引转换为常规索引安全为止。必须满足以下条件：

* 领导者索引必须将"index.lifecycle.indexing_complete"设置为"true"。如果使用滚动更新操作滚动更新领导者索引，则会自动发生这种情况，并且可以使用索引设置 API 手动设置。  * 对领导者索引执行的所有操作都已复制到从属索引。这可确保在转换索引时不会丢失任何操作。

满足这些条件后，取消关注将执行以下操作：

* 暂停关注追随者索引的索引。  * 关闭关注者索引。  * 取消关注领导者索引。  * 打开追随者索引(此时是常规索引)。

###Options

None.

###Example

    
    
    response = client.ilm.put_lifecycle(
      policy: 'my_policy',
      body: {
        policy: {
          phases: {
            hot: {
              actions: {
                unfollow: {}
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
          "hot": {
            "actions": {
              "unfollow" : {}
            }
          }
        }
      }
    }

[« Shrink](ilm-shrink.md) [Wait for snapshot »](ilm-wait-for-snapshot.md)
