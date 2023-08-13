

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Script processor](script-processor.md) [Set security user processor
»](ingest-node-set-security-user-processor.md)

## 设置处理器

设置一个字段并将其与指定值关联。如果该字段已存在，则其值将替换为提供的值。

**表 40.设置选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

要插入、更新插入或更新的字段。支持模板片段。   "价值"

|

yes*

|

-

|

要为字段设置的值。支持模板片段。只能指定"值"或"copy_from"之一。   "copy_from"

|

no

|

-

|

将被复制到"字段"的源字段不能同时设置"值"。支持的数据类型包括"布尔"、"数字"、"数组"、"对象"、"字符串"、"日期"等。   "覆盖"

|

no

|

`true`

|

如果"true"处理器将使用预先存在的非空值字段更新字段。当设置为"false"时，不会触及此类字段。   "ignore_empty_value"

|

no

|

`false`

|

如果"true"和"value"是计算结果为"null"或空字符串的模板片段，则处理器将静默退出而不修改文档"media_type"

|

no

|

`application/json`

|

用于编码"值"的媒体类型。仅当"值"是模板片段时才适用。必须是"application/json"、"text/plain"或"application/x-www-form-urlencoded"之一。   "说明"

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

处理器的标识符。对于调试和指标很有用。               { "description" ： "将计数的值设置为 1"， "set"： { "字段"： "count"， "value"： 1 } }

该处理器还可用于将数据从一个字段复制到另一个字段。例如：

    
    
    response = client.ingest.put_pipeline(
      id: 'set_os',
      body: {
        description: 'sets the value of host.os.name from the field os',
        processors: [
          {
            set: {
              field: 'host.os.name',
              value: '{{{os}}}'
            }
          }
        ]
      }
    )
    puts response
    
    response = client.ingest.simulate(
      id: 'set_os',
      body: {
        docs: [
          {
            _source: {
              os: 'Ubuntu'
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT _ingest/pipeline/set_os
    {
      "description": "sets the value of host.os.name from the field os",
      "processors": [
        {
          "set": {
            "field": "host.os.name",
            "value": "{{{os}}}"
          }
        }
      ]
    }
    
    POST _ingest/pipeline/set_os/_simulate
    {
      "docs": [
        {
          "_source": {
            "os": "Ubuntu"
          }
        }
      ]
    }

Result:

    
    
    {
      "docs" : [
        {
          "doc" : {
            "_index" : "_index",
            "_id" : "_id",
            "_version" : "-3",
            "_source" : {
              "host" : {
                "os" : {
                  "name" : "Ubuntu"
                }
              },
              "os" : "Ubuntu"
            },
            "_ingest" : {
              "timestamp" : "2019-03-11T21:54:37.909224Z"
            }
          }
        }
      ]
    }

此处理器还可以使用点表示法访问数组字段：

    
    
    response = client.ingest.simulate(
      body: {
        pipeline: {
          processors: [
            {
              set: {
                field: 'my_field',
                value: '{{{input_field.1}}}'
              }
            }
          ]
        },
        docs: [
          {
            _index: 'index',
            _id: 'id',
            _source: {
              input_field: [
                'Ubuntu',
                'Windows',
                'Ventura'
              ]
            }
          }
        ]
      }
    )
    puts response
    
    
    POST /_ingest/pipeline/_simulate
    {
      "pipeline": {
        "processors": [
          {
            "set": {
              "field": "my_field",
              "value": "{{{input_field.1}}}"
            }
          }
        ]
      },
      "docs": [
        {
          "_index": "index",
          "_id": "id",
          "_source": {
            "input_field": [
              "Ubuntu",
              "Windows",
              "Ventura"
            ]
          }
        }
      ]
    }

Result:

    
    
    {
      "docs": [
        {
          "doc": {
            "_index": "index",
            "_id": "id",
            "_version": "-3",
            "_source": {
              "input_field": [
                "Ubuntu",
                "Windows",
                "Ventura"
              ],
              "my_field": "Windows"
            },
            "_ingest": {
              "timestamp": "2023-05-05T16:04:16.456475214Z"
            }
          }
        }
      ]
    }

包含复杂值(如数组和对象)的字段内容可以使用"copy_from"复制到另一个字段：

    
    
    response = client.ingest.put_pipeline(
      id: 'set_bar',
      body: {
        description: 'sets the value of bar from the field foo',
        processors: [
          {
            set: {
              field: 'bar',
              copy_from: 'foo'
            }
          }
        ]
      }
    )
    puts response
    
    response = client.ingest.simulate(
      id: 'set_bar',
      body: {
        docs: [
          {
            _source: {
              foo: [
                'foo1',
                'foo2'
              ]
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT _ingest/pipeline/set_bar
    {
      "description": "sets the value of bar from the field foo",
      "processors": [
        {
          "set": {
            "field": "bar",
            "copy_from": "foo"
          }
        }
      ]
    }
    
    POST _ingest/pipeline/set_bar/_simulate
    {
      "docs": [
        {
          "_source": {
            "foo": ["foo1", "foo2"]
          }
        }
      ]
    }

Result:

    
    
    {
      "docs" : [
        {
          "doc" : {
            "_index" : "_index",
            "_id" : "_id",
            "_version" : "-3",
            "_source" : {
              "bar": ["foo1", "foo2"],
              "foo": ["foo1", "foo2"]
            },
            "_ingest" : {
              "timestamp" : "2020-09-30T12:55:17.742795Z"
            }
          }
        }
      ]
    }

[« Script processor](script-processor.md) [Set security user processor
»](ingest-node-set-security-user-processor.md)
