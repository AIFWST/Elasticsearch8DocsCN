

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)

[« Regular expression syntax](regexp-syntax.md) [Bucket aggregations
»](search-aggregations-bucket.md)

#Aggregations

聚合将数据汇总为指标、统计信息或其他分析。聚合可帮助您回答以下问题：

* 我的网站的平均加载时间是多少？  * 根据交易量，谁是最有价值的客户？  * 在我的网络上，什么文件会被视为大文件？  * 每个产品类别中有多少种产品？

Elasticsearch 将聚合分为三类：

* 根据字段值计算指标(如总和或平均值)的指标聚合。  * 存储桶聚合，根据字段值、范围或其他条件将文档分组到存储桶(也称为存储桶)中。  * 从其他聚合而不是文档或字段获取输入的管道聚合。

### 运行聚合

您可以通过指定搜索 API 的"aggs"参数将聚合作为搜索的一部分运行。以下搜索在"my-field"上运行术语聚合：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        aggregations: {
          "my-agg-name": {
            terms: {
              field: 'my-field'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search
    {
      "aggs": {
        "my-agg-name": {
          "terms": {
            "field": "my-field"
          }
        }
      }
    }

聚合结果位于响应的"聚合"对象中：

    
    
    {
      "took": 78,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": {
          "value": 5,
          "relation": "eq"
        },
        "max_score": 1.0,
        "hits": [...]
      },
      "aggregations": {
        "my-agg-name": {                           __"doc_count_error_upper_bound": 0,
          "sum_other_doc_count": 0,
          "buckets": []
        }
      }
    }

__

|

"我的 agg-name"聚合的结果。   ---|--- ### 更改聚合的作用域编辑

使用"query"参数限制运行聚合的文档：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          range: {
            "@timestamp": {
              gte: 'now-1d/d',
              lt: 'now/d'
            }
          }
        },
        aggregations: {
          "my-agg-name": {
            terms: {
              field: 'my-field'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search
    {
      "query": {
        "range": {
          "@timestamp": {
            "gte": "now-1d/d",
            "lt": "now/d"
          }
        }
      },
      "aggs": {
        "my-agg-name": {
          "terms": {
            "field": "my-field"
          }
        }
      }
    }

### 仅返回聚合结果

默认情况下，包含聚合的搜索同时返回搜索命中和聚合结果。要仅返回聚合结果，请将"size"设置为"0"：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        size: 0,
        aggregations: {
          "my-agg-name": {
            terms: {
              field: 'my-field'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search
    {
      "size": 0,
      "aggs": {
        "my-agg-name": {
          "terms": {
            "field": "my-field"
          }
        }
      }
    }

### 运行多个聚合

您可以在同一请求中指定多个聚合：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        aggregations: {
          "my-first-agg-name": {
            terms: {
              field: 'my-field'
            }
          },
          "my-second-agg-name": {
            avg: {
              field: 'my-other-field'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search
    {
      "aggs": {
        "my-first-agg-name": {
          "terms": {
            "field": "my-field"
          }
        },
        "my-second-agg-name": {
          "avg": {
            "field": "my-other-field"
          }
        }
      }
    }

### 运行子聚合

存储桶聚合支持存储桶或指标子聚合。例如，具有 avg 子聚合的术语聚合计算每个文档存储桶的平均值。嵌套子聚合没有级别或深度限制。

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        aggregations: {
          "my-agg-name": {
            terms: {
              field: 'my-field'
            },
            aggregations: {
              "my-sub-agg-name": {
                avg: {
                  field: 'my-other-field'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search
    {
      "aggs": {
        "my-agg-name": {
          "terms": {
            "field": "my-field"
          },
          "aggs": {
            "my-sub-agg-name": {
              "avg": {
                "field": "my-other-field"
              }
            }
          }
        }
      }
    }

响应将子聚合结果嵌套在其父聚合下：

    
    
    {
      ...
      "aggregations": {
        "my-agg-name": {                           __"doc_count_error_upper_bound": 0,
          "sum_other_doc_count": 0,
          "buckets": [
            {
              "key": "foo",
              "doc_count": 5,
              "my-sub-agg-name": { __"value": 75.0
              }
            }
          ]
        }
      }
    }

__

|

父聚合"my-agg-name"的结果。   ---|---    __

|

"my-agg-name"的子聚合"my-sub-agg-name"的结果。   ### 添加自定义元数据编辑

使用"meta"对象将自定义元数据与聚合相关联：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        aggregations: {
          "my-agg-name": {
            terms: {
              field: 'my-field'
            },
            meta: {
              "my-metadata-field": 'foo'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search
    {
      "aggs": {
        "my-agg-name": {
          "terms": {
            "field": "my-field"
          },
          "meta": {
            "my-metadata-field": "foo"
          }
        }
      }
    }

响应返回就地的"meta"对象：

    
    
    {
      ...
      "aggregations": {
        "my-agg-name": {
          "meta": {
            "my-metadata-field": "foo"
          },
          "doc_count_error_upper_bound": 0,
          "sum_other_doc_count": 0,
          "buckets": []
        }
      }
    }

### 返回聚合类型

默认情况下，聚合结果包括聚合的名称，但不包括其类型。若要返回聚合类型，请使用"typed_keys"查询参数。

    
    
    response = client.search(
      index: 'my-index-000001',
      typed_keys: true,
      body: {
        aggregations: {
          "my-agg-name": {
            histogram: {
              field: 'my-field',
              interval: 1000
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search?typed_keys
    {
      "aggs": {
        "my-agg-name": {
          "histogram": {
            "field": "my-field",
            "interval": 1000
          }
        }
      }
    }

响应将聚合类型作为聚合名称的前缀返回。

某些聚合返回与请求中的类型不同的聚合类型。例如，术语、有效术语和百分位数聚合返回不同的聚合类型，具体取决于聚合字段的数据类型。

    
    
    {
      ...
      "aggregations": {
        "histogram#my-agg-name": {                 __"buckets": []
        }
      }
    }

__

|

聚合类型"直方图"，后跟"#"分隔符和聚合的名称"my-agg-name"。   ---|--- ### 在聚合编辑中使用脚本

当字段与所需的聚合不完全匹配时，应聚合到运行时字段上：

    
    
    GET /my-index-000001/_search?size=0
    {
      "runtime_mappings": {
        "message.length": {
          "type": "long",
          "script": "emit(doc['message.keyword'].value.length())"
        }
      },
      "aggs": {
        "message_length": {
          "histogram": {
            "interval": 10,
            "field": "message.length"
          }
        }
      }
    }

脚本动态计算字段值，这会增加聚合的开销。除了计算所花费的时间之外，某些聚合(如"术语"和"筛选器")不能使用它们的某些优化与运行时字段。总的来说，使用运行时字段的性能成本因聚合而异。

### 聚合缓存

为了更快地响应，Elasticsearch 将频繁运行的聚合结果缓存在分片请求缓存中。要获取缓存的结果，请对每个搜索使用相同的"首选项"字符串。如果您不需要搜索命中，请将"size"设置为"0"以避免填充缓存。

Elasticsearch 将具有相同首选项字符串的搜索路由到 sameshards。如果分片的数据在搜索之间没有更改，则分片将返回缓存的聚合结果。

### "多头"值的限制

在运行聚合时，Elasticsearch 使用"double"值来保存和表示数字数据。因此，大于"253"的"长"数的聚合是近似的。

[« Regular expression syntax](regexp-syntax.md) [Bucket aggregations
»](search-aggregations-bucket.md)
