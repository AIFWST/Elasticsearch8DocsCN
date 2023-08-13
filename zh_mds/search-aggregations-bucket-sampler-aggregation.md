

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Reverse nested aggregation](search-aggregations-bucket-reverse-nested-
aggregation.md) [Significant terms aggregation »](search-aggregations-
bucket-significantterms-aggregation.md)

## 采样器聚合

一种筛选聚合，用于将任何子聚合的处理限制为得分最高的文档样本。

**示例用例：**

* 将分析的重点集中在高相关性匹配上，而不是低质量匹配的潜在长尾 * 降低聚合的运行成本，这些聚合可以仅使用样本(例如"significant_terms")产生有用的结果

Example:

对流行的术语"javascript"或罕见术语"kibana"的StackOverflow数据查询将匹配许多文档 - 其中大多数都缺少单词Kibana。为了将"significant_terms"聚合集中在得分最高的文档上，这些文档更有可能与查询中最有趣的部分匹配，我们使用 asample。

    
    
    response = client.search(
      index: 'stackoverflow',
      size: 0,
      body: {
        query: {
          query_string: {
            query: 'tags:kibana OR tags:javascript'
          }
        },
        aggregations: {
          sample: {
            sampler: {
              shard_size: 200
            },
            aggregations: {
              keywords: {
                significant_terms: {
                  field: 'tags',
                  exclude: [
                    'kibana',
                    'javascript'
                  ]
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /stackoverflow/_search?size=0
    {
      "query": {
        "query_string": {
          "query": "tags:kibana OR tags:javascript"
        }
      },
      "aggs": {
        "sample": {
          "sampler": {
            "shard_size": 200
          },
          "aggs": {
            "keywords": {
              "significant_terms": {
                "field": "tags",
                "exclude": [ "kibana", "javascript" ]
              }
            }
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "sample": {
          "doc_count": 200, __"keywords": {
            "doc_count": 200,
            "bg_count": 650,
            "buckets": [
              {
                "key": "elasticsearch",
                "doc_count": 150,
                "score": 1.078125,
                "bg_count": 200
              },
              {
                "key": "logstash",
                "doc_count": 50,
                "score": 0.5625,
                "bg_count": 50
              }
            ]
          }
        }
      }
    }

__

|

总共抽样了200份文件。因此，执行nestedsignificant_terms聚合的成本是有限的，而不是无限的。   ---|--- 如果没有"采样器"聚合，请求查询会考虑低质量匹配的完整"长尾"，因此识别不太重要的术语，例如"jquery"和"angular"，而不是专注于更具洞察力的 Kibana 相关术语。

    
    
    response = client.search(
      index: 'stackoverflow',
      size: 0,
      body: {
        query: {
          query_string: {
            query: 'tags:kibana OR tags:javascript'
          }
        },
        aggregations: {
          low_quality_keywords: {
            significant_terms: {
              field: 'tags',
              size: 3,
              exclude: [
                'kibana',
                'javascript'
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    POST /stackoverflow/_search?size=0
    {
      "query": {
        "query_string": {
          "query": "tags:kibana OR tags:javascript"
        }
      },
      "aggs": {
        "low_quality_keywords": {
          "significant_terms": {
            "field": "tags",
            "size": 3,
            "exclude": [ "kibana", "javascript" ]
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "low_quality_keywords": {
          "doc_count": 600,
          "bg_count": 650,
          "buckets": [
            {
              "key": "angular",
              "doc_count": 200,
              "score": 0.02777,
              "bg_count": 200
            },
            {
              "key": "jquery",
              "doc_count": 200,
              "score": 0.02777,
              "bg_count": 200
            },
            {
              "key": "logstash",
              "doc_count": 50,
              "score": 0.0069,
              "bg_count": 50
            }
          ]
        }
      }
    }

###shard_size

"shard_size"参数限制在每个分片上处理的样本中收集的得分最高的文档数。默认值为 100。

###Limitations

#### 不能嵌套在"breadth_first"聚合下

作为基于质量的过滤器，采样器聚合需要访问为每个文档生成的相关性分数。因此，它不能嵌套在"术语"聚合下，该聚合将"collect_mode"从默认的"depth_first"模式切换到"breadth_first"，因为这会丢弃分数。在这种情况下，将引发错误。

[« Reverse nested aggregation](search-aggregations-bucket-reverse-nested-
aggregation.md) [Significant terms aggregation »](search-aggregations-
bucket-significantterms-aggregation.md)
