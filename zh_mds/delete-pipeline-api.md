

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Ingest APIs](ingest-apis.md)

[« Create or update pipeline API](put-pipeline-api.md) [GeoIP stats API
»](geoip-stats-api.md)

## 删除管道接口

删除一个或多个现有引入管道。

    
    
    response = client.ingest.delete_pipeline(
      id: 'my-pipeline-id'
    )
    puts response
    
    
    DELETE /_ingest/pipeline/my-pipeline-id

###Request

"删除/_ingest/管道/<pipeline>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_pipeline"、"manage_ingest_pipelines"或"管理"集群权限才能使用此 API。

### 路径参数

`<pipeline>`

    

(必需，字符串)用于限制请求的管道 ID 或管道 ID 的通配符表达式。

要删除集群中的所有引入管道，请使用值"*"。

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

#### 删除特定引入管道

    
    
    response = client.ingest.delete_pipeline(
      id: 'pipeline-one'
    )
    puts response
    
    
    DELETE /_ingest/pipeline/pipeline-one

#### 使用通配符表达式删除引入管道

    
    
    response = client.ingest.delete_pipeline(
      id: 'pipeline-*'
    )
    puts response
    
    
    DELETE /_ingest/pipeline/pipeline-*

#### 删除所有引入管道

    
    
    response = client.ingest.delete_pipeline(
      id: '*'
    )
    puts response
    
    
    DELETE /_ingest/pipeline/*

[« Create or update pipeline API](put-pipeline-api.md) [GeoIP stats API
»](geoip-stats-api.md)
