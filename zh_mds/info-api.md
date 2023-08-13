

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md)

[« Simulate pipeline API](simulate-pipeline-api.md) [Licensing APIs
»](licensing-apis.md)

## 信息接口

提供有关已安装的 X-Pack 功能的一般信息。

###Request

"得到/_xpack"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

###Description

此 API 提供的信息包括：

* 内部版本信息 - 包括内部版本号和时间戳。  * 许可证信息 - 有关当前安装的许可证的基本信息。  * 功能信息 - 当前许可证下当前启用和可用的功能。

### 路径参数

`categories`

     (Optional, list) A comma-separated list of the information categories to include in the response. For example, `build,license,features`. 
`human`

     (Optional, Boolean) Defines whether additional human-readable information is included in the response. In particular, it adds descriptions and a tag line. The default value is `true`. 

###Examples

以下示例查询信息 API：

    
    
    response = client.xpack.info
    puts response
    
    
    GET /_xpack

示例响应：

    
    
    {
       "build" : {
          "hash" : "2798b1a3ce779b3611bb53a0082d4d741e4d3168",
          "date" : "2015-04-07T13:34:42Z"
       },
       "license" : {
          "uid" : "893361dc-9749-4997-93cb-xxx",
          "type" : "trial",
          "mode" : "trial",
          "status" : "active",
          "expiry_date_in_millis" : 1542665112332
       },
       "features" : {
          "ccr" : {
            "available" : true,
            "enabled" : true
          },
         "aggregate_metric" : {
              "available" : true,
              "enabled" : true
          },
          "analytics" : {
              "available" : true,
              "enabled" : true
          },
          "archive" : {
              "available" : true,
              "enabled" : true
          },
          "enrich" : {
              "available" : true,
              "enabled" : true
          },
          "frozen_indices" : {
             "available" : true,
             "enabled" : true
          },
          "graph" : {
             "available" : true,
             "enabled" : true
          },
          "ilm" : {
             "available" : true,
             "enabled" : true
          },
          "logstash" : {
             "available" : true,
             "enabled" : true
          },
          "ml" : {
             "available" : true,
             "enabled" : true
          },
          "monitoring" : {
             "available" : true,
             "enabled" : true
          },
          "rollup": {
             "available": true,
             "enabled": true
          },
          "searchable_snapshots" : {
             "available" : true,
             "enabled" : true
          },
          "security" : {
             "available" : true,
             "enabled" : false
          },
          "slm" : {
             "available" : true,
             "enabled" : true
          },
          "spatial" : {
             "available" : true,
             "enabled" : true
          },
          "eql" : {
             "available" : true,
             "enabled" : true
          },
          "sql" : {
             "available" : true,
             "enabled" : true
          },
          "transform" : {
             "available" : true,
             "enabled" : true
          },
          "voting_only" : {
             "available" : true,
             "enabled" : true
          },
          "watcher" : {
             "available" : true,
             "enabled" : true
          },
          "data_streams" : {
             "available" : true,
             "enabled" : true
          },
          "data_tiers" : {
             "available" : true,
             "enabled" : true
          },
          "enterprise_search": {
             "available": true,
             "enabled": true
          }
       },
       "tagline" : "You know, for X"
    }

以下示例仅返回生成和功能信息：

    
    
    response = client.xpack.info(
      categories: 'build,features'
    )
    puts response
    
    
    GET /_xpack?categories=build,features

以下示例从响应中删除说明：

    
    
    response = client.xpack.info(
      human: false
    )
    puts response
    
    
    GET /_xpack?human=false

[« Simulate pipeline API](simulate-pipeline-api.md) [Licensing APIs
»](licensing-apis.md)
