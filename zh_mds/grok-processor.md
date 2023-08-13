

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« GeoIP processor](geoip-processor.md) [Gsub processor »](gsub-
processor.md)

## 格罗克处理器

从文档内的单个文本字段中提取结构化字段。您可以选择要从中提取匹配字段的字段，以及您希望匹配的 grok 模式。grok 模式类似于支持可重用的别名表达式的正则表达式。

该处理器附带了许多可重用的模式。

如果您需要帮助构建模式以匹配您的日志，您会发现 GrokDebugger 工具非常有用！TheGrok Constructor也是一个有用的工具。

### 在 aPipeline 中使用 Grok 处理器

**表 23.格罗克选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

用于 grok 表达式解析"模式"的字段

|

yes

|

-

|

要匹配和提取命名捕获的 grok 表达式的有序列表。返回列表中匹配的第一个表达式。   "pattern_definitions"

|

no

|

-

|

模式名称和模式元组的映射，用于定义当前处理器要使用的自定义模式。与现有名称匹配的模式将覆盖预先存在的定义。   "ecs_compatibility"

|

no

|

`disabled`

|

必须为"禁用"或"v1"。如果为"v1"，则处理器使用具有弹性通用架构 (ECS) 字段名称的模式。   "trace_match"

|

no

|

false

|

如果为 true，则"_ingest._grok_match_index"将入到匹配文档的元数据中，并将索引插入到匹配的"模式"中找到的模式中。   "ignore_missing"

|

no

|

false

|

如果"true"和"field"不存在或为"null"，处理器将悄悄退出而不修改文档"描述"

|

no

|

-

|

处理器的说明。用于描述处理器的目的或其配置。   "如果"

|

no

|

-

|

有条件地执行处理器。请参阅有条件运行处理器。   "ignore_failure"

|

no

|

`false`

|

忽略处理器的故障。请参阅处理管道故障。   "on_failure"

|

no

|

-

|

处理处理器的故障。请参阅处理管道故障。   "标签"

|

no

|

-

|

处理器的标识符。对于调试和指标很有用。   下面是使用提供的模式从文档中的字符串字段中提取和命名结构化字段的示例。

    
    
    response = client.ingest.simulate(
      body: {
        pipeline: {
          description: '...',
          processors: [
            {
              grok: {
                field: 'message',
                patterns: [
                  '%{IP:client} %{WORD:method} %{URIPATHPARAM:request} %{NUMBER:bytes:int} %{NUMBER:duration:double}'
                ]
              }
            }
          ]
        },
        docs: [
          {
            _source: {
              message: '55.3.244.1 GET /index.html 15824 0.043'
            }
          }
        ]
      }
    )
    puts response
    
    
    POST _ingest/pipeline/_simulate
    {
      "pipeline": {
        "description" : "...",
        "processors": [
          {
            "grok": {
              "field": "message",
              "patterns": ["%{IP:client} %{WORD:method} %{URIPATHPARAM:request} %{NUMBER:bytes:int} %{NUMBER:duration:double}"]
            }
          }
        ]
      },
      "docs":[
        {
          "_source": {
            "message": "55.3.244.1 GET /index.html 15824 0.043"
          }
        }
      ]
    }

此管道会将这些命名捕获作为新字段插入到文档中，如下所示：

    
    
    {
      "docs": [
        {
          "doc": {
            "_index": "_index",
            "_id": "_id",
            "_version": "-3",
            "_source" : {
              "duration" : 0.043,
              "request" : "/index.html",
              "method" : "GET",
              "bytes" : 15824,
              "client" : "55.3.244.1",
              "message" : "55.3.244.1 GET /index.html 15824 0.043"
            },
            "_ingest": {
              "timestamp": "2016-11-08T19:43:03.850+0000"
            }
          }
        }
      ]
    }

### 自定义模式

Grok 处理器预包装了一组基本模式。这些模式可能并不总是有你要找的东西。模式具有非常基本的格式。每个条目都有一个名称和模式本身。

您可以在"pattern_definitions"选项下将自己的模式添加到处理器定义中。下面是指定自定义模式定义的管道示例：

    
    
    {
      "description" : "...",
      "processors": [
        {
          "grok": {
            "field": "message",
            "patterns": ["my %{FAVORITE_DOG:dog} is colored %{RGB:color}"],
            "pattern_definitions" : {
              "FAVORITE_DOG" : "beagle",
              "RGB" : "RED|GREEN|BLUE"
            }
          }
        }
      ]
    }

### 提供多个匹配模式

有时，一种模式不足以捕捉到远场的潜在结构。假设我们要匹配包含您最喜欢的猫或狗宠物品种的所有消息。实现此目的的一种方法是提供两个可以匹配的不同模式，而不是一个捕获相同"或"行为的非常复杂的表达式。

下面是针对模拟 API 执行的此类配置的示例：

    
    
    response = client.ingest.simulate(
      body: {
        pipeline: {
          description: 'parse multiple patterns',
          processors: [
            {
              grok: {
                field: 'message',
                patterns: [
                  '%{FAVORITE_DOG:pet}',
                  '%{FAVORITE_CAT:pet}'
                ],
                pattern_definitions: {
                  "FAVORITE_DOG": 'beagle',
                  "FAVORITE_CAT": 'burmese'
                }
              }
            }
          ]
        },
        docs: [
          {
            _source: {
              message: 'I love burmese cats!'
            }
          }
        ]
      }
    )
    puts response
    
    
    POST _ingest/pipeline/_simulate
    {
      "pipeline": {
      "description" : "parse multiple patterns",
      "processors": [
        {
          "grok": {
            "field": "message",
            "patterns": ["%{FAVORITE_DOG:pet}", "%{FAVORITE_CAT:pet}"],
            "pattern_definitions" : {
              "FAVORITE_DOG" : "beagle",
              "FAVORITE_CAT" : "burmese"
            }
          }
        }
      ]
    },
    "docs":[
      {
        "_source": {
          "message": "I love burmese cats!"
        }
      }
      ]
    }

response:

    
    
    {
      "docs": [
        {
          "doc": {
            "_index": "_index",
            "_id": "_id",
            "_version": "-3",
            "_source": {
              "message": "I love burmese cats!",
              "pet": "burmese"
            },
            "_ingest": {
              "timestamp": "2016-11-08T19:43:03.850+0000"
            }
          }
        }
      ]
    }

这两种模式都会将字段"pet"设置为适当的匹配项，但是如果我们想跟踪哪些模式匹配并填充了我们的字段，该怎么办？我们可以使用 'trace_match' 参数来做到这一点。以下是该相同管道的输出，但配置了"trace_match"：true：

    
    
    {
      "docs": [
        {
          "doc": {
            "_index": "_index",
            "_id": "_id",
            "_version": "-3",
            "_source": {
              "message": "I love burmese cats!",
              "pet": "burmese"
            },
            "_ingest": {
              "_grok_match_index": "1",
              "timestamp": "2016-11-08T19:43:03.850+0000"
            }
          }
        }
      ]
    }

在上面的响应中，您可以看到匹配的模式的索引是"1"。也就是说，它是"模式"中的第二个(索引从零开始)模式来匹配。

此跟踪元数据允许调试哪些模式匹配。此信息存储在引入元数据中，不会被编制索引。

### 从 REST 端点检索模式

Grok 处理器附带了自己的 REST 端点，用于检索处理器附带的模式。

    
    
    response = client.ingest.processor_grok
    puts response
    
    
    GET _ingest/processor/grok

上述请求将返回一个响应正文，其中包含内置模式字典的键值表示形式。

    
    
    {
      "patterns" : {
        "BACULA_CAPACITY" : "%{INT}{1,3}(,%{INT}{3})*",
        "PATH" : "(?:%{UNIXPATH}|%{WINPATH})",
        ...
    }

默认情况下，API 返回旧版 Grok 模式的列表。这些旧模式早于弹性通用架构 (ECS)，并且不使用 ECS 字段名称。要返回提取 ECS 字段名称的模式，请在可选的"ecs_compatibility"查询参数中指定"v1"。

    
    
    response = client.ingest.processor_grok(
      ecs_compatibility: 'v1'
    )
    puts response
    
    
    GET _ingest/processor/grok?ecs_compatibility=v1

默认情况下，API 按从磁盘读取模式的顺序返回模式。此排序顺序保留了相关模式的分组。例如，与解析 Linux 系统日志行相关的所有模式都保持分组在一起。

您可以使用可选的布尔 's' 查询参数按键名对返回的模式进行排序。

    
    
    response = client.ingest.processor_grok(
      s: true
    )
    puts response
    
    
    GET _ingest/processor/grok?s

API 返回以下响应。

    
    
    {
      "patterns" : {
        "BACULA_CAPACITY" : "%{INT}{1,3}(,%{INT}{3})*",
        "BACULA_DEVICE" : "%{USER}",
        "BACULA_DEVICEPATH" : "%{UNIXPATH}",
        ...
    }

当内置模式跨版本更改时，参考这一点非常有用。

### 格罗克看门狗

执行时间过长的 grok 表达式将被中断，然后 grokprocessor 失败并出现异常。grok 处理器有一个监视线程，用于确定 grok 表达式的计算时间过长，并由以下设置控制：

**表 24.格罗克看门狗设置**

姓名 |默认 |描述 ---|---|--- 'ingest.grok.watchdog.interval'

|

1s

|

检查是否存在花费超过最大允许执行时间的 grok 评估的频率。   'ingest.grok.watchdog.max_execution_time'

|

1s

|

允许执行 grok 表达式计算的最大值。   ### Grokdebuggingedit

建议使用 Grok 调试器来调试 grok 模式。从那里，您可以针对示例数据测试 UI 中的一个或多个模式。在幕后，它使用与摄取节点处理器相同的引擎。

此外，建议为 Grok 启用调试日志记录，以便在 Elasticsearch 服务器日志中也可以看到任何其他消息。

    
    
    PUT _cluster/settings
    {
      "persistent": {
        "logger.org.elasticsearch.ingest.common.GrokProcessor": "debug"
      }
    }

[« GeoIP processor](geoip-processor.md) [Gsub processor »](gsub-
processor.md)
