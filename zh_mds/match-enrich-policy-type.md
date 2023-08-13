

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Enrich your data](ingest-enriching-data.md)

[« Example: Enrich your data based on geolocation](geo-match-enrich-policy-
type.md) [Example: Enrich your data by matching a value to a range »](range-
enrich-policy-type.md)

## 示例：根据精确值丰富数据

"匹配"扩充策略使用"术语"查询，根据确切值(如电子邮件地址或 ID)将扩充数据与传入文档匹配。

以下示例创建一个"匹配"扩充策略，该策略根据电子邮件地址将用户名和联系信息添加到传入文档。然后，它将"匹配"扩充策略添加到摄取管道中的处理器。

使用创建索引 API 或索引 API 创建源索引。

以下索引 API 请求创建一个源索引，并将新文档索引到该索引。

    
    
    response = client.index(
      index: 'users',
      id: 1,
      refresh: 'wait_for',
      body: {
        email: 'mardy.brown@asciidocsmith.com',
        first_name: 'Mardy',
        last_name: 'Brown',
        city: 'New Orleans',
        county: 'Orleans',
        state: 'LA',
        zip: 70_116,
        web: 'mardy.asciidocsmith.com'
      }
    )
    puts response
    
    
    PUT /users/_doc/1?refresh=wait_for
    {
      "email": "mardy.brown@asciidocsmith.com",
      "first_name": "Mardy",
      "last_name": "Brown",
      "city": "New Orleans",
      "county": "Orleans",
      "state": "LA",
      "zip": 70116,
      "web": "mardy.asciidocsmith.com"
    }

使用创建扩充策略 API 创建具有"匹配"策略类型的扩充策略。此策略必须包括：

* 一个或多个源索引 * "match_field"，源索引中用于匹配传入文档的字段 * 丰富要附加到传入文档的源索引中的字段

    
    
    response = client.enrich.put_policy(
      name: 'users-policy',
      body: {
        match: {
          indices: 'users',
          match_field: 'email',
          enrich_fields: [
            'first_name',
            'last_name',
            'city',
            'zip',
            'state'
          ]
        }
      }
    )
    puts response
    
    
    PUT /_enrich/policy/users-policy
    {
      "match": {
        "indices": "users",
        "match_field": "email",
        "enrich_fields": ["first_name", "last_name", "city", "zip", "state"]
      }
    }

使用执行扩充策略 API 为策略创建扩充索引。

    
    
    POST /_enrich/policy/users-policy/_execute

使用创建或更新管道 API 创建引入管道。在管道中，添加包括以下内容的扩充处理器：

* 您的扩充策略。  * 传入文档的"字段"，用于匹配扩充索引中的文档。  * 用于存储传入文档的追加扩充数据的"target_field"。此字段包含在扩充策略中指定的"match_field"和"enrich_fields"。

    
    
    PUT /_ingest/pipeline/user_lookup
    {
      "processors" : [
        {
          "enrich" : {
            "description": "Add 'user' data based on 'email'",
            "policy_name": "users-policy",
            "field" : "email",
            "target_field": "user",
            "max_matches": "1"
          }
        }
      ]
    }

使用引入管道为文档编制索引。传入文档应包括在扩充处理器中指定的"字段"。

    
    
    PUT /my-index-000001/_doc/my_id?pipeline=user_lookup
    {
      "email": "mardy.brown@asciidocsmith.com"
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
      "found": true,
      "_index": "my-index-000001",
      "_id": "my_id",
      "_version": 1,
      "_seq_no": 55,
      "_primary_term": 1,
      "_source": {
        "user": {
          "email": "mardy.brown@asciidocsmith.com",
          "first_name": "Mardy",
          "last_name": "Brown",
          "zip": 70116,
          "city": "New Orleans",
          "state": "LA"
        },
        "email": "mardy.brown@asciidocsmith.com"
      }
    }

[« Example: Enrich your data based on geolocation](geo-match-enrich-policy-
type.md) [Example: Enrich your data by matching a value to a range »](range-
enrich-policy-type.md)
