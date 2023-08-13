

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Specialized queries](specialized-queries.md)

[« Script query](query-dsl-script-query.md) [Wrapper query »](query-dsl-
wrapper-query.md)

## 脚本分数查询

使用脚本为返回的文档提供自定义分数。

例如，如果评分函数很昂贵，并且您只需要计算一组过滤的文档的分数，则"script_score"查询非常有用。

### 示例请求

以下"script_score"查询为每个返回的文档分配一个分数等于"my-int"字段值除以"10"。

    
    
    response = client.search(
      body: {
        query: {
          script_score: {
            query: {
              match: {
                message: 'elasticsearch'
              }
            },
            script: {
              source: "doc['my-int'].value / 10 "
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "script_score": {
          "query": {
            "match": { "message": "elasticsearch" }
          },
          "script": {
            "source": "doc['my-int'].value / 10 "
          }
        }
      }
    }

### script_score"的顶级参数

`query`

     (Required, query object) Query used to return documents. 
`script`

    

(必需，脚本对象)用于计算"查询"返回的文档分数的脚本。

"script_score"查询的最终相关性分数不能为负数。为了支持某些搜索优化，Lucene 要求分数为正或"0"。

`min_score`

     (Optional, float) Documents with a score lower than this floating point number are excluded from the search results. 
`boost`

     (Optional, float) Documents' scores produced by `script` are multiplied by `boost` to produce final documents' scores. Defaults to `1.0`. 

###Notes

#### 在脚本中使用相关性分数

在脚本中，您可以访问表示文档当前相关性分数的"_score"变量。

#### 预定义函数

您可以在"脚本"中使用任何可用的无痛功能。还可以使用以下预定义函数自定义评分：

* 饱和度 * Sigmoid * 随机评分函数 * 数值字段的衰减函数 * 地理字段的衰减函数 * 日期字段的衰减函数 * 矢量字段的函数

我们建议使用这些预定义的函数，而不是编写自己的函数。这些函数利用了Elasticsearch内部机制的效率。

#####Saturation

'饱和度(值，k) = 值/(k + 值)"

    
    
    "script" : {
        "source" : "saturation(doc['my-int'].value, 1)"
    }

#####Sigmoid

'sigmoid(value， k， a) = value^a/ (k^a + value^a)'

    
    
    "script" : {
        "source" : "sigmoid(doc['my-int'].value, 2, 1)"
    }

##### 随机评分函数

"random_score"函数生成从 0 到但不包括 1 的均匀分布的分数。

'randomScore' 函数具有以下语法："randomScore(<seed>，<fieldName>)"。它有一个必需的参数 - 'seed' 作为整数值，以及一个可选参数 - 'fieldName' 作为字符串值。

    
    
    "script" : {
        "source" : "randomScore(100, '_seq_no')"
    }

如果省略"fieldName"参数，则内部Lucene文档ID将用作随机性来源。这是非常有效的，但不幸的是不可重现，因为文档可能会通过合并重新编号。

    
    
    "script" : {
        "source" : "randomScore(100)"
    }

请注意，位于同一分片中且具有相同 forfield 值的文档将获得相同的分数，因此通常需要使用对分片上所有文档具有唯一值的字段。一个不错的默认选择可能是使用"_seq_no"字段，其唯一的缺点是，如果更新文档，分数会发生变化，因为更新操作也会更新"_seq_no"字段的值。

##### 数值字段的衰减函数

您可以在此处阅读有关衰减函数的更多信息。

* 'Double decayNumericLinear(Double origin， double scale， double offset， double decay， double docValue)' * 'double decayNumericExp(double origin， double scale， double offset， double decay， double docValue)' * 'double decayNumericGauss(double origin， double scale， double offset， double decay， double docValue)'

    
    
    "script" : {
        "source" : "decayNumericLinear(params.origin, params.scale, params.offset, params.decay, doc['dval'].value)",
        "params": { __"origin": 20,
            "scale": 10,
            "decay" : 0.5,
            "offset" : 0
        }
    }

__

|

使用"params"允许只编译脚本一次，即使参数发生变化。   ---|--- ##### Geofields编辑的衰减函数

* 'double decayGeoLinear(String originStr， String scaleStr， String offsetStr， double decay， GeoPoint docValue)' * 'double decayGeoExp(String originStr， String scaleStr， String offsetStr， double decay， GeoPoint docValue)' * 'double decayGeoGauss(String originStr， String scaleStr， String offsetStr， double decay， GeoPoint docValue)'

    
    
    "script" : {
        "source" : "decayGeoExp(params.origin, params.scale, params.offset, params.decay, doc['location'].value)",
        "params": {
            "origin": "40, -70.12",
            "scale": "200km",
            "offset": "0km",
            "decay" : 0.2
        }
    }

##### 日期字段的衰减函数

* 'double decayDateLinear(String originStr， String scaleStr， String offsetStr， double decay， JodaCompatibleZonedDateTime docValueDate)' * 'double decayDateExp(String originStr， String scaleStr， String offsetStr， double decay， JodaCompatibleZonedDateTime docValueDate)' * 'double decayDateGauss(String originStr， String scaleStr， String offsetStr， double decay， JodaCompatibleZonedDateTime docValueDate)'

    
    
    "script" : {
        "source" : "decayDateGauss(params.origin, params.scale, params.offset, params.decay, doc['date'].value)",
        "params": {
            "origin": "2008-01-01T01:00:00Z",
            "scale": "1h",
            "offset" : "0",
            "decay" : 0.5
        }
    }

日期上的衰减函数仅限于默认格式和默认时区的日期。此外，不支持使用"现在"的计算。

##### 向量场的函数

矢量场的函数可通过"script_score"查询访问。

#### 允许昂贵的查询

如果"search.allow_expensive_queries"设置为 false，则不会执行脚本分数查询。

#### 更快的替代方案

"script_score"查询计算每个匹配文档的分数，或者。有更快的替代查询类型可以有效地跳过非竞争性命中：

* 如果要提升某些静态字段的文档，请使用"rank_feature"查询。  * 如果要将文档提升到更接近日期或地理点的位置，请使用"distance_feature"查询。

#### 从函数分数查询转换

我们建议使用"script_score"查询而不是"function_score"查询，以实现"script_score"查询的简单性。

您可以使用"script_score"查询实现"function_score"查询的以下函数：

* "script_score" * "重量" * "random_score" * "field_value_factor" * "衰减"函数

#####'script_score'

在函数分数查询的"script_score"中使用的内容，可以复制到脚本分数查询中。这里没有变化。

######'重量'

"weight"函数可以通过以下脚本在脚本分数查询中实现：

    
    
    "script" : {
        "source" : "params.weight * _score",
        "params": {
            "weight": 2
        }
    }

#####'random_score'

使用随机评分函数中所述的"随机评分"函数。

#####'field_value_factor'

"field_value_factor"功能可以通过脚本轻松实现：

    
    
    "script" : {
        "source" : "Math.log10(doc['field'].value * params.factor)",
        "params" : {
            "factor" : 5
        }
    }

要检查文档是否有缺失值，您可以使用'doc['field'].size() == 0'。例如，如果文档没有字段"field"，则此脚本将使用值"1"：

    
    
    "script" : {
        "source" : "Math.log10((doc['field'].size() == 0 ? 1 : doc['field'].value()) * params.factor)",
        "params" : {
            "factor" : 5
        }
    }

下表列出了如何通过脚本实现"field_value_factor"修饰符：

修饰符 |脚本分数中的实现 ---|--- "无"

|

- "日志"

|

'Math.log10(doc['f'].value)' 'log1p'

|

'Math.log10(doc['f'].value + 1)' 'log2p'

|

'Math.log10(doc['f'].value + 2)' 'ln'

|

'Math.log(doc['f'].value)' 'ln1p'

|

'Math.log(doc['f'].value + 1)' 'ln2p'

|

'Math.log(doc['f'].value + 2)' 'square'

|

'Math.pow(doc['f'].value， 2)' 'sqrt'

|

'Math.sqrt(doc['f'].value)' 'reciprocal'

|

'1.0 / doc'f'].value' ##### 'decay'functions[编辑]

"script_score"查询具有可在脚本中使用的等效衰减函数。

#### 向量场的函数

在向量函数计算过程中，所有匹配的文档都会被线性扫描。因此，预计查询时间会随着匹配文档的数量而线性增长。因此，我们建议使用"query"参数限制匹配文档的数量。

以下是可用的矢量函数和矢量访问方法的列表：

1. "余弦相似性" – 计算余弦相似性 2."点积" – 计算点积 3。"l1norm"") – 计算 L1 距离 4。'l2norm'") \- 计算 L2 距离 5。'doc[<field>].vectorValue' – 以浮点数数组 6 的形式返回向量的值。 'doc[<field>].magnitude' – 返回向量的大小

访问密集向量的推荐方法是通过"余弦相似性"、"点积"、"l1范数"或"l2范数"函数。但请注意，每个脚本只应调用一次这些函数。例如，不要在循环中使用这些函数来计算文档向量与多个其他向量之间的相似性。如果需要该功能，请通过直接访问矢量值自行重新实现这些函数。

让我们创建一个具有"dense_vector"映射的索引，并将几个文档索引到其中。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            my_dense_vector: {
              type: 'dense_vector',
              dims: 3
            },
            status: {
              type: 'keyword'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        my_dense_vector: [
          0.5,
          10,
          6
        ],
        status: 'published'
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      body: {
        my_dense_vector: [
          -0.5,
          10,
          10
        ],
        status: 'published'
      }
    )
    puts response
    
    response = client.indices.refresh(
      index: 'my-index-000001'
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "my_dense_vector": {
            "type": "dense_vector",
            "dims": 3
          },
          "status" : {
            "type" : "keyword"
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "my_dense_vector": [0.5, 10, 6],
      "status" : "published"
    }
    
    PUT my-index-000001/_doc/2
    {
      "my_dense_vector": [-0.5, 10, 10],
      "status" : "published"
    }
    
    POST my-index-000001/_refresh

##### 余弦相似性

"余弦相似性"函数计算给定查询向量和文档向量之间的余弦相似性度量。

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          script_score: {
            query: {
              bool: {
                filter: {
                  term: {
                    status: 'published'
                  }
                }
              }
            },
            script: {
              source: "cosineSimilarity(params.query_vector, 'my_dense_vector') + 1.0",
              params: {
                query_vector: [
                  4,
                  3.4,
                  -0.2
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "query": {
        "script_score": {
          "query" : {
            "bool" : {
              "filter" : {
                "term" : {
                  "status" : "published" __}
              }
            }
          },
          "script": {
            "source": "cosineSimilarity(params.query_vector, 'my_dense_vector') + 1.0", __"params": {
              "query_vector": [4, 3.4, -0.2] __}
          }
        }
      }
    }

__

|

若要限制应用脚本分数计算的文档数，请提供筛选器。   ---|---    __

|

该脚本将余弦相似性加 1.0，以防止分数为负。   __

|

若要利用脚本优化，请提供查询向量作为脚本参数。   如果文档的密集向量字段的多个维度与查询的向量不同，则会引发错误。

##### 点积

"dotProduct"函数计算给定查询向量和文档向量之间的点积度量。

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          script_score: {
            query: {
              bool: {
                filter: {
                  term: {
                    status: 'published'
                  }
                }
              }
            },
            script: {
              source: "\n          double value = dotProduct(params.query_vector, 'my_dense_vector');\n          return sigmoid(1, Math.E, -value); \n        ",
              params: {
                query_vector: [
                  4,
                  3.4,
                  -0.2
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "query": {
        "script_score": {
          "query" : {
            "bool" : {
              "filter" : {
                "term" : {
                  "status" : "published"
                }
              }
            }
          },
          "script": {
            "source": """
              double value = dotProduct(params.query_vector, 'my_dense_vector');
              return sigmoid(1, Math.E, -value); __""",
            "params": {
              "query_vector": [4, 3.4, -0.2]
            }
          }
        }
      }
    }

__

|

使用标准 sigmoid 函数可防止分数为负。   ---|--- ##### L1 距离(曼哈顿距离)编辑

"l1norm"函数计算给定查询向量和文档向量之间的 L1 距离(曼哈顿距离)。

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          script_score: {
            query: {
              bool: {
                filter: {
                  term: {
                    status: 'published'
                  }
                }
              }
            },
            script: {
              source: "1 / (1 + l1norm(params.queryVector, 'my_dense_vector'))",
              params: {
                "queryVector": [
                  4,
                  3.4,
                  -0.2
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "query": {
        "script_score": {
          "query" : {
            "bool" : {
              "filter" : {
                "term" : {
                  "status" : "published"
                }
              }
            }
          },
          "script": {
            "source": "1 / (1 + l1norm(params.queryVector, 'my_dense_vector'))", __"params": {
              "queryVector": [4, 3.4, -0.2]
            }
          }
        }
      }
    }

__

|

与表示相似性的"余弦相似性"不同，下面显示的"l1范数"和"l2范数"表示距离或差异。这意味着，向量越相似，"l1范数"和"l2范数"函数产生的分数就越低。因此，由于我们需要更多相似的向量来获得更高的分数，我们反转了"l1norm"和"l2norm"的输出。此外，为了避免在文档向量与查询完全匹配时除以 0，我们在分母中添加了"1"。   ---|--- ##### L2 距离(欧几里得距离)编辑

"l2norm"函数计算给定查询向量和文档向量之间的 L2 距离(欧氏距离)。

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          script_score: {
            query: {
              bool: {
                filter: {
                  term: {
                    status: 'published'
                  }
                }
              }
            },
            script: {
              source: "1 / (1 + l2norm(params.queryVector, 'my_dense_vector'))",
              params: {
                "queryVector": [
                  4,
                  3.4,
                  -0.2
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "query": {
        "script_score": {
          "query" : {
            "bool" : {
              "filter" : {
                "term" : {
                  "status" : "published"
                }
              }
            }
          },
          "script": {
            "source": "1 / (1 + l2norm(params.queryVector, 'my_dense_vector'))",
            "params": {
              "queryVector": [4, 3.4, -0.2]
            }
          }
        }
      }
    }

##### 检查缺失值

如果文档没有执行向量函数的向量字段的值，则会引发错误。

您可以使用"doc['my_vector'].size() == 0' 检查文档是否具有字段"my_vector"的值。您的整个脚本可能如下所示：

    
    
    "source": "doc['my_vector'].size() == 0 ? 0 : cosineSimilarity(params.queryVector, 'my_vector')"

##### 直接访问向量

您可以通过以下函数直接访问矢量值：

* 'doc[].vectorValue' – 以浮点数数组的形式返回向量<field>的值 * 'doc[<field>].magnitude' – 以浮点数的形式返回向量的大小(对于在版本 7.5 之前创建的向量，不会存储量级。因此，此函数每次调用时都会重新计算它)。

例如，下面的脚本使用这两个函数实现余弦相似性：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          script_score: {
            query: {
              bool: {
                filter: {
                  term: {
                    status: 'published'
                  }
                }
              }
            },
            script: {
              source: "\n          float[] v = doc['my_dense_vector'].vectorValue;\n          float vm = doc['my_dense_vector'].magnitude;\n          float dotProduct = 0;\n          for (int i = 0; i < v.length; i++) {\n            dotProduct += v[i] * params.queryVector[i];\n          }\n          return dotProduct / (vm * (float) params.queryVectorMag);\n        ",
              params: {
                "queryVector": [
                  4,
                  3.4,
                  -0.2
                ],
                "queryVectorMag": 5.25357
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "query": {
        "script_score": {
          "query" : {
            "bool" : {
              "filter" : {
                "term" : {
                  "status" : "published"
                }
              }
            }
          },
          "script": {
            "source": """
              float[] v = doc['my_dense_vector'].vectorValue;
              float vm = doc['my_dense_vector'].magnitude;
              float dotProduct = 0;
              for (int i = 0; i < v.length; i++) {
                dotProduct += v[i] * params.queryVector[i];
              }
              return dotProduct / (vm * (float) params.queryVectorMag);
            """,
            "params": {
              "queryVector": [4, 3.4, -0.2],
              "queryVectorMag": 5.25357
            }
          }
        }
      }
    }

#### 解释请求

使用解释请求可以解释分数的各个部分是如何计算的。"script_score"查询可以通过设置"解释"参数来添加自己的解释：

    
    
    response = client.explain(
      index: 'my-index-000001',
      id: 0,
      body: {
        query: {
          script_score: {
            query: {
              match: {
                message: 'elasticsearch'
              }
            },
            script: {
              source: "\n          long count = doc['count'].value;\n          double normalizedCount = count / 10;\n          if (explanation != nil) {\n            explanation.set('normalized count = count / 10 = ' + count + ' / 10 = ' + normalizedCount);\n          }\n          return normalizedCount;\n        "
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_explain/0
    {
      "query": {
        "script_score": {
          "query": {
            "match": { "message": "elasticsearch" }
          },
          "script": {
            "source": """
              long count = doc['count'].value;
              double normalizedCount = count / 10;
              if (explanation != null) {
                explanation.set('normalized count = count / 10 = ' + count + ' / 10 = ' + normalizedCount);
              }
              return normalizedCount;
            """
          }
        }
      }
    }

请注意，在正常的"_search"请求中使用时，"解释"将为空，因此最好使用条件保护。

[« Script query](query-dsl-script-query.md) [Wrapper query »](query-dsl-
wrapper-query.md)
