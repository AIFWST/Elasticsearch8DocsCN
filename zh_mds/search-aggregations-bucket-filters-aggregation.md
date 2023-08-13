

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Filter aggregation](search-aggregations-bucket-filter-aggregation.md)
[Frequent item sets aggregation »](search-aggregations-bucket-frequent-item-
sets-aggregation.md)

## 筛选器聚合

多存储桶聚合，其中每个存储桶包含与查询匹配的文档。

Example:

    
    
    response = client.bulk(
      index: 'logs',
      refresh: true,
      body: [
        {
          index: {
            _id: 1
          }
        },
        {
          body: 'warning: page could not be rendered'
        },
        {
          index: {
            _id: 2
          }
        },
        {
          body: 'authentication error'
        },
        {
          index: {
            _id: 3
          }
        },
        {
          body: 'warning: connection timed out'
        }
      ]
    )
    puts response
    
    response = client.search(
      index: 'logs',
      body: {
        size: 0,
        aggregations: {
          messages: {
            filters: {
              filters: {
                errors: {
                  match: {
                    body: 'error'
                  }
                },
                warnings: {
                  match: {
                    body: 'warning'
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /logs/_bulk?refresh
    { "index" : { "_id" : 1 } }
    { "body" : "warning: page could not be rendered" }
    { "index" : { "_id" : 2 } }
    { "body" : "authentication error" }
    { "index" : { "_id" : 3 } }
    { "body" : "warning: connection timed out" }
    
    GET logs/_search
    {
      "size": 0,
      "aggs" : {
        "messages" : {
          "filters" : {
            "filters" : {
              "errors" :   { "match" : { "body" : "error"   }},
              "warnings" : { "match" : { "body" : "warning" }}
            }
          }
        }
      }
    }

在上面的示例中，我们分析日志消息。聚合将生成两个日志消息集合(存储桶) - 一个用于所有包含错误的日志消息，另一个用于所有包含警告的消息。

Response:

    
    
    {
      "took": 9,
      "timed_out": false,
      "_shards": ...,
      "hits": ...,
      "aggregations": {
        "messages": {
          "buckets": {
            "errors": {
              "doc_count": 1
            },
            "warnings": {
              "doc_count": 2
            }
          }
        }
      }
    }

### 匿名过滤器

过滤器字段也可以作为过滤器数组提供，如以下请求所示：

    
    
    response = client.search(
      index: 'logs',
      body: {
        size: 0,
        aggregations: {
          messages: {
            filters: {
              filters: [
                {
                  match: {
                    body: 'error'
                  }
                },
                {
                  match: {
                    body: 'warning'
                  }
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET logs/_search
    {
      "size": 0,
      "aggs" : {
        "messages" : {
          "filters" : {
            "filters" : [
              { "match" : { "body" : "error"   }},
              { "match" : { "body" : "warning" }}
            ]
          }
        }
      }
    }

筛选后的存储桶按请求中提供的相同顺序返回。此示例的响应将是：

    
    
    {
      "took": 4,
      "timed_out": false,
      "_shards": ...,
      "hits": ...,
      "aggregations": {
        "messages": {
          "buckets": [
            {
              "doc_count": 1
            },
            {
              "doc_count": 2
            }
          ]
        }
      }
    }

### "其他"存储桶

可以设置"other_bucket"参数以向响应添加一个存储桶，该存储桶将包含与任何给定过滤器不匹配的所有文档。此参数的值可以如下所示：

`false`

     Does not compute the `other` bucket 
`true`

     Returns the `other` bucket either in a bucket (named `_other_` by default) if named filters are being used, or as the last bucket if anonymous filters are being used 

"other_bucket_key"参数可用于将"其他"存储桶的键设置为默认"_other_"以外的值。设置此参数会将"other_bucket"参数隐式设置为"true"。

以下代码片段显示了请求将"其他"存储桶命名为"other_messages"的响应。

    
    
    response = client.index(
      index: 'logs',
      id: 4,
      refresh: true,
      body: {
        body: 'info: user Bob logged out'
      }
    )
    puts response
    
    response = client.search(
      index: 'logs',
      body: {
        size: 0,
        aggregations: {
          messages: {
            filters: {
              other_bucket_key: 'other_messages',
              filters: {
                errors: {
                  match: {
                    body: 'error'
                  }
                },
                warnings: {
                  match: {
                    body: 'warning'
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT logs/_doc/4?refresh
    {
      "body": "info: user Bob logged out"
    }
    
    GET logs/_search
    {
      "size": 0,
      "aggs" : {
        "messages" : {
          "filters" : {
            "other_bucket_key": "other_messages",
            "filters" : {
              "errors" :   { "match" : { "body" : "error"   }},
              "warnings" : { "match" : { "body" : "warning" }}
            }
          }
        }
      }
    }

响应将如下所示：

    
    
    {
      "took": 3,
      "timed_out": false,
      "_shards": ...,
      "hits": ...,
      "aggregations": {
        "messages": {
          "buckets": {
            "errors": {
              "doc_count": 1
            },
            "warnings": {
              "doc_count": 2
            },
            "other_messages": {
              "doc_count": 1
            }
          }
        }
      }
    }

### 非键控响应

默认情况下，命名筛选器聚合将存储桶作为对象返回。但在某些排序情况下，例如存储桶排序，JSON 不能保证对象中元素的顺序。您可以使用"keyed"参数将存储桶指定为对象数组。此参数的值可以如下所示：

`true`

     (Default) Returns the buckets as an object 
`false`

     Returns the buckets as an array of objects 

匿名筛选器将忽略此参数。

Example:

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      filter_path: 'aggregations',
      body: {
        aggregations: {
          the_filter: {
            filters: {
              keyed: false,
              filters: {
                "t-shirt": {
                  term: {
                    type: 't-shirt'
                  }
                },
                hat: {
                  term: {
                    type: 'hat'
                  }
                }
              }
            },
            aggregations: {
              avg_price: {
                avg: {
                  field: 'price'
                }
              },
              sort_by_avg_price: {
                bucket_sort: {
                  sort: {
                    avg_price: 'asc'
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0&filter_path=aggregations
    {
      "aggs": {
        "the_filter": {
          "filters": {
            "keyed": false,
            "filters": {
              "t-shirt": { "term": { "type": "t-shirt" } },
              "hat": { "term": { "type": "hat" } }
            }
          },
          "aggs": {
            "avg_price": { "avg": { "field": "price" } },
            "sort_by_avg_price": {
              "bucket_sort": { "sort": { "avg_price": "asc" } }
            }
          }
        }
      }
    }

Response:

    
    
    {
      "aggregations": {
        "the_filter": {
          "buckets": [
            {
              "key": "t-shirt",
              "doc_count": 3,
              "avg_price": { "value": 128.33333333333334 }
            },
            {
              "key": "hat",
              "doc_count": 3,
              "avg_price": { "value": 150.0 }
            }
          ]
        }
      }
    }

[« Filter aggregation](search-aggregations-bucket-filter-aggregation.md)
[Frequent item sets aggregation »](search-aggregations-bucket-frequent-item-
sets-aggregation.md)
