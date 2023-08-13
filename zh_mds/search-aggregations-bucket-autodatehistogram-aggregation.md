

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Adjacency matrix aggregation](search-aggregations-bucket-adjacency-matrix-
aggregation.md) [Categorize text aggregation »](search-aggregations-bucket-
categorize-text-aggregation.md)

## 自动间隔日期直方图聚合

类似于 Date 直方图的多存储桶聚合，只是没有提供用作每个存储桶宽度的间隔，而是提供目标存储桶数，指示所需的存储桶数，并自动选择存储桶的间隔以最好地实现该目标。返回的存储桶数将始终小于等于此目标数量。

存储桶字段是可选的，如果未指定，则默认为 10 个存储桶。

请求目标为 10 个存储桶。

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          sales_over_time: {
            auto_date_histogram: {
              field: 'date',
              buckets: 10
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "sales_over_time": {
          "auto_date_histogram": {
            "field": "date",
            "buckets": 10
          }
        }
      }
    }

###Keys

在内部，日期表示为 64 位数字，表示时间戳(以毫秒为单位)自纪元以来。这些时间戳作为存储桶密钥的时间戳返回。"key_as_string"是使用"format"参数指定的格式转换为格式化日期字符串的相同时间戳：

如果未指定"format"，则它将使用字段映射中指定的第一个日期格式。

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          sales_over_time: {
            auto_date_histogram: {
              field: 'date',
              buckets: 5,
              format: 'yyyy-MM-dd'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "sales_over_time": {
          "auto_date_histogram": {
            "field": "date",
            "buckets": 5,
            "format": "yyyy-MM-dd" __}
        }
      }
    }

__

|

支持富有表现力的日期格式模式 ---|--- 响应：

    
    
    {
      ...
      "aggregations": {
        "sales_over_time": {
          "buckets": [
            {
              "key_as_string": "2015-01-01",
              "key": 1420070400000,
              "doc_count": 3
            },
            {
              "key_as_string": "2015-02-01",
              "key": 1422748800000,
              "doc_count": 2
            },
            {
              "key_as_string": "2015-03-01",
              "key": 1425168000000,
              "doc_count": 2
            }
          ],
          "interval": "1M"
        }
      }
    }

###Intervals

返回桶的间隔是根据聚合收集的数据选择的，使返回的桶数小于或等于请求的数量。返回的可能间隔为：

seconds

|

以 1、5、10 和 30 的倍数表示 ---|--- 分钟

|

以 1、5、10 和 30 小时的倍数计算

|

以 1、3 和 12 天的倍数

|

在 1 个月和 7 个月的倍数中

|

以 1 年和 3 年的倍数

|

以 1、5、10、20、50 和 100 的倍数表示 在最坏的情况下，如果每日存储桶数对于请求的存储桶数来说太多，则返回的存储桶数将是请求的存储桶数的 1/7。

### 时区

日期时间以 UTC 格式存储在 Elasticsearch 中。默认情况下，所有分桶和舍入也是在 UTC 中完成的。"time_zone"参数可用于指示存储桶应使用不同的时区。

时区可以指定为 ISO 8601 UTC 偏移量(例如"+01：00"或"-08：00")，也可以指定为时区 ID，即 TZ 数据库中使用的标识符，如"America/Los_Angeles"。

请考虑以下示例：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      refresh: true,
      body: {
        date: '2015-10-01T00:30:00Z'
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      refresh: true,
      body: {
        date: '2015-10-01T01:30:00Z'
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 3,
      refresh: true,
      body: {
        date: '2015-10-01T02:30:00Z'
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      size: 0,
      body: {
        aggregations: {
          by_day: {
            auto_date_histogram: {
              field: 'date',
              buckets: 3
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/1?refresh
    {
      "date": "2015-10-01T00:30:00Z"
    }
    
    PUT my-index-000001/_doc/2?refresh
    {
      "date": "2015-10-01T01:30:00Z"
    }
    
    PUT my-index-000001/_doc/3?refresh
    {
      "date": "2015-10-01T02:30:00Z"
    }
    
    GET my-index-000001/_search?size=0
    {
      "aggs": {
        "by_day": {
          "auto_date_histogram": {
            "field":     "date",
            "buckets" : 3
          }
        }
      }
    }

如果未指定时区，则使用 UTC，从 2015 年 10 月 1 日午夜 UTC 开始返回三个 1 小时存储桶：

    
    
    {
      ...
      "aggregations": {
        "by_day": {
          "buckets": [
            {
              "key_as_string": "2015-10-01T00:00:00.000Z",
              "key": 1443657600000,
              "doc_count": 1
            },
            {
              "key_as_string": "2015-10-01T01:00:00.000Z",
              "key": 1443661200000,
              "doc_count": 1
            },
            {
              "key_as_string": "2015-10-01T02:00:00.000Z",
              "key": 1443664800000,
              "doc_count": 1
            }
          ],
          "interval": "1h"
        }
      }
    }

如果指定了"-01：00"的"time_zone"，则午夜从午夜 UTC 前一小时开始：

    
    
    response = client.search(
      index: 'my-index-000001',
      size: 0,
      body: {
        aggregations: {
          by_day: {
            auto_date_histogram: {
              field: 'date',
              buckets: 3,
              time_zone: '-01:00'
            }
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search?size=0
    {
      "aggs": {
        "by_day": {
          "auto_date_histogram": {
            "field":     "date",
            "buckets" : 3,
            "time_zone": "-01:00"
          }
        }
      }
    }

现在仍会返回三个 1 小时的存储桶，但第一个存储桶从 2015 年 9 月 30 日晚上 11：00 开始，因为这是指定时区中存储桶的本地时间。

    
    
    {
      ...
      "aggregations": {
        "by_day": {
          "buckets": [
            {
              "key_as_string": "2015-09-30T23:00:00.000-01:00", __"key": 1443657600000,
              "doc_count": 1
            },
            {
              "key_as_string": "2015-10-01T00:00:00.000-01:00",
              "key": 1443661200000,
              "doc_count": 1
            },
            {
              "key_as_string": "2015-10-01T01:00:00.000-01:00",
              "key": 1443664800000,
              "doc_count": 1
            }
          ],
          "interval": "1h"
        }
      }
    }

__

|

"key_as_string"值表示指定时区中每天的午夜。   ---|--- 使用遵循 DST(夏令时)更改的时区时，接近这些更改发生的时刻的存储桶的大小可能与相邻存储桶略有不同。例如，考虑以"CET"时区开始的 DST：2016 年 3 月 27 日凌晨 2 点，时钟将时钟向前调至当地时间凌晨 1 小时至凌晨 3 点。如果聚合的结果是每日存储桶，则当天的存储桶覆盖将仅保留数据 23 小时，而不是其他存储桶通常的 24 小时。对于较短的间隔(例如 12 小时)也是如此。在这里，当 DSTshift 发生时，我们将在 3 月 27 日早上只有 11 小时的桶。

### 最小间隔参数

"minimum_interval"允许调用方指定应使用的最小舍入间隔。这可以使收集过程更有效率，因为聚合不会尝试以低于"minimum_interval"的任何间隔舍入。

"minimum_interval"接受的单位是：

* 年 * 月 * 日 * 小时 * 分钟 * 秒

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          sale_date: {
            auto_date_histogram: {
              field: 'date',
              buckets: 10,
              minimum_interval: 'minute'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "sale_date": {
          "auto_date_histogram": {
            "field": "date",
            "buckets": 10,
            "minimum_interval": "minute"
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
          sale_date: {
            auto_date_histogram: {
              field: 'date',
              buckets: 10,
              missing: '2000/01/01'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "sale_date": {
          "auto_date_histogram": {
            "field": "date",
            "buckets": 10,
            "missing": "2000/01/01" __}
        }
      }
    }

__

|

"publish_date"字段中没有值的文档将与值为"2000-01-01"的文档属于同一存储桶。   ---|--- « 邻接矩阵聚合 对文本聚合进行分类 »