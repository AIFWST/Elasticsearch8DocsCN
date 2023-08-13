

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md) ›[Index lifecycle actions](ilm-actions.md)

[« Migrate](ilm-migrate.md) [Rollover »](ilm-rollover.md)

## 只读

允许的阶段：热，暖，冷。

使索引数据只读;禁用针对索引的数据写入操作。

要在"热"阶段使用"只读"操作，必须存在"翻转"操作。如果未配置滚动更新操作，ILM 将拒绝该策略。

###Options

None.

###Example

    
    
    response = client.ilm.put_lifecycle(
      policy: 'my_policy',
      body: {
        policy: {
          phases: {
            warm: {
              actions: {
                readonly: {}
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
              "readonly" : { }
            }
          }
        }
      }
    }

[« Migrate](ilm-migrate.md) [Rollover »](ilm-rollover.md)
