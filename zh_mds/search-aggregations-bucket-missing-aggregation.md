

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« IP range aggregation](search-aggregations-bucket-iprange-aggregation.md)
[Multi Terms aggregation »](search-aggregations-bucket-multi-terms-
aggregation.md)

## 缺少聚合

基于字段数据的单个存储桶聚合，用于创建当前文档集上下文中缺少字段值(实际上缺少字段或具有配置的 NULL 值集)的所有文档的存储桶。此聚合器通常与其他字段数据存储桶聚合器(例如范围)结合使用，以返回由于缺少字段数据值而无法放置在任何其他存储桶中的所有文档的信息。

Example:

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          products_without_a_price: {
            missing: {
              field: 'price'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "products_without_a_price": {
          "missing": { "field": "price" }
        }
      }
    }

在上面的例子中，我们得到了没有价格的产品总数。

Response:

    
    
    {
      ...
      "aggregations": {
        "products_without_a_price": {
          "doc_count": 0
        }
      }
    }

[« IP range aggregation](search-aggregations-bucket-iprange-aggregation.md)
[Multi Terms aggregation »](search-aggregations-bucket-multi-terms-
aggregation.md)
