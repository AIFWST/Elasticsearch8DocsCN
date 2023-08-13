

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Diversified sampler aggregation](search-aggregations-bucket-diversified-
sampler-aggregation.md) [Filters aggregation »](search-aggregations-bucket-
filters-aggregation.md)

## 筛选器聚合

单个存储桶聚合，用于将文档集缩小到与查询匹配的文档集。

Example:

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      filter_path: 'aggregations',
      body: {
        aggregations: {
          avg_price: {
            avg: {
              field: 'price'
            }
          },
          t_shirts: {
            filter: {
              term: {
                type: 't-shirt'
              }
            },
            aggregations: {
              avg_price: {
                avg: {
                  field: 'price'
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
        "avg_price": { "avg": { "field": "price" } },
        "t_shirts": {
          "filter": { "term": { "type": "t-shirt" } },
          "aggs": {
            "avg_price": { "avg": { "field": "price" } }
          }
        }
      }
    }

前面的示例计算所有销售的平均价格以及所有 T 恤销售的平均价格。

Response:

    
    
    {
      "aggregations": {
        "avg_price": { "value": 140.71428571428572 },
        "t_shirts": {
          "doc_count": 3,
          "avg_price": { "value": 128.33333333333334 }
        }
      }
    }

### 使用顶级"查询"来限制所有聚合

若要限制运行搜索中所有聚合的文档，请使用顶级"查询"。这比具有子聚合的单个"过滤器"聚合更快。

例如，使用以下命令：

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      filter_path: 'aggregations',
      body: {
        query: {
          term: {
            type: 't-shirt'
          }
        },
        aggregations: {
          avg_price: {
            avg: {
              field: 'price'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0&filter_path=aggregations
    {
      "query": { "term": { "type": "t-shirt" } },
      "aggs": {
        "avg_price": { "avg": { "field": "price" } }
      }
    }

取而代之的是：

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      filter_path: 'aggregations',
      body: {
        aggregations: {
          t_shirts: {
            filter: {
              term: {
                type: 't-shirt'
              }
            },
            aggregations: {
              avg_price: {
                avg: {
                  field: 'price'
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
        "t_shirts": {
          "filter": { "term": { "type": "t-shirt" } },
          "aggs": {
            "avg_price": { "avg": { "field": "price" } }
          }
        }
      }
    }

### 对多个过滤器使用"过滤器"聚合

要使用多个过滤器对文档进行分组，请使用"过滤器"聚合。这比多个"过滤器"聚合更快。

例如，使用以下命令：

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      filter_path: 'aggregations',
      body: {
        aggregations: {
          f: {
            filters: {
              filters: {
                hats: {
                  term: {
                    type: 'hat'
                  }
                },
                t_shirts: {
                  term: {
                    type: 't-shirt'
                  }
                }
              }
            },
            aggregations: {
              avg_price: {
                avg: {
                  field: 'price'
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
        "f": {
          "filters": {
            "filters": {
              "hats": { "term": { "type": "hat" } },
              "t_shirts": { "term": { "type": "t-shirt" } }
            }
          },
          "aggs": {
            "avg_price": { "avg": { "field": "price" } }
          }
        }
      }
    }

取而代之的是：

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      filter_path: 'aggregations',
      body: {
        aggregations: {
          hats: {
            filter: {
              term: {
                type: 'hat'
              }
            },
            aggregations: {
              avg_price: {
                avg: {
                  field: 'price'
                }
              }
            }
          },
          t_shirts: {
            filter: {
              term: {
                type: 't-shirt'
              }
            },
            aggregations: {
              avg_price: {
                avg: {
                  field: 'price'
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
        "hats": {
          "filter": { "term": { "type": "hat" } },
          "aggs": {
            "avg_price": { "avg": { "field": "price" } }
          }
        },
        "t_shirts": {
          "filter": { "term": { "type": "t-shirt" } },
          "aggs": {
            "avg_price": { "avg": { "field": "price" } }
          }
        }
      }
    }

[« Diversified sampler aggregation](search-aggregations-bucket-diversified-
sampler-aggregation.md) [Filters aggregation »](search-aggregations-bucket-
filters-aggregation.md)
