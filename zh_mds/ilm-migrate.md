

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md) ›[Index lifecycle actions](ilm-actions.md)

[« Force merge](ilm-forcemerge.md) [Read only »](ilm-readonly.md)

##Migrate

允许的阶段：暖，冷。

通过更新"index.routing.allocation.include._tier_preference"索引设置，将索引移动到与当前阶段对应的数据层。ILM 在暖阶段和冷阶段自动注入迁移操作。若要防止自动迁移，可以显式包含迁移操作并将"启用"选项设置为"false"。

如果"冷"阶段定义了可搜索的快照操作，则"迁移"操作不会在"冷"阶段自动注入，因为托管索引将使用"迁移"操作配置的相同_tier_preference基础结构直接装载到目标层上。

在暖阶段，"迁移"操作将"index.routing.allocation.include._tier_preference"设置为"data_warm，data_hot"。这会将索引移动到暖层中的节点。如果暖层中没有节点，它将回退到热层。

在冷阶段，"迁移"操作将"index.routing.allocation.include._tier_preference"设置为"data_cold，data_warm，data_hot"。这会将索引移动到更冷的节点。如果冷层中没有节点，则会回退到暖层，如果没有可用的暖节点，则会回退到热层。

在冻结阶段不允许迁移操作。冻结阶段使用"data_frozen"的"index.routing.allocation.include._tier_preference"直接装载可搜索快照。这会将索引移动到冻结层中的节点。

在热阶段不允许迁移操作。初始索引分配是自动执行的，可以手动配置，也可以通过索引模板进行配置。

###Options

`enabled`

     (Optional, Boolean) Controls whether ILM automatically migrates the index during this phase. Defaults to `true`. 

###Example

在以下策略中，指定分配操作是为了在 ILM 将索引迁移到温节点之前减少副本数。

不需要显式指定迁移操作 -- ILM 会自动执行迁移操作，除非您禁用迁移。

    
    
    response = client.ilm.put_lifecycle(
      policy: 'my_policy',
      body: {
        policy: {
          phases: {
            warm: {
              actions: {
                migrate: {},
                allocate: {
                  number_of_replicas: 1
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
              "migrate" : {
              },
              "allocate": {
                "number_of_replicas": 1
              }
            }
          }
        }
      }
    }

### 禁用自动迁移

以下策略中的迁移操作将被禁用，分配操作将索引分配给"rack_id"为 _1_ 或 _two_ 的节点。

    
    
    response = client.ilm.put_lifecycle(
      policy: 'my_policy',
      body: {
        policy: {
          phases: {
            warm: {
              actions: {
                migrate: {
                  enabled: false
                },
                allocate: {
                  include: {
                    rack_id: 'one,two'
                  }
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
              "migrate" : {
               "enabled": false
              },
              "allocate": {
                "include" : {
                  "rack_id": "one,two"
                }
              }
            }
          }
        }
      }
    }

[« Force merge](ilm-forcemerge.md) [Read only »](ilm-readonly.md)
