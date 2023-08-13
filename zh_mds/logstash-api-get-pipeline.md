

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Logstash APIs](logstash-apis.md)

[« Delete Logstash pipeline API](logstash-api-delete-pipeline.md) [Machine
learning APIs »](ml-apis.md)

## 获取管道接口

此 API 检索用于 Logstash 集中管理的管道。

###Request

"获取_logstash/管道"

"获取_logstash/管道/<pipeline_id>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_logstash_pipelines"集群权限才能使用此 API。

###Description

检索一个或多个日志存储管道。

### 路径参数

`<pipeline_id>`

     (Optional, string) Comma-separated list of pipeline identifiers. 

###Examples

以下示例检索名为"my_pipeline"的管道：

    
    
    response = client.logstash.get_pipeline(
      id: 'my_pipeline'
    )
    puts response
    
    
    GET _logstash/pipeline/my_pipeline

如果请求成功，则响应正文包含管道定义：

    
    
    {
      "my_pipeline": {
        "description": "Sample pipeline for illustration purposes",
        "last_modified": "2021-01-02T02:50:51.250Z",
        "pipeline_metadata": {
          "type": "logstash_pipeline",
          "version": "1"
        },
        "username": "elastic",
        "pipeline": "input {}\n filter { grok {} }\n output {}",
        "pipeline_settings": {
          "pipeline.workers": 1,
          "pipeline.batch.size": 125,
          "pipeline.batch.delay": 50,
          "queue.type": "memory",
          "queue.max_bytes": "1gb",
          "queue.checkpoint.writes": 1024
        }
      }
    }

[« Delete Logstash pipeline API](logstash-api-delete-pipeline.md) [Machine
learning APIs »](ml-apis.md)
