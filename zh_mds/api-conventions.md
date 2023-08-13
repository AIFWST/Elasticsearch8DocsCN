

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md)

[« REST APIs](rest-apis.md) [Common options »](common-options.md)

## 接口约定

Elasticsearch REST API 通过 HTTP 公开。除非另有说明，否则以下约定适用于所有 API。

### 内容类型要求

必须在请求正文中发送的内容的类型必须使用"内容类型"标头指定。此标头的值必须映射到 API 支持的受支持格式之一。大多数 API 支持 JSON、YAML、CBOR，和 SMILE。批量和多搜索 API 支持 NDJSON、JSON 和 SMILE;其他类型的将产生错误响应。

使用"源"查询字符串参数时，必须使用"source_content_type"查询字符串参数指定内容类型。

Elasticsearch 仅支持 UTF-8 编码的 JSON。Elasticsearch 会忽略随请求一起发送的任何其他编码标题。响应也是 UTF-8 编码的。

### 'X-Opaque-Id' HTTPheader

您可以传递"X-Opaque-Id"HTTP 标头来跟踪 Elasticsearch 日志和任务中的请求来源。如果提供，Elasticsearch 会在以下位置显示"X-Opaque-Id"值：

* 响应包含标头的任何请求 * 任务管理 API 响应 * 慢日志 * 弃用日志

对于弃用日志，Elasticsearch 还使用"X-Opaque-Id"值来限制和删除重复的弃用警告。请参阅弃用日志限制。

"X-Opaque-Id"标头接受任意值。但是，我们建议您将这些值限制为有限集，例如每个客户端的 ID。不要为每个请求生成唯一的"X-Opaque-Id"标头。太多唯一的"X-Opaque-Id"值可能会阻止 Elasticsearch 在弃用日志中删除重复数据警告。

### 'traceparent' HTTPheader

Elasticsearch 还支持使用官方 W3C 跟踪上下文规范的"traceparent"HTTP 标头。您可以使用 'traceparent' 标头来跟踪跨 Elasticproducts 和其他服务的请求。由于它仅用于跟踪，因此可以安全地为每个请求生成唯一的"traceparent"标头。

如果提供，Elasticsearch 会将标头的"trace-id"值显示为"trace.id"，如下所示：

* JSON 弹性搜索服务器日志 * 慢日志 * 弃用日志

例如，以下"traceparent"值将在上述日志中生成以下"trace.id"值。

    
    
    `traceparent`: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01
    `trace.id`: 0af7651916cd43dd8448eb211c80319c

### 获取和发布请求

许多 Elasticsearch GET API(最引人注目的是搜索 API)都支持请求正文。虽然 GET 操作在检索信息的上下文中有意义，但并非所有 HTTP 库都支持带有正文的 GET 请求。所有需要正文的 Elasticsearch GET API 也可以作为 POST 请求提交。或者，可以在使用 GET 时将请求正文作为"源"查询字符串参数传递。

### 表达式

cron 表达式是以下形式的字符串：

    
    
        <seconds> <minutes> <hours> <day_of_month> <month> <day_of_week> [year]

Elasticsearch 使用 Quartz JobScheduler 中的 cron 解析器。有关编写 Quartz cron 表达式的详细信息，请参阅 Quartz CronTriggerTutorial。

所有计划时间均采用协调世界时 (UTC);不支持其他时区。

您可以使用 _elasticsearch croneval_命令行工具来验证 cron 表达式。

#### Cron 表达式元素

除"年份"外，所有元素都是必需的。有关允许的特殊字符的信息，请参阅 Cron 特殊字符。

`<seconds>`

     (Required) Valid values: `0`-`59` and the special characters `,` `-` `*` `/`
`<minutes>`

     (Required) Valid values: `0`-`59` and the special characters `,` `-` `*` `/`
`<hours>`

     (Required) Valid values: `0`-`23` and the special characters `,` `-` `*` `/`
`<day_of_month>`

     (Required) Valid values: `1`-`31` and the special characters `,` `-` `*` `/` `?` `L` `W`
`<month>`

     (Required) Valid values: `1`-`12`, `JAN`-`DEC`, `jan`-`dec`, and the special characters `,` `-` `*` `/`
`<day_of_week>`

     (Required) Valid values: `1`-`7`, `SUN`-`SAT`, `sun`-`sat`, and the special characters `,` `-` `*` `/` `?` `L` `#`
`<year>`

     (Optional) Valid values: `1970`-`2099` and the special characters `,` `-` `*` `/`

#### Cron 特殊字符

`*`

     Selects every possible value for a field. For example, `*` in the `hours` field means "every hour". 
`?`

     No specific value. Use when you don't care what the value is. For example, if you want the schedule to trigger on a particular day of the month, but don't care what day of the week that happens to be, you can specify `?` in the `day_of_week` field. 
`-`

     A range of values (inclusive). Use to separate a minimum and maximum value. For example, if you want the schedule to trigger every hour between 9:00 a.m. and 5:00 p.m., you could specify `9-17` in the `hours` field. 
`,`

     Multiple values. Use to separate multiple values for a field. For example, if you want the schedule to trigger every Tuesday and Thursday, you could specify `TUE,THU` in the `day_of_week` field. 
`/`

     Increment. Use to separate values when specifying a time increment. The first value represents the starting point, and the second value represents the interval. For example, if you want the schedule to trigger every 20 minutes starting at the top of the hour, you could specify `0/20` in the `minutes` field. Similarly, specifying `1/5` in `day_of_month` field will trigger every 5 days starting on the first day of the month. 
`L`

     Last. Use in the `day_of_month` field to mean the last day of the month--​day 31 for January, day 28 for February in non-leap years, day 30 for April, and so on. Use alone in the `day_of_week` field in place of `7` or `SAT`, or after a particular day of the week to select the last day of that type in the month. For example `6L` means the last Friday of the month. You can specify `LW` in the `day_of_month` field to specify the last weekday of the month. Avoid using the `L` option when specifying lists or ranges of values, as the results likely won't be what you expect. 
`W`

     Weekday. Use to specify the weekday (Monday-Friday) nearest the given day. As an example, if you specify `15W` in the `day_of_month` field and the 15th is a Saturday, the schedule will trigger on the 14th. If the 15th is a Sunday, the schedule will trigger on Monday the 16th. If the 15th is a Tuesday, the schedule will trigger on Tuesday the 15th. However if you specify `1W` as the value for `day_of_month`, and the 1st is a Saturday, the schedule will trigger on Monday the 3rd--​it won't jump over the month boundary. You can specify `LW` in the `day_of_month` field to specify the last weekday of the month. You can only use the `W` option when the `day_of_month` is a single day--​it is not valid when specifying a range or list of days. 
`#`

     Nth XXX day in a month. Use in the `day_of_week` field to specify the nth XXX day of the month. For example, if you specify `6#1`, the schedule will trigger on the first Friday of the month. Note that if you specify `3#5` and there are not 5 Tuesdays in a particular month, the schedule won't trigger that month. 

####Examples

##### 设置每日触发器

'0 5 9 * * ?'

     Trigger at 9:05 a.m. UTC every day. 
`0 5 9 * * ? 2020`

     Trigger at 9:05 a.m. UTC every day during the year 2020. 

##### 将触发器限制为天数或时间范围

'0 5 9 ?* 周一至周五

     Trigger at 9:05 a.m. UTC Monday through Friday. 
`0 0-5 9 * * ?`

     Trigger every minute starting at 9:00 a.m. UTC and ending at 9:05 a.m. UTC every day. 

##### 设置间隔触发器

'0 0/15 9 * * ?'

     Trigger every 15 minutes starting at 9:00 a.m. UTC and ending at 9:45 a.m. UTC every day. 
`0 5 9 1/3 * ?`

     Trigger at 9:05 a.m. UTC every 3 days every month, starting on the first day of the month. 

##### 设置在特定日期触发的计划

'0 1 4 1 4 ?'

     Trigger every April 1st at 4:01 a.m. UTC. 
`0 0,30 9 ? 4 WED`

     Trigger at 9:00 a.m. UTC and at 9:30 a.m. UTC every Wednesday in the month of April. 
`0 5 9 15 * ?`

     Trigger at 9:05 a.m. UTC on the 15th day of every month. 
`0 5 9 15W * ?`

     Trigger at 9:05 a.m. UTC on the nearest weekday to the 15th of every month. 
`0 5 9 ? * 6#1`

     Trigger at 9:05 a.m. UTC on the first Friday of every month. 

##### 使用最后设置触发器

'0 5 9 L * ？"

     Trigger at 9:05 a.m. UTC on the last day of every month. 
`0 5 9 ? * 2L`

     Trigger at 9:05 a.m. UTC on the last Monday of every month. 
`0 5 9 LW * ?`

     Trigger at 9:05 a.m. UTC on the last weekday of every month. 

### 索引和索引别名中的日期数学支持

日期数学名称解析允许您搜索一系列时序索引或索引别名，而不是搜索所有索引并筛选结果。限制搜索索引的数量可减少集群负载并提高搜索性能。例如，如果要在每日日志中搜索错误，则可以使用日期数学名称模板将搜索限制为过去两天。

大多数接受索引或索引别名参数的 API 都支持日期数学。Adate 数学名称采用以下形式：

    
    
    <static_name{date_math_expr{date_format|time_zone}}>

Where:

`static_name`

|

静态文本 ---|--- 'date_math_expr'

|

动态"date_format"计算日期的动态日期数学表达式

|

应呈现计算日期的可选格式。默认为"yyyyy"。唰��格式应与java-time兼容<https://docs.oracle.com/javase/8/docs/api/java/time/format/DateTimeFormatter.html>"time_zone"

|

可选时区。默认为"UTC"。   注意在"date_format"中使用的小字母与大写字母的使用。例如："mm"表示小时分，而"MM"表示一年中的月份。同样，"hh"表示"1-12"范围内的小时与"AM/PM"组合，而"HH"表示"0-23"24小时范围内的小时。

日期数学表达式的解析与区域设置无关。因此，除公历外，不可能使用任何其他日历。

必须将日期数学名称括在尖括号中。如果在请求路径中使用该名称，则必须对特殊字符进行 URI 编码。例如：

    
    
    response = client.indices.create(
      index: '<my-index-{now/d}>'
    )
    puts response
    
    
    # PUT /<my-index-{now/d}>
    PUT /%3Cmy-index-%7Bnow%2Fd%7D%3E

### 日期数学字符的百分比编码

用于日期舍入的特殊字符必须按如下方式进行 URI 编码：

`<`

|

'%3C' ---|--- '>'

|

"%3E" "/"

|

'%2F' '{'

|

'%7B' '}'

|

'%7D' '|'

|

"%7C" "+"

|

"%2B" "："

|

"%3A" ""，""

|

'%2C' 以下示例显示了不同形式的日期数学名称，以及它们在给定当前时间为 2024 年 3 月 22 日中午 UTC 的情况下解析为的最终名称。

表达式 |解析为 ---|--- '<logstash-{now/d}>'

|

'logstash-2024.03.22' '<logstash-{now/M}>'

|

'logstash-2024.03.01' '<logstash-{now/M{yyyy.MM}}>'

|

'logstash-2024.03' '<logstash-{now/M-1M{yyyy.MM}}>'

|

'logstash-2024.02' '<logstash-{now/d{yyyy.MM.dd|+12：00}}>'

|

'logstash-2024.03.23' 要在名称模板的静态部分使用字符"{"和"}"，请使用反斜杠"\"对其进行转义，例如：

* '<elastic\{ON\}-{now/M}>' 解析为 'elastic{ON}-2024.03.01'

以下示例显示了一个搜索请求，该请求搜索过去三天的 Logstashindex 索引，假设索引使用默认的 Logstashindex 名称格式"logstash-YYYY.MM.dd"。

    
    
    $params = [
        'index' => '%3Clogstash-%7Bnow%2Fd-2d%7D%3E%2C%3Clogstash-%7Bnow%2Fd-1d%7D%3E%2C%3Clogstash-%7Bnow%2Fd%7D%3E',
        'body' => [
            'query' => [
                'match' => [
                    'test' => 'data',
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(
        index="%3Clogstash-%7Bnow%2Fd-2d%7D%3E%2C%3Clogstash-%7Bnow%2Fd-1d%7D%3E%2C%3Clogstash-%7Bnow%2Fd%7D%3E",
        body={"query": {"match": {"test": "data"}}},
    )
    print(resp)
    
    
    response = client.search(
      index: '<logstash-{now/d-2d}>,<logstash-{now/d-1d}>,<logstash-{now/d}>',
      body: {
        query: {
          match: {
            test: 'data'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithIndex("%3Clogstash-%7Bnow%2Fd-2d%7D%3E%2C%3Clogstash-%7Bnow%2Fd-1d%7D%3E%2C%3Clogstash-%7Bnow%2Fd%7D%3E"),
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "match": {
    	      "test": "data"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      index: '%3Clogstash-%7Bnow%2Fd-2d%7D%3E%2C%3Clogstash-%7Bnow%2Fd-1d%7D%3E%2C%3Clogstash-%7Bnow%2Fd%7D%3E',
      body: {
        query: {
          match: {
            test: 'data'
          }
        }
      }
    })
    console.log(response)
    
    
    # GET /<logstash-{now/d-2d}>,<logstash-{now/d-1d}>,<logstash-{now/d}>/_search
    GET /%3Clogstash-%7Bnow%2Fd-2d%7D%3E%2C%3Clogstash-%7Bnow%2Fd-1d%7D%3E%2C%3Clogstash-%7Bnow%2Fd%7D%3E/_search
    {
      "query" : {
        "match": {
          "test": "data"
        }
      }
    }

### 多目标语法

大多数接受"<data-stream>"、""<index>或<target>""请求路径参数的 API 也支持_multi目标syntax_。

在多目标语法中，您可以使用逗号分隔的列表对多个资源(例如数据流、索引或别名："test1，test2，test3")运行请求。您还可以使用类似 glob 的通配符 ('*') 表达式来定位与模式匹配的资源："test*"或"*test"或"te*t"或"*test*"。

您可以使用"-"字符"测试*，-test3"排除目标。

别名在通配符表达式之后解析。这可能会导致以排除的别名为目标的请求。例如，如果"test3"是索引别名，则模式"test*，-test3"仍以"test3"的索引为目标。为避免这种情况，请改为排除别名的具体索引。

可以面向索引的多目标 API 支持以下查询字符串参数：

`ignore_unavailable`

     (Optional, Boolean) If `false`, the request returns an error if it targets a missing or closed index. Defaults to `false`. 
`allow_no_indices`

     (Optional, Boolean) If `false`, the request returns an error if any wildcard expression, [index alias](aliases.html "Aliases"), or `_all` value targets only missing or closed indices. This behavior applies even if the request targets other open indices. For example, a request targeting `foo*,bar*` returns an error if an index starts with `foo` but no index starts with `bar`. 
`expand_wildcards`

    

(可选，字符串)通配符模式可以匹配的索引类型。如果请求可以以数据流为目标，则此参数确定通配符表达式是否与隐藏的数据流匹配。支持逗号分隔的值，例如"打开，隐藏"。有效值为：

`all`

     Match any data stream or index, including [hidden](api-conventions.html#multi-hidden "Hidden data streams and indices") ones. 
`open`

     Match open, non-hidden indices. Also matches any non-hidden data stream. 
`closed`

     Match closed, non-hidden indices. Also matches any non-hidden data stream. Data streams cannot be closed. 
`hidden`

     Match hidden data streams and hidden indices. Must be combined with `open`, `closed`, or both. 
`none`

     Wildcard patterns are not accepted. 

上述参数的默认设置取决于所使用的 API。

一些可以以索引为目标的多目标 API 还支持以下查询字符串参数：

`ignore_throttled`

     (Optional, Boolean) If `true`, concrete, expanded or aliased indices are ignored when frozen. Defaults to `true`. 

具有单个目标的 API(例如获取文档 API)不支持多目标语法。

#### 隐藏的数据流和索引

对于大多数 API，默认情况下，通配符表达式与隐藏的数据流和索引不匹配。要使用通配符表达式匹配隐藏的数据流和索引，必须指定"expand_wildcards"查询参数。

或者，默认情况下，查询以点开头的索引模式(例如".watcher_hist*")将与隐藏索引匹配。这旨在镜像 Unix 文件通配行为，并提供到隐藏索引的更平滑的过渡路径。

您可以通过在流的匹配索引模板中将"data_stream.hidden"设置为"true"来创建隐藏的数据流。您可以使用"index.hidden"索引设置隐藏索引。

数据流的支持索引会自动隐藏。某些功能(如机器学习)将信息存储在隐藏索引中。

匹配所有索引的全局索引模板不会应用于隐藏索引。

#### 系统索引

Elasticsearch 模块和插件可以将配置和状态信息存储在内部_system indices_中。不应直接访问或修改系统索引，因为它们包含对系统操作至关重要的数据。

直接访问系统索引已弃用，并且在将来的主要版本中将不再允许。

###Parameters

其余参数(使用 HTTP 时，映射到 HTTP URL 参数)遵循使用下划线大小写的约定。

### 查询字符串中的请求正文

对于不接受非 POST 请求的请求正文的库，可以改为将请求正文作为"源"查询字符串参数传递。使用此方法时，还应传递"source_content_type"参数，其中包含指示源格式的媒体类型值，例如"application/json"。

### REST API 版本兼容性

主要版本升级通常包括许多重大更改，这些更改会影响您与 Elasticsearch 的交互方式。虽然我们建议您在升级 Elasticsearch 之前监控弃用日志并更新应用程序，但必须协调必要的更改可能会成为升级的障碍。

您可以通过包含 API 兼容性标头使现有应用程序在升级后无需修改即可运行，这些标头告诉 Elasticsearch您仍在使用以前版本的 REST API。使用这些标头允许请求和响应的结构保持不变;它不保证相同的行为。

您可以在"内容类型"和"接受"标头中基于每个请求设置版本兼容性。将"兼容"设置为与您正在运行的版本相同的主要版本不会产生任何影响，但可以确保请求在升级 Elasticsearch 后仍然有效。

要告诉 Elasticsearch 8.0 您使用的是 7.x 请求和响应格式，请设置 'compatible-with=7'：

    
    
    Content-Type: application/vnd.elasticsearch+json; compatible-with=7
    Accept: application/vnd.elasticsearch+json; compatible-with=7

### 基于 URL 的访问控制

许多用户使用具有基于 URL 的访问控制的代理来保护对 Elasticsearch 数据流和索引的访问。对于多搜索、多获取 API")和批量请求，用户可以选择在 URL 中以及请求正文中的每个请求中指定数据流或索引。这会使基于 URL 的访问控制具有挑战性。

要防止用户覆盖 URL 中指定的数据流或索引，请在 'elasticsearch.yml' 中将"rest.action.multi.allow_explicit_index"设置为"false"。

这会导致 Elasticsearch 拒绝在请求正文中显式指定数据流或索引的请求。

### 布尔值

所有 REST API 参数(请求参数和 JSON 正文)都支持提供布尔值"false"作为值"false"，提供布尔值"true"作为值"true"。所有其他值将引发错误。

### 数字值

所有 REST API 都支持在支持本机 JSON 数字类型的基础上以"字符串"形式提供编号参数。

### 字节大小单位

每当需要指定数据的字节大小时，例如在设置缓冲区大小参数时，该值必须指定单位，例如"10kb"表示 10KB。请注意，这些单位使用 1024 的幂，因此"1kb"表示 1024 字节。支持的单位包括：

`b`

|

字节 ---|--- 'kb'

|

千字节 'mb'

|

兆字节"千兆字节"

|

千兆字节"TB"

|

兆字节"pb"

|

PB ### 距离单位编辑

在需要指定距离的地方，例如地理距离中的"距离"参数，如果未指定，则默认单位为米。距离可以用其他单位指定，例如"1公里"或"2英里"(2 英里)。

完整的单位列表如下：

Mile

|

"mi"或"miles" ---|---码

|

"码"或"码"脚

|

"英尺"或"英尺"英寸

|

"英寸"或"英寸"公里

|

"公里"或"公里"米

|

"米"或"米"厘米

|

"厘米"或"厘米"毫米

|

"毫米"或"毫米"海里

|

"NM"、"NMI"或"海里" ### 时间单位编辑

每当需要指定持续时间时，例如对于"超时"参数，持续时间必须指定单位，例如"2d"表示 2 天。支持的单位包括：

`d`

|

天---|--- 'h'

|

小时 'm'

|

分钟's'

|

秒"毫秒"

|

毫秒"微"

|

微秒"纳米"

|

纳秒 ### 单位无数量编辑

无单位数量意味着它们没有像"字节"或"赫兹"或"米"或"长吨"这样的"单位"。

如果其中一个数量很大，我们将打印出 10m 表示 10，000，000 或 7k 表示 7，000。不过，当我们的意思是 87 时，我们仍然会打印 87。这些是支持的乘数：

`k`

|

基洛 ---|--- 'm'

|

兆"克"

|

千兆't'

|

Tera 'p'

|

Peta « REST API 常用选项 »