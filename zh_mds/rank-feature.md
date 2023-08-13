

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Range field types](range.md) [Rank features field type »](rank-
features.md)

## 排名要素字段类型

"rank_feature"字段可以索引数字，以便以后可以使用它们在具有"rank_feature"查询的查询中提升文档。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            pagerank: {
              type: 'rank_feature'
            },
            url_length: {
              type: 'rank_feature',
              positive_score_impact: false
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        pagerank: 8,
        url_length: 22
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          rank_feature: {
            field: 'pagerank'
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "pagerank": {
            "type": "rank_feature" __},
          "url_length": {
            "type": "rank_feature",
            "positive_score_impact": false __}
        }
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "pagerank": 8,
      "url_length": 22
    }
    
    GET my-index-000001/_search
    {
      "query": {
        "rank_feature": {
          "field": "pagerank"
        }
      }
    }

__

|

排名特征字段必须使用"rank_feature"字段类型 ---|--- __

|

与分数负相关的排名要素需要声明为"rank_feature"字段仅支持单值字段和严格的正值。多值字段和负值将被拒绝。

"rank_feature"字段不支持查询、排序或聚合。它们只能在"rank_feature"查询中使用。

"rank_feature"字段仅保留 9 个有效位的精度，这意味着相对误差约为 0.4%。

与分数呈负相关的排名要素应将"positive_score_impact"设置为"false"(默认为"true")。"rank_feature"查询将使用此方法修改评分公式，使分数随特征值而降低而不是增加。例如，在网络搜索中，url长度是一个常用的功能，它与分数呈负相关。

[« Range field types](range.md) [Rank features field type »](rank-
features.md)
