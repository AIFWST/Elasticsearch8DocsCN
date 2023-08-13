

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md)

[« Migrate index allocation filters to node roles](migrate-index-allocation-
filters.md) [Start and stop index lifecycle management »](start-stop-
ilm.md)

## 排查索引生命周期管理错误

当 ILM 执行生命周期策略时，在为步骤执行必要的索引操作时可能会发生错误。发生这种情况时，ILM 会将索引移动到"错误"步骤。如果 ILM 无法自动解决错误，则执行将暂停，直到您解决策略、索引或群集的根本问题。

例如，您可能有一个"收缩索引"策略，该策略在索引至少存在五天后将其收缩为四个分片：

    
    
    response = client.ilm.put_lifecycle(
      policy: 'shrink-index',
      body: {
        policy: {
          phases: {
            warm: {
              min_age: '5d',
              actions: {
                shrink: {
                  number_of_shards: 4
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT _ilm/policy/shrink-index
    {
      "policy": {
        "phases": {
          "warm": {
            "min_age": "5d",
            "actions": {
              "shrink": {
                "number_of_shards": 4
              }
            }
          }
        }
      }
    }

没有什么可以阻止您将"收缩索引"策略应用于只有两个分片的新索引：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          "index.number_of_shards": 2,
          "index.lifecycle.name": 'shrink-index'
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001
    {
      "settings": {
        "index.number_of_shards": 2,
        "index.lifecycle.name": "shrink-index"
      }
    }

五天后，ILM 尝试将"my-index-000001"从两个分片缩减为四个分片。由于收缩操作无法_增加_分片数，因此此操作将失败，ILM 会将"my-index-000001"移动到"错误"步骤。

您可以使用 ILM 解释 API 获取有关出错情况的信息：

    
    
    response = client.ilm.explain_lifecycle(
      index: 'my-index-000001'
    )
    puts response
    
    
    GET /my-index-000001/_ilm/explain

返回以下信息：

    
    
    {
      "indices" : {
        "my-index-000001" : {
          "index" : "my-index-000001",
          "managed" : true,
          "index_creation_date_millis" : 1541717265865,
          "time_since_index_creation": "5.1d",
          "policy" : "shrink-index",                __"lifecycle_date_millis" : 1541717265865,
          "age": "5.1d", __"phase" : "warm", __"phase_time_millis" : 1541717272601,
          "action" : "shrink", __"action_time_millis" : 1541717272601,
          "step" : "ERROR", __"step_time_millis" : 1541717272688,
          "failed_step" : "shrink", __"step_info" : {
            "type" : "illegal_argument_exception", __"reason" : "the number of target shards [4] must be less that the number of source shards [2]"
          },
          "phase_execution" : {
            "policy" : "shrink-index",
            "phase_definition" : { __"min_age" : "5d",
              "actions" : {
                "shrink" : {
                  "number_of_shards" : 4
                }
              }
            },
            "version" : 1,
            "modified_date_in_millis" : 1541717264230
          }
        }
      }
    }

__

|

用于管理索引的策略："收缩索引"---|---__

|

指数年龄：5.1天__

|

指数当前所处的阶段："暖"__

|

当前操作："收缩"__

|

索引当前所在的步骤："错误" __

|

执行失败的步骤："收缩"__

|

错误的类型和该错误的描述。   __

|

"收缩索引"策略中当前阶段的定义 要解决此问题，您可以更新策略以在 5 天后将索引收缩为单个分片：

    
    
    response = client.ilm.put_lifecycle(
      policy: 'shrink-index',
      body: {
        policy: {
          phases: {
            warm: {
              min_age: '5d',
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
    
    
    PUT _ilm/policy/shrink-index
    {
      "policy": {
        "phases": {
          "warm": {
            "min_age": "5d",
            "actions": {
              "shrink": {
                "number_of_shards": 1
              }
            }
          }
        }
      }
    }

### 重试失败的生命周期策略步骤

修复将索引置于"错误"步骤中的问题后，可能需要显式指示 ILM 重试该步骤：

    
    
    POST /my-index-000001/_ilm/retry

ILM 随后尝试重新运行失败的步骤。您可以使用 ILMExplain API 来监视进度。

### 常见 ILM 错误

下面介绍了如何解决"错误"步骤中报告的最常见错误。

翻转别名问题是导致错误的常见原因。请考虑使用数据流，而不是使用别名管理滚动更新。

#### 翻转别名 x] 可以指向多个索引，在索引模板 [z][

目标翻转别名在索引模板的"index.lifecycle.rollover_alias"设置中指定。您需要在引导初始索引时显式配置此别名_one time_。然后，翻转操作管理设置和更新别名以滚动更新到每个后续索引。

不要在索引模板的别名部分中显式配置此相同别名。

#### index.lifecycle.rollover_alias x] 不指向索引[y][

索引使用了错误的别名或别名不存在。

检查"index.lifecycle.rollover_alias"索引设置。要查看配置了哪些别名，请使用_cat/别名。

#### 索引 [y] 的设置 index.lifecycle.rollover_alias] 为空或未定义[

必须配置"index.lifecycle.rollover_alias"设置才能使翻转操作正常工作。

更新索引设置以设置"index.lifecycle.rollover_alias"。

#### 别名 x] 具有多个写入索引[y，z][

只能将一个索引指定为特定别名的写入索引。

使用别名 API 为除一个索引之外的所有索引设置"is_write_index：false"。

#### 索引名称 x] 与模式不匹配^.*-\d+[

索引名称必须与正则表达式模式"^.*-\d+"匹配，滚动更新操作才能正常工作。最常见的问题是索引名称不包含尾随数字。例如，"my-index"与模式要求不匹配。

将数值附加到索引名称，例如"my-index-000001"。

#### 断路异常：x] 数据太大，数据为 [y][

这表示群集正在达到资源限制。

在继续设置 ILM 之前，您需要采取措施来缓解源问题。有关详细信息，请参阅断路器错误。

#### 高磁盘水位线 x] 超出 on[y][

这表示群集磁盘空间不足。如果未将索引生命周期管理设置为从热节点滚动更新到温节点，则可能会发生这种情况。

请考虑添加节点、升级硬件或删除不需要的索引。

#### security_exception：操作 ] <action-name>对于具有角色 [] 的用户 [] 是未经授权的，<user-name><role-name>此操作由索引权限 [manage_follow_index，管理，全部][

这表示无法执行 ILM 操作，因为 ILM 用于执行该操作的用户没有适当的权限。更新 ILM 策略后删除用户的权限时，可能会发生这种情况。ILM 操作的运行就像由修改策略的最后一个用户执行一样。用于从中创建或修改策略的帐户应具有执行属于该策略的所有操作的权限。

[« Migrate index allocation filters to node roles](migrate-index-allocation-
filters.md) [Start and stop index lifecycle management »](start-stop-
ilm.md)
