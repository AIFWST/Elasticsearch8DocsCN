

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Nested aggregation](search-aggregations-bucket-nested-aggregation.md)
[Random sampler aggregation »](search-aggregations-random-sampler-
aggregation.md)

## 父聚合

一种特殊的单存储桶聚合，用于选择具有指定类型的父文档，如"join"字段中所定义。

此聚合具有单个选项：

* 'type' \- 应选择的子类型。

例如，假设我们有一个问题和答案的索引。答案类型在映射中具有以下"join"字段：

    
    
    response = client.indices.create(
      index: 'parent_example',
      body: {
        mappings: {
          properties: {
            join: {
              type: 'join',
              relations: {
                question: 'answer'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT parent_example
    {
      "mappings": {
         "properties": {
           "join": {
             "type": "join",
             "relations": {
               "question": "answer"
             }
           }
         }
      }
    }

"问题"文档包含一个标记字段，"答案"文档包含一个所有者字段。使用"父"聚合，所有者存储桶可以在单个请求中映射到标签存储桶，即使这两个字段存在于两种不同类型的文档中。

问题文档示例：

    
    
    PUT parent_example/_doc/1
    {
      "join": {
        "name": "question"
      },
      "body": "<p>I have Windows 2003 server and i bought a new Windows 2008 server...",
      "title": "Whats the best way to file transfer my site from server to a newer one?",
      "tags": [
        "windows-server-2003",
        "windows-server-2008",
        "file-transfer"
      ]
    }

"答复"文件示例：

    
    
    PUT parent_example/_doc/2?routing=1
    {
      "join": {
        "name": "answer",
        "parent": "1"
      },
      "owner": {
        "location": "Norfolk, United Kingdom",
        "display_name": "Sam",
        "id": 48
      },
      "body": "<p>Unfortunately you're pretty much limited to FTP...",
      "creation_date": "2009-05-04T13:45:37.030"
    }
    
    PUT parent_example/_doc/3?routing=1&refresh
    {
      "join": {
        "name": "answer",
        "parent": "1"
      },
      "owner": {
        "location": "Norfolk, United Kingdom",
        "display_name": "Troll",
        "id": 49
      },
      "body": "<p>Use Linux...",
      "creation_date": "2009-05-05T13:45:37.030"
    }

可以生成以下请求，将两者连接在一起：

    
    
    response = client.search(
      index: 'parent_example',
      size: 0,
      body: {
        aggregations: {
          "top-names": {
            terms: {
              field: 'owner.display_name.keyword',
              size: 10
            },
            aggregations: {
              "to-questions": {
                parent: {
                  type: 'answer'
                },
                aggregations: {
                  "top-tags": {
                    terms: {
                      field: 'tags.keyword',
                      size: 10
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
    
    
    POST parent_example/_search?size=0
    {
      "aggs": {
        "top-names": {
          "terms": {
            "field": "owner.display_name.keyword",
            "size": 10
          },
          "aggs": {
            "to-questions": {
              "parent": {
                "type" : "answer" __},
              "aggs": {
                "top-tags": {
                  "terms": {
                    "field": "tags.keyword",
                    "size": 10
                  }
                }
              }
            }
          }
        }
      }
    }

__

|

"类型"指向名称为"答案"的类型/映射。   ---|--- 上面的示例返回排名靠前的答案所有者，并返回每个所有者的热门问题标签。

可能的响应：

    
    
    {
      "took": 9,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total" : {
          "value": 3,
          "relation": "eq"
        },
        "max_score": null,
        "hits": []
      },
      "aggregations": {
        "top-names": {
          "doc_count_error_upper_bound": 0,
          "sum_other_doc_count": 0,
          "buckets": [
            {
              "key": "Sam",
              "doc_count": 1, __"to-questions": {
                "doc_count": 1, __"top-tags": {
                  "doc_count_error_upper_bound": 0,
                  "sum_other_doc_count": 0,
                  "buckets": [
                    {
                      "key": "file-transfer",
                      "doc_count": 1
                    },
                    {
                      "key": "windows-server-2003",
                      "doc_count": 1
                    },
                    {
                      "key": "windows-server-2008",
                      "doc_count": 1
                    }
                  ]
                }
              }
            },
            {
              "key": "Troll",
              "doc_count": 1,
              "to-questions": {
                "doc_count": 1,
                "top-tags": {
                  "doc_count_error_upper_bound": 0,
                  "sum_other_doc_count": 0,
                  "buckets": [
                    {
                      "key": "file-transfer",
                      "doc_count": 1
                    },
                    {
                      "key": "windows-server-2003",
                      "doc_count": 1
                    },
                    {
                      "key": "windows-server-2008",
                      "doc_count": 1
                    }
                  ]
                }
              }
            }
          ]
        }
      }
    }

__

|

带有"山姆"、"巨魔"等标签的答案文档的数量。   ---|---    __

|

与带有标签"山姆"、"巨魔"等的答案文档相关的问题文档的数量。   « 嵌套聚合随机采样器聚合 »