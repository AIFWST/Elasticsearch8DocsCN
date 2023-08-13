

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[How
to](how-to.md) ›[Recipes](recipes.md)

[« Recipes](recipes.md) [Getting consistent scoring »](consistent-
scoring.md)

## 将精确搜索与词干混合

在构建搜索应用程序时，词干提取通常是必须的，因为关于"ski"的查询需要匹配包含"ski"或"skis"的文档。但是，如果用户想要专门搜索"滑雪"怎么办？执行此操作的典型方法是使用多字段，以便以两种不同的方式为相同的内容编制索引：

    
    
    response = client.indices.create(
      index: 'index',
      body: {
        settings: {
          analysis: {
            analyzer: {
              english_exact: {
                tokenizer: 'standard',
                filter: [
                  'lowercase'
                ]
              }
            }
          }
        },
        mappings: {
          properties: {
            body: {
              type: 'text',
              analyzer: 'english',
              fields: {
                exact: {
                  type: 'text',
                  analyzer: 'english_exact'
                }
              }
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
        body: 'Ski resort'
      }
    )
    puts response
    
    response = client.index(
      index: 'index',
      id: 2,
      body: {
        body: 'A pair of skis'
      }
    )
    puts response
    
    response = client.indices.refresh(
      index: 'index'
    )
    puts response
    
    
    PUT index
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "english_exact": {
              "tokenizer": "standard",
              "filter": [
                "lowercase"
              ]
            }
          }
        }
      },
      "mappings": {
        "properties": {
          "body": {
            "type": "text",
            "analyzer": "english",
            "fields": {
              "exact": {
                "type": "text",
                "analyzer": "english_exact"
              }
            }
          }
        }
      }
    }
    
    PUT index/_doc/1
    {
      "body": "Ski resort"
    }
    
    PUT index/_doc/2
    {
      "body": "A pair of skis"
    }
    
    POST index/_refresh

通过这样的设置，在"body"上搜索"ski"将返回两个文档：

    
    
    response = client.search(
      index: 'index',
      body: {
        query: {
          simple_query_string: {
            fields: [
              'body'
            ],
            query: 'ski'
          }
        }
      }
    )
    puts response
    
    
    GET index/_search
    {
      "query": {
        "simple_query_string": {
          "fields": [ "body" ],
          "query": "ski"
        }
      }
    }
    
    
    {
      "took": 2,
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
        "max_score": 0.18232156,
        "hits": [
          {
            "_index": "index",
            "_id": "1",
            "_score": 0.18232156,
            "_source": {
              "body": "Ski resort"
            }
          },
          {
            "_index": "index",
            "_id": "2",
            "_score": 0.18232156,
            "_source": {
              "body": "A pair of skis"
            }
          }
        ]
      }
    }

另一方面，在"body.exact"上搜索"ski"只会返回文档"1"，因为"body.exact"的分析链不执行词干提取。

    
    
    response = client.search(
      index: 'index',
      body: {
        query: {
          simple_query_string: {
            fields: [
              'body.exact'
            ],
            query: 'ski'
          }
        }
      }
    )
    puts response
    
    
    GET index/_search
    {
      "query": {
        "simple_query_string": {
          "fields": [ "body.exact" ],
          "query": "ski"
        }
      }
    }
    
    
    {
      "took": 1,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped" : 0,
        "failed": 0
      },
      "hits": {
        "total" : {
            "value": 1,
            "relation": "eq"
        },
        "max_score": 0.8025915,
        "hits": [
          {
            "_index": "index",
            "_id": "1",
            "_score": 0.8025915,
            "_source": {
              "body": "Ski resort"
            }
          }
        ]
      }
    }

这不是一件容易暴露给最终用户的事情，因为我们需要一种方法来确定他们是否在寻找完全匹配，并相应地重定向到适当的字段。另外，如果只有查询的一部分需要完全匹配，而其他部分仍应考虑词干，该怎么办？

幸运的是，"query_string"和"simple_query_string"查询具有解决此确切问题的功能："quote_field_suffix"。这告诉Elasticsearch，出现在引号之间的单词将被重定向到不同的字段，如下所示：

    
    
    response = client.search(
      index: 'index',
      body: {
        query: {
          simple_query_string: {
            fields: [
              'body'
            ],
            quote_field_suffix: '.exact',
            query: '"ski"'
          }
        }
      }
    )
    puts response
    
    
    GET index/_search
    {
      "query": {
        "simple_query_string": {
          "fields": [ "body" ],
          "quote_field_suffix": ".exact",
          "query": "\"ski\""
        }
      }
    }
    
    
    {
      "took": 2,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped" : 0,
        "failed": 0
      },
      "hits": {
        "total" : {
            "value": 1,
            "relation": "eq"
        },
        "max_score": 0.8025915,
        "hits": [
          {
            "_index": "index",
            "_id": "1",
            "_score": 0.8025915,
            "_source": {
              "body": "Ski resort"
            }
          }
        ]
      }
    }

在上述情况下，由于"ski"位于引号之间，因此由于"quote_field_suffix"参数在"body.exact"字段中搜索了它，因此只有文档"1"匹配。这允许用户根据需要将精确搜索与词干搜索混合使用。

如果选择在"quote_field_suffix"中传递的字段不存在，则搜索将回退到使用查询字符串的默认字段。

[« Recipes](recipes.md) [Getting consistent scoring »](consistent-
scoring.md)
