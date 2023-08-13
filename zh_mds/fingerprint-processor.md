

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Fail processor](fail-processor.md) [Foreach processor »](foreach-
processor.md)

## 指纹处理器

计算文档内容的哈希。您可以将此哈希用于内容指纹识别)。

**表 19.指纹选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'fields'

|

yes

|

n/a

|

要包含在指纹中的字段数组。对于对象，处理器对字段键和值进行哈希处理。对于其他字段，处理器仅对字段值进行哈希处理。   "target_field"

|

no

|

`fingerprint`

|

指纹的输出字段。   "盐"

|

no

|

<none>

|

盐值)作为哈希函数。   "方法"

|

no

|

`SHA-1`

|

用于计算指纹的哈希方法。必须是"MD5"、"SHA-1"、"SHA-256"、"SHA-512"或"MurmurHash3"之一。   "ignore_missing"

|

no

|

`false`

|

如果为"true"，则处理器将忽略任何缺失的"字段"。如果缺少所有字段，处理器将以静默方式退出而不修改文档。   "说明"

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

处理器的标识符。对于调试和指标很有用。   #####Exampleedit

以下示例说明了指纹处理器的用法：

    
    
    response = client.ingest.simulate(
      body: {
        pipeline: {
          processors: [
            {
              fingerprint: {
                fields: [
                  'user'
                ]
              }
            }
          ]
        },
        docs: [
          {
            _source: {
              user: {
                last_name: 'Smith',
                first_name: 'John',
                date_of_birth: '1980-01-15',
                is_active: true
              }
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
            "fingerprint": {
              "fields": ["user"]
            }
          }
        ]
      },
      "docs": [
        {
          "_source": {
            "user": {
              "last_name": "Smith",
              "first_name": "John",
              "date_of_birth": "1980-01-15",
              "is_active": true
            }
          }
        }
      ]
    }

这将产生以下结果：

    
    
    {
      "docs": [
        {
          "doc": {
            ...
            "_source": {
              "fingerprint" : "WbSUPW4zY1PBPehh2AA/sSxiRjw=",
              "user" : {
                "last_name" : "Smith",
                "first_name" : "John",
                "date_of_birth" : "1980-01-15",
                "is_active" : true
              }
            }
          }
        }
      ]
    }

[« Fail processor](fail-processor.md) [Foreach processor »](foreach-
processor.md)
