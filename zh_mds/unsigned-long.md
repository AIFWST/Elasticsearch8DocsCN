

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Token count field type](token-count.md) [Version field type
»](version.md)

## 无符号长字段类型

无符号长整型是一种数值字段类型，表示最小值为 0，最大值为"264-1"(包括 0 到 18446744073709551615)的无符号 64 位整数。

    
    
    response = client.indices.create(
      index: 'my_index',
      body: {
        mappings: {
          properties: {
            my_counter: {
              type: 'unsigned_long'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my_index
    {
      "mappings": {
        "properties": {
          "my_counter": {
            "type": "unsigned_long"
          }
        }
      }
    }

无符号长整型可以以数字或字符串形式编制索引，表示 [0， 18446744073709551615] 范围内的整数值。它们不能有小数部分。

    
    
    response = client.bulk(
      index: 'my_index',
      refresh: true,
      body: [
        {
          index: {
            _id: 1
          }
        },
        {
          my_counter: 0
        },
        {
          index: {
            _id: 2
          }
        },
        {
          my_counter: 9_223_372_036_854_776_000
        },
        {
          index: {
            _id: 3
          }
        },
        {
          my_counter: 18_446_744_073_709_552_000
        },
        {
          index: {
            _id: 4
          }
        },
        {
          my_counter: 18_446_744_073_709_552_000
        }
      ]
    )
    puts response
    
    
    POST /my_index/_bulk?refresh
    {"index":{"_id":1}}
    {"my_counter": 0}
    {"index":{"_id":2}}
    {"my_counter": 9223372036854775808}
    {"index":{"_id":3}}
    {"my_counter": 18446744073709551614}
    {"index":{"_id":4}}
    {"my_counter": 18446744073709551615}

术语查询接受数字或字符串形式的任何数字。

    
    
    response = client.search(
      index: 'my_index',
      body: {
        query: {
          term: {
            my_counter: 18_446_744_073_709_552_000
          }
        }
      }
    )
    puts response
    
    
    GET /my_index/_search
    {
        "query": {
            "term" : {
                "my_counter" : 18446744073709551615
            }
        }
    }

范围查询词可以包含带有小数部分的值。在这种情况下，Elasticsearch 将它们转换为整数值："gte"和"gt"项将转换为最接近的整数(包括)，"lt"和"lte"范围将转换为最接近的整数(包括向下)。

建议将范围作为字符串传递，以确保解析它们时不会损失任何精度。

    
    
    response = client.search(
      index: 'my_index',
      body: {
        query: {
          range: {
            my_counter: {
              gte: '9223372036854775808',
              lte: '18446744073709551615'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my_index/_search
    {
        "query": {
            "range" : {
                "my_counter" : {
                    "gte" : "9223372036854775808",
                    "lte" : "18446744073709551615"
                }
            }
        }
    }

### 排序值

对于对"unsigned_long"字段进行排序的查询，对于特定文档，如果此文档的值在长整型值范围内，则返回类型为"long"的排序值，如果值超过此范围，则返回类型为"BigInteger"的排序值。

REST 客户端需要能够处理 JSON 中的大整数值才能正确支持此字段类型。

    
    
    response = client.search(
      index: 'my_index',
      body: {
        query: {
          match_all: {}
        },
        sort: {
          my_counter: 'desc'
        }
      }
    )
    puts response
    
    
    GET /my_index/_search
    {
        "query": {
            "match_all" : {}
        },
        "sort" : {"my_counter" : "desc"}
    }

### 存储字段

存储的"unsigned_long"字段被存储并作为"字符串"返回。

###Aggregations

对于"术语"聚合，与排序值类似，使用"长整型"或"大整数"值。对于其他聚合，值将转换为"双精度"类型。

### 脚本值

默认情况下，"unsigned_long"字段的脚本值以 Javasigned "Long"返回，这意味着大于 "Long.MAX_VALUE" 的值显示为负值。您可以使用"Long.compareUnsigned(long， long)"，"Long.divideUnsigned(long， long)"和"Long.RemainderUnsigned(long， long)"来正确使用这些值。

例如，下面的脚本返回计数器除以 10 的值。

    
    
    response = client.search(
      index: 'my_index',
      body: {
        query: {
          match_all: {}
        },
        script_fields: {
          "count10": {
            script: {
              source: "Long.divideUnsigned(doc['my_counter'].value, 10)"
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my_index/_search
    {
        "query": {
            "match_all" : {}
        },
        "script_fields": {
            "count10" : {
              "script": {
                "source": "Long.divideUnsigned(doc['my_counter'].value, 10)"
              }
            }
        }
    }

或者，您可以使用字段 API 在脚本中将无符号长型视为"BigInteger"。例如，此脚本将"my_counter"视为默认值为"BigInteger.ZERO"的"BigInteger"：

    
    
    "script": {
        "source": "field('my_counter').asBigInteger(BigInteger.ZERO)"
    }

对于需要返回浮点数或双精度值的脚本，您可以将"BigInteger"值进一步转换为双精度或浮点数：

    
    
    response = client.search(
      index: 'my_index',
      body: {
        query: {
          script_score: {
            query: {
              match_all: {}
            },
            script: {
              source: "field('my_counter').asBigInteger(BigInteger.ZERO).floatValue()"
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my_index/_search
    {
        "query": {
            "script_score": {
              "query": {"match_all": {}},
              "script": {
                "source": "field('my_counter').asBigInteger(BigInteger.ZERO).floatValue()"
              }
            }
        }
    }

### 具有混合数字类型的查询

支持使用混合数字类型(其中一种是"unsigned_long")进行搜索，但具有排序的查询除外。因此，跨两个索引的排序查询(其中相同的字段名称在一个索引中具有"unsigned_long"类型，而在另一个索引中具有"long"类型)不会产生正确的结果，必须避免。如果需要这种排序，则可以改用基于脚本的排序。

支持跨多种数值类型的聚合，其中一种是"unsigned_long"。在这种情况下，值将转换为"双精度"类型。

[« Token count field type](token-count.md) [Version field type
»](version.md)
