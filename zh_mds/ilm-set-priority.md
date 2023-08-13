

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md) ›[Index lifecycle actions](ilm-actions.md)

[« Searchable snapshot](ilm-searchable-snapshot.md) [Shrink »](ilm-
shrink.md)

## 设置优先级

允许的阶段：热，暖，冷。

在策略进入热、暖或冷阶段后立即设置索引的优先级。在节点重新启动后，优先级较高的索引先于优先级较低的索引恢复。

通常，热相中的索引应具有最高值，冷相中的索引应具有最低值。例如：100 表示热相，50 表示暖相，0 表示冷相。未设置此值的索引的默认优先级为 1。

###Options

`priority`

     (Required, integer) The priority for the index. Must be 0 or greater. Set to `null` to remove the priority. 

###Example

    
    
    response = client.ilm.put_lifecycle(
      policy: 'my_policy',
      body: {
        policy: {
          phases: {
            warm: {
              actions: {
                set_priority: {
                  priority: 50
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
              "set_priority" : {
                "priority": 50
              }
            }
          }
        }
      }
    }

[« Searchable snapshot](ilm-searchable-snapshot.md) [Shrink »](ilm-
shrink.md)
