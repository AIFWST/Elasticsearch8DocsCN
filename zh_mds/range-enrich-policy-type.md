

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Enrich your data](ingest-enriching-data.md)

[« Example: Enrich your data based on exact values](match-enrich-policy-
type.md) [Ingest processor reference »](processors.md)

## 示例：通过将值与范围匹配来丰富数据

"范围"扩充策略使用"term"查询将传入文档中的数字、日期或 IP 地址与扩充索引中相同类型的范围进行匹配。不支持将范围与范围匹配。

以下示例创建一个"范围"扩充策略，该策略根据 IP 地址向传入文档添加描述性网络名称和负责部门。然后，它将扩充策略添加到引入管道中的处理器。

使用具有适当映射的创建索引 API 来创建源索引。

    
    
    response = client.indices.create(
      index: 'networks',
      body: {
        mappings: {
          properties: {
            range: {
              type: 'ip_range'
            },
            name: {
              type: 'keyword'
            },
            department: {
              type: 'keyword'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /networks
    {
      "mappings": {
        "properties": {
          "range": { "type": "ip_range" },
          "name": { "type": "keyword" },
          "department": { "type": "keyword" }
        }
      }
    }

以下索引 API 请求将新文档索引到该索引。

    
    
    response = client.index(
      index: 'networks',
      id: 1,
      refresh: 'wait_for',
      body: {
        range: '10.100.0.0/16',
        name: 'production',
        department: 'OPS'
      }
    )
    puts response
    
    
    PUT /networks/_doc/1?refresh=wait_for
    {
      "range": "10.100.0.0/16",
      "name": "production",
      "department": "OPS"
    }

使用创建扩充策略 API 创建具有"范围"策略类型的扩充策略。此策略必须包括：

* 一个或多个源索引 * "match_field"，源索引中用于匹配传入文档的字段 * 丰富要附加到传入文档的源索引中的字段

由于我们计划根据 IP 地址丰富文档，因此策略的"match_field"必须是"ip_range"字段。

    
    
    response = client.enrich.put_policy(
      name: 'networks-policy',
      body: {
        range: {
          indices: 'networks',
          match_field: 'range',
          enrich_fields: [
            'name',
            'department'
          ]
        }
      }
    )
    puts response
    
    
    PUT /_enrich/policy/networks-policy
    {
      "range": {
        "indices": "networks",
        "match_field": "range",
        "enrich_fields": ["name", "department"]
      }
    }

使用执行扩充策略 API 为策略创建扩充索引。

    
    
    POST /_enrich/policy/networks-policy/_execute

使用创建或更新管道 API 创建引入管道。在管道中，添加包括以下内容的扩充处理器：

* 您的扩充策略。  * 传入文档的"字段"，用于匹配扩充索引中的文档。  * 用于存储传入文档的追加扩充数据的"target_field"。此字段包含在扩充策略中指定的"match_field"和"enrich_fields"。

    
    
    PUT /_ingest/pipeline/networks_lookup
    {
      "processors" : [
        {
          "enrich" : {
            "description": "Add 'network' data based on 'ip'",
            "policy_name": "networks-policy",
            "field" : "ip",
            "target_field": "network",
            "max_matches": "10"
          }
        }
      ]
    }

使用引入管道为文档编制索引。传入文档应包括在扩充处理器中指定的"字段"。

    
    
    PUT /my-index-000001/_doc/my_id?pipeline=networks_lookup
    {
      "ip": "10.100.34.1"
    }

若要验证扩充处理器是否匹配并附加了相应的字段数据，请使用 get API 查看索引文档。

    
    
    response = client.get(
      index: 'my-index-000001',
      id: 'my_id'
    )
    puts response
    
    
    GET /my-index-000001/_doc/my_id

API 返回以下响应：

    
    
    {
      "_index" : "my-index-000001",
      "_id" : "my_id",
      "_version" : 1,
      "_seq_no" : 0,
      "_primary_term" : 1,
      "found" : true,
      "_source" : {
        "ip" : "10.100.34.1",
        "network" : [
          {
            "name" : "production",
            "range" : "10.100.0.0/16",
            "department" : "OPS"
          }
        ]
      }
    }

[« Example: Enrich your data based on exact values](match-enrich-policy-
type.md) [Ingest processor reference »](processors.md)
