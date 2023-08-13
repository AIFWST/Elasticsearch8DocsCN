

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Search your
data](search-your-data.md)

[« Collapse search results](collapse-search-results.md) [Highlighting
»](highlighting.md)

## 筛选搜索结果

您可以使用两种方法筛选搜索结果：

* 使用带有"filter"子句的布尔查询。搜索请求将布尔筛选器应用于搜索命中和聚合。  * 使用搜索 API 的"post_filter"参数。搜索请求仅将帖子过滤器应用于搜索匹配，而不应用于聚合。可以使用后置筛选器根据更广泛的结果集计算聚合，然后进一步缩小结果范围。

您还可以在帖子过滤器之后对匹配进行重新评分，以提高相关性并重新排序结果。

### 后置过滤器

当您使用"post_filter"参数筛选搜索结果时，系统会在计算聚合后过滤搜索命中。后置过滤器对聚合结果没有影响。

例如，您销售的衬衫具有以下属性：

    
    
    response = client.indices.create(
      index: 'shirts',
      body: {
        mappings: {
          properties: {
            brand: {
              type: 'keyword'
            },
            color: {
              type: 'keyword'
            },
            model: {
              type: 'keyword'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'shirts',
      id: 1,
      refresh: true,
      body: {
        brand: 'gucci',
        color: 'red',
        model: 'slim'
      }
    )
    puts response
    
    
    PUT /shirts
    {
      "mappings": {
        "properties": {
          "brand": { "type": "keyword"},
          "color": { "type": "keyword"},
          "model": { "type": "keyword"}
        }
      }
    }
    
    PUT /shirts/_doc/1?refresh
    {
      "brand": "gucci",
      "color": "red",
      "model": "slim"
    }

假设用户指定了两个筛选器：

"颜色：红色"和"品牌：古驰"。您只想在搜索结果中向他们展示Gucci制造的红色衬衫。通常你会使用"bool"查询来执行此操作：

    
    
    response = client.search(
      index: 'shirts',
      body: {
        query: {
          bool: {
            filter: [
              {
                term: {
                  color: 'red'
                }
              },
              {
                term: {
                  brand: 'gucci'
                }
              }
            ]
          }
        }
      }
    )
    puts response
    
    
    GET /shirts/_search
    {
      "query": {
        "bool": {
          "filter": [
            { "term": { "color": "red"   }},
            { "term": { "brand": "gucci" }}
          ]
        }
      }
    }

但是，您还希望使用 _faceted navigation_ 显示用户可以单击的其他选项的列表。也许您有一个"模型"字段，允许用户将搜索结果限制为红色Gucci't恤"或"正装衬衫"。

这可以通过"术语"聚合来完成：

    
    
    response = client.search(
      index: 'shirts',
      body: {
        query: {
          bool: {
            filter: [
              {
                term: {
                  color: 'red'
                }
              },
              {
                term: {
                  brand: 'gucci'
                }
              }
            ]
          }
        },
        aggregations: {
          models: {
            terms: {
              field: 'model'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /shirts/_search
    {
      "query": {
        "bool": {
          "filter": [
            { "term": { "color": "red"   }},
            { "term": { "brand": "gucci" }}
          ]
        }
      },
      "aggs": {
        "models": {
          "terms": { "field": "model" } __}
      }
    }

__

|

返回 Gucci 最受欢迎的红色衬衫款式。   ---|--- 但也许你也想告诉用户有多少件Gucci衬衫有**其他颜色**可供选择。如果您只是在"颜色"字段上添加"术语"聚合，则只会返回颜色"红色"，因为您的查询仅返回Gucci的红色衬衫。

相反，您希望在聚合期间包含所有颜色的衬衫，然后仅将"颜色"过滤器应用于搜索结果。这就是"post_filter"的目的：

    
    
    response = client.search(
      index: 'shirts',
      body: {
        query: {
          bool: {
            filter: {
              term: {
                brand: 'gucci'
              }
            }
          }
        },
        aggregations: {
          colors: {
            terms: {
              field: 'color'
            }
          },
          color_red: {
            filter: {
              term: {
                color: 'red'
              }
            },
            aggregations: {
              models: {
                terms: {
                  field: 'model'
                }
              }
            }
          }
        },
        post_filter: {
          term: {
            color: 'red'
          }
        }
      }
    )
    puts response
    
    
    GET /shirts/_search
    {
      "query": {
        "bool": {
          "filter": {
            "term": { "brand": "gucci" } __}
        }
      },
      "aggs": {
        "colors": {
          "terms": { "field": "color" } __},
        "color_red": {
          "filter": {
            "term": { "color": "red" } __},
          "aggs": {
            "models": {
              "terms": { "field": "model" } __}
          }
        }
      },
      "post_filter": { __"term": { "color": "red" }
      }
    }

__

|

主查询现在查找 Gucci 的所有衬衫，无论颜色如何。   ---|---    __

|

"颜色"agg 返回 Gucci 衬衫的流行颜色。   __

|

"color_red"agg 将"模特"子聚合限制为**红色** Guccishirt。   __

|

最后，"post_filter"从搜索"命中"中删除红色以外的颜色。   ### 重新评分过滤的搜索结果编辑

重新评分可以帮助提高精度，方法是使用辅助(通常成本更高)算法对"查询"和"post_filter"阶段返回的顶级(例如 100 -500)文档进行重新排序，而不是将昂贵的算法应用于索引中的所有文档。

在每个分片上执行"重新评分"请求，然后返回其结果，由处理整个搜索请求的节点排序。

目前，重新评分 API 只有一个实现：查询重新评分器，它使用查询来调整评分。将来，可能会提供替代的重新评分器，例如，成对重新评分器。

如果为"rescore"查询提供了显式的"排序"(而不是降序的"_score")，则会引发错误。

向用户公开分页时，不应在单步浏览每个页面时更改"window_size"(通过传递不同的"from"值)，因为这会改变热门点击，导致结果在用户单步浏览页面时发生混淆性变化。

#### 查询评分器

查询重新评分器仅对"查询"和"post_filter"阶段返回的 Top-K 结果执行第二个查询。每个分片上将检查的文档数量可以通过"window_size"参数控制，该参数默认为 10。

默认情况下，原始查询和重新评分查询的分数以线性方式组合，以生成每个文档的最终"_score"。原始查询和重新评分查询的相对重要性可以分别用"query_weight"和"rescore_query_weight"来控制。两者都默认为"1"。

例如：

    
    
    response = client.search(
      body: {
        query: {
          match: {
            message: {
              operator: 'or',
              query: 'the quick brown'
            }
          }
        },
        rescore: {
          window_size: 50,
          query: {
            rescore_query: {
              match_phrase: {
                message: {
                  query: 'the quick brown',
                  slop: 2
                }
              }
            },
            query_weight: 0.7,
            rescore_query_weight: 1.2
          }
        }
      }
    )
    puts response
    
    
    POST /_search
    {
       "query" : {
          "match" : {
             "message" : {
                "operator" : "or",
                "query" : "the quick brown"
             }
          }
       },
       "rescore" : {
          "window_size" : 50,
          "query" : {
             "rescore_query" : {
                "match_phrase" : {
                   "message" : {
                      "query" : "the quick brown",
                      "slop" : 2
                   }
                }
             },
             "query_weight" : 0.7,
             "rescore_query_weight" : 1.2
          }
       }
    }

分数的组合方式可以通过"score_mode"来控制：

评分模式 |描述 ---|--- '总计'

|

添加原始分数和重新评分查询分数。默认值。   "乘"

|

将原始分数乘以重新评分查询分数。对于"函数查询"重新评分很有用。   '平均'

|

平均原始分数和重新评分查询分数。   "最大"

|

取原始分数的最大值和重新评分查询分数。   "分钟"

|

取原始分数和重新评分查询分数的最小值。   #### 多重重分编辑

也可以按顺序执行多个重新评分：

    
    
    response = client.search(
      body: {
        query: {
          match: {
            message: {
              operator: 'or',
              query: 'the quick brown'
            }
          }
        },
        rescore: [
          {
            window_size: 100,
            query: {
              rescore_query: {
                match_phrase: {
                  message: {
                    query: 'the quick brown',
                    slop: 2
                  }
                }
              },
              query_weight: 0.7,
              rescore_query_weight: 1.2
            }
          },
          {
            window_size: 10,
            query: {
              score_mode: 'multiply',
              rescore_query: {
                function_score: {
                  script_score: {
                    script: {
                      source: 'Math.log10(doc.count.value + 2)'
                    }
                  }
                }
              }
            }
          }
        ]
      }
    )
    puts response
    
    
    POST /_search
    {
       "query" : {
          "match" : {
             "message" : {
                "operator" : "or",
                "query" : "the quick brown"
             }
          }
       },
       "rescore" : [ {
          "window_size" : 100,
          "query" : {
             "rescore_query" : {
                "match_phrase" : {
                   "message" : {
                      "query" : "the quick brown",
                      "slop" : 2
                   }
                }
             },
             "query_weight" : 0.7,
             "rescore_query_weight" : 1.2
          }
       }, {
          "window_size" : 10,
          "query" : {
             "score_mode": "multiply",
             "rescore_query" : {
                "function_score" : {
                   "script_score": {
                      "script": {
                        "source": "Math.log10(doc.count.value + 2)"
                      }
                   }
                }
             }
          }
       } ]
    }

第一个获取查询结果，然后第二个获取第一个查询的结果，依此类推。第二次重新评分将"看到"第一次重新评分完成的排序，因此可以在第一次重新评分上使用大窗口将文档拉入较小的窗口进行第二次重新评分。

[« Collapse search results](collapse-search-results.md) [Highlighting
»](highlighting.md)
