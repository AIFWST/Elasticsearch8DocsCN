

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Multi Terms aggregation](search-aggregations-bucket-multi-terms-
aggregation.md) [Parent aggregation »](search-aggregations-bucket-parent-
aggregation.md)

## 嵌套聚合

一种特殊的单存储桶聚合，支持聚合嵌套文档。

例如，假设我们有一个产品索引，每个产品都包含经销商列表 - 每个经销商都有自己的产品价格。映射可能如下所示：

    
    
    response = client.indices.create(
      index: 'products',
      body: {
        mappings: {
          properties: {
            resellers: {
              type: 'nested',
              properties: {
                reseller: {
                  type: 'keyword'
                },
                price: {
                  type: 'double'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /products
    {
      "mappings": {
        "properties": {
          "resellers": { __"type": "nested",
            "properties": {
              "reseller": {
                "type": "keyword"
              },
              "price": {
                "type": "double"
              }
            }
          }
        }
      }
    }

__

|

"经销商"是一个保存嵌套文档的数组。   ---|--- 以下请求添加具有两个经销商的产品：

    
    
    PUT /products/_doc/0?refresh
    {
      "name": "LED TV", __"resellers": [
        {
          "reseller": "companyA",
          "price": 350
        },
        {
          "reseller": "companyB",
          "price": 500
        }
      ]
    }

__

|

我们正在对"name"属性使用动态映射。   ---|--- 以下请求返回可以购买产品的最低价格：

    
    
    response = client.search(
      index: 'products',
      size: 0,
      body: {
        query: {
          match: {
            name: 'led tv'
          }
        },
        aggregations: {
          resellers: {
            nested: {
              path: 'resellers'
            },
            aggregations: {
              min_price: {
                min: {
                  field: 'resellers.price'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /products/_search?size=0
    {
      "query": {
        "match": {
          "name": "led tv"
        }
      },
      "aggs": {
        "resellers": {
          "nested": {
            "path": "resellers"
          },
          "aggs": {
            "min_price": {
              "min": {
                "field": "resellers.price"
              }
            }
          }
        }
      }
    }

正如您在上面看到的，嵌套聚合需要顶级文档中嵌套文档的"路径"。然后，可以在这些嵌套文档上定义任何类型的聚合。

Response:

    
    
    {
      ...
      "aggregations": {
        "resellers": {
          "doc_count": 2,
          "min_price": {
            "value": 350.0
          }
        }
      }
    }

您可以使用"筛选器"子聚合返回特定经销商的结果。

    
    
    response = client.search(
      index: 'products',
      size: 0,
      body: {
        query: {
          match: {
            name: 'led tv'
          }
        },
        aggregations: {
          resellers: {
            nested: {
              path: 'resellers'
            },
            aggregations: {
              filter_reseller: {
                filter: {
                  bool: {
                    filter: [
                      {
                        term: {
                          "resellers.reseller": 'companyB'
                        }
                      }
                    ]
                  }
                },
                aggregations: {
                  min_price: {
                    min: {
                      field: 'resellers.price'
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
    
    
    GET /products/_search?size=0
    {
      "query": {
        "match": {
          "name": "led tv"
        }
      },
      "aggs": {
        "resellers": {
          "nested": {
            "path": "resellers"
          },
          "aggs": {
            "filter_reseller": {
              "filter": {
                "bool": {
                  "filter": [
                    {
                      "term": {
                        "resellers.reseller": "companyB"
                      }
                    }
                  ]
                }
              },
              "aggs": {
                "min_price": {
                  "min": {
                    "field": "resellers.price"
                  }
                }
              }
            }
          }
        }
      }
    }

搜索返回：

    
    
    {
      ...
      "aggregations": {
        "resellers": {
          "doc_count": 2,
          "filter_reseller": {
            "doc_count": 1,
            "min_price": {
              "value": 500.0
            }
          }
        }
      }
    }

[« Multi Terms aggregation](search-aggregations-bucket-multi-terms-
aggregation.md) [Parent aggregation »](search-aggregations-bucket-parent-
aggregation.md)
