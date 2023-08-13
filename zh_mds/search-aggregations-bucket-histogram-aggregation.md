

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Global aggregation](search-aggregations-bucket-global-aggregation.md) [IP
prefix aggregation »](search-aggregations-bucket-ipprefix-aggregation.md)

## 直方图聚合

基于源的多存储桶值聚合，可应用于从文档中提取的数字值或数值范围值。它在值上动态构建固定大小(也称为间隔)存储桶。例如，如果文档有一个保存价格(数字)的字段，我们可以配置此聚合以动态构建间隔为"5"的存储桶(在价格的情况下它可能代表 $5)。当聚合执行时，将评估每个文档的价格字段，并将其向下舍入到其最接近的存储桶 - 例如，如果价格为"32"，存储桶大小为"5"，则舍入将产生"30"，因此文档将"落入"与键"30"关联的存储桶中。为了使它更正式，下面是使用的舍入函数：

    
    
    bucket_key = Math.floor((value - offset) / interval) * interval + offset

对于范围值，一个文档可以属于多个存储桶。第一个存储桶从范围的下限计算，其计算方式与计算单个值的存储桶的方式相同。从范围的上限以相同的方式计算最终存储桶，并且该范围计入介于两者之间的所有存储桶中，包括这两个存储桶。

"间隔"必须是正小数，而"偏移量"必须是"[0，间隔)"中的小数(大于或等于"0"且小于"间隔"的小数)

以下代码段根据产品的"价格"(间隔为"50")对产品进行"桶化"：

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          prices: {
            histogram: {
              field: 'price',
              interval: 50
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "prices": {
          "histogram": {
            "field": "price",
            "interval": 50
          }
        }
      }
    }

以下是可能的响应：

    
    
    {
      ...
      "aggregations": {
        "prices": {
          "buckets": [
            {
              "key": 0.0,
              "doc_count": 1
            },
            {
              "key": 50.0,
              "doc_count": 1
            },
            {
              "key": 100.0,
              "doc_count": 0
            },
            {
              "key": 150.0,
              "doc_count": 2
            },
            {
              "key": 200.0,
              "doc_count": 3
            }
          ]
        }
      }
    }

### 最小文档计数

上面的响应显示，没有文档的价格在"[100， 150)"范围内。默认情况下，响应将使用空存储桶填充直方图中的空白。由于"min_doc_count"设置，可以更改它并请求具有更高最小计数的存储桶：

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          prices: {
            histogram: {
              field: 'price',
              interval: 50,
              min_doc_count: 1
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "prices": {
          "histogram": {
            "field": "price",
            "interval": 50,
            "min_doc_count": 1
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "prices": {
          "buckets": [
            {
              "key": 0.0,
              "doc_count": 1
            },
            {
              "key": 50.0,
              "doc_count": 1
            },
            {
              "key": 150.0,
              "doc_count": 2
            },
            {
              "key": 200.0,
              "doc_count": 3
            }
          ]
        }
      }
    }

默认情况下，"直方图"返回数据本身范围内的所有存储桶，也就是说，具有最小值的文档(带有直方图)将确定最小存储桶(具有最小键的存储桶)，具有最高值的文档将确定最大存储桶(具有最高键的存储桶)。通常，在请求空存储桶时，这会导致混淆，特别是当数据也被过滤时。

为了理解原因，让我们看一个例子：

假设您正在过滤请求以获取值介于"0"和"500"之间的所有文档，此外，您希望使用间隔为"50"的直方图对每个价格的数据进行切片。您还可以指定"min_doc_count"：0"，因为您希望获得所有存储桶，甚至是空存储桶。如果碰巧所有产品(文档)的价格都高于"100"，您将获得的第一个存储桶将是以"100"为键的存储桶。这很令人困惑，因为很多时候，您还想在"0 - 100"之间获取这些存储桶。

使用"extended_bounds"设置，您现在可以"强制"直方图聚合开始根据特定的"最小"值构建存储桶，并继续构建存储桶，直到"最大"值(即使不再有文档)。仅当"min_doc_count"为 0 时才使用"extended_bounds"才有意义(如果"min_doc_count"大于 0，则永远不会返回空桶)。

请注意，(顾名思义)"extended_bounds"不是过滤桶。这意味着，如果"extended_bounds.min"高于从文档中提取的值，文档仍将指示第一个存储桶是什么("extended_bounds.max"和最后一个存储桶也是如此)。对于过滤存储桶，应将直方图聚合嵌套在具有适当"发件人"/"到"设置的"过滤器"聚合范围下。

Example:

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        query: {
          constant_score: {
            filter: {
              range: {
                price: {
                  to: '500'
                }
              }
            }
          }
        },
        aggregations: {
          prices: {
            histogram: {
              field: 'price',
              interval: 50,
              extended_bounds: {
                min: 0,
                max: 500
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "query": {
        "constant_score": { "filter": { "range": { "price": { "to": "500" } } } }
      },
      "aggs": {
        "prices": {
          "histogram": {
            "field": "price",
            "interval": 50,
            "extended_bounds": {
              "min": 0,
              "max": 500
            }
          }
        }
      }
    }

聚合范围时，存储桶基于返回文档的值。这意味着响应可能包含查询范围之外的存储桶。例如，如果您的查询查找大于 100 的值，并且您的范围涵盖 50 到 150，间隔为 50，则该文档将位于 3 个存储桶中 - 50、100 和 150。通常，最好将查询和聚合步骤视为独立的 - 查询选择一组文档，然后聚合存储桶这些文档，而不考虑它们的选择方式。有关详细信息和示例，请参阅有关存储桶范围字段的说明。

"hard_bounds"与"extended_bounds"相对应，可以限制直方图中的桶范围。在打开数据范围的情况下，它特别有用，这可能会导致非常大量的存储桶。

Example:

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        query: {
          constant_score: {
            filter: {
              range: {
                price: {
                  to: '500'
                }
              }
            }
          }
        },
        aggregations: {
          prices: {
            histogram: {
              field: 'price',
              interval: 50,
              hard_bounds: {
                min: 100,
                max: 200
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "query": {
        "constant_score": { "filter": { "range": { "price": { "to": "500" } } } }
      },
      "aggs": {
        "prices": {
          "histogram": {
            "field": "price",
            "interval": 50,
            "hard_bounds": {
              "min": 100,
              "max": 200
            }
          }
        }
      }
    }

在此示例中，即使查询中指定的范围最大为 500，直方图也只有 2 个存储桶，从 100 和 150 开始。即使结果中存在应转到此存储桶的文档，也将省略所有其他存储桶。

###Order

默认情况下，返回的存储桶按其"键"升序排序，但可以使用"顺序"设置控制顺序行为。支持与"术语聚合"相同的"订单"功能。

###Offset

默认情况下，存储桶键从 0 开始，然后以偶数间隔的"间隔"步骤继续，例如，如果间隔为"10"，则前三个存储桶(假设其中有数据)将是"[0， 10)"、"[10， 20)"、"[20， 30)"。可以使用"偏移"选项移动存储桶边界。

这可以用一个例子来最好地说明。如果有 10 个文档的值范围为 5 到 14，则使用间隔"10"将生成两个存储桶，每个存储桶包含 5 个文档。如果使用额外的偏移量"5"，则只有一个存储桶"[5， 15)"包含所有 10 个文档。

### 响应格式

默认情况下，存储桶以有序数组的形式返回。也可以请求响应作为哈希，而不是由存储桶键：

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          prices: {
            histogram: {
              field: 'price',
              interval: 50,
              keyed: true
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "prices": {
          "histogram": {
            "field": "price",
            "interval": 50,
            "keyed": true
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "prices": {
          "buckets": {
            "0.0": {
              "key": 0.0,
              "doc_count": 1
            },
            "50.0": {
              "key": 50.0,
              "doc_count": 1
            },
            "100.0": {
              "key": 100.0,
              "doc_count": 0
            },
            "150.0": {
              "key": 150.0,
              "doc_count": 2
            },
            "200.0": {
              "key": 200.0,
              "doc_count": 3
            }
          }
        }
      }
    }

### 缺失值

"missing"参数定义应如何处理缺少值的文档。默认情况下，它们将被忽略，但也可以将它们视为具有值。

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          quantity: {
            histogram: {
              field: 'quantity',
              interval: 10,
              missing: 0
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "quantity": {
          "histogram": {
            "field": "quantity",
            "interval": 10,
            "missing": 0 __}
        }
      }
    }

__

|

"数量"字段中没有值的文档将与值为"0"的文档属于同一存储桶。   ---|--- ### 直方图字段编辑

对直方图字段运行直方图聚合将计算每个间隔的计数总数。

例如，针对以下索引执行直方图聚合，该索引存储了不同网络的带有延迟指标(以毫秒为单位)的预聚合直方图：

    
    
    PUT metrics_index
    {
      "mappings": {
        "properties": {
          "network": {
            "properties": {
              "name": {
                "type": "keyword"
              }
            }
          },
          "latency_histo": {
             "type": "histogram"
          }
        }
      }
    }
    
    PUT metrics_index/_doc/1?refresh
    {
      "network.name" : "net-1",
      "latency_histo" : {
          "values" : [1, 3, 8, 12, 15],
          "counts" : [3, 7, 23, 12, 6]
       }
    }
    
    PUT metrics_index/_doc/2?refresh
    {
      "network.name" : "net-2",
      "latency_histo" : {
          "values" : [1, 6, 8, 12, 14],
          "counts" : [8, 17, 8, 7, 6]
       }
    }
    
    POST /metrics_index/_search?size=0
    {
      "aggs": {
        "latency_buckets": {
          "histogram": {
            "field": "latency_histo",
            "interval": 5
          }
        }
      }
    }

"直方图"聚合将根据"值"计算的每个区间的计数求和，并返回以下输出：

    
    
    {
      ...
      "aggregations": {
        "latency_buckets": {
          "buckets": [
            {
              "key": 0.0,
              "doc_count": 18
            },
            {
              "key": 5.0,
              "doc_count": 48
            },
            {
              "key": 10.0,
              "doc_count": 25
            },
            {
              "key": 15.0,
              "doc_count": 6
            }
          ]
        }
      }
    }

直方图聚合是一种存储桶聚合，它将文档分区到存储桶中，而不是像指标聚合那样通过字段计算指标。每个存储桶表示运行子聚合扫描的文档集合。另一方面，直方图字段是一个预先聚合的字段，表示单个字段中的多个值：数字数据的桶和每个桶的项目/文档计数。直方图聚合预期输入(需要原始文档)和直方图字段(提供摘要信息)之间的这种不匹配将聚合的结果限制为每个存储桶的文档计数。

**因此，在直方图字段上执行直方图聚合时，不允许子聚合。

此外，在直方图字段上运行直方图聚合时，不支持"missing"参数。

[« Global aggregation](search-aggregations-bucket-global-aggregation.md) [IP
prefix aggregation »](search-aggregations-bucket-ipprefix-aggregation.md)
