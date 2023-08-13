

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Composite aggregation](search-aggregations-bucket-composite-
aggregation.md) [Date range aggregation »](search-aggregations-bucket-
daterange-aggregation.md)

## 日期直方图聚合

此多存储桶聚合类似于普通直方图，但只能与日期或日期范围值一起使用。由于日期在 Elasticsearch 内部表示为长值，因此也可以(但不那么准确)对日期使用正常的"直方图"。这两个 API 的主要区别在于，此处可以使用日期/时间表达式指定间隔。基于时间的数据需要特殊支持，因为基于时间的间隔并不总是固定长度。

与直方图一样，值向下舍入到最接近的存储桶中。例如，如果间隔是日历日，则"2020-01-03T07：00：01Z"将舍入为"2020-01-03T00：00：00Z"。值四舍五入如下：

    
    
    bucket_key = Math.floor(value / interval) * interval

### 日历和固定间隔

配置日期直方图聚合时，可以通过两种方式指定间隔：日历感知时间间隔和固定时间间隔。

日历感知间隔了解夏令时会更改特定日期的长度，月份具有不同的天数，并且闰秒可以附加到特定年份。

相比之下，固定间隔始终是 SI 单位的倍数，并且不会根据日历上下文而变化。

### 日历间隔

日历感知间隔使用"calendar_interval"参数进行配置。您可以使用单位名称(如"月")或单个单位数量(如"1M")指定日历间隔。例如，"day"和"1d"是等效的。不支持多个数量，例如"2d"。

接受的日历间隔为：

"分钟"、"1m"

     All minutes begin at 00 seconds. One minute is the interval between 00 seconds of the first minute and 00 seconds of the following minute in the specified time zone, compensating for any intervening leap seconds, so that the number of minutes and seconds past the hour is the same at the start and end. 
`hour`, `1h`

     All hours begin at 00 minutes and 00 seconds. One hour (1h) is the interval between 00:00 minutes of the first hour and 00:00 minutes of the following hour in the specified time zone, compensating for any intervening leap seconds, so that the number of minutes and seconds past the hour is the same at the start and end. 
`day`, `1d`

     All days begin at the earliest possible time, which is usually 00:00:00 (midnight). One day (1d) is the interval between the start of the day and the start of the following day in the specified time zone, compensating for any intervening time changes. 
`week`, `1w`

     One week is the interval between the start day_of_week:hour:minute:second and the same day of the week and time of the following week in the specified time zone. 
`month`, `1M`

     One month is the interval between the start day of the month and time of day and the same day of the month and time of the following month in the specified time zone, so that the day of the month and time of day are the same at the start and end. Note that the day may differ if an [`offset` is used that is longer than a month](search-aggregations-bucket-datehistogram-aggregation.html#search-aggregations-bucket-datehistogram-offset-months "Long offsets over calendar intervals"). 
`quarter`, `1q`

     One quarter is the interval between the start day of the month and time of day and the same day of the month and time of day three months later, so that the day of the month and time of day are the same at the start and end.  

"年"、"1y"

     One year is the interval between the start day of the month and time of day and the same day of the month and time of day the following year in the specified time zone, so that the date and time are the same at the start and end.  

#### 日历间隔示例

例如，下面是一个聚合，请求一个月的存储桶间隔在日历时间中：

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          sales_over_time: {
            date_histogram: {
              field: 'date',
              calendar_interval: 'month'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithIndex("sales"),
    	es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "sales_over_time": {
    	      "date_histogram": {
    	        "field": "date",
    	        "calendar_interval": "month"
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithSize(0),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "sales_over_time": {
          "date_histogram": {
            "field": "date",
            "calendar_interval": "month"
          }
        }
      }
    }

如果尝试使用多个日历单位，聚合将失败，因为仅支持单个日历单位：

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          sales_over_time: {
            date_histogram: {
              field: 'date',
              calendar_interval: '2d'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithIndex("sales"),
    	es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "sales_over_time": {
    	      "date_histogram": {
    	        "field": "date",
    	        "calendar_interval": "2d"
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithSize(0),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "sales_over_time": {
          "date_histogram": {
            "field": "date",
            "calendar_interval": "2d"
          }
        }
      }
    }
    
    
    {
      "error" : {
        "root_cause" : [...],
        "type" : "x_content_parse_exception",
        "reason" : "[1:82] [date_histogram] failed to parse field [calendar_interval]",
        "caused_by" : {
          "type" : "illegal_argument_exception",
          "reason" : "The supplied interval [2d] could not be parsed as a calendar interval.",
          "stack_trace" : "java.lang.IllegalArgumentException: The supplied interval [2d] could not be parsed as a calendar interval."
        }
      }
    }

### 固定间隔

固定间隔配置有"fixed_interval"参数。

与日历感知间隔相比，固定间隔是固定数量的 SI 单位，无论它们落在日历上的位置，都不会偏离。一秒始终由"1000ms"组成。这允许以任意倍数支持的单位指定固定间隔。

但是，这意味着固定间隔不能表示其他单位，例如月，因为一个月的持续时间不是固定数量。尝试指定日历间隔(如月或季度)将引发异常。

固定间隔的接受单位为：

毫秒("毫秒")

     A single millisecond. This is a very, very small interval. 
seconds (`s`)

     Defined as 1000 milliseconds each. 
minutes (`m`)

     Defined as 60 seconds each (60,000 milliseconds). All minutes begin at 00 seconds. 
hours (`h`)

     Defined as 60 minutes each (3,600,000 milliseconds). All hours begin at 00 minutes and 00 seconds. 
days (`d`)

     Defined as 24 hours (86,400,000 milliseconds). All days begin at the earliest possible time, which is usually 00:00:00 (midnight). 

#### 固定间隔示例

如果我们尝试重新创建之前的"月""calendar_interval"，我们可以用 30 个固定天数来近似：

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          sales_over_time: {
            date_histogram: {
              field: 'date',
              fixed_interval: '30d'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithIndex("sales"),
    	es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "sales_over_time": {
    	      "date_histogram": {
    	        "field": "date",
    	        "fixed_interval": "30d"
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithSize(0),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "sales_over_time": {
          "date_histogram": {
            "field": "date",
            "fixed_interval": "30d"
          }
        }
      }
    }

但是，如果我们尝试使用不支持的日历单位，例如周，我们将得到一个异常：

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          sales_over_time: {
            date_histogram: {
              field: 'date',
              fixed_interval: '2w'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithIndex("sales"),
    	es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "sales_over_time": {
    	      "date_histogram": {
    	        "field": "date",
    	        "fixed_interval": "2w"
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithSize(0),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "sales_over_time": {
          "date_histogram": {
            "field": "date",
            "fixed_interval": "2w"
          }
        }
      }
    }
    
    
    {
      "error" : {
        "root_cause" : [...],
        "type" : "x_content_parse_exception",
        "reason" : "[1:82] [date_histogram] failed to parse field [fixed_interval]",
        "caused_by" : {
          "type" : "illegal_argument_exception",
          "reason" : "failed to parse setting [date_histogram.fixedInterval] with value [2w] as a time value: unit is missing or unrecognized",
          "stack_trace" : "java.lang.IllegalArgumentException: failed to parse setting [date_histogram.fixedInterval] with value [2w] as a time value: unit is missing or unrecognized"
        }
      }
    }

### 日期直方图用法说明

在所有情况下，当指定的结束时间不存在时，实际结束时间是指定结束之后最接近的可用时间。

广泛分布的应用程序还必须考虑变幻莫测的情况，例如在上午 12：01 开始和停止夏令时的国家/地区，因此最终每年一次以一分钟的星期日，然后是额外的 59 分钟星期六，以及决定跨越国际日期变更线的国家/地区。像这样的情况会使不规则的时区偏移看起来很容易。

与往常一样，严格的测试，尤其是围绕时变事件的测试，将确保您的时间间隔规范符合您的预期。

为避免意外结果，所有连接的服务器和客户端必须同步到可靠的网络时间服务。

不支持分数时间值，但您可以通过切换到另一个时间单位来解决此问题(例如，可以将"1.5h"指定为"90m")。

您还可以使用时间单位分析支持的缩写来指定时间值。

###Keys

在内部，日期表示为 64 位数字，表示自纪元 (01/01/1970 午夜 UTC) 以来的时间戳(以毫秒为单位)。这些时间戳作为存储桶的"键"名称返回。"key_as_string"是使用"format"参数规范转换为格式化日期字符串的相同时间戳：

如果未指定"格式"，则使用字段映射中指定的第一个日期格式。

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          sales_over_time: {
            date_histogram: {
              field: 'date',
              calendar_interval: '1M',
              format: 'yyyy-MM-dd'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithIndex("sales"),
    	es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "sales_over_time": {
    	      "date_histogram": {
    	        "field": "date",
    	        "calendar_interval": "1M",
    	        "format": "yyyy-MM-dd"
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithSize(0),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "sales_over_time": {
          "date_histogram": {
            "field": "date",
            "calendar_interval": "1M",
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
          ]
        }
      }
    }

### 时区

Elasticsearch 以协调世界时 (UTC) 存储日期时间。默认情况下，所有分桶和舍入也是在 UTC 中完成的。使用"time_zone"参数指示存储桶应使用不同的时区。

例如，如果间隔是日历日，时区为"美国/New_York"，则"2020-01-03T01：00：01Z"为：# 转换为"2020-01-02T18：00：01" # 向下舍入为"2020-01-02T00：00：00" # 然后转换回 UTC 以生成 '2020-01-02T05：00：00：00Z' # 最后，当存储桶转换为字符串键时，它会打印在"America/New_York"中，因此它将显示为""2020-01-02T00：00：00""。

它看起来像：

    
    
    bucket_key = localToUtc(Math.floor(utcToLocal(value) / interval) * interval))

您可以将时区指定为 ISO 8601 UTC 偏移量(例如"+01：00"或"-08：00")或 IANA 时区 ID，例如"美国/Los_Angeles"。

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
    
    response = client.search(
      index: 'my-index-000001',
      size: 0,
      body: {
        aggregations: {
          by_day: {
            date_histogram: {
              field: 'date',
              calendar_interval: 'day'
            }
          }
        }
      }
    )
    puts response
    
    
    {
    	res, err := es.Index(
    		"my-index-000001",
    		strings.NewReader(`{
    	  "date": "2015-10-01T00:30:00Z"
    	}`),
    		es.Index.WithDocumentID("1"),
    		es.Index.WithRefresh("true"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Index(
    		"my-index-000001",
    		strings.NewReader(`{
    	  "date": "2015-10-01T01:30:00Z"
    	}`),
    		es.Index.WithDocumentID("2"),
    		es.Index.WithRefresh("true"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Search(
    		es.Search.WithIndex("my-index-000001"),
    		es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "by_day": {
    	      "date_histogram": {
    	        "field": "date",
    	        "calendar_interval": "day"
    	      }
    	    }
    	  }
    	}`)),
    		es.Search.WithSize(0),
    		es.Search.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    
    PUT my-index-000001/_doc/1?refresh
    {
      "date": "2015-10-01T00:30:00Z"
    }
    
    PUT my-index-000001/_doc/2?refresh
    {
      "date": "2015-10-01T01:30:00Z"
    }
    
    GET my-index-000001/_search?size=0
    {
      "aggs": {
        "by_day": {
          "date_histogram": {
            "field":     "date",
            "calendar_interval":  "day"
          }
        }
      }
    }

如果未指定时区，则使用 UTC。这将导致这两个文档被放入同一天存储桶中，该存储桶从 2015 年 10 月 1 日午夜 UTC 开始：

    
    
    {
      ...
      "aggregations": {
        "by_day": {
          "buckets": [
            {
              "key_as_string": "2015-10-01T00:00:00.000Z",
              "key":           1443657600000,
              "doc_count":     2
            }
          ]
        }
      }
    }

如果将"time_zone"指定为"-01：00"，则该时区的午夜为 UTC 午夜前一小时：

    
    
    response = client.search(
      index: 'my-index-000001',
      size: 0,
      body: {
        aggregations: {
          by_day: {
            date_histogram: {
              field: 'date',
              calendar_interval: 'day',
              time_zone: '-01:00'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithIndex("my-index-000001"),
    	es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "by_day": {
    	      "date_histogram": {
    	        "field": "date",
    	        "calendar_interval": "day",
    	        "time_zone": "-01:00"
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithSize(0),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET my-index-000001/_search?size=0
    {
      "aggs": {
        "by_day": {
          "date_histogram": {
            "field":     "date",
            "calendar_interval":  "day",
            "time_zone": "-01:00"
          }
        }
      }
    }

现在，第一个文档属于 2015 年 9 月 30 日的存储桶，而第二个文档属于 2015 年 10 月 1 日的存储桶：

    
    
    {
      ...
      "aggregations": {
        "by_day": {
          "buckets": [
            {
              "key_as_string": "2015-09-30T00:00:00.000-01:00", __"key": 1443574800000,
              "doc_count": 1
            },
            {
              "key_as_string": "2015-10-01T00:00:00.000-01:00", __"key": 1443661200000,
              "doc_count": 1
            }
          ]
        }
      }
    }

__

|

"key_as_string"值表示指定时区中每天的午夜。   ---|--- 许多时区会改变夏令时的时钟。接近发生这些更改的时刻的存储桶的大小可能与您从"calendar_interval"或"fixed_interval"中预期的大小略有不同。例如，考虑以"CET"时区开始的 DST：2016 年 3 月 27 日凌晨 2 点，时钟将时钟调前 1 小时到当地时间凌晨 3 点。如果您使用"天"作为"calendar_interval"，则覆盖当天的存储桶将仅将数据保留 23 小时，而不是其他存储桶通常的 24 小时。对于较短的间隔也是如此，例如"12 小时"的"fixed_interval"，在 3 月 27 日早上 DST 班次发生时，您只有 11h 存储桶。

###Offset

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
          by_day: {
            date_histogram: {
              field: 'date',
              calendar_interval: 'day',
              offset: '+6h'
            }
          }
        }
      }
    )
    puts response
    
    
    {
    	res, err := es.Index(
    		"my-index-000001",
    		strings.NewReader(`{
    	  "date": "2015-10-01T05:30:00Z"
    	}`),
    		es.Index.WithDocumentID("1"),
    		es.Index.WithRefresh("true"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Index(
    		"my-index-000001",
    		strings.NewReader(`{
    	  "date": "2015-10-01T06:30:00Z"
    	}`),
    		es.Index.WithDocumentID("2"),
    		es.Index.WithRefresh("true"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Search(
    		es.Search.WithIndex("my-index-000001"),
    		es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "by_day": {
    	      "date_histogram": {
    	        "field": "date",
    	        "calendar_interval": "day",
    	        "offset": "+6h"
    	      }
    	    }
    	  }
    	}`)),
    		es.Search.WithSize(0),
    		es.Search.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    
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
        "by_day": {
          "date_histogram": {
            "field":     "date",
            "calendar_interval":  "day",
            "offset":    "+6h"
          }
        }
      }
    }

上述请求不是从午夜开始的单个存储桶，而是从早上 6 点开始将文档分组到存储桶中：

    
    
    {
      ...
      "aggregations": {
        "by_day": {
          "buckets": [
            {
              "key_as_string": "2015-09-30T06:00:00.000Z",
              "key": 1443592800000,
              "doc_count": 1
            },
            {
              "key_as_string": "2015-10-01T06:00:00.000Z",
              "key": 1443679200000,
              "doc_count": 1
            }
          ]
        }
      }
    }

每个存储桶的起始"偏移量"是在进行"time_zone"调整后计算的。

#### 日历间隔上的长偏移量

通常以小于"calendar_interval"为单位使用偏移量。例如，当间隔为天时，使用以小时为单位的偏移量，当间隔为月时，使用以天为单位的偏移量。如果日历间隔始终为标准长度，或者"偏移量"小于日历间隔的一个单位(例如，"天"小于"+24h"或月小于"+28d")，则每个存储桶将具有重复启动。例如，"天"的"+6h"将导致所有存储桶从每天早上 6 点开始。但是，"+30h"也会导致桶从早上 6 点开始，除非从标准时间更改为夏季节省时间的日子，反之亦然。

这种情况在几个月内更为明显，其中每个月的长度至少与其相邻月份中的一个不同。为了证明这一点，请考虑八个文档，每个文档的日期字段分别位于 2022 年 1 月至 8 月的八个月中每个月的第 20 天。

在月份的日历间隔内查询日期直方图时，响应将每月返回一个存储桶，每个存储桶包含一个文档。每个存储桶都有一个以该月第一天命名的键，以及任意偏移量。例如，"+19d"的偏移量将导致存储桶的名称为"2022-01-20"。

    
    
    "buckets": [
      { "key_as_string": "2022-01-20", "key": 1642636800000, "doc_count": 1 },
      { "key_as_string": "2022-02-20", "key": 1645315200000, "doc_count": 1 },
      { "key_as_string": "2022-03-20", "key": 1647734400000, "doc_count": 1 },
      { "key_as_string": "2022-04-20", "key": 1650412800000, "doc_count": 1 },
      { "key_as_string": "2022-05-20", "key": 1653004800000, "doc_count": 1 },
      { "key_as_string": "2022-06-20", "key": 1655683200000, "doc_count": 1 },
      { "key_as_string": "2022-07-20", "key": 1658275200000, "doc_count": 1 },
      { "key_as_string": "2022-08-20", "key": 1660953600000, "doc_count": 1 }
    ]

将偏移量增加到"+20d"，每个文档将显示在上个月的存储桶中，所有存储桶键都以该月的同一天结尾，这是正常的。然而，进一步增加到"+28d"，曾经是二月桶现在变成了"2022-03-01"。

    
    
    "buckets": [
      { "key_as_string": "2021-12-29", "key": 1640736000000, "doc_count": 1 },
      { "key_as_string": "2022-01-29", "key": 1643414400000, "doc_count": 1 },
      { "key_as_string": "2022-03-01", "key": 1646092800000, "doc_count": 1 },
      { "key_as_string": "2022-03-29", "key": 1648512000000, "doc_count": 1 },
      { "key_as_string": "2022-04-29", "key": 1651190400000, "doc_count": 1 },
      { "key_as_string": "2022-05-29", "key": 1653782400000, "doc_count": 1 },
      { "key_as_string": "2022-06-29", "key": 1656460800000, "doc_count": 1 },
      { "key_as_string": "2022-07-29", "key": 1659052800000, "doc_count": 1 }
    ]

如果我们继续增加偏移量，则 30 天的月份也将转移到下个月，因此 8 个存储桶中的 3 个与其他 5 个存储桶的天数不同。事实上，如果我们继续前进，我们会发现两个文件在同一个月出现的情况。最初相隔 30 天的文档可以转移到同一个 31 天的月存储桶中。

例如，对于"+50d"，我们看到：

    
    
    "buckets": [
      { "key_as_string": "2022-01-20", "key": 1642636800000, "doc_count": 1 },
      { "key_as_string": "2022-02-20", "key": 1645315200000, "doc_count": 2 },
      { "key_as_string": "2022-04-20", "key": 1650412800000, "doc_count": 2 },
      { "key_as_string": "2022-06-20", "key": 1655683200000, "doc_count": 2 },
      { "key_as_string": "2022-08-20", "key": 1660953600000, "doc_count": 1 }
    ]

因此，当使用"偏移量"和"calendar_interval"桶大小时，了解使用大于区间大小的偏移量的后果始终很重要。

更多示例：

* 例如，如果目标是有一个每年从 2 月 5 日开始的年度直方图，则可以使用"年"的"calendar_interval"和"+33d"的"偏移"，并且每年的偏移量将相同，因为偏移量仅包括每年相同的长度 1 月。但是，如果目标是让一年从 3 月 5 日开始，则此技术将不起作用，因为偏移量包括每四年更改一次长度的 2 月。  * 如果您希望季度直方图从一年中第一个月内的某个日期开始，它将起作用，但是一旦您将开始日期推到第二个月，偏移量超过一个月，这些季度都将从不同的日期开始。

### 键控响应

将"keyed"标志设置为"true"会将唯一的字符串键与每个存储桶相关联，并将范围作为哈希而不是数组返回：

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          sales_over_time: {
            date_histogram: {
              field: 'date',
              calendar_interval: '1M',
              format: 'yyyy-MM-dd',
              keyed: true
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithIndex("sales"),
    	es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "sales_over_time": {
    	      "date_histogram": {
    	        "field": "date",
    	        "calendar_interval": "1M",
    	        "format": "yyyy-MM-dd",
    	        "keyed": true
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithSize(0),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "sales_over_time": {
          "date_histogram": {
            "field": "date",
            "calendar_interval": "1M",
            "format": "yyyy-MM-dd",
            "keyed": true
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "sales_over_time": {
          "buckets": {
            "2015-01-01": {
              "key_as_string": "2015-01-01",
              "key": 1420070400000,
              "doc_count": 3
            },
            "2015-02-01": {
              "key_as_string": "2015-02-01",
              "key": 1422748800000,
              "doc_count": 2
            },
            "2015-03-01": {
              "key_as_string": "2015-03-01",
              "key": 1425168000000,
              "doc_count": 2
            }
          }
        }
      }
    }

###Scripts

如果文档中的数据与要聚合的数据不完全匹配，请使用运行时字段。例如，如果促销销售的收入应在销售日期后的第二天确认：

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        runtime_mappings: {
          "date.promoted_is_tomorrow": {
            type: 'date',
            script: "\n        long date = doc['date'].value.toInstant().toEpochMilli();\n        if (doc['promoted'].value) {\n          date += 86400;\n        }\n        emit(date);\n      "
          }
        },
        aggregations: {
          sales_over_time: {
            date_histogram: {
              field: 'date.promoted_is_tomorrow',
              calendar_interval: '1M'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "runtime_mappings": {
        "date.promoted_is_tomorrow": {
          "type": "date",
          "script": """
            long date = doc['date'].value.toInstant().toEpochMilli();
            if (doc['promoted'].value) {
              date += 86400;
            }
            emit(date);
          """
        }
      },
      "aggs": {
        "sales_over_time": {
          "date_histogram": {
            "field": "date.promoted_is_tomorrow",
            "calendar_interval": "1M"
          }
        }
      }
    }

###Parameters

您可以使用"order"设置控制返回存储桶的顺序，并根据"min_doc_count"设置筛选返回的存储桶(默认情况下，返回与文档匹配的第一个存储桶和最后一个存储桶之间的所有存储桶)。此直方图还支持"extended_bounds"设置，该设置可以将直方图的边界扩展到数据本身之外，以及将直方图限制为指定边界的"hard_bounds"。更多信息请参阅"扩展边界"和"硬边界"。

#### 缺失值

"missing"参数定义如何处理缺少值的文档。默认情况下，它们被忽略，但也可以将它们视为具有值。

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          sale_date: {
            date_histogram: {
              field: 'date',
              calendar_interval: 'year',
              missing: '2000/01/01'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithIndex("sales"),
    	es.Search.WithBody(strings.NewReader(`{
    	  "aggs": {
    	    "sale_date": {
    	      "date_histogram": {
    	        "field": "date",
    	        "calendar_interval": "year",
    	        "missing": "2000/01/01"
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithSize(0),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "sale_date": {
          "date_histogram": {
            "field": "date",
            "calendar_interval": "year",
            "missing": "2000/01/01" __}
        }
      }
    }

__

|

"日期"字段中没有值的文档将与值为"2000-01-01"的文档属于同一存储桶。   ---|--- ####Orderedit

默认情况下，返回的存储桶按其"键"升序排序，但您可以使用"顺序"设置控制顺序。此设置支持与"术语聚合"相同的"订单"功能。

#### 使用脚本按星期几进行聚合

当您需要按星期几聚合结果时，请在返回星期几的运行时字段上运行"terms"聚合：

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        runtime_mappings: {
          "date.day_of_week": {
            type: 'keyword',
            script: "emit(doc['date'].value.dayOfWeekEnum.getDisplayName(TextStyle.FULL, Locale.ROOT))"
          }
        },
        aggregations: {
          day_of_week: {
            terms: {
              field: 'date.day_of_week'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "runtime_mappings": {
        "date.day_of_week": {
          "type": "keyword",
          "script": "emit(doc['date'].value.dayOfWeekEnum.getDisplayName(TextStyle.FULL, Locale.ROOT))"
        }
      },
      "aggs": {
        "day_of_week": {
          "terms": { "field": "date.day_of_week" }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "day_of_week": {
          "doc_count_error_upper_bound": 0,
          "sum_other_doc_count": 0,
          "buckets": [
            {
              "key": "Sunday",
              "doc_count": 4
            },
            {
              "key": "Thursday",
              "doc_count": 3
            }
          ]
        }
      }
    }

响应将包含具有一周中相对日期的所有存储桶作为键：1 表示星期一，2 表示星期二...7 周日。

[« Composite aggregation](search-aggregations-bucket-composite-
aggregation.md) [Date range aggregation »](search-aggregations-bucket-
daterange-aggregation.md)
