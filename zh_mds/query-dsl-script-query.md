

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Specialized queries](specialized-queries.md)

[« Rank feature query](query-dsl-rank-feature-query.md) [Script score query
»](query-dsl-script-score-query.md)

## 脚本查询

运行时字段提供了非常相似的功能，该功能更灵活。您编写一个脚本来创建字段值，它们在任何地方都可用，例如"字段"、所有查询和聚合。

根据提供的脚本筛选文档。"脚本"查询通常用于筛选器上下文。

使用脚本可能会导致搜索速度变慢。请参阅脚本、缓存和搜索速度。

### 示例请求

    
    
    response = client.search(
      body: {
        query: {
          bool: {
            filter: {
              script: {
                script: "\n            double amount = doc['amount'].value;\n            if (doc['type'].value == 'expense') {\n              amount *= -1;\n            }\n            return amount < 10;\n          "
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "bool": {
          "filter": {
            "script": {
              "script": """
                double amount = doc['amount'].value;
                if (doc['type'].value == 'expense') {
                  amount *= -1;
                }
                return amount < 10;
              """
            }
          }
        }
      }
    }

您可以使用运行时字段在搜索查询中获得相同的结果。使用"_search"API 上的"fields"参数获取值作为同一查询的一部分：

    
    
    response = client.search(
      body: {
        runtime_mappings: {
          "amount.signed": {
            type: 'double',
            script: "\n        double amount = doc['amount'].value;\n        if (doc['type'].value == 'expense') {\n          amount *= -1;\n        }\n        emit(amount);\n      "
          }
        },
        query: {
          bool: {
            filter: {
              range: {
                "amount.signed": {
                  lt: 10
                }
              }
            }
          }
        },
        fields: [
          {
            field: 'amount.signed'
          }
        ]
      }
    )
    puts response
    
    
    GET /_search
    {
      "runtime_mappings": {
        "amount.signed": {
          "type": "double",
          "script": """
            double amount = doc['amount'].value;
            if (doc['type'].value == 'expense') {
              amount *= -1;
            }
            emit(amount);
          """
        }
      },
      "query": {
        "bool": {
          "filter": {
            "range": {
              "amount.signed": { "lt": 10 }
            }
          }
        }
      },
      "fields": [{"field": "amount.signed"}]
    }

### "脚本"的顶级参数

`script`

     (Required, [script object](modules-scripting-using.html "How to write scripts")) Contains a script to run as a query. This script must return a boolean value, `true` or `false`. 

###Notes

#### 自定义参数

与筛选器一样，脚本被缓存以加快执行速度。如果您经常更改 ascript 的参数，我们建议您将它们存储在脚本的 'params' 参数中。例如：

    
    
    response = client.search(
      body: {
        query: {
          bool: {
            filter: {
              script: {
                script: {
                  source: "doc['num1'].value > params.param1",
                  lang: 'painless',
                  params: {
                    "param1": 5
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "bool": {
          "filter": {
            "script": {
              "script": {
                "source": "doc['num1'].value > params.param1",
                "lang": "painless",
                "params": {
                  "param1": 5
                }
              }
            }
          }
        }
      }
    }

#### 允许昂贵的查询

如果"search.allow_expensive_queries"设置为 false，则不会执行脚本查询。

[« Rank feature query](query-dsl-rank-feature-query.md) [Script score query
»](query-dsl-script-score-query.md)
