

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `enabled`](enabled.md) [`ignore_above` »](ignore-above.md)

##'格式'

在 JSON 文档中，日期表示为字符串。Elasticsearch 使用一组预配置的格式来识别这些字符串并将其解析为以 UTC 表示自epoch_以来_milliseconds的长值。

除了内置格式之外，您还可以使用熟悉的"yyyy/MM/dd"语法指定您自己的自定义格式：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            date: {
              type: 'date',
              format: 'yyyy-MM-dd'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.Create(
    	"my-index-000001",
    	es.Indices.Create.WithBody(strings.NewReader(`{
    	  "mappings": {
    	    "properties": {
    	      "date": {
    	        "type": "date",
    	        "format": "yyyy-MM-dd"
    	      }
    	    }
    	  }
    	}`)),
    )
    fmt.Println(res, err)
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "date": {
            "type":   "date",
            "format": "yyyy-MM-dd"
          }
        }
      }
    }

许多支持日期值的 API 也支持日期数学表达式，例如"now-1m/d"——当前时间减去一个月，向下舍入到最接近的日期。

### 自定义日期格式

支持完全可自定义的日期格式。这些语法解释为DateTimeFormatterdocs。

### 内置格式

以下大多数格式都有"严格"的配套格式，这意味着月份的年、月和日部分必须分别使用 4、2 和 2 位数字，可能预置零。例如，像"5/11/1"这样的日期将被视为无效，需要重写为"2005/11/01"才能被日期解析器接受。

要使用它们，您需要在日期格式的名称前面加上"strict_"，例如"strict_date_optional_time"而不是"date_optional_time"。

当动态映射日期字段时，这些严格的日期格式特别有用，以确保不会意外映射不相关的字符串作为日期。

下表列出了支持的所有默认 ISO 格式：

`epoch_millis`

     A formatter for the number of milliseconds since the epoch. Note, that this timestamp is subject to the limits of a Java `Long.MIN_VALUE` and `Long.MAX_VALUE`. 
`epoch_second`

     A formatter for the number of seconds since the epoch. Note, that this timestamp is subject to the limits of a Java `Long.MIN_VALUE` and `Long. MAX_VALUE` divided by 1000 (the number of milliseconds in a second). 
`date_optional_time` or `strict_date_optional_time`

     A generic ISO datetime parser, where the date must include the year at a minimum, and the time (separated by `T`), is optional. Examples: `yyyy-MM-dd'T'HH:mm:ss.SSSZ` or `yyyy-MM-dd`. 
`strict_date_optional_time_nanos`

     A generic ISO datetime parser, where the date must include the year at a minimum, and the time (separated by `T`), is optional. The fraction of a second part has a nanosecond resolution. Examples: `yyyy-MM-dd'T'HH:mm:ss.SSSSSSZ` or `yyyy-MM-dd`. 
`basic_date`

     A basic formatter for a full date as four digit year, two digit month of year, and two digit day of month: `yyyyMMdd`. 
`basic_date_time`

     A basic formatter that combines a basic date and time, separated by a _T_ : `yyyyMMdd'T'HHmmss.SSSZ`. 
`basic_date_time_no_millis`

     A basic formatter that combines a basic date and time without millis, separated by a _T_ : `yyyyMMdd'T'HHmmssZ`. 
`basic_ordinal_date`

     A formatter for a full ordinal date, using a four digit year and three digit dayOfYear: `yyyyDDD`. 
`basic_ordinal_date_time`

     A formatter for a full ordinal date and time, using a four digit year and three digit dayOfYear: `yyyyDDD'T'HHmmss.SSSZ`. 
`basic_ordinal_date_time_no_millis`

     A formatter for a full ordinal date and time without millis, using a four digit year and three digit dayOfYear: `yyyyDDD'T'HHmmssZ`. 
`basic_time`

     A basic formatter for a two digit hour of day, two digit minute of hour, two digit second of minute, three digit millis, and time zone offset: `HHmmss.SSSZ`. 
`basic_time_no_millis`

     A basic formatter for a two digit hour of day, two digit minute of hour, two digit second of minute, and time zone offset: `HHmmssZ`. 
`basic_t_time`

     A basic formatter for a two digit hour of day, two digit minute of hour, two digit second of minute, three digit millis, and time zone off set prefixed by _T_ : `'T'HHmmss.SSSZ`. 
`basic_t_time_no_millis`

     A basic formatter for a two digit hour of day, two digit minute of hour, two digit second of minute, and time zone offset prefixed by _T_ : `'T'HHmmssZ`. 
`basic_week_date` or `strict_basic_week_date`

     A basic formatter for a full date as four digit weekyear, two digit week of weekyear, and one digit day of week: `xxxx'W'wwe`. 
`basic_week_date_time` or `strict_basic_week_date_time`

     A basic formatter that combines a basic weekyear date and time, separated by a _T_ : `xxxx'W'wwe'T'HHmmss.SSSZ`. 
`basic_week_date_time_no_millis` or `strict_basic_week_date_time_no_millis`

     A basic formatter that combines a basic weekyear date and time without millis, separated by a _T_ : `xxxx'W'wwe'T'HHmmssZ`. 
`date` or `strict_date`

     A formatter for a full date as four digit year, two digit month of year, and two digit day of month: `yyyy-MM-dd`. 
`date_hour` or `strict_date_hour`

     A formatter that combines a full date and two digit hour of day: `yyyy-MM-dd'T'HH`. 
`date_hour_minute` or `strict_date_hour_minute`

     A formatter that combines a full date, two digit hour of day, and two digit minute of hour: `yyyy-MM-dd'T'HH:mm`. 
`date_hour_minute_second` or `strict_date_hour_minute_second`

     A formatter that combines a full date, two digit hour of day, two digit minute of hour, and two digit second of minute: `yyyy-MM-dd'T'HH:mm:ss`. 
`date_hour_minute_second_fraction` or
`strict_date_hour_minute_second_fraction`

     A formatter that combines a full date, two digit hour of day, two digit minute of hour, two digit second of minute, and three digit fraction of second: `yyyy-MM-dd'T'HH:mm:ss.SSS`. 
`date_hour_minute_second_millis` or `strict_date_hour_minute_second_millis`

     A formatter that combines a full date, two digit hour of day, two digit minute of hour, two digit second of minute, and three digit fraction of second: `yyyy-MM-dd'T'HH:mm:ss.SSS`. 
`date_time` or `strict_date_time`

     A formatter that combines a full date and time, separated by a _T_ : `yyyy-MM-dd'T'HH:mm:ss.SSSZ`. 
`date_time_no_millis` or `strict_date_time_no_millis`

     A formatter that combines a full date and time without millis, separated by a _T_ : `yyyy-MM-dd'T'HH:mm:ssZ`. 
`hour` or `strict_hour`

     A formatter for a two digit hour of day: `HH`
`hour_minute` or `strict_hour_minute`

     A formatter for a two digit hour of day and two digit minute of hour: `HH:mm`. 
`hour_minute_second` or `strict_hour_minute_second`

     A formatter for a two digit hour of day, two digit minute of hour, and two digit second of minute: `HH:mm:ss`. 
`hour_minute_second_fraction` or `strict_hour_minute_second_fraction`

     A formatter for a two digit hour of day, two digit minute of hour, two digit second of minute, and three digit fraction of second: `HH:mm:ss.SSS`. 
`hour_minute_second_millis` or `strict_hour_minute_second_millis`

     A formatter for a two digit hour of day, two digit minute of hour, two digit second of minute, and three digit fraction of second: `HH:mm:ss.SSS`. 
`ordinal_date` or `strict_ordinal_date`

     A formatter for a full ordinal date, using a four digit year and three digit dayOfYear: `yyyy-DDD`. 
`ordinal_date_time` or `strict_ordinal_date_time`

     A formatter for a full ordinal date and time, using a four digit year and three digit dayOfYear: `yyyy-DDD'T'HH:mm:ss.SSSZ`. 
`ordinal_date_time_no_millis` or `strict_ordinal_date_time_no_millis`

     A formatter for a full ordinal date and time without millis, using a four digit year and three digit dayOfYear: `yyyy-DDD'T'HH:mm:ssZ`. 
`time` or `strict_time`

     A formatter for a two digit hour of day, two digit minute of hour, two digit second of minute, three digit fraction of second, and time zone offset: `HH:mm:ss.SSSZ`. 
`time_no_millis` or `strict_time_no_millis`

     A formatter for a two digit hour of day, two digit minute of hour, two digit second of minute, and time zone offset: `HH:mm:ssZ`. 
`t_time` or `strict_t_time`

     A formatter for a two digit hour of day, two digit minute of hour, two digit second of minute, three digit fraction of second, and time zone offset prefixed by _T_ : `'T'HH:mm:ss.SSSZ`. 
`t_time_no_millis` or `strict_t_time_no_millis`

     A formatter for a two digit hour of day, two digit minute of hour, two digit second of minute, and time zone offset prefixed by _T_ : `'T'HH:mm:ssZ`. 
`week_date` or `strict_week_date`

     A formatter for a full date as four digit weekyear, two digit week of weekyear, and one digit day of week: `xxxx-'W'ww-e`. 
`week_date_time` or `strict_week_date_time`

     A formatter that combines a full weekyear date and time, separated by a _T_ : `xxxx-'W'ww-e'T'HH:mm:ss.SSSZ`. 
`week_date_time_no_millis` or `strict_week_date_time_no_millis`

     A formatter that combines a full weekyear date and time without millis, separated by a _T_ : `xxxx-'W'ww-e'T'HH:mm:ssZ`. 
`weekyear` or `strict_weekyear`

     A formatter for a four digit weekyear: `xxxx`. 
`weekyear_week` or `strict_weekyear_week`

     A formatter for a four digit weekyear and two digit week of weekyear: `xxxx-'W'ww`. 
`weekyear_week_day` or `strict_weekyear_week_day`

     A formatter for a four digit weekyear, two digit week of weekyear, and one digit day of week: `xxxx-'W'ww-e`. 
`year` or `strict_year`

     A formatter for a four digit year: `yyyy`. 
`year_month` or `strict_year_month`

     A formatter for a four digit year and two digit month of year: `yyyy-MM`. 
`year_month_day` or `strict_year_month_day`

     A formatter for a four digit year, two digit month of year, and two digit day of month: `yyyy-MM-dd`. 

[« `enabled`](enabled.md) [`ignore_above` »](ignore-above.md)
