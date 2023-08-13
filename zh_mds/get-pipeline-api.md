

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Ingest APIs](ingest-apis.md)

[« GeoIP stats API](geoip-stats-api.md) [Simulate pipeline API »](simulate-
pipeline-api.md)

## 获取管道接口

返回有关一个或多个引入管道的信息。此 API 返回管道的本地引用。

    
    
    response = client.ingest.get_pipeline(
      id: 'my-pipeline-id'
    )
    puts response
    
    
    GET /_ingest/pipeline/my-pipeline-id

###Request

'获取/_ingest/管道/<pipeline>'

'获取/_ingest/管道'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"read_pipeline"、"manage_pipeline"、"manage_ingest_pipelines"或"管理"集群权限才能使用此 API。

### 路径参数

`<pipeline>`

    

(可选，字符串)要检索的管道 ID 的逗号分隔列表。支持通配符 ('*') 表达式。

若要获取所有引入管道，请省略此参数或使用"*"。

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

#### 获取特定引入管道的信息

    
    
    response = client.ingest.get_pipeline(
      id: 'my-pipeline-id'
    )
    puts response
    
    
    GET /_ingest/pipeline/my-pipeline-id

API 返回以下响应：

    
    
    {
      "my-pipeline-id" : {
        "description" : "describe pipeline",
        "version" : 123,
        "processors" : [
          {
            "set" : {
              "field" : "foo",
              "value" : "bar"
            }
          }
        ]
      }
    }

[« GeoIP stats API](geoip-stats-api.md) [Simulate pipeline API »](simulate-
pipeline-api.md)
