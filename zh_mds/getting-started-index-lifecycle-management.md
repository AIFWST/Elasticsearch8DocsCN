

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md)

[« Tutorial: Customize built-in ILM policies](example-using-index-lifecycle-
policy.md) [Index management in Kibana »](index-mgmt.md)

## 教程：使用 ILM 自动滚动更新

当您连续将带有时间戳的文档索引到 Elasticsearch 中时，您通常会使用数据流，以便可以定期滚动到新索引。这使您能够实施热温冷体系结构，以满足最新数据的性能要求，控制一段时间内的成本，实施保留策略，并仍然充分利用数据。

数据流最适合仅追加用例。如果您需要跨多个索引频繁更新或删除现有文档，我们建议改用索引别名和索引模板。您仍然可以使用 ILM 来管理和滚动更新别名的索引。跳到管理没有数据流的时序数据。

要使用 ILM 自动滚动更新和管理数据流，您需要：

1. 创建定义相应阶段和操作的生命周期策略。  2. 创建索引模板以创建数据流，并为后备索引应用 ILM 策略以及索引设置和映射配置。  3. 验证索引是否按预期在生命周期阶段移动。

有关滚动索引的介绍，请参阅滚动更新。

当您为 Beats 或 LogstashElasticsearch 输出插件启用索引生命周期管理时，生命周期策略会自动设置。您无需执行任何其他操作。您可以通过 Kibana 管理或 ILM API 修改默认策略。

### 创建生命周期策略

生命周期策略指定索引生命周期中的阶段以及每个阶段要执行的操作。生命周期最多可以有五个阶段："热"、"暖"、"冷"、"冻结"和"删除"。

例如，您可以定义一个包含两个阶段的"timeseries_policy"：

* 一个"热"阶段，用于定义滚动更新操作，以指定索引在达到 50 GB 的"max_primary_shard_size"或 30 天的"max_age"时滚动更新。  * "删除"阶段，设置"min_age"以在展期后 90 天删除索引。

"min_age"值相对于滚动更新时间，而不是索引创建时间。

您可以通过 Kibana 或使用创建或更新策略创建策略 API.To 从 Kibana 创建策略，请打开菜单并转到**堆栈管理>索引生命周期策略**。单击**创建策略**。

!"创建策略"页

接口示例

    
    
    response = client.ilm.put_lifecycle(
      policy: 'timeseries_policy',
      body: {
        policy: {
          phases: {
            hot: {
              actions: {
                rollover: {
                  max_primary_shard_size: '50GB',
                  max_age: '30d'
                }
              }
            },
            delete: {
              min_age: '90d',
              actions: {
                delete: {}
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT _ilm/policy/timeseries_policy
    {
      "policy": {
        "phases": {
          "hot": {                                __"actions": {
              "rollover": {
                "max_primary_shard_size": "50GB", __"max_age": "30d"
              }
            }
          },
          "delete": {
            "min_age": "90d", __"actions": {
              "delete": {} __}
          }
        }
      }
    }

__

|

"min_age"默认为"0ms"，因此新索引立即进入"热"阶段。   ---|---    __

|

当满足任一条件时触发"翻转"操作。   __

|

在滚动更新 90 天后将索引移至"删除"阶段。   __

|

当索引进入删除阶段时触发"删除"操作。   ### 创建索引模板以创建数据流并应用生命周期策略编辑

要设置数据流，请首先创建一个索引模板来指定生命周期策略。由于模板用于数据流，因此还必须包含"data_stream"定义。

例如，您可以创建一个"timeseries_template"以用于名为"timeseries"的未来数据流。

若要使 ILM 能够管理数据流，该模板配置了一个 ILM 设置：

* "index.lifecycle.name"指定要应用于数据流的生命周期策略的名称。

您可以使用 Kibana 创建模板向导来添加模板。从 Kibana 开始，打开菜单并转到堆栈管理>索引管理**。在"**索引模板**"选项卡中，单击"**创建模板**"。

!创建模板页面

此向导调用创建或更新索引模板 API，以使用指定的选项创建索引模板。

接口示例

    
    
    response = client.indices.put_index_template(
      name: 'timeseries_template',
      body: {
        index_patterns: [
          'timeseries'
        ],
        data_stream: {},
        template: {
          settings: {
            number_of_shards: 1,
            number_of_replicas: 1,
            "index.lifecycle.name": 'timeseries_policy'
          }
        }
      }
    )
    puts response
    
    
    PUT _index_template/timeseries_template
    {
      "index_patterns": ["timeseries"],                   __"data_stream": { },
      "template": {
        "settings": {
          "number_of_shards": 1,
          "number_of_replicas": 1,
          "index.lifecycle.name": "timeseries_policy" __}
      }
    }

__

|

在将文档索引到"时间序列"目标时应用模板。   ---|---    __

|

用于管理数据流的 ILM 策略的名称。   ### 创建数据流编辑

要开始操作，请将文档索引为索引模板的"index_patterns"中定义的名称或通配符模式。只要现有数据流、索引或索引别名尚未使用该名称，索引请求就会自动创建具有单个后备索引的相应数据流。Elasticsearch自动将请求的文档索引到此后备索引中，该后备索引也充当流的写入索引。

例如，以下请求创建"时间序列"数据流和名为".ds-timeseries-2099.03.08-000001"的第一代支持索引。

    
    
    POST timeseries/_doc
    {
      "message": "logged the request",
      "@timestamp": "1591890611"
    }

当满足生命周期策略中的滚动更新条件时，"滚动更新"操作：

* 创建名为".ds-timeseries-2099.03.08-000002"的第二代后备索引。由于它是"时间序列"数据流的支持索引，因此"timeseries_template"索引模板中的配置将应用于新索引。  * 由于它是"时间序列"数据流的最新一代索引，因此新创建的后备索引".ds-timeseries-2099.03.08-000002"将成为数据流的写入索引。

每次满足翻转条件时，都会重复此过程。您可以使用"时间序列"数据流名称搜索由"timeseries_policy"管理的所有数据流的支持索引。写入操作路由到当前写入索引。读取操作将由所有支持索引处理。

### 检查生命周期进度

若要获取托管索引的状态信息，请使用 ILM 说明 API。这使您可以了解以下内容：

* 指数处于哪个阶段以及何时进入该阶段。  * 当前操作和正在执行的步骤。  * 如果发生任何错误或进度被阻止。

例如，以下请求获取有关"时间序列"数据流的支持索引的信息：

    
    
    response = client.ilm.explain_lifecycle(
      index: '.ds-timeseries-*'
    )
    puts response
    
    
    GET .ds-timeseries-*/_ilm/explain

以下响应显示数据流的第一代支持索引正在等待"热"阶段的"滚动更新"操作。它保持此状态，ILM 将继续调用"检查-滚动更新就绪"，直到满足滚动更新条件。

    
    
    {
      "indices": {
        ".ds-timeseries-2099.03.07-000001": {
          "index": ".ds-timeseries-2099.03.07-000001",
          "index_creation_date_millis": 1538475653281,
          "time_since_index_creation": "30s",        __"managed": true,
          "policy": "timeseries_policy", __"lifecycle_date_millis": 1538475653281,
          "age": "30s", __"phase": "hot",
          "phase_time_millis": 1538475653317,
          "action": "rollover",
          "action_time_millis": 1538475653317,
          "step": "check-rollover-ready", __"step_time_millis": 1538475653317,
          "phase_execution": {
            "policy": "timeseries_policy",
            "phase_definition": { __"min_age": "0ms",
              "actions": {
                "rollover": {
                  "max_primary_shard_size": "50gb",
                  "max_age": "30d"
                }
              }
            },
            "version": 1,
            "modified_date_in_millis": 1539609701576
          }
        }
      }
    }

__

|

用于计算何时通过"max_age"---|---__ 展期的指数年龄

|

用于管理索引 __ 的策略

|

用于过渡到下一阶段的索引的年龄(在本例中，它与索引的年龄相同)。   __

|

ILM 正在索引 __ 上执行的步骤

|

当前阶段的定义("热"阶段)### 在没有数据流的情况下管理时间序列数据编辑

尽管数据流是缩放和管理时序数据的便捷方法，但它们设计为仅追加。我们认识到可能存在需要就地更新或删除数据的用例，并且数据流不支持直接删除和更新请求，因此索引 API 需要直接在数据流的后备索引上使用。

在这些情况下，您可以使用索引别名来管理包含时序数据的索引，并定期滚动到新索引。

要使用索引别名通过 ILM 自动滚动更新和管理时序索引，您需要：

1. 创建定义相应阶段和操作的生命周期策略。请参阅上面的创建生命周期策略。  2. 创建索引模板以将策略应用于每个新索引。  3. 引导索引作为初始写入索引。  4. 验证索引是否按预期在生命周期阶段移动。

### 创建索引模板以应用生命周期策略

要在滚动更新时自动将生命周期策略应用于新的写入索引，请在索引模板中指定用于创建新索引的策略。

例如，您可以创建一个"timeseries_template"，该""应用于名称与"timeseries-*"索引模式匹配的新索引。

若要启用自动滚动更新，该模板将配置两个 ILM 设置：

* "index.lifecycle.name"指定要应用于与索引模式匹配的新索引的生命周期策略的名称。  * "index.lifecycle.rollover_alias"指定为索引触发翻转操作时要滚动更新的索引别名。

您可以使用 Kibana 创建模板向导来添加模板。要访问该向导，请打开菜单并转到**堆栈管理>索引管理**。在"**索引模板**"选项卡中，单击"**创建模板**"。

!创建模板页面

示例模板的创建模板请求如下所示：

    
    
    PUT _index_template/timeseries_template
    {
      "index_patterns": ["timeseries-*"],                 __"template": {
        "settings": {
          "number_of_shards": 1,
          "number_of_replicas": 1,
          "index.lifecycle.name": "timeseries_policy", __"index.lifecycle.rollover_alias": "timeseries" __}
      }
    }

__

|

如果模板的名称以"timeseries-"开头，则将模板应用于新索引。   ---|---    __

|

要应用于每个新索引的生命周期策略的名称。   __

|

用于引用这些索引的别名的名称。对于使用滚动更新操作的策略是必需的。   ### 使用写入索引别名编辑引导初始时序索引

要开始操作，您需要引导初始索引，并将其指定为索引模板中指定的滚动更新别名的写入索引。此索引的名称必须与模板的索引模式匹配，并以数字结尾。滚动更新时，此值将递增以生成新索引的名称。

例如，以下请求创建一个名为"timeseries-000001"的索引，并使其成为"timeseries"别名的写入索引。

    
    
    PUT timeseries-000001
    {
      "aliases": {
        "timeseries": {
          "is_write_index": true
        }
      }
    }

当满足翻转条件时，"翻转"操作：

* 创建一个名为"timeseries-000002"的新索引。这与"时间序列-*"模式匹配，因此"timeseries_template"中的设置将应用于新索引。  * 将新索引指定为写入索引，并使引导索引为只读。

每次满足翻转条件时，都会重复此过程。您可以使用"时间序列"别名搜索由"timeseries_policy"管理的所有索引。写入操作将路由到当前写入索引。

### 检查生命周期进度

检索托管索引的状态信息与数据流的情况非常相似。有关详细信息，请参阅数据流检查进度部分。唯一的区别是索引命名空间，因此检索进度将需要以下 api 调用：

    
    
    response = client.ilm.explain_lifecycle(
      index: 'timeseries-*'
    )
    puts response
    
    
    GET timeseries-*/_ilm/explain

[« Tutorial: Customize built-in ILM policies](example-using-index-lifecycle-
policy.md) [Index management in Kibana »](index-mgmt.md)
