

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« T-test aggregation](search-aggregations-metrics-ttest-aggregation.md)
[Top metrics aggregation »](search-aggregations-metrics-top-metrics.md)

## 热门聚合

"top_hits"指标聚合器跟踪要聚合的最相关的文档。此聚合器旨在用作子聚合器，以便可以按存储桶聚合排名靠前的匹配文档。

我们不建议使用"top_hits"作为顶级聚合。如果要对搜索命中进行分组，请改用"折叠"参数。

"top_hits"聚合器可以有效地用于通过存储桶聚合器按某些字段对结果集进行分组。一个或多个存储桶聚合器确定将结果集切成哪些属性。

###Options

* 'from' \- 与要获取的第一个结果的偏移量。  * "大小" \- 每个存储桶要返回的最大匹配命中数。默认情况下，将返回前三个匹配命中。  * 'sort' \- 应该如何对排名靠前的匹配命中进行排序。默认情况下，命中按主查询的分数排序。

### 支持每个命中功能

top_hits聚合返回常规搜索命中，因此可以支持许多 perhit 功能：

* 突出显示 * 解释 * 命名查询 * 搜索字段 * 源过滤 * 存储字段 * 脚本字段 * 文档值字段 * 包括版本 * 包括序列号和主要术语

如果您**只需要"docvalue_fields"、"大小"和"排序"，那么 Topmetrics 可能是比热门聚合更有效的选择。

"top_hits"不支持"重新评分"参数。查询重新评分仅适用于搜索命中，不适用于聚合结果。若要更改聚合使用的分数，请使用"function_score"或"script_score"查询。

###Example

在下面的示例中，我们按类型对销售额进行分组，并按类型显示上次销售。对于每笔销售，源中仅包含日期和价格字段。

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          top_tags: {
            terms: {
              field: 'type',
              size: 3
            },
            aggregations: {
              top_sales_hits: {
                top_hits: {
                  sort: [
                    {
                      date: {
                        order: 'desc'
                      }
                    }
                  ],
                  _source: {
                    includes: [
                      'date',
                      'price'
                    ]
                  },
                  size: 1
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "top_tags": {
          "terms": {
            "field": "type",
            "size": 3
          },
          "aggs": {
            "top_sales_hits": {
              "top_hits": {
                "sort": [
                  {
                    "date": {
                      "order": "desc"
                    }
                  }
                ],
                "_source": {
                  "includes": [ "date", "price" ]
                },
                "size": 1
              }
            }
          }
        }
      }
    }

可能的响应：

    
    
    {
      ...
      "aggregations": {
        "top_tags": {
           "doc_count_error_upper_bound": 0,
           "sum_other_doc_count": 0,
           "buckets": [
              {
                 "key": "hat",
                 "doc_count": 3,
                 "top_sales_hits": {
                    "hits": {
                       "total" : {
                           "value": 3,
                           "relation": "eq"
                       },
                       "max_score": null,
                       "hits": [
                          {
                             "_index": "sales",
                             "_id": "AVnNBmauCQpcRyxw6ChK",
                             "_source": {
                                "date": "2015/03/01 00:00:00",
                                "price": 200
                             },
                             "sort": [
                                1425168000000
                             ],
                             "_score": null
                          }
                       ]
                    }
                 }
              },
              {
                 "key": "t-shirt",
                 "doc_count": 3,
                 "top_sales_hits": {
                    "hits": {
                       "total" : {
                           "value": 3,
                           "relation": "eq"
                       },
                       "max_score": null,
                       "hits": [
                          {
                             "_index": "sales",
                             "_id": "AVnNBmauCQpcRyxw6ChL",
                             "_source": {
                                "date": "2015/03/01 00:00:00",
                                "price": 175
                             },
                             "sort": [
                                1425168000000
                             ],
                             "_score": null
                          }
                       ]
                    }
                 }
              },
              {
                 "key": "bag",
                 "doc_count": 1,
                 "top_sales_hits": {
                    "hits": {
                       "total" : {
                           "value": 1,
                           "relation": "eq"
                       },
                       "max_score": null,
                       "hits": [
                          {
                             "_index": "sales",
                             "_id": "AVnNBmatCQpcRyxw6ChH",
                             "_source": {
                                "date": "2015/01/01 00:00:00",
                                "price": 150
                             },
                             "sort": [
                                1420070400000
                             ],
                             "_score": null
                          }
                       ]
                    }
                 }
              }
           ]
        }
      }
    }

### 字段折叠示例

字段折叠或结果分组是一项功能，它将结果集逻辑地分组为组，每个组返回顶部文档。组的顺序由组中第一个文档的相关性决定。在Elasticsearch中，这可以通过一个桶聚合器来实现，该桶聚合器将'top_hits'聚合器包装为子聚合器。

在下面的示例中，我们跨已爬网的网页进行搜索。对于每个网页，我们存储网页所属的正文和域。通过在"域"字段上定义"术语"聚合器，我们按域对网页的结果集进行分组。然后将"top_hits"聚合器定义为子聚合器，以便按存储桶收集排名靠前的匹配命中。

还定义了一个"max"聚合器，"terms"聚合器的 order 功能使用它来按存储桶中最相关文档的相关性顺序返回存储桶。

    
    
    response = client.search(
      index: 'sales',
      body: {
        query: {
          match: {
            body: 'elections'
          }
        },
        aggregations: {
          top_sites: {
            terms: {
              field: 'domain',
              order: {
                top_hit: 'desc'
              }
            },
            aggregations: {
              top_tags_hits: {
                top_hits: {}
              },
              top_hit: {
                max: {
                  script: {
                    source: '_score'
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search
    {
      "query": {
        "match": {
          "body": "elections"
        }
      },
      "aggs": {
        "top_sites": {
          "terms": {
            "field": "domain",
            "order": {
              "top_hit": "desc"
            }
          },
          "aggs": {
            "top_tags_hits": {
              "top_hits": {}
            },
            "top_hit" : {
              "max": {
                "script": {
                  "source": "_score"
                }
              }
            }
          }
        }
      }
    }

目前，需要"最大"(或"最小")聚合器来确保"术语"聚合器中的存储桶根据每个域最相关网页的分数进行排序。不幸的是，"top_hits"聚合器还不能在"术语"聚合器的"顺序"选项中使用。

### top_hits嵌套或reverse_nestedaggregator中的支持

如果"top_hits"聚合器包装在"嵌套"或"reverse_nested"聚合器中，则会返回嵌套的匹配。嵌套命中在某种意义上隐藏的迷你文档中，这些文档是常规文档的一部分，其中在映射中配置了嵌套字段类型。如果"top_hits"聚合器包装在"嵌套"或"reverse_nested"聚合器中，则可以取消隐藏这些文档。阅读有关嵌套类型映射中嵌套的更多信息。

如果配置了嵌套类型，则单个文档实际上被索引为多个Lucene文档，并且它们共享相同的id。为了确定嵌套命中的身份，需要的不仅仅是 id，因此嵌套命中还包括它们的嵌套身份。嵌套标识保存在搜索命中的"_nested"字段下，包括数组字段和嵌套命中所属数组字段中的偏移量。偏移量从零开始。

让我们看看它是如何与真实样本一起工作的。考虑以下映射：

    
    
    response = client.indices.create(
      index: 'sales',
      body: {
        mappings: {
          properties: {
            tags: {
              type: 'keyword'
            },
            comments: {
              type: 'nested',
              properties: {
                username: {
                  type: 'keyword'
                },
                comment: {
                  type: 'text'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /sales
    {
      "mappings": {
        "properties": {
          "tags": { "type": "keyword" },
          "comments": {                           __"type": "nested",
            "properties": {
              "username": { "type": "keyword" },
              "comment": { "type": "text" }
            }
          }
        }
      }
    }

__

|

"注释"是一个数组，用于保存"product"对象下的嵌套文档。   ---|--- 还有一些文件：

    
    
    PUT /sales/_doc/1?refresh
    {
      "tags": [ "car", "auto" ],
      "comments": [
        { "username": "baddriver007", "comment": "This car could have better brakes" },
        { "username": "dr_who", "comment": "Where's the autopilot? Can't find it" },
        { "username": "ilovemotorbikes", "comment": "This car has two extra wheels" }
      ]
    }

现在可以执行以下"top_hits"聚合(包装在"嵌套"聚合中)：

    
    
    response = client.search(
      index: 'sales',
      body: {
        query: {
          term: {
            tags: 'car'
          }
        },
        aggregations: {
          by_sale: {
            nested: {
              path: 'comments'
            },
            aggregations: {
              by_user: {
                terms: {
                  field: 'comments.username',
                  size: 1
                },
                aggregations: {
                  by_nested: {
                    top_hits: {}
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search
    {
      "query": {
        "term": { "tags": "car" }
      },
      "aggs": {
        "by_sale": {
          "nested": {
            "path": "comments"
          },
          "aggs": {
            "by_user": {
              "terms": {
                "field": "comments.username",
                "size": 1
              },
              "aggs": {
                "by_nested": {
                  "top_hits": {}
                }
              }
            }
          }
        }
      }
    }

具有嵌套命中的热门响应片段，该片段位于第一个插槽数组字段"注释"中：

    
    
    {
      ...
      "aggregations": {
        "by_sale": {
          "by_user": {
            "buckets": [
              {
                "key": "baddriver007",
                "doc_count": 1,
                "by_nested": {
                  "hits": {
                    "total" : {
                       "value": 1,
                       "relation": "eq"
                    },
                    "max_score": 0.3616575,
                    "hits": [
                      {
                        "_index": "sales",
                        "_id": "1",
                        "_nested": {
                          "field": "comments",  __"offset": 0 __},
                        "_score": 0.3616575,
                        "_source": {
                          "comment": "This car could have better brakes", __"username": "baddriver007"
                        }
                      }
                    ]
                  }
                }
              }
              ...
            ]
          }
        }
      }
    }

__

|

包含嵌套命中符的数组字段的名称 ---|--- __

|

如果嵌套命中在包含数组中的位置 __

|

嵌套命中的来源 如果请求"_source"，则仅返回嵌套对象的部分源，而不是文档的整个源。此外，存储在 **嵌套** 内部对象级别的字段可通过驻留在"嵌套"或"reverse_nested"聚合器中的"top_hits"聚合器进行访问。

只有嵌套命中才会在命中中具有"_nested"字段，非嵌套(常规)命中不会有"_nested"字段。

如果未启用"_source"，则"_nested"中的信息也可用于在其他地方解析原始源。

如果在映射中定义了多个级别的嵌套对象类型，则"_nested"信息也可以是分层的，以表达两层或更多层深度的嵌套命中的身份。

在下面的示例中，嵌套命中驻留在字段"nested_grand_child_field"的第一个插槽中，该插槽驻留在"nested_child_field"字段的第二个慢速中：

    
    
    ...
    "hits": {
     "total" : {
         "value": 2565,
         "relation": "eq"
     },
     "max_score": 1,
     "hits": [
       {
         "_index": "a",
         "_id": "1",
         "_score": 1,
         "_nested" : {
           "field" : "nested_child_field",
           "offset" : 1,
           "_nested" : {
             "field" : "nested_grand_child_field",
             "offset" : 0
           }
         }
         "_source": ...
       },
       ...
     ]
    }
    ...

### 在管道聚合中使用

"top_hits"可用于使用每个存储桶单个值的管道聚合，例如应用于每个存储桶筛选的"bucket_selector"，类似于在 SQL 中使用 HAVING 子句。这需要将"size"设置为 1，并为要传递给包装聚合器的值指定正确的路径。后者可以是"_source"、"_sort"或"_score"值。例如：

    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "top_tags": {
          "terms": {
            "field": "type",
            "size": 3
          },
          "aggs": {
            "top_sales_hits": {
              "top_hits": {
                "sort": [
                  {
                    "date": {
                      "order": "desc"
                    }
                  }
                ],
                "_source": {
                  "includes": [ "date", "price" ]
                },
                "size": 1
              }
            },
            "having.top_salary": {
              "bucket_selector": {
                "buckets_path": {
                  "tp": "top_sales_hits[_source.price]"
                },
                "script": "params.tp < 180"
              }
            }
          }
        }
      }
    }

"bucket_path"使用"top_hits"名称"top_sales_hits"和提供聚合值的字段的关键字，即上面示例中的"_source"字段"价格"。其他选项包括"top_sales_hits[_sort]"(用于筛选上面的排序值"date")和"top_sales_hits[_score]"(用于筛选最高命中的分数)。

[« T-test aggregation](search-aggregations-metrics-ttest-aggregation.md)
[Top metrics aggregation »](search-aggregations-metrics-top-metrics.md)
