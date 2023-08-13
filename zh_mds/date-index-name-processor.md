

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Date processor](date-processor.md) [Dissect processor »](dissect-
processor.md)

## 日期索引名称处理器

此处理器的目的是通过使用日期 mathindex 名称支持，根据文档中的日期或时间戳字段将文档指向正确的基于时间的索引。

处理器根据提供的索引名称前缀、正在处理的文档中的日期或时间戳字段以及提供的日期舍入，使用日期数学索引名称表达式设置"_index"元数据字段。

首先，此处理器从正在处理的文档的字段中获取日期或时间戳。或者，可以根据如何将字段的值解析为日期来配置日期格式。然后，此日期、提供的索引名称前缀和提供的日期舍入将格式化为 datemath 索引名称表达式。同样在这里，可以选择日期格式指定日期应如何格式化为日期数学索引名称表达式。

一个示例管道，它将文档指向以基于"date1"字段中的日期的"my-index-"前缀开头的月度索引：

    
    
    response = client.ingest.put_pipeline(
      id: 'monthlyindex',
      body: {
        description: 'monthly date-time index naming',
        processors: [
          {
            date_index_name: {
              field: 'date1',
              index_name_prefix: 'my-index-',
              date_rounding: 'M'
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT _ingest/pipeline/monthlyindex
    {
      "description": "monthly date-time index naming",
      "processors" : [
        {
          "date_index_name" : {
            "field" : "date1",
            "index_name_prefix" : "my-index-",
            "date_rounding" : "M"
          }
        }
      ]
    }

将该管道用于索引请求：

    
    
    response = client.index(
      index: 'my-index',
      id: 1,
      pipeline: 'monthlyindex',
      body: {
        "date1": '2016-04-25T12:02:01.789Z'
      }
    )
    puts response
    
    
    PUT /my-index/_doc/1?pipeline=monthlyindex
    {
      "date1" : "2016-04-25T12:02:01.789Z"
    }
    
    
    {
      "_index" : "my-index-2016-04-01",
      "_id" : "1",
      "_version" : 1,
      "result" : "created",
      "_shards" : {
        "total" : 2,
        "successful" : 1,
        "failed" : 0
      },
      "_seq_no" : 55,
      "_primary_term" : 1
    }

上述请求不会将此文档索引到"my-index"索引中，而是索引到"my-index-2016-04-01"索引中，因为它是按月四舍五入的。这是因为日期索引名称处理器覆盖了文档的"_index"属性。

要查看实际索引请求中提供的索引的日期数学值这导致上述文档被索引到"my-index-2016-04-01"我们可以使用模拟请求检查处理器的效果。

    
    
    response = client.ingest.simulate(
      body: {
        pipeline: {
          description: 'monthly date-time index naming',
          processors: [
            {
              date_index_name: {
                field: 'date1',
                index_name_prefix: 'my-index-',
                date_rounding: 'M'
              }
            }
          ]
        },
        docs: [
          {
            _source: {
              "date1": '2016-04-25T12:02:01.789Z'
            }
          }
        ]
      }
    )
    puts response
    
    
    POST _ingest/pipeline/_simulate
    {
      "pipeline" :
      {
        "description": "monthly date-time index naming",
        "processors" : [
          {
            "date_index_name" : {
              "field" : "date1",
              "index_name_prefix" : "my-index-",
              "date_rounding" : "M"
            }
          }
        ]
      },
      "docs": [
        {
          "_source": {
            "date1": "2016-04-25T12:02:01.789Z"
          }
        }
      ]
    }

结果是：

    
    
    {
      "docs" : [
        {
          "doc" : {
            "_id" : "_id",
            "_index" : "<my-index-{2016-04-25||/M{yyyy-MM-dd|UTC}}>",
            "_version" : "-3",
            "_source" : {
              "date1" : "2016-04-25T12:02:01.789Z"
            },
            "_ingest" : {
              "timestamp" : "2016-11-08T19:43:03.850+0000"
            }
          }
        }
      ]
    }

上面的示例显示"_index"设置为"<my-index-{2016-04-25||/M{yyyy-MM-dd|UTC}}>'.Elasticsearch 将此理解为"2016-04-01"，如日期数学索引名称文档中所述

**表 12.日期索引名称选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

要从中获取日期或时间戳的字段。   "index_name_prefix"

|

no

|

-

|

要在打印日期之前附加的索引名称的前缀。支持模板代码段。   "date_rounding"

|

yes

|

-

|

在将日期格式化为索引名称时，如何舍入日期。有效值为："y"(年)、"M"(月)、"w"(周)、"d"(日)、"h"(小时)、"m"(分钟)和"s"(秒)。支持模板代码段。   "date_formats"

|

no

|

yyyy-MM-dd'T'HH:mm:ss.SSSXX

|

用于解析正在预处理的文档中的日期/时间戳的预期日期格式数组。可以是 Java 时间模式或以下格式之一：ISO8601、UNIX、UNIX_MS 或 TAI64N。   "时区"

|

no

|

UTC

|

分析日期和日期数学索引支持时使用的时区将表达式解析为具体的索引名称。   "区域设置"

|

no

|

ENGLISH

|

解析正在预处理的文档的日期时要使用的区域设置，与分析月份名称或工作日相关。   "index_name_format"

|

no

|

yyyy-MM-dd

|

将分析的日期打印到索引名称中时要使用的格式。此处应使用有效的 Java 时间模式。支持模板片段。   "说明"

|

no

|

-

|

处理器的说明。用于描述处理器的目的或其配置。   "如果"

|

no

|

-

|

有条件地执行处理器。请参阅有条件运行处理器。   "ignore_failure"

|

no

|

`false`

|

忽略处理器的故障。请参阅处理管道故障。   "on_failure"

|

no

|

-

|

处理处理器的故障。请参阅处理管道故障。   "标签"

|

no

|

-

|

处理器的标识符。对于调试和指标很有用。   « 日期处理器 剖析处理器 »