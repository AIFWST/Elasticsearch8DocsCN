

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Specialized queries](specialized-queries.md)

[« Percolate query](query-dsl-percolate-query.md) [Script query »](query-
dsl-script-query.md)

## 排名功能查询

根据"rank_feature"或"rank_features"字段的数值提高文档的相关性分数。

"rank_feature"查询通常用于"bool"查询的"should"子句，因此其相关性分数将添加到"bool"查询中的其他分数中。

将"rank_feature"或"rank_features"字段的"positive_score_impact"设置为"false"，我们建议参与 aquery 的每个文档都具有此字段的值。否则，如果在 should 子句中使用"rank_feature"查询，它不会向缺少值的文档分数添加任何内容，但会为包含功能的文档增加一些提升。这与我们想要的相反 - 由于我们认为这些功能是负面的，我们希望将包含它们的文档排名低于缺少它们的文档。

与"function_score"查询或其他更改相关性分数的方法不同，当"track_total_hits"参数"不"为真"时，"rank_feature"查询会有效地跳过非竞争性命中。这可以显著提高查询速度。

### 对功能函数进行排名

要根据排名特征字段计算相关性分数，"rank_feature"查询支持以下数学函数：

* 饱和度 * 对数 * S形 * 线性

如果您不知道从哪里开始，我们建议您使用"饱和"功能。如果未提供任何函数，则默认情况下，"rank_feature"查询使用"饱和度"函数。

### 示例请求

#### 索引设置

要使用"rank_feature"查询，索引必须包含"rank_feature"或"rank_features"字段映射。若要了解如何为"rank_feature"查询设置索引，请尝试以下示例。

使用以下字段映射创建"测试"索引：

* "pagerank"，一个衡量网站重要性的"rank_feature"字段 * "url_length"，一个包含网站URL长度的"rank_feature"字段。在本例中，长 URL 与相关性呈负相关，由"positive_score_impact"值"false"表示。  * "主题"，一个"rank_features"字段，其中包含主题列表以及每个文档与此主题的联系程度的度量

    
    
    response = client.indices.create(
      index: 'test',
      body: {
        mappings: {
          properties: {
            pagerank: {
              type: 'rank_feature'
            },
            url_length: {
              type: 'rank_feature',
              positive_score_impact: false
            },
            topics: {
              type: 'rank_features'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /test
    {
      "mappings": {
        "properties": {
          "pagerank": {
            "type": "rank_feature"
          },
          "url_length": {
            "type": "rank_feature",
            "positive_score_impact": false
          },
          "topics": {
            "type": "rank_features"
          }
        }
      }
    }

将多个文档索引到"测试"索引。

    
    
    response = client.index(
      index: 'test',
      id: 1,
      refresh: true,
      body: {
        url: 'https://en.wikipedia.org/wiki/2016_Summer_Olympics',
        content: 'Rio 2016',
        pagerank: 50.3,
        url_length: 42,
        topics: {
          sports: 50,
          brazil: 30
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'test',
      id: 2,
      refresh: true,
      body: {
        url: 'https://en.wikipedia.org/wiki/2016_Brazilian_Grand_Prix',
        content: 'Formula One motor race held on 13 November 2016',
        pagerank: 50.3,
        url_length: 47,
        topics: {
          sports: 35,
          "formula one": 65,
          brazil: 20
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'test',
      id: 3,
      refresh: true,
      body: {
        url: 'https://en.wikipedia.org/wiki/Deadpool_(film)',
        content: 'Deadpool is a 2016 American superhero film',
        pagerank: 50.3,
        url_length: 37,
        topics: {
          movies: 60,
          "super hero": 65
        }
      }
    )
    puts response
    
    
    PUT /test/_doc/1?refresh
    {
      "url": "https://en.wikipedia.org/wiki/2016_Summer_Olympics",
      "content": "Rio 2016",
      "pagerank": 50.3,
      "url_length": 42,
      "topics": {
        "sports": 50,
        "brazil": 30
      }
    }
    
    PUT /test/_doc/2?refresh
    {
      "url": "https://en.wikipedia.org/wiki/2016_Brazilian_Grand_Prix",
      "content": "Formula One motor race held on 13 November 2016",
      "pagerank": 50.3,
      "url_length": 47,
      "topics": {
        "sports": 35,
        "formula one": 65,
        "brazil": 20
      }
    }
    
    PUT /test/_doc/3?refresh
    {
      "url": "https://en.wikipedia.org/wiki/Deadpool_(film)",
      "content": "Deadpool is a 2016 American superhero film",
      "pagerank": 50.3,
      "url_length": 37,
      "topics": {
        "movies": 60,
        "super hero": 65
      }
    }

#### 示例查询

以下查询搜索"2016"，并根据"pagerank"、"url_length"和"体育"主题提高相关性分数。

    
    
    GET /test/_search
    {
      "query": {
        "bool": {
          "must": [
            {
              "match": {
                "content": "2016"
              }
            }
          ],
          "should": [
            {
              "rank_feature": {
                "field": "pagerank"
              }
            },
            {
              "rank_feature": {
                "field": "url_length",
                "boost": 0.1
              }
            },
            {
              "rank_feature": {
                "field": "topics.sports",
                "boost": 0.4
              }
            }
          ]
        }
      }
    }

### rank_feature"的顶级参数

`field`

     (Required, string) [`rank_feature`](rank-feature.html "Rank feature field type") or [`rank_features`](rank-features.html "Rank features field type") field used to boost [relevance scores](query-filter-context.html#relevance-scores "Relevance scores"). 
`boost`

    

(可选，浮动)用于降低或增加相关性分数的浮点数。默认为"1.0"。

提升值相对于默认值"1.0"。介于"0"和"1.0"之间的提升值会降低相关性分数。大于"1.0"的值会增加相关性分数。

`saturation`

    

(可选，函数对象)饱和度函数，用于根据排名功能"字段"的值提高相关性分数。如果未提供任何函数，则"rank_feature"查询默认为"饱和"函数。有关详细信息，请参阅饱和度。

只能提供一个功能"饱和"、"对数"、"sigmoid"或"线性"。

`log`

    

(可选，函数对象)对数函数，用于根据排名特征"字段"的值提高相关性分数。有关详细信息，请参阅对数。

只能提供一个功能"饱和"、"对数"、"sigmoid"或"线性"。

`sigmoid`

    

(可选，函数对象)Sigmoid 函数用于根据排名特征"字段"的值提高相关性分数。有关详细信息，请参阅 Sigmoid。

只能提供一个功能"饱和"、"对数"、"sigmoid"或"线性"。

`linear`

    

(可选，函数对象)线性函数，用于根据排名特征"字段"的值提高相关性分数。有关详细信息，请参阅线性。

只能提供一个功能"饱和"、"对数"、"sigmoid"或"线性"。

###Notes

####Saturation

"饱和度"函数给出的分数等于"S / (S + pivot)"，其中"S"是排名特征字段的值，"pivot"是可配置的枢轴值，因此如果"S"小于枢轴，则结果将小于"0.5"，否则大于"0.5"。分数始终为"(0，1)"。

如果排名特征具有负分数影响，则该函数将计算为"枢轴/(S + 枢轴)"，当"S"增加时会减少。

    
    
    GET /test/_search
    {
      "query": {
        "rank_feature": {
          "field": "pagerank",
          "saturation": {
            "pivot": 8
          }
        }
      }
    }

如果未提供"透视"值，Elasticsearch 将计算一个默认值，该值等于索引中所有排名特征值的近似几何平均值。如果您没有机会训练良好的透视值，我们建议使用此默认值。

    
    
    GET /test/_search
    {
      "query": {
        "rank_feature": {
          "field": "pagerank",
          "saturation": {}
        }
      }
    }

####Logarithm

"log"函数给出的分数等于"log(scaling_factor + S)"，其中"S"是排名特征字段的值，"scaling_factor"是可配置的缩放因子。分数是无限的。

此函数仅支持对分数产生积极影响的排名功能。

    
    
    GET /test/_search
    {
      "query": {
        "rank_feature": {
          "field": "pagerank",
          "log": {
            "scaling_factor": 4
          }
        }
      }
    }

####Sigmoid

"sigmoid"函数是"饱和度"的扩展，它增加了可配置的指数。分数计算为"S^exp^ / (S^exp^ +pivot^exp^)"。与"饱和度"函数一样，"枢轴"是"S"的值，得分为"0.5"，分数为"(0，1)"。

"指数"必须是正数，通常为"[0.5， 1]"。应通过训练来计算良好的值。如果您没有机会这样做，我们建议您改用"饱和"功能。

    
    
    GET /test/_search
    {
      "query": {
        "rank_feature": {
          "field": "pagerank",
          "sigmoid": {
            "pivot": 7,
            "exponent": 0.6
          }
        }
      }
    }

####Linear

"线性"函数是最简单的函数，给出的分数等于索引值"S"，其中"S"是排名特征字段的值。如果 arank 特征字段以 '"positive_score_impact"： true' 为索引，则其索引值等于 'S' 并四舍五入以仅保留 9 个有效位以获得精度。如果排名特征字段的索引为"positive_score_impact"： false，则其索引值等于"1/S"并四舍五入以仅保留 9 个有效位的精度。

    
    
    GET /test/_search
    {
      "query": {
        "rank_feature": {
          "field": "pagerank",
          "linear": {}
        }
      }
    }

[« Percolate query](query-dsl-percolate-query.md) [Script query »](query-
dsl-script-query.md)
