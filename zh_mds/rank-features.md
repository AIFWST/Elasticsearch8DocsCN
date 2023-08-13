

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Rank feature field type](rank-feature.md) [Search-as-you-type field type
»](search-as-you-type.md)

## 排名功能字段类型

"rank_features"字段可以为数字特征向量编制索引，以便它们后来可用于通过"rank_feature"查询提升查询中的文档。

它类似于"rank_feature"数据类型，但更适合于要素列表稀疏的情况，因此在每个要素的映射中添加一个字段是不合理的。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            topics: {
              type: 'rank_features'
            },
            negative_reviews: {
              type: 'rank_features',
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
        topics: {
          politics: 20,
          economics: 50.8
        },
        negative_reviews: {
          "1star": 10,
          "2star": 100
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      body: {
        topics: {
          politics: 5.2,
          sports: 80.1
        },
        negative_reviews: {
          "1star": 1,
          "2star": 10
        }
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          rank_feature: {
            field: 'topics.politics'
          }
        }
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          rank_feature: {
            field: 'negative_reviews.1star'
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "topics": {
            "type": "rank_features" __},
          "negative_reviews" : {
            "type": "rank_features",
            "positive_score_impact": false __}
        }
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "topics": { __"politics": 20,
        "economics": 50.8
      },
      "negative_reviews": {
        "1star": 10,
        "2star": 100
      }
    }
    
    PUT my-index-000001/_doc/2
    {
      "topics": {
        "politics": 5.2,
        "sports": 80.1
      },
      "negative_reviews": {
        "1star": 1,
        "2star": 10
      }
    }
    
    GET my-index-000001/_search
    {
      "query": { __"rank_feature": {
          "field": "topics.politics"
        }
      }
    }
    
    GET my-index-000001/_search
    {
      "query": { __"rank_feature": {
          "field": "negative_reviews.1star"
        }
      }
    }

__

|

排名要素字段必须使用"rank_features"字段类型 ---|--- __

|

与分数负相关的排名特征需要声明 __

|

排名要素字段必须是具有字符串键和严格正数值 __ 的哈希

|

此查询按文档与"政治"主题的关系对文档进行排名。   __

|

此查询对文档的排名与收到的"1 星"评论数成反比。   "rank_features"字段仅支持单值特征和严格正值。多值字段和零值或负值将被拒绝。

"rank_features"字段不支持排序或聚合，只能使用"rank_feature"或"term"查询进行查询。

对"rank_features"字段的"term"查询通过将匹配的存储特征值乘以提供的"boost"来评分。

"rank_features"字段仅保留 9 个有效位的精度，这意味着相对误差约为 0.4%。

与分数呈负相关的排名要素应将"positive_score_impact"设置为"false"(默认为"true")。"rank_feature"查询将使用此方法修改评分公式，使分数随特征值而降低而不是增加。

[« Rank feature field type](rank-feature.md) [Search-as-you-type field type
»](search-as-you-type.md)
