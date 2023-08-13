

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md)

[« Wait for snapshot](ilm-wait-for-snapshot.md) [Migrate index allocation
filters to node roles »](migrate-index-allocation-filters.md)

## 配置生命周期策略

要使 ILM 管理索引，必须在"索引.生命周期.名称"索引设置中指定有效的策略。

要为滚动索引配置生命周期策略，请创建该策略并将其添加到索引模板中。

要使用策略管理不滚动更新的索引，您可以在创建索引时指定生命周期策略，或将策略直接应用于现有索引。

ILM 策略存储在全局群集状态中，并且可以通过在拍摄快照时将"include_global_state"设置为"true"来包含在快照中。还原快照时，将还原全局状态的所有策略，并覆盖具有相同名称的任何本地策略。

当您为 Beats 或 LogstashElasticsearch 输出插件启用索引生命周期管理时，将自动应用必要的策略和配置更改。您可以修改默认策略，但无需显式配置策略或引导初始索引。

### 创建生命周期策略

要从 Kibana 创建生命周期策略，请打开菜单并转到 **堆栈管理>索引生命周期策略**。单击**创建策略**。

!"创建策略"页

您可以指定策略的生命周期阶段以及在每个阶段中要执行的操作。

调用创建或更新策略 API 以将策略添加到 Elasticsearchcluster。

接口示例

    
    
    response = client.ilm.put_lifecycle(
      policy: 'my_policy',
      body: {
        policy: {
          phases: {
            hot: {
              actions: {
                rollover: {
                  max_primary_shard_size: '25GB'
                }
              }
            },
            delete: {
              min_age: '30d',
              actions: {
                delete: {}
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
              "rollover": {
                "max_primary_shard_size": "25GB" __}
            }
          },
          "delete": {
            "min_age": "30d",
            "actions": {
              "delete": {} __}
          }
        }
      }
    }

__

|

当索引的大小达到 25GB 时，滚动更新索引 ---|--- __

|

展期后 30 天删除索引 ### 使用索引模板编辑应用生命周期策略

要使用触发滚动更新操作的策略，您需要在用于创建每个新索引的索引模板中配置策略。您可以指定策略的名称和用于引用滚动索引的别名。

您可以使用 Kibana 创建模板向导来创建模板。要访问该向导，请打开菜单并转到**堆栈管理>索引管理**。在"**索引模板**"选项卡中，单击"**创建模板**"。

!创建模板页面

该向导将调用创建或更新索引模板 API 以将模板添加到群集。

接口示例

    
    
    response = client.indices.put_index_template(
      name: 'my_template',
      body: {
        index_patterns: [
          'test-*'
        ],
        template: {
          settings: {
            number_of_shards: 1,
            number_of_replicas: 1,
            "index.lifecycle.name": 'my_policy',
            "index.lifecycle.rollover_alias": 'test-alias'
          }
        }
      }
    )
    puts response
    
    
    PUT _index_template/my_template
    {
      "index_patterns": ["test-*"], __"template": {
        "settings": {
          "number_of_shards": 1,
          "number_of_replicas": 1,
          "index.lifecycle.name": "my_policy", __"index.lifecycle.rollover_alias": "test-alias" __}
      }
    }

__

|

将此模板用于名称以"test-"开头的所有新索引 ---|--- __

|

将"my_policy"应用于使用此模板创建的新索引 __

|

定义索引别名以引用由"my_policy"管理的索引 #### 创建初始托管索引编辑

为自己的滚动索引设置策略时，需要手动创建由策略管理的第一个索引，并将其指定为 writeindex。

当您为 Beats 或 LogstashElasticsearch 输出插件启用索引生命周期管理时，将自动应用必要的策略和配置更改。您可以修改默认策略，但无需显式配置策略或引导初始索引。

索引的名称必须与索引模板中定义的模式匹配，并以数字结尾。此数字递增以生成由翻转操作创建的索引的名称。

例如，以下请求创建"test-00001"索引。由于它与"my_template"中指定的索引模式匹配，因此 Elasticsearch 会自动应用该模板中的设置。

    
    
    response = client.indices.create(
      index: 'test-000001',
      body: {
        aliases: {
          "test-alias": {
            is_write_index: true
          }
        }
      }
    )
    puts response
    
    
    PUT test-000001
    {
      "aliases": {
        "test-alias":{
          "is_write_index": true __}
      }
    }

__

|

将此初始索引设置为此别名的写入索引。   ---|--- 现在，您可以开始将数据索引到生命周期策略中指定的滚动更新别名。使用示例"my_policy"策略，一旦初始索引超过 25GB，就会触发滚动更新操作。然后，ILM 创建一个新索引，该索引将成为"测试别名"的写入索引。

### 手动应用生命周期策略

您可以在创建索引时指定策略，也可以通过 Kibana 管理或更新设置 API 将策略应用于现有索引。应用策略后，ILM 会立即开始管理索引。

不要手动应用使用滚动更新操作的策略。使用滚动更新的策略必须由索引模板应用。否则，当滚动更新操作创建新索引时，不会继续执行策略。

"index.lifecycle.name"设置指定索引的策略。

接口示例

    
    
    response = client.indices.create(
      index: 'test-index',
      body: {
        settings: {
          number_of_shards: 1,
          number_of_replicas: 1,
          "index.lifecycle.name": 'my_policy'
        }
      }
    )
    puts response
    
    
    PUT test-index
    {
      "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1,
        "index.lifecycle.name": "my_policy" __}
    }

__

|

设置索引的生命周期策略。   ---|--- #### 将策略应用于多个索引编辑

调用更新设置 API 时，可以通过在索引名称中使用通配符将同一策略应用于多个索引。

请注意不要无意中匹配不想修改的索引。

    
    
    response = client.indices.put_settings(
      index: 'mylogs-pre-ilm*',
      body: {
        index: {
          lifecycle: {
            name: 'mylogs_policy_existing'
          }
        }
      }
    )
    puts response
    
    
    PUT mylogs-pre-ilm*/_settings __{
      "index": {
        "lifecycle": {
          "name": "mylogs_policy_existing"
        }
      }
    }

__

|

更新名称以"mylogs-pre-ilm"开头的所有索引 ---|--- #### 交换机生命周期策略编辑

要切换索引的生命周期策略，请执行以下步骤：

1. 使用删除策略 API 删除现有策略。以数据流或别名为目标，以删除其所有索引的策略。           响应 = client.ilm.remove_policy( 索引："logs-my_app-default" ) 放置响应 POST 日志-my_app-默认/_ilm/删除

2. 删除策略 API 从索引中删除所有 ILM 元数据，并且不考虑索引的生命周期状态。这可能会使索引处于不需要的状态。

例如，"强制合并"操作在重新打开索引之前暂时关闭索引。在"强制合并"期间删除索引的 ILM 策略可能会使索引无限期关闭。

删除策略后，使用 get index API 检查索引的状态。以数据流或别名为目标以获取其所有索引的状态。

    
        response = client.indices.get(
      index: 'logs-my_app-default'
    )
    puts response
    
        GET logs-my_app-default

然后，您可以根据需要更改索引。例如，您可以使用开放索引 API 重新打开任何已关闭的索引。

    
        response = client.indices.open(
      index: 'logs-my_app-default'
    )
    puts response
    
        POST logs-my_app-default/_open

3. 使用更新设置 API 分配新策略。以数据流或别名为目标，将策略分配给其所有索引。

在未先删除现有策略的情况下，请勿分配新策略。这可能会导致阶段执行以静默方式失败。

    
        response = client.indices.put_settings(
      index: 'logs-my_app-default',
      body: {
        index: {
          lifecycle: {
            name: 'new-lifecycle-policy'
          }
        }
      }
    )
    puts response
    
        PUT logs-my_app-default/_settings
    {
      "index": {
        "lifecycle": {
          "name": "new-lifecycle-policy"
        }
      }
    }

[« Wait for snapshot](ilm-wait-for-snapshot.md) [Migrate index allocation
filters to node roles »](migrate-index-allocation-filters.md)
