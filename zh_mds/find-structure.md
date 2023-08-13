

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md)

[« Fleet multi search API](fleet-multi-search.md) [Graph explore API
»](graph-explore-api.md)

## 查找结构接口

查找文本的结构。文本必须包含适合放入弹性堆栈的数据。

###Request

"发布_text_structure/find_structure"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"monitor_text_structure"或"监控"集群权限才能使用此 API。请参阅安全权限。

###Description

此 API 提供了一个起点，用于将数据以适合后续与其他 Elastic Stack 功能一起使用的格式摄取到 Elasticsearch 中。

与其他 Elasticsearch 端点不同，发布到此端点的数据不需要采用 UTF-8 编码和 JSON 格式。然而，它必须文本;当前不支持二进制文本格式。

来自 API 的响应包含：

*文本开头的几条消息。  * 显示文本中检测到的所有字段的最常见值的统计信息以及数字字段的基本数值统计信息。  * 有关文本结构的信息，这在编写收录配置以为其编制索引或类似格式的文本时非常有用。  * Elasticsearch 索引的适当映射，可用于摄取文本。

所有这些信息都可以由结构查找器在没有指导的情况下计算出来。但是，您可以选择通过指定一个或多个查询参数来重写有关文本结构的某些决策。

可以在示例中看到输出的详细信息。

如果结构查找器为某些文本生成意外结果，请指定"解释"查询参数。它会导致响应中出现"解释"，这应该有助于确定选择返回结构的原因。

### 查询参数

`charset`

     (Optional, string) The text's character set. It must be a character set that is supported by the JVM that Elasticsearch uses. For example, `UTF-8`, `UTF-16LE`, `windows-1252`, or `EUC-JP`. If this parameter is not specified, the structure finder chooses an appropriate character set. 
`column_names`

     (Optional, string) If you have set `format` to `delimited`, you can specify the column names in a comma-separated list. If this parameter is not specified, the structure finder uses the column names from the header row of the text. If the text does not have a header role, columns are named "column1", "column2", "column3", etc. 
`delimiter`

     (Optional, string) If you have set `format` to `delimited`, you can specify the character used to delimit the values in each row. Only a single character is supported; the delimiter cannot have multiple characters. By default, the API considers the following possibilities: comma, tab, semi-colon, and pipe (`|`). In this default scenario, all rows must have the same number of fields for the delimited format to be detected. If you specify a delimiter, up to 10% of the rows can have a different number of columns than the first row. 
`explain`

     (Optional, Boolean) If this parameter is set to `true`, the response includes a field named `explanation`, which is an array of strings that indicate how the structure finder produced its result. The default value is `false`. 
`format`

     (Optional, string) The high level structure of the text. Valid values are `ndjson`, `xml`, `delimited`, and `semi_structured_text`. By default, the API chooses the format. In this default scenario, all rows must have the same number of fields for a delimited format to be detected. If the `format` is set to `delimited` and the `delimiter` is not set, however, the API tolerates up to 5% of rows that have a different number of columns than the first row. 
`grok_pattern`

     (Optional, string) If you have set `format` to `semi_structured_text`, you can specify a Grok pattern that is used to extract fields from every message in the text. The name of the timestamp field in the Grok pattern must match what is specified in the `timestamp_field` parameter. If that parameter is not specified, the name of the timestamp field in the Grok pattern must match "timestamp". If `grok_pattern` is not specified, the structure finder creates a Grok pattern. 
`ecs_compatibility`

     (Optional, string) The mode of compatibility with ECS compliant Grok patterns. Use this parameter to specify whether to use ECS Grok patterns instead of legacy ones when the structure finder creates a Grok pattern. Valid values are `disabled` and `v1`. The default value is `disabled`. This setting primarily has an impact when a whole message Grok pattern such as `%{CATALINALOG}` matches the input. If the structure finder identifies a common structure but has no idea of meaning then generic field names such as `path`, `ipaddress`, `field1` and `field2` are used in the `grok_pattern` output, with the intention that a user who knows the meanings rename these fields before using it. 
`has_header_row`

     (Optional, Boolean) If you have set `format` to `delimited`, you can use this parameter to indicate whether the column names are in the first row of the text. If this parameter is not specified, the structure finder guesses based on the similarity of the first row of the text to other rows. 
`line_merge_size_limit`

     (Optional, unsigned integer) The maximum number of characters in a message when lines are merged to form messages while analyzing semi-structured text. The default is `10000`. If you have extremely long messages you may need to increase this, but be aware that this may lead to very long processing times if the way to group lines into messages is misdetected. 
`lines_to_sample`

    

(可选，无符号整数)要包含在结构分析中的行数，从文本的开头开始。最小值为 2;默认值为"1000"。如果此参数的值大于文本中的行数，则对所有行进行分析(只要文本中至少有两行)。

线的数量和线的变化会影响分析的速度。例如，如果您上传的文本的前 1000 行是同一消息的所有变体，则分析将发现比使用较大样本时看到的更多共性。但是，如果可能的话，在前 1000 行中上传具有更多多样性的示例文本比请求分析 100000 行以实现某些多样性更有效。

`quote`

     (Optional, string) If you have set `format` to `delimited`, you can specify the character used to quote the values in each row if they contain newlines or the delimiter character. Only a single character is supported. If this parameter is not specified, the default value is a double quote (`"`). If your delimited text format does not use quoting, a workaround is to set this argument to a character that does not appear anywhere in the sample. 
`should_trim_fields`

     (Optional, Boolean) If you have set `format` to `delimited`, you can specify whether values between delimiters should have whitespace trimmed from them. If this parameter is not specified and the delimiter is pipe (`|`), the default value is `true`. Otherwise, the default value is `false`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Sets the maximum amount of time that the structure analysis make take. If the analysis is still running when the timeout expires then it will be aborted. The default value is 25 seconds. 
`timestamp_field`

    

(可选，字符串)包含文本中每条记录的主时间戳的字段的名称。特别是，如果文本被摄取到 anindex 中，则这是用于填充"@timestamp"字段的字段。

如果"格式"为"semi_structured_text"，则此字段必须与"grok_pattern"中相应提取的名称匹配。因此，对于半结构化文本，最好不要指定此参数，除非还指定了"grok_pattern"。

对于结构化文本，如果指定此参数，则文本中必须存在该字段。

如果未指定此参数，结构查找器将决定哪个字段(如果有)是主时间戳字段。对于结构化文本，文本中不强制使用时间戳。

`timestamp_format`

    

(可选，字符串)文本中时间戳字段的 Java 时间格式。

仅支持 Java 时间格式字母组的子集：

* "a" * "d" * "dd" * "EEE" * "EEEE" * "H" * "HH" * "h" * "m" * "mm" * "mmm" * "mmmm" * "mm" * "ss" * "XX" * "XXX" * "yy" * "yyyy" * "zzz"

此外，支持长度为 1 到 9 的"S"字母组(秒的小数部分)，前提是它们出现在"ss"之后，并且与"ss"之间用 a'."、"、' 或 '：' 分隔。还允许使用空格和标点符号，但"？"、换行符和回车符以及括在单引号中的文字文本除外。例如，'MM/dd HH.mm.ss，SSSSSS 'in' yyyy' 是一种有效的覆盖格式。

此参数的一个有价值的用例是，当格式为半结构化文本时，文本中有多种时间戳格式，并且您知道哪种格式对应于主时间戳，但您不想指定完整的"grok_pattern"。另一种是当时间戳格式是结构查找器默认不考虑的格式时。

如果未指定此参数，结构查找器将从内置集中选择最佳格式。

如果指定了特殊值"null"，则结构查找器将不会在文本中查找主时间戳。当格式为半结构化文本时，这将导致结构查找器将文本视为单行消息。

下表为某些示例时间戳提供了适当的"时间格式"值：

时间格式 |演示文稿 ---|--- 年-月-日 HH：mm：ssZ

|

2019-04-20 13：15：22+0000 EEE， d MMM yyyy HH：mm：ss Z

|

周六， 20 四月 2019 13：15：22 +0000 dd.MM.yy HH：mm：ss.SSS

|

20.04.19 13：15：22.285 有关日期和时间格式语法的更多信息，请参阅 Java 日期/时间格式文档。

### 请求正文

要分析的文本。它必须包含适合被纳入 Elasticsearch 的数据。它不需要采用 JSON 格式，也不需要采用 UTF-8 编码。大小限制为 Elasticsearch HTTPreceive 缓冲区大小，默认为 100 Mb。

###Examples

#### 摄取换行符分隔的 JSON

假设您有换行符分隔的 JSON 文本，其中包含有关某些书籍的信息。您可以将内容发送到"find_structure"端点：

    
    
    response = client.text_structure.find_structure(
      body: [
        {
          name: 'Leviathan Wakes',
          author: 'James S.A. Corey',
          release_date: '2011-06-02',
          page_count: 561
        },
        {
          name: 'Hyperion',
          author: 'Dan Simmons',
          release_date: '1989-05-26',
          page_count: 482
        },
        {
          name: 'Dune',
          author: 'Frank Herbert',
          release_date: '1965-06-01',
          page_count: 604
        },
        {
          name: 'Dune Messiah',
          author: 'Frank Herbert',
          release_date: '1969-10-15',
          page_count: 331
        },
        {
          name: 'Children of Dune',
          author: 'Frank Herbert',
          release_date: '1976-04-21',
          page_count: 408
        },
        {
          name: 'God Emperor of Dune',
          author: 'Frank Herbert',
          release_date: '1981-05-28',
          page_count: 454
        },
        {
          name: 'Consider Phlebas',
          author: 'Iain M. Banks',
          release_date: '1987-04-23',
          page_count: 471
        },
        {
          name: "Pandora's Star",
          author: 'Peter F. Hamilton',
          release_date: '2004-03-02',
          page_count: 768
        },
        {
          name: 'Revelation Space',
          author: 'Alastair Reynolds',
          release_date: '2000-03-15',
          page_count: 585
        },
        {
          name: 'A Fire Upon the Deep',
          author: 'Vernor Vinge',
          release_date: '1992-06-01',
          page_count: 613
        },
        {
          name: "Ender's Game",
          author: 'Orson Scott Card',
          release_date: '1985-06-01',
          page_count: 324
        },
        {
          name: '1984',
          author: 'George Orwell',
          release_date: '1985-06-01',
          page_count: 328
        },
        {
          name: 'Fahrenheit 451',
          author: 'Ray Bradbury',
          release_date: '1953-10-15',
          page_count: 227
        },
        {
          name: 'Brave New World',
          author: 'Aldous Huxley',
          release_date: '1932-06-01',
          page_count: 268
        },
        {
          name: 'Foundation',
          author: 'Isaac Asimov',
          release_date: '1951-06-01',
          page_count: 224
        },
        {
          name: 'The Giver',
          author: 'Lois Lowry',
          release_date: '1993-04-26',
          page_count: 208
        },
        {
          name: 'Slaughterhouse-Five',
          author: 'Kurt Vonnegut',
          release_date: '1969-06-01',
          page_count: 275
        },
        {
          name: "The Hitchhiker's Guide to the Galaxy",
          author: 'Douglas Adams',
          release_date: '1979-10-12',
          page_count: 180
        },
        {
          name: 'Snow Crash',
          author: 'Neal Stephenson',
          release_date: '1992-06-01',
          page_count: 470
        },
        {
          name: 'Neuromancer',
          author: 'William Gibson',
          release_date: '1984-07-01',
          page_count: 271
        },
        {
          name: "The Handmaid's Tale",
          author: 'Margaret Atwood',
          release_date: '1985-06-01',
          page_count: 311
        },
        {
          name: 'Starship Troopers',
          author: 'Robert A. Heinlein',
          release_date: '1959-12-01',
          page_count: 335
        },
        {
          name: 'The Left Hand of Darkness',
          author: 'Ursula K. Le Guin',
          release_date: '1969-06-01',
          page_count: 304
        },
        {
          name: 'The Moon is a Harsh Mistress',
          author: 'Robert A. Heinlein',
          release_date: '1966-04-01',
          page_count: 288
        }
      ]
    )
    puts response
    
    
    POST _text_structure/find_structure
    {"name": "Leviathan Wakes", "author": "James S.A. Corey", "release_date": "2011-06-02", "page_count": 561}
    {"name": "Hyperion", "author": "Dan Simmons", "release_date": "1989-05-26", "page_count": 482}
    {"name": "Dune", "author": "Frank Herbert", "release_date": "1965-06-01", "page_count": 604}
    {"name": "Dune Messiah", "author": "Frank Herbert", "release_date": "1969-10-15", "page_count": 331}
    {"name": "Children of Dune", "author": "Frank Herbert", "release_date": "1976-04-21", "page_count": 408}
    {"name": "God Emperor of Dune", "author": "Frank Herbert", "release_date": "1981-05-28", "page_count": 454}
    {"name": "Consider Phlebas", "author": "Iain M. Banks", "release_date": "1987-04-23", "page_count": 471}
    {"name": "Pandora's Star", "author": "Peter F. Hamilton", "release_date": "2004-03-02", "page_count": 768}
    {"name": "Revelation Space", "author": "Alastair Reynolds", "release_date": "2000-03-15", "page_count": 585}
    {"name": "A Fire Upon the Deep", "author": "Vernor Vinge", "release_date": "1992-06-01", "page_count": 613}
    {"name": "Ender's Game", "author": "Orson Scott Card", "release_date": "1985-06-01", "page_count": 324}
    {"name": "1984", "author": "George Orwell", "release_date": "1985-06-01", "page_count": 328}
    {"name": "Fahrenheit 451", "author": "Ray Bradbury", "release_date": "1953-10-15", "page_count": 227}
    {"name": "Brave New World", "author": "Aldous Huxley", "release_date": "1932-06-01", "page_count": 268}
    {"name": "Foundation", "author": "Isaac Asimov", "release_date": "1951-06-01", "page_count": 224}
    {"name": "The Giver", "author": "Lois Lowry", "release_date": "1993-04-26", "page_count": 208}
    {"name": "Slaughterhouse-Five", "author": "Kurt Vonnegut", "release_date": "1969-06-01", "page_count": 275}
    {"name": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "release_date": "1979-10-12", "page_count": 180}
    {"name": "Snow Crash", "author": "Neal Stephenson", "release_date": "1992-06-01", "page_count": 470}
    {"name": "Neuromancer", "author": "William Gibson", "release_date": "1984-07-01", "page_count": 271}
    {"name": "The Handmaid's Tale", "author": "Margaret Atwood", "release_date": "1985-06-01", "page_count": 311}
    {"name": "Starship Troopers", "author": "Robert A. Heinlein", "release_date": "1959-12-01", "page_count": 335}
    {"name": "The Left Hand of Darkness", "author": "Ursula K. Le Guin", "release_date": "1969-06-01", "page_count": 304}
    {"name": "The Moon is a Harsh Mistress", "author": "Robert A. Heinlein", "release_date": "1966-04-01", "page_count": 288}

如果请求未遇到错误，您将收到以下结果：

    
    
    {
      "num_lines_analyzed" : 24, __"num_messages_analyzed" : 24, __"sample_start" : "{\"name\": \"Leviathan Wakes\", \"author\": \"James S.A. Corey\", \"release_date\": \"2011-06-02\", \"page_count\": 561}\n{\"name\": \"Hyperion\", \"author\": \"Dan Simmons\", \"release_date\": \"1989-05-26\", \"page_count\": 482}\n", __"charset" : "UTF-8", __"has_byte_order_marker" : false, __"format" : "ndjson", __"ecs_compatibility" : "disabled", __"timestamp_field" : "release_date", __"joda_timestamp_formats" : [ __"ISO8601"
      ],
      "java_timestamp_formats" : [ __"ISO8601"
      ],
      "need_client_timezone" : true, __"mappings" : { __"properties" : {
          "@timestamp" : {
            "type" : "date"
          },
          "author" : {
            "type" : "keyword"
          },
          "name" : {
            "type" : "keyword"
          },
          "page_count" : {
            "type" : "long"
          },
          "release_date" : {
            "type" : "date",
            "format" : "iso8601"
          }
        }
      },
      "ingest_pipeline" : {
        "description" : "Ingest pipeline created by text structure finder",
        "processors" : [
          {
            "date" : {
              "field" : "release_date",
              "timezone" : "{{ event.timezone }}",
              "formats" : [
                "ISO8601"
              ]
            }
          }
        ]
      },
      "field_stats" : { __"author" : {
          "count" : 24,
          "cardinality" : 20,
          "top_hits" : [
            {
              "value" : "Frank Herbert",
              "count" : 4
            },
            {
              "value" : "Robert A. Heinlein",
              "count" : 2
            },
            {
              "value" : "Alastair Reynolds",
              "count" : 1
            },
            {
              "value" : "Aldous Huxley",
              "count" : 1
            },
            {
              "value" : "Dan Simmons",
              "count" : 1
            },
            {
              "value" : "Douglas Adams",
              "count" : 1
            },
            {
              "value" : "George Orwell",
              "count" : 1
            },
            {
              "value" : "Iain M. Banks",
              "count" : 1
            },
            {
              "value" : "Isaac Asimov",
              "count" : 1
            },
            {
              "value" : "James S.A. Corey",
              "count" : 1
            }
          ]
        },
        "name" : {
          "count" : 24,
          "cardinality" : 24,
          "top_hits" : [
            {
              "value" : "1984",
              "count" : 1
            },
            {
              "value" : "A Fire Upon the Deep",
              "count" : 1
            },
            {
              "value" : "Brave New World",
              "count" : 1
            },
            {
              "value" : "Children of Dune",
              "count" : 1
            },
            {
              "value" : "Consider Phlebas",
              "count" : 1
            },
            {
              "value" : "Dune",
              "count" : 1
            },
            {
              "value" : "Dune Messiah",
              "count" : 1
            },
            {
              "value" : "Ender's Game",
              "count" : 1
            },
            {
              "value" : "Fahrenheit 451",
              "count" : 1
            },
            {
              "value" : "Foundation",
              "count" : 1
            }
          ]
        },
        "page_count" : {
          "count" : 24,
          "cardinality" : 24,
          "min_value" : 180,
          "max_value" : 768,
          "mean_value" : 387.0833333333333,
          "median_value" : 329.5,
          "top_hits" : [
            {
              "value" : 180,
              "count" : 1
            },
            {
              "value" : 208,
              "count" : 1
            },
            {
              "value" : 224,
              "count" : 1
            },
            {
              "value" : 227,
              "count" : 1
            },
            {
              "value" : 268,
              "count" : 1
            },
            {
              "value" : 271,
              "count" : 1
            },
            {
              "value" : 275,
              "count" : 1
            },
            {
              "value" : 288,
              "count" : 1
            },
            {
              "value" : 304,
              "count" : 1
            },
            {
              "value" : 311,
              "count" : 1
            }
          ]
        },
        "release_date" : {
          "count" : 24,
          "cardinality" : 20,
          "earliest" : "1932-06-01",
          "latest" : "2011-06-02",
          "top_hits" : [
            {
              "value" : "1985-06-01",
              "count" : 3
            },
            {
              "value" : "1969-06-01",
              "count" : 2
            },
            {
              "value" : "1992-06-01",
              "count" : 2
            },
            {
              "value" : "1932-06-01",
              "count" : 1
            },
            {
              "value" : "1951-06-01",
              "count" : 1
            },
            {
              "value" : "1953-10-15",
              "count" : 1
            },
            {
              "value" : "1959-12-01",
              "count" : 1
            },
            {
              "value" : "1965-06-01",
              "count" : 1
            },
            {
              "value" : "1966-04-01",
              "count" : 1
            },
            {
              "value" : "1969-10-15",
              "count" : 1
            }
          ]
        }
      }
    }

__

|

"num_lines_analyzed"表示分析了多少行文本。   ---|---    __

|

"num_messages_analyzed"表示行包含多少条不同的消息。对于 NDJSON，此值与"num_lines_analyzed"相同。对于其他文本格式，消息可以跨越多行。   __

|

"sample_start"逐字再现文本中的前两条消息。这可能有助于诊断解析错误或意外上传错误文本。   __

|

"charset"表示用于解析文本的字符编码。   __

|

对于 UTF 字符编码，"has_byte_order_marker"指示文本是否以字节顺序标记开头。   __

|

"格式"是"NDJSON"、"XML"、"分隔"或"semi_structured_text"之一。   __

|

"ecs_compatibility"为"禁用"或"v1"，默认为"禁用"。   __

|

"timestamp_field"命名最有可能成为每个文档的主时间戳的字段。   __

|

"joda_timestamp_formats"用于告诉 Logstash 如何解析时间戳。   __

|

"java_timestamp_formats"是在时间字段中识别的 Java 时间格式。Elasticsearch 映射和摄取管道使用此格式。   __

|

如果检测到不包含时区的时间戳格式，则"need_client_timezone"将为"true"。因此，客户端必须告诉解析文本的服务器正确的时区。   __

|

"映射"包含一些适合索引的映射，数据可以摄取到其中。在这种情况下，"release_date"字段被赋予了"关键字"类型，因为它被认为不够具体，无法转换为"日期"类型。   __

|

"field_stats"包含每个字段的最常见值，以及数字"page_count"字段的基本数值统计信息。此信息可能会提供线索，表明在由其他 Elastic Stack 功能使用之前，需要清理或转换数据。   #### 查找纽约市黄色出租车的结构示例数据编辑

下一个示例演示如何查找某些纽约市黄色出租车行程数据的结构。第一个"curl"命令下载数据，然后将前 20000 行数据通过管道传输到"find_structure"端点。终结点的"lines_to_sample"查询参数设置为 20000，以匹配"head"命令中指定的内容。

    
    
    curl -s "s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2018-06.csv" | head -20000 | curl -s -H "Content-Type: application/json" -XPOST "localhost:9200/_text_structure/find_structure?pretty&lines_to_sample=20000" -T -

必须设置"内容类型：应用程序/json"标头，即使在这种情况下数据不是 JSON。(或者，可以将"内容类型"设置为Elasticsearch支持的任何其他内容，但必须进行设置。

如果请求未遇到错误，您将收到以下结果：

    
    
    {
      "num_lines_analyzed" : 20000,
      "num_messages_analyzed" : 19998, __"sample_start" : "VendorID,tpep_pickup_datetime,tpep_dropoff_datetime,passenger_count,trip_distance,RatecodeID,store_and_fwd_flag,PULocationID,DOLocationID,payment_type,fare_amount,extra,mta_tax,tip_amount,tolls_amount,improvement_surcharge,total_amount\n\n1,2018-06-01 00:15:40,2018-06-01 00:16:46,1,.00,1,N,145,145,2,3,0.5,0.5,0,0,0.3,4.3\n",
      "charset" : "UTF-8",
      "has_byte_order_marker" : false,
      "format" : "delimited", __"multiline_start_pattern" : "^.*?,\"?\\d{4}-\\d{2}-\\d{2}[T ]\\d{2}:\\d{2}",
      "exclude_lines_pattern" : "^\"?VendorID\"?,\"?tpep_pickup_datetime\"?,\"?tpep_dropoff_datetime\"?,\"?passenger_count\"?,\"?trip_distance\"?,\"?RatecodeID\"?,\"?store_and_fwd_flag\"?,\"?PULocationID\"?,\"?DOLocationID\"?,\"?payment_type\"?,\"?fare_amount\"?,\"?extra\"?,\"?mta_tax\"?,\"?tip_amount\"?,\"?tolls_amount\"?,\"?improvement_surcharge\"?,\"?total_amount\"?",
      "column_names" : [ __"VendorID",
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
        "passenger_count",
        "trip_distance",
        "RatecodeID",
        "store_and_fwd_flag",
        "PULocationID",
        "DOLocationID",
        "payment_type",
        "fare_amount",
        "extra",
        "mta_tax",
        "tip_amount",
        "tolls_amount",
        "improvement_surcharge",
        "total_amount"
      ],
      "has_header_row" : true, __"delimiter" : ",", __"quote" : "\"", __"timestamp_field" : "tpep_pickup_datetime", __"joda_timestamp_formats" : [ __"YYYY-MM-dd HH:mm:ss"
      ],
      "java_timestamp_formats" : [ __"yyyy-MM-dd HH:mm:ss"
      ],
      "need_client_timezone" : true, __"mappings" : {
        "properties" : {
          "@timestamp" : {
            "type" : "date"
          },
          "DOLocationID" : {
            "type" : "long"
          },
          "PULocationID" : {
            "type" : "long"
          },
          "RatecodeID" : {
            "type" : "long"
          },
          "VendorID" : {
            "type" : "long"
          },
          "extra" : {
            "type" : "double"
          },
          "fare_amount" : {
            "type" : "double"
          },
          "improvement_surcharge" : {
            "type" : "double"
          },
          "mta_tax" : {
            "type" : "double"
          },
          "passenger_count" : {
            "type" : "long"
          },
          "payment_type" : {
            "type" : "long"
          },
          "store_and_fwd_flag" : {
            "type" : "keyword"
          },
          "tip_amount" : {
            "type" : "double"
          },
          "tolls_amount" : {
            "type" : "double"
          },
          "total_amount" : {
            "type" : "double"
          },
          "tpep_dropoff_datetime" : {
            "type" : "date",
            "format" : "yyyy-MM-dd HH:mm:ss"
          },
          "tpep_pickup_datetime" : {
            "type" : "date",
            "format" : "yyyy-MM-dd HH:mm:ss"
          },
          "trip_distance" : {
            "type" : "double"
          }
        }
      },
      "ingest_pipeline" : {
        "description" : "Ingest pipeline created by text structure finder",
        "processors" : [
          {
            "csv" : {
              "field" : "message",
              "target_fields" : [
                "VendorID",
                "tpep_pickup_datetime",
                "tpep_dropoff_datetime",
                "passenger_count",
                "trip_distance",
                "RatecodeID",
                "store_and_fwd_flag",
                "PULocationID",
                "DOLocationID",
                "payment_type",
                "fare_amount",
                "extra",
                "mta_tax",
                "tip_amount",
                "tolls_amount",
                "improvement_surcharge",
                "total_amount"
              ]
            }
          },
          {
            "date" : {
              "field" : "tpep_pickup_datetime",
              "timezone" : "{{ event.timezone }}",
              "formats" : [
                "yyyy-MM-dd HH:mm:ss"
              ]
            }
          },
          {
            "convert" : {
              "field" : "DOLocationID",
              "type" : "long"
            }
          },
          {
            "convert" : {
              "field" : "PULocationID",
              "type" : "long"
            }
          },
          {
            "convert" : {
              "field" : "RatecodeID",
              "type" : "long"
            }
          },
          {
            "convert" : {
              "field" : "VendorID",
              "type" : "long"
            }
          },
          {
            "convert" : {
              "field" : "extra",
              "type" : "double"
            }
          },
          {
            "convert" : {
              "field" : "fare_amount",
              "type" : "double"
            }
          },
          {
            "convert" : {
              "field" : "improvement_surcharge",
              "type" : "double"
            }
          },
          {
            "convert" : {
              "field" : "mta_tax",
              "type" : "double"
            }
          },
          {
            "convert" : {
              "field" : "passenger_count",
              "type" : "long"
            }
          },
          {
            "convert" : {
              "field" : "payment_type",
              "type" : "long"
            }
          },
          {
            "convert" : {
              "field" : "tip_amount",
              "type" : "double"
            }
          },
          {
            "convert" : {
              "field" : "tolls_amount",
              "type" : "double"
            }
          },
          {
            "convert" : {
              "field" : "total_amount",
              "type" : "double"
            }
          },
          {
            "convert" : {
              "field" : "trip_distance",
              "type" : "double"
            }
          },
          {
            "remove" : {
              "field" : "message"
            }
          }
        ]
      },
      "field_stats" : {
        "DOLocationID" : {
          "count" : 19998,
          "cardinality" : 240,
          "min_value" : 1,
          "max_value" : 265,
          "mean_value" : 150.26532653265312,
          "median_value" : 148,
          "top_hits" : [
            {
              "value" : 79,
              "count" : 760
            },
            {
              "value" : 48,
              "count" : 683
            },
            {
              "value" : 68,
              "count" : 529
            },
            {
              "value" : 170,
              "count" : 506
            },
            {
              "value" : 107,
              "count" : 468
            },
            {
              "value" : 249,
              "count" : 457
            },
            {
              "value" : 230,
              "count" : 441
            },
            {
              "value" : 186,
              "count" : 432
            },
            {
              "value" : 141,
              "count" : 409
            },
            {
              "value" : 263,
              "count" : 386
            }
          ]
        },
        "PULocationID" : {
          "count" : 19998,
          "cardinality" : 154,
          "min_value" : 1,
          "max_value" : 265,
          "mean_value" : 153.4042404240424,
          "median_value" : 148,
          "top_hits" : [
            {
              "value" : 79,
              "count" : 1067
            },
            {
              "value" : 230,
              "count" : 949
            },
            {
              "value" : 148,
              "count" : 940
            },
            {
              "value" : 132,
              "count" : 897
            },
            {
              "value" : 48,
              "count" : 853
            },
            {
              "value" : 161,
              "count" : 820
            },
            {
              "value" : 234,
              "count" : 750
            },
            {
              "value" : 249,
              "count" : 722
            },
            {
              "value" : 164,
              "count" : 663
            },
            {
              "value" : 114,
              "count" : 646
            }
          ]
        },
        "RatecodeID" : {
          "count" : 19998,
          "cardinality" : 5,
          "min_value" : 1,
          "max_value" : 5,
          "mean_value" : 1.0656565656565653,
          "median_value" : 1,
          "top_hits" : [
            {
              "value" : 1,
              "count" : 19311
            },
            {
              "value" : 2,
              "count" : 468
            },
            {
              "value" : 5,
              "count" : 195
            },
            {
              "value" : 4,
              "count" : 17
            },
            {
              "value" : 3,
              "count" : 7
            }
          ]
        },
        "VendorID" : {
          "count" : 19998,
          "cardinality" : 2,
          "min_value" : 1,
          "max_value" : 2,
          "mean_value" : 1.59005900590059,
          "median_value" : 2,
          "top_hits" : [
            {
              "value" : 2,
              "count" : 11800
            },
            {
              "value" : 1,
              "count" : 8198
            }
          ]
        },
        "extra" : {
          "count" : 19998,
          "cardinality" : 3,
          "min_value" : -0.5,
          "max_value" : 0.5,
          "mean_value" : 0.4815981598159816,
          "median_value" : 0.5,
          "top_hits" : [
            {
              "value" : 0.5,
              "count" : 19281
            },
            {
              "value" : 0,
              "count" : 698
            },
            {
              "value" : -0.5,
              "count" : 19
            }
          ]
        },
        "fare_amount" : {
          "count" : 19998,
          "cardinality" : 208,
          "min_value" : -100,
          "max_value" : 300,
          "mean_value" : 13.937719771977209,
          "median_value" : 9.5,
          "top_hits" : [
            {
              "value" : 6,
              "count" : 1004
            },
            {
              "value" : 6.5,
              "count" : 935
            },
            {
              "value" : 5.5,
              "count" : 909
            },
            {
              "value" : 7,
              "count" : 903
            },
            {
              "value" : 5,
              "count" : 889
            },
            {
              "value" : 7.5,
              "count" : 854
            },
            {
              "value" : 4.5,
              "count" : 802
            },
            {
              "value" : 8.5,
              "count" : 790
            },
            {
              "value" : 8,
              "count" : 789
            },
            {
              "value" : 9,
              "count" : 711
            }
          ]
        },
        "improvement_surcharge" : {
          "count" : 19998,
          "cardinality" : 3,
          "min_value" : -0.3,
          "max_value" : 0.3,
          "mean_value" : 0.29915991599159913,
          "median_value" : 0.3,
          "top_hits" : [
            {
              "value" : 0.3,
              "count" : 19964
            },
            {
              "value" : -0.3,
              "count" : 22
            },
            {
              "value" : 0,
              "count" : 12
            }
          ]
        },
        "mta_tax" : {
          "count" : 19998,
          "cardinality" : 3,
          "min_value" : -0.5,
          "max_value" : 0.5,
          "mean_value" : 0.4962246224622462,
          "median_value" : 0.5,
          "top_hits" : [
            {
              "value" : 0.5,
              "count" : 19868
            },
            {
              "value" : 0,
              "count" : 109
            },
            {
              "value" : -0.5,
              "count" : 21
            }
          ]
        },
        "passenger_count" : {
          "count" : 19998,
          "cardinality" : 7,
          "min_value" : 0,
          "max_value" : 6,
          "mean_value" : 1.6201620162016201,
          "median_value" : 1,
          "top_hits" : [
            {
              "value" : 1,
              "count" : 14219
            },
            {
              "value" : 2,
              "count" : 2886
            },
            {
              "value" : 5,
              "count" : 1047
            },
            {
              "value" : 3,
              "count" : 804
            },
            {
              "value" : 6,
              "count" : 523
            },
            {
              "value" : 4,
              "count" : 406
            },
            {
              "value" : 0,
              "count" : 113
            }
          ]
        },
        "payment_type" : {
          "count" : 19998,
          "cardinality" : 4,
          "min_value" : 1,
          "max_value" : 4,
          "mean_value" : 1.315631563156316,
          "median_value" : 1,
          "top_hits" : [
            {
              "value" : 1,
              "count" : 13936
            },
            {
              "value" : 2,
              "count" : 5857
            },
            {
              "value" : 3,
              "count" : 160
            },
            {
              "value" : 4,
              "count" : 45
            }
          ]
        },
        "store_and_fwd_flag" : {
          "count" : 19998,
          "cardinality" : 2,
          "top_hits" : [
            {
              "value" : "N",
              "count" : 19910
            },
            {
              "value" : "Y",
              "count" : 88
            }
          ]
        },
        "tip_amount" : {
          "count" : 19998,
          "cardinality" : 717,
          "min_value" : 0,
          "max_value" : 128,
          "mean_value" : 2.010959095909593,
          "median_value" : 1.45,
          "top_hits" : [
            {
              "value" : 0,
              "count" : 6917
            },
            {
              "value" : 1,
              "count" : 1178
            },
            {
              "value" : 2,
              "count" : 624
            },
            {
              "value" : 3,
              "count" : 248
            },
            {
              "value" : 1.56,
              "count" : 206
            },
            {
              "value" : 1.46,
              "count" : 205
            },
            {
              "value" : 1.76,
              "count" : 196
            },
            {
              "value" : 1.45,
              "count" : 195
            },
            {
              "value" : 1.36,
              "count" : 191
            },
            {
              "value" : 1.5,
              "count" : 187
            }
          ]
        },
        "tolls_amount" : {
          "count" : 19998,
          "cardinality" : 26,
          "min_value" : 0,
          "max_value" : 35,
          "mean_value" : 0.2729697969796978,
          "median_value" : 0,
          "top_hits" : [
            {
              "value" : 0,
              "count" : 19107
            },
            {
              "value" : 5.76,
              "count" : 791
            },
            {
              "value" : 10.5,
              "count" : 36
            },
            {
              "value" : 2.64,
              "count" : 21
            },
            {
              "value" : 11.52,
              "count" : 8
            },
            {
              "value" : 5.54,
              "count" : 4
            },
            {
              "value" : 8.5,
              "count" : 4
            },
            {
              "value" : 17.28,
              "count" : 4
            },
            {
              "value" : 2,
              "count" : 2
            },
            {
              "value" : 2.16,
              "count" : 2
            }
          ]
        },
        "total_amount" : {
          "count" : 19998,
          "cardinality" : 1267,
          "min_value" : -100.3,
          "max_value" : 389.12,
          "mean_value" : 17.499898989898995,
          "median_value" : 12.35,
          "top_hits" : [
            {
              "value" : 7.3,
              "count" : 478
            },
            {
              "value" : 8.3,
              "count" : 443
            },
            {
              "value" : 8.8,
              "count" : 420
            },
            {
              "value" : 6.8,
              "count" : 406
            },
            {
              "value" : 7.8,
              "count" : 405
            },
            {
              "value" : 6.3,
              "count" : 371
            },
            {
              "value" : 9.8,
              "count" : 368
            },
            {
              "value" : 5.8,
              "count" : 362
            },
            {
              "value" : 9.3,
              "count" : 332
            },
            {
              "value" : 10.3,
              "count" : 332
            }
          ]
        },
        "tpep_dropoff_datetime" : {
          "count" : 19998,
          "cardinality" : 9066,
          "earliest" : "2018-05-31 06:18:15",
          "latest" : "2018-06-02 02:25:44",
          "top_hits" : [
            {
              "value" : "2018-06-01 01:12:12",
              "count" : 10
            },
            {
              "value" : "2018-06-01 00:32:15",
              "count" : 9
            },
            {
              "value" : "2018-06-01 00:44:27",
              "count" : 9
            },
            {
              "value" : "2018-06-01 00:46:42",
              "count" : 9
            },
            {
              "value" : "2018-06-01 01:03:22",
              "count" : 9
            },
            {
              "value" : "2018-06-01 01:05:13",
              "count" : 9
            },
            {
              "value" : "2018-06-01 00:11:20",
              "count" : 8
            },
            {
              "value" : "2018-06-01 00:16:03",
              "count" : 8
            },
            {
              "value" : "2018-06-01 00:19:47",
              "count" : 8
            },
            {
              "value" : "2018-06-01 00:25:17",
              "count" : 8
            }
          ]
        },
        "tpep_pickup_datetime" : {
          "count" : 19998,
          "cardinality" : 8760,
          "earliest" : "2018-05-31 06:08:31",
          "latest" : "2018-06-02 01:21:21",
          "top_hits" : [
            {
              "value" : "2018-06-01 00:01:23",
              "count" : 12
            },
            {
              "value" : "2018-06-01 00:04:31",
              "count" : 10
            },
            {
              "value" : "2018-06-01 00:05:38",
              "count" : 10
            },
            {
              "value" : "2018-06-01 00:09:50",
              "count" : 10
            },
            {
              "value" : "2018-06-01 00:12:01",
              "count" : 10
            },
            {
              "value" : "2018-06-01 00:14:17",
              "count" : 10
            },
            {
              "value" : "2018-06-01 00:00:34",
              "count" : 9
            },
            {
              "value" : "2018-06-01 00:00:40",
              "count" : 9
            },
            {
              "value" : "2018-06-01 00:02:53",
              "count" : 9
            },
            {
              "value" : "2018-06-01 00:05:40",
              "count" : 9
            }
          ]
        },
        "trip_distance" : {
          "count" : 19998,
          "cardinality" : 1687,
          "min_value" : 0,
          "max_value" : 64.63,
          "mean_value" : 3.6521062106210715,
          "median_value" : 2.16,
          "top_hits" : [
            {
              "value" : 0.9,
              "count" : 335
            },
            {
              "value" : 0.8,
              "count" : 320
            },
            {
              "value" : 1.1,
              "count" : 316
            },
            {
              "value" : 0.7,
              "count" : 304
            },
            {
              "value" : 1.2,
              "count" : 303
            },
            {
              "value" : 1,
              "count" : 296
            },
            {
              "value" : 1.3,
              "count" : 280
            },
            {
              "value" : 1.5,
              "count" : 268
            },
            {
              "value" : 1.6,
              "count" : 268
            },
            {
              "value" : 0.6,
              "count" : 256
            }
          ]
        }
      }
    }

__

|

"num_messages_analyzed"比"num_lines_analyzed"低 2，因为只有数据记录才算作消息。第一行包含列名，在此示例中，第二行为空。   ---|---    __

|

与第一个示例不同，在这种情况下，"格式"已被标识为"分隔"。   __

|

由于"格式"是"分隔的"，因此输出中的"column_names"字段按列名在示例中出现的顺序列出列名。   __

|

"has_header_row"表示对于此示例，列名位于示例的第一行。(如果不是这样，那么在"column_names"查询参数中指定它们是个好主意。   __

|

此示例的"分隔符"是逗号，因为它是 CSV 格式的文本。   __

|

"引号"字符是默认的双引号。(结构查找器不会尝试推断任何其他引号字符，因此，如果您有用其他字符引用的分隔文本，则必须使用"quote"query 参数指定它。   __

|

"timestamp_field"被选为"tpep_pickup_datetime".tpep_dropoff_datetime"也可以正常工作，但选择"tpep_pickup_datetime"是因为它在列顺序中排在第一位。如果您更喜欢"tpep_dropoff_datetime"，请使用"timestamp_field"查询参数强制选择它。   __

|

"joda_timestamp_formats"用于告诉 Logstash 如何解析时间戳。   __

|

"java_timestamp_formats"是在时间字段中识别的 Java 时间格式。Elasticsearch 映射和摄取管道使用此格式。   __

|

此示例中的时间戳格式未指定时区，因此要将它们准确地转换为 UTC 时间戳以存储在 Elasticsearch 中，必须提供它们相关的时区。对于包含时区的时间戳格式，"need_client_timezone"将为"false"。   #### 设置超时参数编辑

如果您尝试分析大量数据，那么分析将需要很长时间。如果要限制 Elasticsearch 集群对请求执行的处理量，请使用"timeout"查询参数。分析将中止，并在超时到期时返回错误。例如，您可以将上一示例中的 20000 行替换为 200000，并在分析中设置 1 秒超时：

    
    
    curl -s "s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2018-06.csv" | head -200000 | curl -s -H "Content-Type: application/json" -XPOST "localhost:9200/_text_structure/find_structure?pretty&lines_to_sample=200000&timeout=1s" -T -

除非您使用的是速度非常快的计算机，否则您将收到超时错误：

    
    
    {
      "error" : {
        "root_cause" : [
          {
            "type" : "timeout_exception",
            "reason" : "Aborting structure analysis during [delimited record parsing] as it has taken longer than the timeout of [1s]"
          }
        ],
        "type" : "timeout_exception",
        "reason" : "Aborting structure analysis during [delimited record parsing] as it has taken longer than the timeout of [1s]"
      },
      "status" : 500
    }

如果您自己尝试上面的示例，您会注意到 'curl' 命令的总运行时间远长于 1 秒。这是因为从互联网下载 200000 行 CSV 需要一段时间，并且超时是从该端点开始处理数据时开始测量的。

#### 分析 Elasticsearch 日志文件

这是分析 Elasticsearch 日志文件的示例：

    
    
    curl -s -H "Content-Type: application/json" -XPOST
    "localhost:9200/_text_structure/find_structure?pretty&ecs_compatibility=disabled" -T "$ES_HOME/logs/elasticsearch.log"

如果请求未遇到错误，结果将如下所示：

    
    
    {
      "num_lines_analyzed" : 53,
      "num_messages_analyzed" : 53,
      "sample_start" : "[2018-09-27T14:39:28,518][INFO ][o.e.e.NodeEnvironment    ] [node-0] using [1] data paths, mounts [[/ (/dev/disk1)]], net usable_space [165.4gb], net total_space [464.7gb], types [hfs]\n[2018-09-27T14:39:28,521][INFO ][o.e.e.NodeEnvironment    ] [node-0] heap size [494.9mb], compressed ordinary object pointers [true]\n",
      "charset" : "UTF-8",
      "has_byte_order_marker" : false,
      "format" : "semi_structured_text", __"multiline_start_pattern" : "^\\[\\b\\d{4}-\\d{2}-\\d{2}[T ]\\d{2}:\\d{2}", __"grok_pattern" : "\\[%{TIMESTAMP_ISO8601:timestamp}\\]\\[%{LOGLEVEL:loglevel}.*", __"ecs_compatibility" : "disabled", __"timestamp_field" : "timestamp",
      "joda_timestamp_formats" : [
        "ISO8601"
      ],
      "java_timestamp_formats" : [
        "ISO8601"
      ],
      "need_client_timezone" : true,
      "mappings" : {
        "properties" : {
          "@timestamp" : {
            "type" : "date"
          },
          "loglevel" : {
            "type" : "keyword"
          },
          "message" : {
            "type" : "text"
          }
        }
      },
      "ingest_pipeline" : {
        "description" : "Ingest pipeline created by text structure finder",
        "processors" : [
          {
            "grok" : {
              "field" : "message",
              "patterns" : [
                "\\[%{TIMESTAMP_ISO8601:timestamp}\\]\\[%{LOGLEVEL:loglevel}.*"
              ]
            }
          },
          {
            "date" : {
              "field" : "timestamp",
              "timezone" : "{{ event.timezone }}",
              "formats" : [
                "ISO8601"
              ]
            }
          },
          {
            "remove" : {
              "field" : "timestamp"
            }
          }
        ]
      },
      "field_stats" : {
        "loglevel" : {
          "count" : 53,
          "cardinality" : 3,
          "top_hits" : [
            {
              "value" : "INFO",
              "count" : 51
            },
            {
              "value" : "DEBUG",
              "count" : 1
            },
            {
              "value" : "WARN",
              "count" : 1
            }
          ]
        },
        "timestamp" : {
          "count" : 53,
          "cardinality" : 28,
          "earliest" : "2018-09-27T14:39:28,518",
          "latest" : "2018-09-27T14:39:37,012",
          "top_hits" : [
            {
              "value" : "2018-09-27T14:39:29,859",
              "count" : 10
            },
            {
              "value" : "2018-09-27T14:39:29,860",
              "count" : 9
            },
            {
              "value" : "2018-09-27T14:39:29,858",
              "count" : 6
            },
            {
              "value" : "2018-09-27T14:39:28,523",
              "count" : 3
            },
            {
              "value" : "2018-09-27T14:39:34,234",
              "count" : 2
            },
            {
              "value" : "2018-09-27T14:39:28,518",
              "count" : 1
            },
            {
              "value" : "2018-09-27T14:39:28,521",
              "count" : 1
            },
            {
              "value" : "2018-09-27T14:39:28,522",
              "count" : 1
            },
            {
              "value" : "2018-09-27T14:39:29,861",
              "count" : 1
            },
            {
              "value" : "2018-09-27T14:39:32,786",
              "count" : 1
            }
          ]
        }
      }
    }

__

|

这次"格式"被标识为"semi_structured_text"。   ---|---    __

|

"multiline_start_pattern"是根据时间戳出现在每个多行日志消息的第一行来设置的。   __

|

创建了一个非常简单的"grok_pattern"，它提取出现在每条分析消息中的时间戳和可识别字段。在这种情况下，时间戳之外唯一被识别的字段是日志级别。   __

|

使用的 ECS Grok 模式兼容模式可以是"禁用"(如果未在请求中指定则为默认值)或"v1"之一 #### 指定"grok_pattern"作为查询参数编辑

如果您识别的字段多于结构查找器独立生成的简单"grok_pattern"，则可以重新提交请求，指定更高级的"grok_pattern"作为查询参数，结构查找器将计算"field_stats"的其他字段。

在 Elasticsearch log 的情况下，更完整的 Grok 模式是'\[%{TIMESTAMP_ISO8601：timestamp}\]\[%{LOGLEVEL：loglevel}*\]\[%{JAVACLASS：class} *\] \[%{HOSTNAME：node}\] %{JAVALOGMESSAGE：message}'.您可以再次分析相同的文本，将此"grok_pattern"作为查询参数提交(适当地对URL进行转义)：

    
    
    curl -s -H "Content-Type: application/json" -XPOST "localhost:9200/_text_structure/find_structure?pretty&format=semi_structured_text&grok_pattern=%5C%5B%25%7BTIMESTAMP_ISO8601:timestamp%7D%5C%5D%5C%5B%25%7BLOGLEVEL:loglevel%7D%20*%5C%5D%5C%5B%25%7BJAVACLASS:class%7D%20*%5C%5D%20%5C%5B%25%7BHOSTNAME:node%7D%5C%5D%20%25%7BJAVALOGMESSAGE:message%7D" -T "$ES_HOME/logs/elasticsearch.log"

如果请求未遇到错误，结果将如下所示：

    
    
    {
      "num_lines_analyzed" : 53,
      "num_messages_analyzed" : 53,
      "sample_start" : "[2018-09-27T14:39:28,518][INFO ][o.e.e.NodeEnvironment    ] [node-0] using [1] data paths, mounts [[/ (/dev/disk1)]], net usable_space [165.4gb], net total_space [464.7gb], types [hfs]\n[2018-09-27T14:39:28,521][INFO ][o.e.e.NodeEnvironment    ] [node-0] heap size [494.9mb], compressed ordinary object pointers [true]\n",
      "charset" : "UTF-8",
      "has_byte_order_marker" : false,
      "format" : "semi_structured_text",
      "multiline_start_pattern" : "^\\[\\b\\d{4}-\\d{2}-\\d{2}[T ]\\d{2}:\\d{2}",
      "grok_pattern" : "\\[%{TIMESTAMP_ISO8601:timestamp}\\]\\[%{LOGLEVEL:loglevel} *\\]\\[%{JAVACLASS:class} *\\] \\[%{HOSTNAME:node}\\] %{JAVALOGMESSAGE:message}", __"ecs_compatibility" : "disabled", __"timestamp_field" : "timestamp",
      "joda_timestamp_formats" : [
        "ISO8601"
      ],
      "java_timestamp_formats" : [
        "ISO8601"
      ],
      "need_client_timezone" : true,
      "mappings" : {
        "properties" : {
          "@timestamp" : {
            "type" : "date"
          },
          "class" : {
            "type" : "keyword"
          },
          "loglevel" : {
            "type" : "keyword"
          },
          "message" : {
            "type" : "text"
          },
          "node" : {
            "type" : "keyword"
          }
        }
      },
      "ingest_pipeline" : {
        "description" : "Ingest pipeline created by text structure finder",
        "processors" : [
          {
            "grok" : {
              "field" : "message",
              "patterns" : [
                "\\[%{TIMESTAMP_ISO8601:timestamp}\\]\\[%{LOGLEVEL:loglevel} *\\]\\[%{JAVACLASS:class} *\\] \\[%{HOSTNAME:node}\\] %{JAVALOGMESSAGE:message}"
              ]
            }
          },
          {
            "date" : {
              "field" : "timestamp",
              "timezone" : "{{ event.timezone }}",
              "formats" : [
                "ISO8601"
              ]
            }
          },
          {
            "remove" : {
              "field" : "timestamp"
            }
          }
        ]
      },
      "field_stats" : { __"class" : {
          "count" : 53,
          "cardinality" : 14,
          "top_hits" : [
            {
              "value" : "o.e.p.PluginsService",
              "count" : 26
            },
            {
              "value" : "o.e.c.m.MetadataIndexTemplateService",
              "count" : 8
            },
            {
              "value" : "o.e.n.Node",
              "count" : 7
            },
            {
              "value" : "o.e.e.NodeEnvironment",
              "count" : 2
            },
            {
              "value" : "o.e.a.ActionModule",
              "count" : 1
            },
            {
              "value" : "o.e.c.s.ClusterApplierService",
              "count" : 1
            },
            {
              "value" : "o.e.c.s.MasterService",
              "count" : 1
            },
            {
              "value" : "o.e.d.DiscoveryModule",
              "count" : 1
            },
            {
              "value" : "o.e.g.GatewayService",
              "count" : 1
            },
            {
              "value" : "o.e.l.LicenseService",
              "count" : 1
            }
          ]
        },
        "loglevel" : {
          "count" : 53,
          "cardinality" : 3,
          "top_hits" : [
            {
              "value" : "INFO",
              "count" : 51
            },
            {
              "value" : "DEBUG",
              "count" : 1
            },
            {
              "value" : "WARN",
              "count" : 1
            }
          ]
        },
        "message" : {
          "count" : 53,
          "cardinality" : 53,
          "top_hits" : [
            {
              "value" : "Using REST wrapper from plugin org.elasticsearch.xpack.security.Security",
              "count" : 1
            },
            {
              "value" : "adding template [.monitoring-alerts] for index patterns [.monitoring-alerts-6]",
              "count" : 1
            },
            {
              "value" : "adding template [.monitoring-beats] for index patterns [.monitoring-beats-6-*]",
              "count" : 1
            },
            {
              "value" : "adding template [.monitoring-es] for index patterns [.monitoring-es-6-*]",
              "count" : 1
            },
            {
              "value" : "adding template [.monitoring-kibana] for index patterns [.monitoring-kibana-6-*]",
              "count" : 1
            },
            {
              "value" : "adding template [.monitoring-logstash] for index patterns [.monitoring-logstash-6-*]",
              "count" : 1
            },
            {
              "value" : "adding template [.triggered_watches] for index patterns [.triggered_watches*]",
              "count" : 1
            },
            {
              "value" : "adding template [.watch-history-9] for index patterns [.watcher-history-9*]",
              "count" : 1
            },
            {
              "value" : "adding template [.watches] for index patterns [.watches*]",
              "count" : 1
            },
            {
              "value" : "starting ...",
              "count" : 1
            }
          ]
        },
        "node" : {
          "count" : 53,
          "cardinality" : 1,
          "top_hits" : [
            {
              "value" : "node-0",
              "count" : 53
            }
          ]
        },
        "timestamp" : {
          "count" : 53,
          "cardinality" : 28,
          "earliest" : "2018-09-27T14:39:28,518",
          "latest" : "2018-09-27T14:39:37,012",
          "top_hits" : [
            {
              "value" : "2018-09-27T14:39:29,859",
              "count" : 10
            },
            {
              "value" : "2018-09-27T14:39:29,860",
              "count" : 9
            },
            {
              "value" : "2018-09-27T14:39:29,858",
              "count" : 6
            },
            {
              "value" : "2018-09-27T14:39:28,523",
              "count" : 3
            },
            {
              "value" : "2018-09-27T14:39:34,234",
              "count" : 2
            },
            {
              "value" : "2018-09-27T14:39:28,518",
              "count" : 1
            },
            {
              "value" : "2018-09-27T14:39:28,521",
              "count" : 1
            },
            {
              "value" : "2018-09-27T14:39:28,522",
              "count" : 1
            },
            {
              "value" : "2018-09-27T14:39:29,861",
              "count" : 1
            },
            {
              "value" : "2018-09-27T14:39:32,786",
              "count" : 1
            }
          ]
        }
      }
    }

__

|

输出中的"grok_pattern"现在是查询参数中提供的被覆盖的。   ---|---    __

|

使用的 ECS Grok 模式兼容模式可以是"禁用"(如果未在请求中指定则为默认值)或"v1"__

|

返回的"field_stats"包括被覆盖的"grok_pattern"中的字段条目。   URL 转义很难，因此如果您正在交互式工作，最好使用 UI！

[« Fleet multi search API](fleet-multi-search.md) [Graph explore API
»](graph-explore-api.md)
