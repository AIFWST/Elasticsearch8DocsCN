

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Logstash APIs](logstash-apis.md)

[« Create or update Logstash pipeline API](logstash-api-put-pipeline.md)
[Get pipeline API »](logstash-api-get-pipeline.md)

## 删除日志存储管道API

此 API 删除用于 Logstash 集中管理的管道。

###Request

"删除_logstash/管道/<pipeline_id>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_logstash_pipelines"集群权限才能使用此 API。

###Description

删除日志存储管道。

### 路径参数

`<pipeline_id>`

     (Required, string) Identifier for the Pipeline. 

###Examples

以下示例删除名为"my_pipeline"的管道：

    
    
    response = client.logstash.delete_pipeline(
      id: 'my_pipeline'
    )
    puts response
    
    
    DELETE _logstash/pipeline/my_pipeline

如果请求成功，您将收到一个空响应，其中包含适当的状态代码。

[« Create or update Logstash pipeline API](logstash-api-put-pipeline.md)
[Get pipeline API »](logstash-api-get-pipeline.md)
