

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Pipeline processor](pipeline-processor.md) [Registered domain processor
»](registered-domain-processor.md)

## 编校处理器

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

编校处理器使用 Grok 规则引擎来遮盖输入文档中与给定 Grok 模式匹配的文本。处理器可用于通过配置个人识别信息 (PII) 来检测已知模式(如电子邮件或 IP 地址)。与 Grok 模式匹配的文本将替换为可配置的字符串(例如""，其中电子邮件地址匹配<EMAIL>)，或者如果<REDACTED>愿意，则只需将所有匹配项替换为文本""。

Elasticsearch附带了许多有用的预定义模式，这些模式可以被编校处理器方便地引用。如果其中一个不符合您的需求，请使用自定义模式定义创建新模式。编校处理器替换匹配项的每次匹配项。如果有多个匹配项，则所有匹配项都将替换为模式名称。

编校处理器与弹性通用模式 (ECS) 模式兼容。不支持旧版 Grokpatterns。

### 在管道中使用编校处理器

**表 34.密文选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

要编辑的字段"模式"

|

yes

|

-

|

要匹配和编辑名为"pattern_definitions"捕获的 grok 表达式列表

|

no

|

-

|

模式名称和模式元组的映射，用于定义处理器要使用的自定义模式。与现有名称匹配的模式将覆盖预先存在的定义"前缀"

|

no

|

<

|

使用此标记"后缀"开始编辑的部分

|

no

|

>

|

使用此标记"ignore_missing"结束已编辑的部分

|

no

|

`true`

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

处理器的标识符。对于调试和指标很有用。   在此示例中，预定义的"IP"Grok 模式用于匹配和编辑"消息"文本字段中的 IP 地址。管道使用模拟 API 进行测试。

    
    
    response = client.ingest.simulate(
      body: {
        pipeline: {
          description: 'Hide my IP',
          processors: [
            {
              redact: {
                field: 'message',
                patterns: [
                  '%{IP:client}'
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
        "description" : "Hide my IP",
        "processors": [
          {
            "redact": {
              "field": "message",
              "patterns": ["%{IP:client}"]
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

响应中的文档仍包含"消息"字段，但现在 IP 地址"55.3.244.1"被文本""替换<client>。

    
    
    {
      "docs": [
        {
          "doc": {
            "_index": "_index",
            "_id": "_id",
            "_version": "-3",
            "_source": {
              "message": "<client> GET /index.html 15824 0.043"
            },
            "_ingest": {
              "timestamp": "2023-02-01T16:08:39.419056008Z"
            }
          }
        }
      ]
    }

IP 地址将替换为单词"client"，因为这是 Grok 模式 '%{IP：client}' 中指定的内容。围绕模式名称的"<"和">"标记可以使用"前缀"和"后缀"选项进行配置。

下一个示例定义了多个模式，这两种模式都替换为单词"REDACTED"，前缀和后缀标记设置为"*"

    
    
    response = client.ingest.simulate(
      body: {
        pipeline: {
          description: 'Hide my IP',
          processors: [
            {
              redact: {
                field: 'message',
                patterns: [
                  '%{IP:REDACTED}',
                  '%{EMAILADDRESS:REDACTED}'
                ],
                prefix: '*',
                suffix: '*'
              }
            }
          ]
        },
        docs: [
          {
            _source: {
              message: '55.3.244.1 GET /index.html 15824 0.043 test@elastic.co'
            }
          }
        ]
      }
    )
    puts response
    
    
    POST _ingest/pipeline/_simulate
    {
      "pipeline": {
        "description": "Hide my IP",
        "processors": [
          {
            "redact": {
              "field": "message",
              "patterns": [
                "%{IP:REDACTED}",
                "%{EMAILADDRESS:REDACTED}"
              ],
              "prefix": "*",
              "suffix": "*"
            }
          }
        ]
      },
      "docs": [
        {
          "_source": {
            "message": "55.3.244.1 GET /index.html 15824 0.043 test@elastic.co"
          }
        }
      ]
    }

在回复中，IP "55.3.244.1"和电子邮件地址"test@elastic.co"均已替换为"*已编辑*"。

    
    
    {
      "docs": [
        {
          "doc": {
            "_index": "_index",
            "_id": "_id",
            "_version": "-3",
            "_source": {
              "message": "*REDACTED* GET /index.html 15824 0.043 *REDACTED*"
            },
            "_ingest": {
              "timestamp": "2023-02-01T16:53:14.560005377Z"
            }
          }
        }
      ]
    }

### 自定义模式

如果现有的 Grokpatterns 之一不符合您的要求，可以使用"pattern_definitions"选项添加自定义模式。新模式定义由模式名称和模式本身组成。该模式可以是引用现有 Grok 模式的正则表达式或。

此示例定义自定义模式"GITHUB_NAME"以匹配 GitHub 用户名。模式定义使用现有的"用户名"Grokpattern，前缀为文字"@"。

Grok 调试器是用于构建自定义模式的非常有用的工具。

    
    
    response = client.ingest.simulate(
      body: {
        pipeline: {
          processors: [
            {
              redact: {
                field: 'message',
                patterns: [
                  '%{GITHUB_NAME:GITHUB_NAME}'
                ],
                pattern_definitions: {
                  "GITHUB_NAME": '@%<USERNAME>s'
                }
              }
            }
          ]
        },
        docs: [
          {
            _source: {
              message: '@elastic-data-management the PR is ready for review'
            }
          }
        ]
      }
    )
    puts response
    
    
    POST _ingest/pipeline/_simulate
    {
      "pipeline": {
        "processors": [
          {
            "redact": {
              "field": "message",
              "patterns": [
                "%{GITHUB_NAME:GITHUB_NAME}"
              ],
              "pattern_definitions": {
                "GITHUB_NAME": "@%{USERNAME}"
              }
            }
          }
        ]
      },
      "docs": [
        {
          "_source": {
            "message": "@elastic-data-management the PR is ready for review"
          }
        }
      ]
    }

用户名在响应中被编辑。

    
    
    {
      "docs": [
        {
          "doc": {
            "_index": "_index",
            "_id": "_id",
            "_version": "-3",
            "_source": {
              "message": "<GITHUB_NAME> the PR is ready for review"
            },
            "_ingest": {
              "timestamp": "2023-02-01T16:53:14.560005377Z"
            }
          }
        }
      ]
    }

### 格罗克看门狗

监视器会中断执行时间过长的表达式。中断时，编校处理器将失败并显示错误。控制 Grok 监视器超时的相同设置也适用于编校处理器。

[« Pipeline processor](pipeline-processor.md) [Registered domain processor
»](registered-domain-processor.md)
