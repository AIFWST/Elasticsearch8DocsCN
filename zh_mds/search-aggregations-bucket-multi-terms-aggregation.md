

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Missing aggregation](search-aggregations-bucket-missing-aggregation.md)
[Nested aggregation »](search-aggregations-bucket-nested-aggregation.md)

## 多术语聚合

基于多存储桶值源的聚合，其中存储桶是动态构建的 - 每个唯一的值集一个。多术语聚合与"术语聚合"非常相似，但在大多数情况下，它将比术语聚合慢，并且会消耗更多内存。因此，如果经常使用同一组字段，则将此字段的组合键索引为单独的字段并在此字段上使用术语聚合会更有效。

当您需要按多个文档或组合键上的指标聚合进行排序并获得前 N 个结果时，multi_term聚合最有用。如果不需要排序，并且预期使用嵌套术语聚合或"复合聚合"将是一个更快、更节省内存的解决方案。

Example:

    
    
    response = client.search(
      index: 'products',
      body: {
        aggregations: {
          genres_and_products: {
            multi_terms: {
              terms: [
                {
                  field: 'genre'
                },
                {
                  field: 'product'
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET /products/_search
    {
      "aggs": {
        "genres_and_products": {
          "multi_terms": {
            "terms": [{
              "field": "genre" __}, {
              "field": "product"
            }]
          }
        }
      }
    }

__

|

"multi_terms"聚合可以使用与"术语聚合"相同的字段类型，并支持大多数术语聚合参数。   ---|--- 响应：

    
    
    {
      ...
      "aggregations" : {
        "genres_and_products" : {
          "doc_count_error_upper_bound" : 0,  __"sum_other_doc_count" : 0, __"buckets" : [ __{
              "key" : [ __"rock",
                "Product A"
              ],
              "key_as_string" : "rock|Product A",
              "doc_count" : 2
            },
            {
              "key" : [
                "electronic",
                "Product B"
              ],
              "key_as_string" : "electronic|Product B",
              "doc_count" : 1
            },
            {
              "key" : [
                "jazz",
                "Product B"
              ],
              "key_as_string" : "jazz|Product B",
              "doc_count" : 1
            },
            {
              "key" : [
                "rock",
                "Product B"
              ],
              "key_as_string" : "rock|Product B",
              "doc_count" : 1
            }
          ]
        }
      }
    }

__

|

文档错误对每个术语计数的上限，请参阅<<搜索聚合桶多术语聚合近似计数，下面> ---|---__

|

当有很多唯一术语时，Elasticsearch 只返回排名靠前的术语;这个数字是不属于响应的所有存储桶的文档计数之和 __

|

排名靠前的存储桶列表。   __

|

键是值数组，排序方式与聚合的"terms"参数中的表达式相同 默认情况下，"multi_terms"聚合将返回按"doc_count"排序的前十个术语的存储桶。可以通过设置"size"参数来更改此默认行为。

### 聚合参数

支持以下参数。有关这些参数的更详细说明，请参阅"术语聚合"。

size

|

自选。定义应从总体术语列表中返回的术语存储桶数。默认值为 10。   ---|--- shard_size

|

自选。请求的"大小"越高，结果就越准确，但计算最终结果的成本也就越高。默认的"shard_size"是"(大小 * 1.5 + 10)"。   show_term_doc_count_error

|

自选。按学期计算文档计数错误。默认为"假"顺序

|

自选。指定存储桶的顺序。默认为每个存储桶的文档数。存储桶条款值用作具有相同文档计数的存储桶的仲裁规则。   min_doc_count

|

自选。存储桶中要返回的最小文档数。默认值为 1。   shard_min_doc_count

|

自选。每个分片上存储桶中要返回的最小文档数。默认为"min_doc_count"。   collect_mode

|

自选。指定数据收集的策略。支持"depth_first"或"breadth_first"模式。默认为"breadth_first"。   ###Scriptedit

使用脚本生成项：

    
    
    response = client.search(
      index: 'products',
      body: {
        runtime_mappings: {
          "genre.length": {
            type: 'long',
            script: "emit(doc['genre'].value.length())"
          }
        },
        aggregations: {
          genres_and_products: {
            multi_terms: {
              terms: [
                {
                  field: 'genre.length'
                },
                {
                  field: 'product'
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET /products/_search
    {
      "runtime_mappings": {
        "genre.length": {
          "type": "long",
          "script": "emit(doc['genre'].value.length())"
        }
      },
      "aggs": {
        "genres_and_products": {
          "multi_terms": {
            "terms": [
              {
                "field": "genre.length"
              },
              {
                "field": "product"
              }
            ]
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations" : {
        "genres_and_products" : {
          "doc_count_error_upper_bound" : 0,
          "sum_other_doc_count" : 0,
          "buckets" : [
            {
              "key" : [
                4,
                "Product A"
              ],
              "key_as_string" : "4|Product A",
              "doc_count" : 2
            },
            {
              "key" : [
                4,
                "Product B"
              ],
              "key_as_string" : "4|Product B",
              "doc_count" : 2
            },
            {
              "key" : [
                10,
                "Product B"
              ],
              "key_as_string" : "10|Product B",
              "doc_count" : 1
            }
          ]
        }
      }
    }

### 缺失值

"missing"参数定义应如何处理缺少值的文档。默认情况下，如果缺少任何关键组件，则将忽略整个文档，但也可以使用"missing"参数将它们视为具有值。

    
    
    response = client.search(
      index: 'products',
      body: {
        aggregations: {
          genres_and_products: {
            multi_terms: {
              terms: [
                {
                  field: 'genre'
                },
                {
                  field: 'product',
                  missing: 'Product Z'
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET /products/_search
    {
      "aggs": {
        "genres_and_products": {
          "multi_terms": {
            "terms": [
              {
                "field": "genre"
              },
              {
                "field": "product",
                "missing": "Product Z"
              }
            ]
          }
        }
      }
    }

Response:

    
    
    {
       ...
       "aggregations" : {
        "genres_and_products" : {
          "doc_count_error_upper_bound" : 0,
          "sum_other_doc_count" : 0,
          "buckets" : [
            {
              "key" : [
                "rock",
                "Product A"
              ],
              "key_as_string" : "rock|Product A",
              "doc_count" : 2
            },
            {
              "key" : [
                "electronic",
                "Product B"
              ],
              "key_as_string" : "electronic|Product B",
              "doc_count" : 1
            },
            {
              "key" : [
                "electronic",
                "Product Z"
              ],
              "key_as_string" : "electronic|Product Z",  __"doc_count" : 1
            },
            {
              "key" : [
                "jazz",
                "Product B"
              ],
              "key_as_string" : "jazz|Product B",
              "doc_count" : 1
            },
            {
              "key" : [
                "rock",
                "Product B"
              ],
              "key_as_string" : "rock|Product B",
              "doc_count" : 1
            }
          ]
        }
      }
    }

__

|

"产品"字段中没有值的文档将与值为"产品 Z"的文档属于同一存储桶。   ---|--- ### 混合字段类型编辑

聚合多个索引时，聚合字段的类型在所有索引中可能不同。某些类型彼此兼容("整数"和"长整型"或"浮点数"和"双精度数")，但是当类型是十进制数和非十进制数的混合时，术语聚合会将非十进制数提升为十进制数。这可能会导致存储桶值的精度损失。

### 子聚合和排序示例

与大多数存储桶聚合一样，"multi_term"支持子聚合并按指标子聚合对存储桶进行排序：

    
    
    response = client.search(
      index: 'products',
      body: {
        aggregations: {
          genres_and_products: {
            multi_terms: {
              terms: [
                {
                  field: 'genre'
                },
                {
                  field: 'product'
                }
              ],
              order: {
                total_quantity: 'desc'
              }
            },
            aggregations: {
              total_quantity: {
                sum: {
                  field: 'quantity'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /products/_search
    {
      "aggs": {
        "genres_and_products": {
          "multi_terms": {
            "terms": [
              {
                "field": "genre"
              },
              {
                "field": "product"
              }
            ],
            "order": {
              "total_quantity": "desc"
            }
          },
          "aggs": {
            "total_quantity": {
              "sum": {
                "field": "quantity"
              }
            }
          }
        }
      }
    }
    
    
    {
      ...
      "aggregations" : {
        "genres_and_products" : {
          "doc_count_error_upper_bound" : 0,
          "sum_other_doc_count" : 0,
          "buckets" : [
            {
              "key" : [
                "jazz",
                "Product B"
              ],
              "key_as_string" : "jazz|Product B",
              "doc_count" : 1,
              "total_quantity" : {
                "value" : 10.0
              }
            },
            {
              "key" : [
                "rock",
                "Product A"
              ],
              "key_as_string" : "rock|Product A",
              "doc_count" : 2,
              "total_quantity" : {
                "value" : 9.0
              }
            },
            {
              "key" : [
                "electronic",
                "Product B"
              ],
              "key_as_string" : "electronic|Product B",
              "doc_count" : 1,
              "total_quantity" : {
                "value" : 3.0
              }
            },
            {
              "key" : [
                "rock",
                "Product B"
              ],
              "key_as_string" : "rock|Product B",
              "doc_count" : 1,
              "total_quantity" : {
                "value" : 1.0
              }
            }
          ]
        }
      }
    }

[« Missing aggregation](search-aggregations-bucket-missing-aggregation.md)
[Nested aggregation »](search-aggregations-bucket-nested-aggregation.md)
