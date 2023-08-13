

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Children aggregation](search-aggregations-bucket-children-aggregation.md)
[Date histogram aggregation »](search-aggregations-bucket-datehistogram-
aggregation.md)

## 复合聚合

复合聚合的成本很高。在生产环境中部署复合聚合之前对应用程序进行负载测试。

从不同来源创建复合存储桶的多存储桶聚合。

与其他"多存储桶"聚合不同，您可以使用"复合"聚合有效地从多级聚合中分页**所有**存储桶。此聚合提供了一种流式传输非特定聚合的 **all** 存储桶的方法，类似于滚动对文档执行的操作。

复合存储桶是根据为每个文档提取/创建的值的组合构建的，每个组合都被视为复合存储桶。

例如，请考虑以下文档：

    
    
    {
      "keyword": ["foo", "bar"],
      "number": [23, 65, 76]
    }

使用"关键字"和"数字"作为聚合的源字段会产生以下组合存储桶：

    
    
    { "keyword": "foo", "number": 23 }
    { "keyword": "foo", "number": 65 }
    { "keyword": "foo", "number": 76 }
    { "keyword": "bar", "number": 23 }
    { "keyword": "bar", "number": 65 }
    { "keyword": "bar", "number": 76 }

### 价值来源

"sources"参数定义构建复合存储桶时要使用的源字段。定义"源"的顺序控制返回键的顺序。

定义"源"时必须使用唯一名称。

"sources"参数可以是以下任何类型：

* 术语 * 直方图 * 日期直方图 * 地理磁贴网格

####Terms

"术语"值源类似于简单的"术语"聚合。这些值是从与"术语"聚合完全相同的字段中提取的。

Example:

    
    
    response = client.search(
      body: {
        size: 0,
        aggregations: {
          my_buckets: {
            composite: {
              sources: [
                {
                  product: {
                    terms: {
                      field: 'product'
                    }
                  }
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "size": 0,
      "aggs": {
        "my_buckets": {
          "composite": {
            "sources": [
              { "product": { "terms": { "field": "product" } } }
            ]
          }
        }
      }
    }

与"terms"聚合一样，可以使用运行时字段为复合桶创建值：

    
    
    response = client.search(
      body: {
        runtime_mappings: {
          day_of_week: {
            type: 'keyword',
            script: "\n        emit(doc['timestamp'].value.dayOfWeekEnum\n          .getDisplayName(TextStyle.FULL, Locale.ROOT))\n      "
          }
        },
        size: 0,
        aggregations: {
          my_buckets: {
            composite: {
              sources: [
                {
                  dow: {
                    terms: {
                      field: 'day_of_week'
                    }
                  }
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "runtime_mappings": {
        "day_of_week": {
          "type": "keyword",
          "script": """
            emit(doc['timestamp'].value.dayOfWeekEnum
              .getDisplayName(TextStyle.FULL, Locale.ROOT))
          """
        }
      },
      "size": 0,
      "aggs": {
        "my_buckets": {
          "composite": {
            "sources": [
              {
                "dow": {
                  "terms": { "field": "day_of_week" }
                }
              }
            ]
          }
        }
      }
    }

尽管类似，但"术语"值源不支持与"术语"聚合相同的参数集。有关其他受支持的值源参数，请参阅：

* 订单 * 缺少存储桶

####Histogram

"直方图"值源可以应用于数值，以在值上构建固定大小的间隔。"interval"参数定义应如何转换数值。例如，设置为 5 的"间隔"会将任何数值转换为最接近的间隔，值"101"将转换为"100"，这是 100 到 105 之间间隔的键。

Example:

    
    
    response = client.search(
      body: {
        size: 0,
        aggregations: {
          my_buckets: {
            composite: {
              sources: [
                {
                  histo: {
                    histogram: {
                      field: 'price',
                      interval: 5
                    }
                  }
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "size": 0,
      "aggs": {
        "my_buckets": {
          "composite": {
            "sources": [
              { "histo": { "histogram": { "field": "price", "interval": 5 } } }
            ]
          }
        }
      }
    }

与"直方图"聚合一样，可以使用运行时字段为复合桶创建值：

    
    
    response = client.search(
      body: {
        runtime_mappings: {
          "price.discounted": {
            type: 'double',
            script: "\n        double price = doc['price'].value;\n        if (doc['product'].value == 'mad max') {\n          price *= 0.8;\n        }\n        emit(price);\n      "
          }
        },
        size: 0,
        aggregations: {
          my_buckets: {
            composite: {
              sources: [
                {
                  price: {
                    histogram: {
                      interval: 5,
                      field: 'price.discounted'
                    }
                  }
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "runtime_mappings": {
        "price.discounted": {
          "type": "double",
          "script": """
            double price = doc['price'].value;
            if (doc['product'].value == 'mad max') {
              price *= 0.8;
            }
            emit(price);
          """
        }
      },
      "size": 0,
      "aggs": {
        "my_buckets": {
          "composite": {
            "sources": [
              {
                "price": {
                  "histogram": {
                    "interval": 5,
                    "field": "price.discounted"
                  }
                }
              }
            ]
          }
        }
      }
    }

#### 日期直方图

"date_histogram"类似于"直方图"值源，不同之处在于间隔由日期/时间表达式指定：

    
    
    response = client.search(
      body: {
        size: 0,
        aggregations: {
          my_buckets: {
            composite: {
              sources: [
                {
                  date: {
                    date_histogram: {
                      field: 'timestamp',
                      calendar_interval: '1d'
                    }
                  }
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "size": 0,
      "aggs": {
        "my_buckets": {
          "composite": {
            "sources": [
              { "date": { "date_histogram": { "field": "timestamp", "calendar_interval": "1d" } } }
            ]
          }
        }
      }
    }

上面的示例每天创建一个间隔，并将所有"时间戳"值转换为其最接近间隔的开始。间隔的可用表达式："年"、"季度"、"月"、"周"、"日"、"小时"、"分钟"、"秒"

时间值也可以通过时间单位解析支持的缩写来指定。请注意，不支持分数时间值，但您可以通过切换到另一个时间单位来解决此问题(例如，可以将"1.5h"指定为"90m")。

**Format**

在内部，日期表示为 64 位数字，表示时间戳(以毫秒为单位)自纪元以来。这些时间戳作为存储桶键返回。可以使用使用 format 参数指定的格式返回格式化的日期字符串：

    
    
    response = client.search(
      body: {
        size: 0,
        aggregations: {
          my_buckets: {
            composite: {
              sources: [
                {
                  date: {
                    date_histogram: {
                      field: 'timestamp',
                      calendar_interval: '1d',
                      format: 'yyyy-MM-dd'
                    }
                  }
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "size": 0,
      "aggs": {
        "my_buckets": {
          "composite": {
            "sources": [
              {
                "date": {
                  "date_histogram": {
                    "field": "timestamp",
                    "calendar_interval": "1d",
                    "format": "yyyy-MM-dd"         __}
                }
              }
            ]
          }
        }
      }
    }

__

|

支持富有表现力的日期格式模式 ---|--- **时区**

日期时间以 UTC 格式存储在 Elasticsearch 中。默认情况下，所有分桶和舍入也是在 UTC 中完成的。"time_zone"参数可用于指示存储桶应使用不同的时区。

时区可以指定为 ISO 8601 UTC 偏移量(例如"+01：00"或"-08：00")，也可以指定为时区 ID，即 TZ 数据库中使用的标识符，如"America/Los_Angeles"。

**Offset**

使用 "offset" 参数将每个存储桶的起始值更改为指定的正 (+") 或负偏移 ('-') 持续时间，例如"1h"foran 小时或"1d"表示一天。有关更多可能的持续时间选项，请参阅时间单位。

例如，当使用"天"间隔时，每个存储桶从午夜运行到午夜。将"偏移"参数设置为"+6h"会将每个存储桶从早上 6 点更改为早上 6 点运行：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      refresh: true,
      body: {
        date: '2015-10-01T05:30:00Z'
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      refresh: true,
      body: {
        date: '2015-10-01T06:30:00Z'
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      size: 0,
      body: {
        aggregations: {
          my_buckets: {
            composite: {
              sources: [
                {
                  date: {
                    date_histogram: {
                      field: 'date',
                      calendar_interval: 'day',
                      offset: '+6h',
                      format: 'iso8601'
                    }
                  }
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/1?refresh
    {
      "date": "2015-10-01T05:30:00Z"
    }
    
    PUT my-index-000001/_doc/2?refresh
    {
      "date": "2015-10-01T06:30:00Z"
    }
    
    GET my-index-000001/_search?size=0
    {
      "aggs": {
        "my_buckets": {
          "composite" : {
            "sources" : [
              {
                "date": {
                  "date_histogram" : {
                    "field": "date",
                    "calendar_interval": "day",
                    "offset": "+6h",
                    "format": "iso8601"
                  }
                }
              }
            ]
          }
        }
      }
    }

上述请求不是从午夜开始的单个存储桶，而是从早上 6 点开始将文档分组到存储桶中：

    
    
    {
      ...
      "aggregations": {
        "my_buckets": {
          "after_key": { "date": "2015-10-01T06:00:00.000Z" },
          "buckets": [
            {
              "key": { "date": "2015-09-30T06:00:00.000Z" },
              "doc_count": 1
            },
            {
              "key": { "date": "2015-10-01T06:00:00.000Z" },
              "doc_count": 1
            }
          ]
        }
      }
    }

每个存储桶的起始"偏移量"是在进行"time_zone"调整后计算的。

#### 地理瓦片网格

"geotile_grid"值源适用于"geo_point"字段，并将点分组到表示网格中单元格的存储桶中。生成的网格可以是稀疏的，并且仅包含具有匹配数据的单元格。每个单元格对应于许多在线地图站点使用的地图磁贴。每个单元格都使用"{zoom}/{x}/{y}"格式进行标记，其中缩放等于用户指定的精度。

    
    
    response = client.search(
      body: {
        size: 0,
        aggregations: {
          my_buckets: {
            composite: {
              sources: [
                {
                  tile: {
                    geotile_grid: {
                      field: 'location',
                      precision: 8
                    }
                  }
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "size": 0,
      "aggs": {
        "my_buckets": {
          "composite": {
            "sources": [
              { "tile": { "geotile_grid": { "field": "location", "precision": 8 } } }
            ]
          }
        }
      }
    }

**Precision**

长度为 29 的最高精度土工瓦产生的细胞覆盖不到 10 厘米 x 10 厘米的土地。此精度特别适用于复合聚合，因为不必生成每个切片并将其加载到内存中。

请参阅缩放级别文档，了解精度 (缩放) 如何与地面大小相关联。此聚合的精度可以介于 0 和 29 之间(包括 0 和 29)。

**边界框筛选**

可以选择将地理切片源限制为特定的地理边界框，从而减少使用的切片范围。当只有地理区域的特定部分需要高精度切片时，这些边界非常有用。

    
    
    response = client.search(
      body: {
        size: 0,
        aggregations: {
          my_buckets: {
            composite: {
              sources: [
                {
                  tile: {
                    geotile_grid: {
                      field: 'location',
                      precision: 22,
                      bounds: {
                        top_left: 'POINT (4.9 52.4)',
                        bottom_right: 'POINT (5.0 52.3)'
                      }
                    }
                  }
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "size": 0,
      "aggs": {
        "my_buckets": {
          "composite": {
            "sources": [
              {
                "tile": {
                  "geotile_grid": {
                    "field": "location",
                    "precision": 22,
                    "bounds": {
                      "top_left": "POINT (4.9 52.4)",
                      "bottom_right": "POINT (5.0 52.3)"
                    }
                  }
                }
              }
            ]
          }
        }
      }
    }

#### 混合不同的价值源

"sources"参数接受值源数组。可以混合不同的价值源来创建复合存储桶。例如：

    
    
    response = client.search(
      body: {
        size: 0,
        aggregations: {
          my_buckets: {
            composite: {
              sources: [
                {
                  date: {
                    date_histogram: {
                      field: 'timestamp',
                      calendar_interval: '1d'
                    }
                  }
                },
                {
                  product: {
                    terms: {
                      field: 'product'
                    }
                  }
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "size": 0,
      "aggs": {
        "my_buckets": {
          "composite": {
            "sources": [
              { "date": { "date_histogram": { "field": "timestamp", "calendar_interval": "1d" } } },
              { "product": { "terms": { "field": "product" } } }
            ]
          }
        }
      }
    }

这将从两个值源("date_histogram"和"术语")创建的值创建复合存储桶。每个存储桶由两个值组成，一个值用于聚合中定义的每个值源。允许任何类型的组合，并且数组中的顺序保留在复合存储桶中。

    
    
    response = client.search(
      body: {
        size: 0,
        aggregations: {
          my_buckets: {
            composite: {
              sources: [
                {
                  shop: {
                    terms: {
                      field: 'shop'
                    }
                  }
                },
                {
                  product: {
                    terms: {
                      field: 'product'
                    }
                  }
                },
                {
                  date: {
                    date_histogram: {
                      field: 'timestamp',
                      calendar_interval: '1d'
                    }
                  }
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "size": 0,
      "aggs": {
        "my_buckets": {
          "composite": {
            "sources": [
              { "shop": { "terms": { "field": "shop" } } },
              { "product": { "terms": { "field": "product" } } },
              { "date": { "date_histogram": { "field": "timestamp", "calendar_interval": "1d" } } }
            ]
          }
        }
      }
    }

###Order

默认情况下，复合存储桶按其自然顺序排序。值按其值的升序排序。当请求多个值源时，按值源进行排序，将复合桶的第一个值与另一个复合桶的第一个值进行比较，如果它们相等，则使用复合桶中的下一个值。这意味着复合桶 '[foo， 100]' 被认为小于 '[foobar， 0]'，因为 'foo' 被认为小于 'foobar'。可以通过直接在值源定义中将"order"设置为"asc"(默认值)或"desc"(降序)来定义每个值源的排序方向。例如：

    
    
    response = client.search(
      body: {
        size: 0,
        aggregations: {
          my_buckets: {
            composite: {
              sources: [
                {
                  date: {
                    date_histogram: {
                      field: 'timestamp',
                      calendar_interval: '1d',
                      order: 'desc'
                    }
                  }
                },
                {
                  product: {
                    terms: {
                      field: 'product',
                      order: 'asc'
                    }
                  }
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "size": 0,
      "aggs": {
        "my_buckets": {
          "composite": {
            "sources": [
              { "date": { "date_histogram": { "field": "timestamp", "calendar_interval": "1d", "order": "desc" } } },
              { "product": { "terms": { "field": "product", "order": "asc" } } }
            ]
          }
        }
      }
    }

...比较来自"date_histogram"源的值时将按降序对复合存储桶进行排序，在比较来自"术语"源的值时将按升序对复合存储桶进行排序。

### 缺少存储桶

默认情况下，将忽略没有给定源值的文档。可以通过将"missing_bucket"设置为"true"(默认为"false")将它们包含在响应中：

    
    
    response = client.search(
      body: {
        size: 0,
        aggregations: {
          my_buckets: {
            composite: {
              sources: [
                {
                  product_name: {
                    terms: {
                      field: 'product',
                      missing_bucket: true,
                      missing_order: 'last'
                    }
                  }
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "size": 0,
      "aggs": {
        "my_buckets": {
          "composite": {
            "sources": [{
              "product_name": {
                "terms": {
                  "field": "product",
                  "missing_bucket": true,
                  "missing_order": "last"
                }
              }
            }]
          }
        }
      }
    }

在上面的示例中，"product_name"源为没有"product"值的文档发出显式的"null"存储桶。此存储桶放在最后。

您可以使用可选的"空"参数控制"空"存储桶的位置missing_order。如果"missing_order"是"第一个"或"最后一个"，则"null"存储桶将放置在相应的第一个或最后一个位置。如果省略"missing_order"或"默认"，则源的"顺序"将决定存储桶的位置。如果"order"为"asc"(升序)，则存储桶位于第一个位置。如果"order"为"desc"(降序)，则存储桶位于最后一个位置。

###Size

可以设置"size"参数来定义应返回的复合存储桶数。每个复合存储桶被视为单个存储桶，因此将 asize 设置为 10 将返回从 valuesources 创建的前 10 个复合存储桶。响应包含数组中每个复合存储桶的值，其中包含从每个值源中提取的值。默认为"10"。

###Pagination

如果复合存储桶的数量太大(或未知)，无法在单个响应中返回，则可以将检索拆分为多个请求。由于复合存储桶本质上是扁平的，因此请求的"大小"正是将在响应中返回的复合存储桶的数量(假设它们至少是要返回的复合存储桶的"大小")。如果要检索所有复合存储桶，最好使用较小的大小(例如"100"或"1000")，然后使用"after"参数检索下一个结果。例如：

    
    
    response = client.search(
      body: {
        size: 0,
        aggregations: {
          my_buckets: {
            composite: {
              size: 2,
              sources: [
                {
                  date: {
                    date_histogram: {
                      field: 'timestamp',
                      calendar_interval: '1d'
                    }
                  }
                },
                {
                  product: {
                    terms: {
                      field: 'product'
                    }
                  }
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "size": 0,
      "aggs": {
        "my_buckets": {
          "composite": {
            "size": 2,
            "sources": [
              { "date": { "date_histogram": { "field": "timestamp", "calendar_interval": "1d" } } },
              { "product": { "terms": { "field": "product" } } }
            ]
          }
        }
      }
    }

...返回：

    
    
    {
      ...
      "aggregations": {
        "my_buckets": {
          "after_key": {
            "date": 1494288000000,
            "product": "mad max"
          },
          "buckets": [
            {
              "key": {
                "date": 1494201600000,
                "product": "rocky"
              },
              "doc_count": 1
            },
            {
              "key": {
                "date": 1494288000000,
                "product": "mad max"
              },
              "doc_count": 2
            }
          ]
        }
      }
    }

要获取下一组存储桶，请将"after"参数设置为响应中返回的"after_key"值的相同聚合重新发送。例如，此请求使用上一个响应中提供的"after_key"值：

    
    
    response = client.search(
      body: {
        size: 0,
        aggregations: {
          my_buckets: {
            composite: {
              size: 2,
              sources: [
                {
                  date: {
                    date_histogram: {
                      field: 'timestamp',
                      calendar_interval: '1d',
                      order: 'desc'
                    }
                  }
                },
                {
                  product: {
                    terms: {
                      field: 'product',
                      order: 'asc'
                    }
                  }
                }
              ],
              after: {
                date: 1_494_288_000_000,
                product: 'mad max'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "size": 0,
      "aggs": {
        "my_buckets": {
          "composite": {
            "size": 2,
            "sources": [
              { "date": { "date_histogram": { "field": "timestamp", "calendar_interval": "1d", "order": "desc" } } },
              { "product": { "terms": { "field": "product", "order": "asc" } } }
            ],
            "after": { "date": 1494288000000, "product": "mad max" } __}
        }
      }
    }

__

|

应将聚合限制为在提供的值之后排序的存储桶。   ---|--- "after_key"通常是响应中返回的最后一个存储桶的键，但这并不能保证。始终使用返回的"after_key"，而不是从存储桶派生它。

### 提前终止

为了获得最佳性能，应在索引上设置索引排序，使其与复合聚合中的部分或完全匹配源顺序。例如，以下索引排序：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          index: {
            "sort.field": [
              'username',
              'timestamp'
            ],
            "sort.order": [
              'asc',
              'desc'
            ]
          }
        },
        mappings: {
          properties: {
            username: {
              type: 'keyword',
              doc_values: true
            },
            timestamp: {
              type: 'date'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "settings": {
        "index": {
          "sort.field": [ "username", "timestamp" ],   __"sort.order": [ "asc", "desc" ] __}
      },
      "mappings": {
        "properties": {
          "username": {
            "type": "keyword",
            "doc_values": true
          },
          "timestamp": {
            "type": "date"
          }
        }
      }
    }

__

|

此索引首先按"用户名"排序，然后按"时间戳"排序。   ---|---    __

|

...​"用户名"字段按升序排列，"时间戳"字段按降序排列。

1. 可用于优化这些复合聚合：

响应 = client.search( body： { size： 0， aggregations： { my_buckets： { composite： { sources： [ { user_name： { terms： { field： 'user_name' } } } } ] } } } } ) put response GET /_search { "size"： 0， "aggs"： { "my_buckets"： {         "复合"： { "来源"： [ { "user_name"： { "术语"： { "字段"： "user_name" } } } } __] } } } } }

__

|

"user_name"是索引排序的前缀，顺序匹配("ASC")。   ---|--- 响应 = client.search( 正文： { 大小： 0， 聚合： { my_buckets： { 复合： { 来源： [ { user_name： { 术语： { 字段： 'user_name' } } }， { 日期： { date_histogram： { 字段： '时间戳'，                     calendar_interval： '1d'， order： 'desc' } } } ] } } } ) 把响应 GET /_search { "size"： 0， "aggs"： { "my_buckets"： { "composite"： { "sources"： [ { "user_name"： { "terms"： { "field"： "user_name" } } }， __{ "date"： { "date_histogram"： { "field"： "timestamp"， "calendar_interval"： "1d"， "order"： "desc" } } } __]          }        }      }    }

__

|

"user_name"是索引排序的前缀，顺序匹配("ASC")。   ---|---    __

|

"时间戳"也与前缀匹配，顺序匹配("desc")。   为了优化提前终止，建议将请求中的"track_total_hits"设置为"false"。可以在第一个请求上检索与请求匹配的总命中数，并且在每个页面上计算此数字的成本很高：

    
    
    response = client.search(
      body: {
        size: 0,
        track_total_hits: false,
        aggregations: {
          my_buckets: {
            composite: {
              sources: [
                {
                  user_name: {
                    terms: {
                      field: 'user_name'
                    }
                  }
                },
                {
                  date: {
                    date_histogram: {
                      field: 'timestamp',
                      calendar_interval: '1d',
                      order: 'desc'
                    }
                  }
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "size": 0,
      "track_total_hits": false,
      "aggs": {
        "my_buckets": {
          "composite": {
            "sources": [
              { "user_name": { "terms": { "field": "user_name" } } },
              { "date": { "date_histogram": { "field": "timestamp", "calendar_interval": "1d", "order": "desc" } } }
            ]
          }
        }
      }
    }

请注意，源的顺序很重要，在下面的示例中，将"user_name"与"时间戳"切换将停用排序优化，因为此配置与索引排序规范不匹配。如果源的顺序对您的用例无关紧要，您可以遵循以下简单准则：

* 将基数最高的字段放在第一位。  * 确保字段的顺序与索引排序的顺序匹配。  * 将多值字段放在最后，因为它们不能用于提前终止。

索引排序可能会降低索引速度，使用特定用例和数据集测试索引排序以确保它符合您的要求非常重要。如果没有注意到，如果查询匹配所有文档("match_all"查询)，"复合"聚合也将尝试在未排序的索引上提前终止。

### 子聚合

与任何"多存储桶"聚合一样，"复合"聚合可以保存子聚合。这些子聚合可用于计算其他存储桶或此父聚合创建的每个复合存储桶的统计信息。例如，以下示例计算每个复合存储桶的字段的平均值：

    
    
    response = client.search(
      body: {
        size: 0,
        aggregations: {
          my_buckets: {
            composite: {
              sources: [
                {
                  date: {
                    date_histogram: {
                      field: 'timestamp',
                      calendar_interval: '1d',
                      order: 'desc'
                    }
                  }
                },
                {
                  product: {
                    terms: {
                      field: 'product'
                    }
                  }
                }
              ]
            },
            aggregations: {
              the_avg: {
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
    
    
    GET /_search
    {
      "size": 0,
      "aggs": {
        "my_buckets": {
          "composite": {
            "sources": [
              { "date": { "date_histogram": { "field": "timestamp", "calendar_interval": "1d", "order": "desc" } } },
              { "product": { "terms": { "field": "product" } } }
            ]
          },
          "aggregations": {
            "the_avg": {
              "avg": { "field": "price" }
            }
          }
        }
      }
    }

...返回：

    
    
    {
      ...
      "aggregations": {
        "my_buckets": {
          "after_key": {
            "date": 1494201600000,
            "product": "rocky"
          },
          "buckets": [
            {
              "key": {
                "date": 1494460800000,
                "product": "apocalypse now"
              },
              "doc_count": 1,
              "the_avg": {
                "value": 10.0
              }
            },
            {
              "key": {
                "date": 1494374400000,
                "product": "mad max"
              },
              "doc_count": 1,
              "the_avg": {
                "value": 27.0
              }
            },
            {
              "key": {
                "date": 1494288000000,
                "product": "mad max"
              },
              "doc_count": 2,
              "the_avg": {
                "value": 22.5
              }
            },
            {
              "key": {
                "date": 1494201600000,
                "product": "rocky"
              },
              "doc_count": 1,
              "the_avg": {
                "value": 10.0
              }
            }
          ]
        }
      }
    }

### 管道聚合

复合 agg 目前与管道聚合不兼容，在大多数情况下也没有意义。例如，由于 compositeaggs 的分页性质，单个逻辑分区(例如一天)可能分布在多个页面上。由于管道聚合纯粹是对存储桶的最终列表进行后处理，因此在复合页面上运行类似衍生物的内容可能会导致结果不准确，因为它只考虑该页面上的"部分"结果。

将来可能会支持自包含到单个存储桶(例如"bucket_selector")的管道 agg。

[« Children aggregation](search-aggregations-bucket-children-aggregation.md)
[Date histogram aggregation »](search-aggregations-bucket-datehistogram-
aggregation.md)
