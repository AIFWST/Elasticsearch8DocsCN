

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `fields`](multi-fields.md) [`norms` »](norms.md)

##'规范化器'

"关键字"字段的"规范化器"属性类似于"分析器"，不同之处在于它保证分析链生成单个令牌。

"规范化器"在为关键字编制索引之前应用，以及在通过查询解析器(如"匹配"查询)或通过术语级查询(如"term"query)搜索"关键字"字段时应用。

一个名为"小写"的简单规范化器附带了 elasticsearch，可以使用。自定义归一化器可以定义为分析设置的一部分，如下所示。

    
    
    response = client.indices.create(
      index: 'index',
      body: {
        settings: {
          analysis: {
            normalizer: {
              my_normalizer: {
                type: 'custom',
                char_filter: [],
                filter: [
                  'lowercase',
                  'asciifolding'
                ]
              }
            }
          }
        },
        mappings: {
          properties: {
            foo: {
              type: 'keyword',
              normalizer: 'my_normalizer'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'index',
      id: 1,
      body: {
        foo: 'BÀR'
      }
    )
    puts response
    
    response = client.index(
      index: 'index',
      id: 2,
      body: {
        foo: 'bar'
      }
    )
    puts response
    
    response = client.index(
      index: 'index',
      id: 3,
      body: {
        foo: 'baz'
      }
    )
    puts response
    
    response = client.indices.refresh(
      index: 'index'
    )
    puts response
    
    response = client.search(
      index: 'index',
      body: {
        query: {
          term: {
            foo: 'BAR'
          }
        }
      }
    )
    puts response
    
    response = client.search(
      index: 'index',
      body: {
        query: {
          match: {
            foo: 'BAR'
          }
        }
      }
    )
    puts response
    
    
    PUT index
    {
      "settings": {
        "analysis": {
          "normalizer": {
            "my_normalizer": {
              "type": "custom",
              "char_filter": [],
              "filter": ["lowercase", "asciifolding"]
            }
          }
        }
      },
      "mappings": {
        "properties": {
          "foo": {
            "type": "keyword",
            "normalizer": "my_normalizer"
          }
        }
      }
    }
    
    PUT index/_doc/1
    {
      "foo": "BÀR"
    }
    
    PUT index/_doc/2
    {
      "foo": "bar"
    }
    
    PUT index/_doc/3
    {
      "foo": "baz"
    }
    
    POST index/_refresh
    
    GET index/_search
    {
      "query": {
        "term": {
          "foo": "BAR"
        }
      }
    }
    
    GET index/_search
    {
      "query": {
        "match": {
          "foo": "BAR"
        }
      }
    }

上述查询与文档 1 和 2 匹配，因为"BÀR"在索引和查询时间都转换为"bar"。

    
    
    {
      "took": $body.took,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped" : 0,
        "failed": 0
      },
      "hits": {
        "total" : {
            "value": 2,
            "relation": "eq"
        },
        "max_score": 0.4700036,
        "hits": [
          {
            "_index": "index",
            "_id": "1",
            "_score": 0.4700036,
            "_source": {
              "foo": "BÀR"
            }
          },
          {
            "_index": "index",
            "_id": "2",
            "_score": 0.4700036,
            "_source": {
              "foo": "bar"
            }
          }
        ]
      }
    }

此外，关键字在索引编制之前被转换的事实也意味着聚合返回规范化值：

    
    
    response = client.search(
      index: 'index',
      body: {
        size: 0,
        aggregations: {
          foo_terms: {
            terms: {
              field: 'foo'
            }
          }
        }
      }
    )
    puts response
    
    
    GET index/_search
    {
      "size": 0,
      "aggs": {
        "foo_terms": {
          "terms": {
            "field": "foo"
          }
        }
      }
    }

returns

    
    
    {
      "took": 43,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped" : 0,
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
        "foo_terms": {
          "doc_count_error_upper_bound": 0,
          "sum_other_doc_count": 0,
          "buckets": [
            {
              "key": "bar",
              "doc_count": 2
            },
            {
              "key": "baz",
              "doc_count": 1
            }
          ]
        }
      }
    }

[« `fields`](multi-fields.md) [`norms` »](norms.md)
