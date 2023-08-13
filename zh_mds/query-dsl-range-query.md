

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Term-level queries](term-level-queries.md)

[« Prefix query](query-dsl-prefix-query.md) [Regexp query »](query-dsl-
regexp-query.md)

## 范围查询

返回包含指定范围内的术语的文档。

### 示例请求

以下搜索返回"age"字段包含"10"和"20"之间的术语的文档。

    
    
    response = client.search(
      body: {
        query: {
          range: {
            age: {
              gte: 10,
              lte: 20,
              boost: 2
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "range": {
    	      "age": {
    	        "gte": 10,
    	        "lte": 20,
    	        "boost": 2.0
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "range": {
          "age": {
            "gte": 10,
            "lte": 20,
            "boost": 2.0
          }
        }
      }
    }

### "范围"的顶级参数

`<field>`

    

(必填，对象)您要搜索的字段。

### 参数 '<field>'

`gt`

     (Optional) Greater than. 
`gte`

     (Optional) Greater than or equal to. 
`lt`

     (Optional) Less than. 
`lte`

     (Optional) Less than or equal to. 
`format`

    

(可选，字符串)用于转换查询中的"日期"值的日期格式。

默认情况下，Elasticsearch 使用"映射"中提供的日期"格式<field>"。此值将覆盖该映射格式。

有关有效语法，请参阅"格式"。

如果格式或日期值不完整，则范围查询会将任何缺少的组件替换为默认值。请参阅缺少日期组件。

`relation`

    

(可选，字符串)指示范围查询如何匹配"范围"字段的值。有效值为：

"相交"(默认)

     Matches documents with a range field value that intersects the query's range. 
`CONTAINS`

     Matches documents with a range field value that entirely contains the query's range. 
`WITHIN`

     Matches documents with a range field value entirely within the query's range. 

`time_zone`

    

(可选，字符串)协调世界时 (UTC) 偏移量或 IANA 时区，用于将查询中的"日期"值转换为 UTC。

有效值为 ISO 8601 UTC 偏移量(例如"+01：00"或"08：00")和 IANA时区 ID(例如"美国/Los_Angeles"。

有关使用"time_zone"参数的示例查询，请参阅"范围"查询中的时区。

"time_zone"参数不会影响"now"的日期数学值。"now"始终是 UTC 格式的当前系统时间。

但是，"time_zone"参数确实会转换使用"现在"和日期数学舍入计算的日期。例如，"time_zone"参数将转换值"now/d"。

`boost`

    

(可选，浮动)用于减少或增加查询的相关性分数的浮点数。默认为"1.0"。

您可以使用"boost"参数来调整包含两个或多个查询的搜索的相关性分数。

提升值相对于默认值"1.0"。介于"0"和"1.0"之间的提升值会降低相关性分数。大于"1.0"的值会增加相关性分数。

###Notes

#### 将"范围"查询与"文本"和"关键字"字段一起使用

如果"search.allow_expensive_queries"设置为 false，则不会对"文本"或"关键字"字段执行范围查询。

#### 将"范围"查询与"日期"字段一起使用

当 '' 参数<field>是 'date' 字段数据类型时，您可以将日期数学与以下参数一起使用：

* "gt" * "gte" * "lt" * "LTE"

例如，以下搜索返回文档，其中"时间戳"字段包含今天和昨天之间的日期。

    
    
    response = client.search(
      body: {
        query: {
          range: {
            timestamp: {
              gte: 'now-1d/d',
              lte: 'now/d'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "range": {
          "timestamp": {
            "gte": "now-1d/d",
            "lte": "now/d"
          }
        }
      }
    }

##### 缺少日期组件

对于范围查询和日期范围聚合，Elasticsearch 将缺少的日期组件替换为以下值。缺失的年份组件不会被替换。

    
    
    MONTH_OF_YEAR:    01
    DAY_OF_MONTH:     01
    HOUR_OF_DAY:      23
    MINUTE_OF_HOUR:   59
    SECOND_OF_MINUTE: 59
    NANO_OF_SECOND:   999_999_999

例如，如果格式为"yyyy-MM"，则 Elasticsearch 会将"gt"值"2099-12"转换为"2099-12-01T23：59：59.999_999_999Z"。此日期使用提供的年份 ('2099') 和月份 ('12')，但使用默认的日期 ('01')、小时 ('23')、分钟 ('59')、秒 ('59') 和纳秒 ('999_999_999')。

##### 数字日期范围值

如果未指定日期格式，并且范围查询以日期字段为目标，则会解释表示自纪元以来的毫秒数的数值。如果您希望该值表示年份，例如 2020，则需要将其作为字符串值(例如"2020")传递，该值将根据默认格式或设置格式进行分析。

##### 日期数学和舍入

Elasticsearch 对参数中的日期数学值进行舍入，如下所示：

`gt`

    

向上舍入到舍入日期未涵盖的第一个毫秒。

例如，'2014-11-18||/M"向上舍入为"2014-12-01T00：00：00.000"，不包括整个 11 月。

`gte`

    

向下舍入到第一毫秒。

例如，'2014-11-18||/M"向下舍入为"2014-11-01T00：00：00.000"，包括整个月。

`lt`

    

向下舍入到舍入值之前的最后一毫秒。

例如，'2014-11-18||/M"向下舍入为"2014-10-31T23：59：59.999"，不包括整个 11 月。

`lte`

    

向上舍入到舍入间隔中的最新毫秒。

例如，'2014-11-18||/M"向上舍入为"2014-11-30T23：59：59.999"，包括整个月。

#### 使用"time_zone"参数的示例查询

您可以使用"time_zone"参数通过 UTC 偏移量将"日期"值转换为 UTC。例如：

    
    
    $params = [
        'body' => [
            'query' => [
                'range' => [
                    'timestamp' => [
                        'time_zone' => '+01:00',
                        'gte' => '2020-01-01T00:00:00',
                        'lte' => 'now',
                    ],
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(
        body={
            "query": {
                "range": {
                    "timestamp": {
                        "time_zone": "+01:00",
                        "gte": "2020-01-01T00:00:00",
                        "lte": "now",
                    }
                }
            }
        },
    )
    print(resp)
    
    
    response = client.search(
      body: {
        query: {
          range: {
            timestamp: {
              time_zone: '+01:00',
              gte: '2020-01-01T00:00:00',
              lte: 'now'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "range": {
    	      "timestamp": {
    	        "time_zone": "+01:00",
    	        "gte": "2020-01-01T00:00:00",
    	        "lte": "now"
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      body: {
        query: {
          range: {
            timestamp: {
              time_zone: '+01:00',
              gte: '2020-01-01T00:00:00',
              lte: 'now'
            }
          }
        }
      }
    })
    console.log(response)
    
    
    GET /_search
    {
      "query": {
        "range": {
          "timestamp": {
            "time_zone": "+01:00",        __"gte": "2020-01-01T00:00:00", __"lte": "now" __}
        }
      }
    }

__

|

指示"日期"值使用 UTC 偏移量"+01：00"。   ---|---    __

|

当 UTC 偏移量为"+01：00"时，Elasticsearch 将此日期转换为"2019-12-31T23：00：00 UTC"。   __

|

"time_zone"参数不会影响"现在"值。   « 前缀查询正则表达式查询 »