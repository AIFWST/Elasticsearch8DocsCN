

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Enrich your data](ingest-enriching-data.md)

[« Set up an enrich processor](enrich-setup.md) [Example: Enrich your data
based on exact values »](match-enrich-policy-type.md)

## 示例：根据地理位置丰富数据

"geo_match"扩充策略使用"geo_shape"查询，根据地理位置将扩充数据与传入文档进行匹配。

以下示例创建一个"geo_match"扩充策略，该策略根据一组坐标向传入文档添加邮政编码。然后，它将"geo_match"扩充策略添加到引入管道中的处理器。

使用创建索引 API 创建至少包含一个"geo_shape"字段的源索引。

    
    
    response = client.indices.create(
      index: 'postal_codes',
      body: {
        mappings: {
          properties: {
            location: {
              type: 'geo_shape'
            },
            postal_code: {
              type: 'keyword'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /postal_codes
    {
      "mappings": {
        "properties": {
          "location": {
            "type": "geo_shape"
          },
          "postal_code": {
            "type": "keyword"
          }
        }
      }
    }

使用索引 API 将扩充数据索引到此源索引。

    
    
    response = client.index(
      index: 'postal_codes',
      id: 1,
      refresh: 'wait_for',
      body: {
        location: {
          type: 'envelope',
          coordinates: [
            [
              13,
              53
            ],
            [
              14,
              52
            ]
          ]
        },
        postal_code: '96598'
      }
    )
    puts response
    
    
    PUT /postal_codes/_doc/1?refresh=wait_for
    {
      "location": {
        "type": "envelope",
        "coordinates": [ [ 13.0, 53.0 ], [ 14.0, 52.0 ] ]
      },
      "postal_code": "96598"
    }

使用创建扩充策略 API 创建具有"geo_match"策略类型的扩充策略。此策略必须包括：

* 一个或多个源索引 * "match_field"，源索引中用于匹配传入文档的"geo_shape"字段 * 从要附加到传入文档的源索引中丰富字段

    
    
    response = client.enrich.put_policy(
      name: 'postal_policy',
      body: {
        geo_match: {
          indices: 'postal_codes',
          match_field: 'location',
          enrich_fields: [
            'location',
            'postal_code'
          ]
        }
      }
    )
    puts response
    
    
    PUT /_enrich/policy/postal_policy
    {
      "geo_match": {
        "indices": "postal_codes",
        "match_field": "location",
        "enrich_fields": [ "location", "postal_code" ]
      }
    }

使用执行扩充策略 API 为策略创建扩充索引。

    
    
    POST /_enrich/policy/postal_policy/_execute

使用创建或更新管道 API 创建引入管道。在管道中，添加包括以下内容的扩充处理器：

* 您的扩充策略。  * 传入文档的"字段"，用于匹配扩充索引中文档的地理形状。  * 用于存储传入文档的追加扩充数据的"target_field"。此字段包含在扩充策略中指定的"match_field"和"enrich_fields"。  * "shape_relation"，指示处理器如何将传入文档中的地理形状与丰富索引文档中的地理形状进行匹配。有关有效选项和详细信息，请参阅空间关系。

    
    
    PUT /_ingest/pipeline/postal_lookup
    {
      "processors": [
        {
          "enrich": {
            "description": "Add 'geo_data' based on 'geo_location'",
            "policy_name": "postal_policy",
            "field": "geo_location",
            "target_field": "geo_data",
            "shape_relation": "INTERSECTS"
          }
        }
      ]
    }

使用引入管道为文档编制索引。传入文档应包括在扩充处理器中指定的"字段"。

    
    
    PUT /users/_doc/0?pipeline=postal_lookup
    {
      "first_name": "Mardy",
      "last_name": "Brown",
      "geo_location": "POINT (13.5 52.5)"
    }

若要验证扩充处理器是否匹配并附加了相应的字段数据，请使用 get API 查看索引文档。

    
    
    response = client.get(
      index: 'users',
      id: 0
    )
    puts response
    
    
    GET /users/_doc/0

API 返回以下响应：

    
    
    {
      "found": true,
      "_index": "users",
      "_id": "0",
      "_version": 1,
      "_seq_no": 55,
      "_primary_term": 1,
      "_source": {
        "geo_data": {
          "location": {
            "type": "envelope",
            "coordinates": [[13.0, 53.0], [14.0, 52.0]]
          },
          "postal_code": "96598"
        },
        "first_name": "Mardy",
        "last_name": "Brown",
        "geo_location": "POINT (13.5 52.5)"
      }
    }

[« Set up an enrich processor](enrich-setup.md) [Example: Enrich your data
based on exact values »](match-enrich-policy-type.md)
