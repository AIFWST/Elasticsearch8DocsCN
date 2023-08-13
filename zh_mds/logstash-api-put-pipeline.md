

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Logstash APIs](logstash-apis.md)

[« Logstash APIs](logstash-apis.md) [Delete Logstash pipeline API
»](logstash-api-delete-pipeline.md)

## 创建或更新 Logstash 管道API

此 API 创建或更新用于 Logstash CentralManagement 的 Logstash 管道。

###Request

"放置_logstash/管道/<pipeline_id>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_logstash_pipelines"集群权限才能使用此 API。

###Description

创建日志存储管道。如果指定的管道存在，则会替换该管道。

### 路径参数

`<pipeline_id>`

     (Required, string) Identifier for the pipeline. 

### 请求正文

`description`

     (Optional, string) Description of the pipeline. This description is not used by Elasticsearch or Logstash. 
`last_modified`

     (Required, string) Date the pipeline was last updated. Must be in the `yyyy-MM-dd'T'HH:mm:ss.SSSZZ` [`strict_date_time`](mapping-date-format.html "format") format. 
`pipeline`

     (Required, string) Configuration for the pipeline. For supported syntax, see the [Logstash configuration documentation](/guide/en/logstash/8.9/configuration-file-structure.html). 
`pipeline_metadata`

     (Required, object) Optional metadata about the pipeline. May have any contents. This metadata is not generated or used by Elasticsearch or Logstash. 
`pipeline_settings`

     (Required, object) Settings for the pipeline. Supports only flat keys in dot notation. For supported settings, see the [Logstash settings documentation](/guide/en/logstash/8.9/logstash-settings-file.html). 
`username`

     (Required, string) User who last updated the pipeline. 

###Examples

以下示例创建一个名为"my_pipeline"的新管道：

    
    
    PUT _logstash/pipeline/my_pipeline
    {
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

如果请求成功，您将收到一个空响应，其中包含适当的状态代码。

[« Logstash APIs](logstash-apis.md) [Delete Logstash pipeline API
»](logstash-api-delete-pipeline.md)
