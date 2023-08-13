

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Network direction processor](network-direction-processor.md) [Redact
processor »](redact-processor.md)

## 管道处理器

执行另一个管道。

**表 33.管道选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'name'

|

yes

|

-

|

要执行的管道的名称。支持模板片段。   "ignore_missing_pipeline"

|

no

|

false

|

是否忽略缺少的管道而不是失败。   "说明"

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

处理器的标识符。对于调试和指标很有用。               { "管道"： { "名称"： "内部管道" } }

可以从"_ingest.pipeline"引入元数据密钥访问当前管道的名称。

将此处理器用于嵌套管道的示例如下：

定义内部管道：

    
    
    response = client.ingest.put_pipeline(
      id: 'pipelineA',
      body: {
        description: 'inner pipeline',
        processors: [
          {
            set: {
              field: 'inner_pipeline_set',
              value: 'inner'
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT _ingest/pipeline/pipelineA
    {
      "description" : "inner pipeline",
      "processors" : [
        {
          "set" : {
            "field": "inner_pipeline_set",
            "value": "inner"
          }
        }
      ]
    }

定义另一个使用先前定义的内部管道的管道：

    
    
    response = client.ingest.put_pipeline(
      id: 'pipelineB',
      body: {
        description: 'outer pipeline',
        processors: [
          {
            pipeline: {
              name: 'pipelineA'
            }
          },
          {
            set: {
              field: 'outer_pipeline_set',
              value: 'outer'
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT _ingest/pipeline/pipelineB
    {
      "description" : "outer pipeline",
      "processors" : [
        {
          "pipeline" : {
            "name": "pipelineA"
          }
        },
        {
          "set" : {
            "field": "outer_pipeline_set",
            "value": "outer"
          }
        }
      ]
    }

现在，在应用外部管道时为文档编制索引将看到从外部管道执行的内部管道：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      pipeline: 'pipelineB',
      body: {
        field: 'value'
      }
    )
    puts response
    
    
    PUT /my-index-000001/_doc/1?pipeline=pipelineB
    {
      "field": "value"
    }

来自索引请求的响应：

    
    
    {
      "_index": "my-index-000001",
      "_id": "1",
      "_version": 1,
      "result": "created",
      "_shards": {
        "total": 2,
        "successful": 1,
        "failed": 0
      },
      "_seq_no": 66,
      "_primary_term": 1
    }

索引文档：

    
    
    {
      "field": "value",
      "inner_pipeline_set": "inner",
      "outer_pipeline_set": "outer"
    }

[« Network direction processor](network-direction-processor.md) [Redact
processor »](redact-processor.md)
