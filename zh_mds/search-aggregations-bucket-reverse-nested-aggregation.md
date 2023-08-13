

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Rare terms aggregation](search-aggregations-bucket-rare-terms-
aggregation.md) [Sampler aggregation »](search-aggregations-bucket-sampler-
aggregation.md)

## 反向嵌套聚合

一种特殊的单存储桶聚合，允许从嵌套文档中聚合父文档。实际上，此聚合可以脱离当时的块结构并链接到其他嵌套结构或根文档，这允许在嵌套聚合中嵌套不属于然后对象的其他聚合。

必须在"嵌套"聚合中定义"reverse_nested"聚合。

**Options:**

* 'path' \- 它定义了应该重新连接的嵌套对象字段。默认值为空，这意味着它联接回根/主文档级别。路径不能包含对嵌套对象字段的引用，该对象字段位于"嵌套"聚合的"reverse_nested"所在的嵌套结构之外。

例如，假设我们有一个带有问题和注释的工单系统的索引。注释作为嵌套文档内联到问题文档中。映射可能如下所示：

    
    
    response = client.indices.create(
      index: 'issues',
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
    
    
    PUT /issues
    {
      "mappings": {
        "properties": {
          "tags": { "type": "keyword" },
          "comments": {                            __"type": "nested",
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

"注释"是一个数组，用于保存"issue"对象下的嵌套文档。   ---|--- 以下聚合将返回已评论的热门评论者的用户名，以及每个排名靠前的评论者的热门标签用户已评论的问题的热门标签：

    
    
    response = client.search(
      index: 'issues',
      body: {
        query: {
          match_all: {}
        },
        aggregations: {
          comments: {
            nested: {
              path: 'comments'
            },
            aggregations: {
              top_usernames: {
                terms: {
                  field: 'comments.username'
                },
                aggregations: {
                  comment_to_issue: {
                    reverse_nested: {},
                    aggregations: {
                      top_tags_per_comment: {
                        terms: {
                          field: 'tags'
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /issues/_search
    {
      "query": {
        "match_all": {}
      },
      "aggs": {
        "comments": {
          "nested": {
            "path": "comments"
          },
          "aggs": {
            "top_usernames": {
              "terms": {
                "field": "comments.username"
              },
              "aggs": {
                "comment_to_issue": {
                  "reverse_nested": {}, __"aggs": {
                    "top_tags_per_comment": {
                      "terms": {
                        "field": "tags"
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }

正如您在上面看到的，"reverse_nested"聚合被放入"嵌套"聚合中，因为这是 dsl 中唯一可以使用"reverse_nested"聚合的地方。它的唯一目的是在嵌套结构中重新连接回父文档。

__

|

一个"reverse_nested"聚合，它联接回根/主文档级别，因为尚未定义"路径"。如果在映射---|中定义了多层嵌套对象类型，则通过"路径"选项，"reverse_nested"聚合可以联接回不同的级别--- 可能的响应代码段：

    
    
    {
      "aggregations": {
        "comments": {
          "doc_count": 1,
          "top_usernames": {
            "doc_count_error_upper_bound" : 0,
            "sum_other_doc_count" : 0,
            "buckets": [
              {
                "key": "username_1",
                "doc_count": 1,
                "comment_to_issue": {
                  "doc_count": 1,
                  "top_tags_per_comment": {
                    "doc_count_error_upper_bound" : 0,
                    "sum_other_doc_count" : 0,
                    "buckets": [
                      {
                        "key": "tag_1",
                        "doc_count": 1
                      }
                      ...
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

[« Rare terms aggregation](search-aggregations-bucket-rare-terms-
aggregation.md) [Sampler aggregation »](search-aggregations-bucket-sampler-
aggregation.md)
