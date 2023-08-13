

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Geotile grid aggregation](search-aggregations-bucket-geotilegrid-
aggregation.md) [Histogram aggregation »](search-aggregations-bucket-
histogram-aggregation.md)

## 全局聚合

定义搜索执行上下文中所有文档的单个存储桶。此上下文由您正在研究的索引和文档类型定义，但不受搜索查询本身的影响。

全局聚合器只能作为顶级聚合器放置，因为将全局聚合器嵌入到另一个存储桶聚合器中没有意义。

Example:

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        query: {
          match: {
            type: 't-shirt'
          }
        },
        aggregations: {
          all_products: {
            global: {},
            aggregations: {
              avg_price: {
                avg: {
                  field: 'price'
                }
              }
            }
          },
          t_shirts: {
            avg: {
              field: 'price'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "query": {
        "match": { "type": "t-shirt" }
      },
      "aggs": {
        "all_products": {
          "global": {}, __"aggs": { __"avg_price": { "avg": { "field": "price" } }
          }
        },
        "t_shirts": { "avg": { "field": "price" } }
      }
    }

__

|

"全局"聚合有一个空体 ---|--- __

|

为此"全局"聚合注册的子聚合 上面的聚合演示了如何计算搜索上下文中所有文档的聚合(本例中为"avg_price")，而不考虑查询(在我们的示例中，它将计算目录中所有产品的平均价格，而不仅仅是"衬衫")。

上述聚合的响应：

    
    
    {
      ...
      "aggregations": {
        "all_products": {
          "doc_count": 7, __"avg_price": {
            "value": 140.71428571428572 __}
        },
        "t_shirts": {
          "value": 128.33333333333334 __}
      }
    }

__

|

聚合的文档数(在本例中为搜索上下文中的所有文档)---|--- __

|

指数中所有产品的平均价格 __

|

所有T恤的平均价格 « 地瓦网格聚合直方图聚合 »