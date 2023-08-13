

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[EQL APIs](eql-apis.md)

[« Delete async EQL search API](delete-async-eql-search-api.md) [Get async
EQL search API »](get-async-eql-search-api.md)

## EQL 搜索接口

返回事件查询语言 (EQL) 查询的搜索结果。

EQL 假定数据流或索引中的每个文档都对应一个事件。

    
    
    response = client.eql.search(
      index: 'my-data-stream',
      body: {
        query: "\n    process where process.name == \"regsvr32.exe\"\n  "
      }
    )
    puts response
    
    
    GET /my-data-stream/_eql/search
    {
      "query": """
        process where process.name == "regsvr32.exe"
      """
    }

###Request

'获取 /<target>/_eql/搜索'

"发布/<target>/_eql/搜索"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"读取"索引权限。  * 请参阅必填字段。  * 预览] 此功能处于技术预览状态，可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持约束。 对于跨集群搜索，如果本地和远程集群的版本低于 7.17.7(含)或低于 8.5.1(含)，则必须使用相同的 Elasticsearch 版本。有关安全性，请参阅 [配置具有安全性的远程群集。

####Limitations

请参阅 EQL 限制。

### 路径参数

`<target>`

    

(必需，字符串)数据流、索引或别名的逗号分隔列表，用于限制请求。支持通配符 ("*")。要搜索所有数据流和索引，请使用"*"或"_all"。

preview] 此功能处于技术预览状态，可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。 要搜索远程群集，请使用"<cluster>："<target>语法。请参阅[跨集群运行 EQL 搜索。

### 查询参数

`allow_no_indices`

    

(可选，布尔值)

此参数的行为不同于其他多目标 API 中使用的"allow_no_indices"参数。

如果为"false"，则当任何通配符模式、别名或"_all"值仅针对缺失或关闭的索引时，请求将返回错误。即使请求以其他打开的索引为目标，此行为也适用。例如，如果索引以"foo"开头，但 noindex 以"bar"开头，则请求目标 'foo*，bar*' 将返回错误。

如果为"true"，则只有专门针对缺失或关闭索引的请求才会返回错误。例如，如果索引以"foo"开头，但没有索引以"bar"开头，则以"foo*，bar*"为目标的请求不会返回错误。但是，仅针对"bar*"的请求仍会返回错误。

默认为"真"。

`ccs_minimize_roundtrips`

    

(可选，布尔值)如果为"true"，则在运行跨集群搜索 (CCS) 请求时，本地集群和远程集群之间的网络往返将最小化。

此选项对于以完全包含在一个远程群集中的数据为目标的请求有效;当数据分布在多个群集中时，将忽略该设置。

默认为"真"。

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

默认为"打开"。

`filter_path`

     (Optional, string) Comma-separated list of filters for the API response. See [Response Filtering](common-options.html#common-options-response-filtering "Response Filtering"). 
`ignore_unavailable`

     (Optional, Boolean) If `false`, the request returns an error if it targets a missing or closed index. Defaults to `true`. 
`keep_alive`

    

(可选，时间值)搜索及其结果在群集上的存储周期。默认为"5d"(五天)。

当此期限到期时，搜索及其结果将被删除，即使搜索仍在进行中。

如果 'keep_on_completion' 参数为 'false'，则 Elasticsearch 仅存储未在 'wait_for_completion_timeout' 参数设置的时间段内完成的异步搜索，无论此值如何。

您还可以使用"keep_alive"请求正文参数指定此值。如果同时指定了这两个参数，则仅使用查询参数。

`keep_on_completion`

    

(可选，布尔值)如果为"true"，则搜索及其结果存储在群集上。

如果为 'false'，则仅当请求在 'wait_for_completion_timeout' 参数设置的时间段内未完成时，搜索及其结果才会存储在集群上。默认为"假"。

还可以使用"keep_on_completion"请求正文参数指定此值。如果同时指定了这两个参数，则仅使用查询参数。

`wait_for_completion_timeout`

    

(可选，时间值)等待请求完成的超时持续时间。默认为无超时，表示请求等待完整的搜索结果。

如果指定了该参数，且在此期间请求完成，则返回完整的搜索结果。

如果请求在此期间未完成，则搜索将变为异步搜索。

您还可以使用"wait_for_completion_timeout"请求正文参数指定此值。如果同时指定了这两个参数，则仅使用查询参数。

### 请求正文

`event_category_field`

    

(必填*，字符串)包含事件分类的字段，例如"进程"、"文件"或"网络"。

默认为弹性云服务器(ECS)中定义的"event.category"。如果数据流或索引不包含"event.category"字段，则此值是必需的。

事件类别字段必须映射为"关键字"系列中的字段类型。

`fetch_size`

    

(可选，整数)一次要为序列查询搜索的最大事件数。默认为"1000"。

此值必须大于"2"，但不能超过"index.max_result_window"设置的值，该值默认为"10000"。

在内部，序列查询提取和分页事件集以搜索匹配项。此参数控制这些集的大小。此参数不限制搜索的事件总数或返回的匹配事件数。

较大的"fetch_size"值通常会提高搜索速度，但会占用更多内存。

`fields`

    

(可选，字符串和对象的数组)字段模式数组。请求返回与响应的"hits.fields"属性中的这些模式匹配的字段名称的值。

可以将数组中的项指定为字符串或对象。请参阅"字段"选项。

"字段"对象的属性

`field`

     (Required, string) Field to return. Supports wildcards (`*`). 
`format`

    

(可选，字符串)日期和地理空间字段的格式。其他字段数据类型不支持此参数。

"日期"和"date_nanos"字段接受日期格式。"geo_point"和"geo_shape"字段接受：

"geojson"(默认)

     [GeoJSON](http://www.geojson.org)
`wkt`

     [Well Known Text](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry)
`mvt(<spec>)`

    

二进制地图框矢量图块。API 将磁贴作为 base64 编码的字符串返回。""<spec>的格式为"//<zoom><x><y>"，带有两个可选的后缀："@<extent>"和/或"："<buffer>。例如，"2/0/1"或"2/0/1@4096：5"。

"MVT"参数

`<zoom>`

     (Required, integer) Zoom level for the tile. Accepts `0`-`29`. 
`<x>`

     (Required, integer) X coordinate for the tile. 
`<y>`

     (Required, integer) Y coordinate for the tile. 
`<extent>`

     (Optional, integer) Size, in pixels, of a side of the tile. Vector tiles are square with equal sides. Defaults to `4096`. 
`<buffer>`

     (Optional, integer) Size, in pixels, of a clipping buffer outside the tile. This allows renderers to avoid outline artifacts from geometries that extend past the extent of the tile. Defaults to `5`. 

`filter`

     (Optional, [Query DSL object](query-dsl.html "Query DSL")) Query, written in Query DSL, used to filter the events on which the EQL query runs. 
`keep_alive`

    

(可选，时间值)搜索及其结果在群集上的存储周期。默认为"5d"(五天)。

当此期限到期时，搜索及其结果将被删除，即使搜索仍在进行中。

如果 'keep_on_completion' 参数为 'false'，则 Elasticsearch 仅存储未在 'wait_for_completion_timeout' 参数设置的时间段内完成的异步搜索，无论此值如何。

您还可以使用"keep_alive"查询参数指定此值。如果同时指定了这两个参数，则仅使用查询参数。

`keep_on_completion`

    

(可选，布尔值)如果为"true"，则搜索及其结果存储在群集上。

如果为 'false'，则仅当请求在 'wait_for_completion_timeout' 参数设置的时间段内未完成时，搜索及其结果才会存储在集群上。默认为"假"。

您还可以使用"keep_on_completion"查询参数指定此值。如果同时指定了这两个参数，则仅使用查询参数。

`query`

     (Required, string) [EQL](eql-syntax.html "EQL syntax reference") query you wish to run. 
`result_position`

    

(可选，枚举)要返回的匹配事件或序列集。

"result_position"的有效值

`tail`

     (Default) Return the most recent matches, similar to the [Unix tail command](https://en.wikipedia.org/wiki/Tail_\(Unix\)). 
`head`

     Return the earliest matches, similar to the [Unix head command](https://en.wikipedia.org/wiki/Head_\(Unix\)). 

此参数可能会更改返回的命中集。但是，它不会更改响应中命中的排序顺序。

`runtime_mappings`

    

(可选，对象的对象)在搜索请求中定义一个或多个运行时字段。这些字段优先于具有相同名称的映射字段。

"runtime_mappings"对象的属性

`<field-name>`

    

(必填，对象)运行时字段的配置。键是字段名称。

""的属性<field-name>

`type`

    

(必需，字符串)字段类型，可以是以下任何一种：

* "布尔值" * "复合" * "日期" * "双精度" * "geo_point" * "IP" * "关键字" * "长" * "查找"

`script`

    

(可选，字符串)查询时执行的无痛脚本。该脚本可以访问文档的整个上下文，包括原始"_source"和任何映射字段及其值。

此脚本必须包含"emit"以返回计算值。例如：

    
    
    "script": "emit(doc['@timestamp'].value.dayOfWeekEnum.toString())"

`size`

    

(可选、整数或浮点数)对于基本查询，要返回的最大匹配事件数。

对于序列查询，要返回的最大匹配序列数。

默认为"10"。此值必须大于"0"。

不能使用管道(如"头"或"尾")超过此值。

`tiebreaker_field`

     (Optional, string) Field used to sort hits with the same [timestamp](eql-search-api.html#eql-search-api-timestamp-field) in ascending order. See [Specify a sort tiebreaker](eql.html#eql-search-specify-a-sort-tiebreaker "Specify a sort tiebreaker"). 

`timestamp_field`

    

(必填*，字符串)包含事件时间戳的字段。

默认为弹性云服务器(ECS)中定义的"@timestamp"。如果数据流或索引不包含"@timestamp"字段，则此值是必需的。

API 响应中的事件按此字段的值排序，自 Unix 纪元以来按升序转换为毫秒。

时间戳字段应映射为"日期"。不支持"date_nanos"字段类型。

`wait_for_completion_timeout`

    

(可选，时间值)等待请求完成的超时持续时间。默认为无超时，表示请求等待完整的搜索结果。

如果指定了该参数，且在此期间请求完成，则返回完整的搜索结果。

如果请求在此期间未完成，则搜索将变为异步搜索。

您还可以使用"wait_for_completion_timeout"查询参数指定此值。如果同时指定了这两个参数，则仅使用查询参数。

### 响应正文

`id`

    

(字符串)搜索的标识符。

仅当满足以下条件之一时，才提供此搜索 ID：

* 搜索请求在"wait_for_completion_timeout"参数的超时期限内不返回完整结果，成为异步搜索。  * 搜索请求的"keep_on_completion"参数为"true"。

可以将此 ID 与获取异步 EQL 搜索 API 一起使用，以获取搜索的当前状态和可用结果，或获取异步 EQL 状态 API 以仅获取当前状态。

`is_partial`

     (Boolean) If `true`, the response does not contain complete search results. 
`is_running`

    

(布尔值)如果为"true"，则搜索请求仍在执行。

如果此参数和"is_partial"参数为"true"，则搜索是正在进行的异步搜索。如果"keep_alive"期限未过，则搜索完成后将提供完整的搜索结果。

如果"is_partial"为"真"，但"is_running"为"假"，则搜索将返回部分结果，因为失败。只有一些分片返回结果或协调搜索的节点失败。

`took`

    

(整数)Elasticsearch 执行请求所花费的毫秒数。

此值是通过测量从协调节点上收到请求到协调节点准备好发送响应的时间之间经过的时间来计算的。

花费的时间包括：

* 协调节点和数据节点之间的通信时间 * 请求在"搜索"线程池中等待执行的时间 * 实际执行时间

花费的时间**不包括**包括：

* 将请求发送到 Elasticsearch 所需的时间 * 序列化 JSON 响应所需的时间 * 将响应发送到客户端所需的时间

`timed_out`

     (Boolean) If `true`, the request timed out before completion. 
`hits`

    

(对象)包含匹配的事件和序列。还包含相关元数据。

"命中"的属性

`total`

    

(对象)有关匹配事件或序列数的元数据。

"总计"的属性

`value`

    

(整数)对于基本查询，为匹配事件的总数。

对于序列查询，为匹配序列的总数。

`relation`

    

(字符串)指示返回的事件或序列数是准确的还是下限。

返回的值为：

`eq`

     Accurate 
`gte`

     Lower bound, including returned events or sequences 

`sequences`

    

(对象数组)包含与查询匹配的事件序列。每个对象表示一个匹配的序列。仅对包含序列的 EQL查询返回此参数。

"序列"对象的属性

`join_keys`

     (array of values) Shared field values used to constrain matches in the sequence. These are defined using the [`by` keyword](eql-syntax.html#eql-sequences "Sequences") in the EQL query syntax. 
`events`

    

(对象数组)包含与查询匹配的事件。每个对象表示一个匹配事件。

"事件"对象的属性

`_index`

     (string) Name of the index containing the event. 
`_id`

     (string) Unique identifier for the event. This ID is only unique within the index. 
`_source`

     (object) Original JSON body passed for the event at index time. 

`events`

    

(对象数组)包含与查询匹配的事件。每个对象表示一个匹配事件。

"事件"对象的属性

`_index`

     (string) Name of the index containing the event. 
`_id`

     (string) (string) Unique identifier for the event. This ID is only unique within the index. 
`_source`

     (object) Original JSON body passed for the event at index time. 

###Examples

#### 基本查询示例

以下 EQL 搜索请求搜索具有"事件.类别"的"进程"且满足以下条件的事件：

* "cmd.exe"的"process.name" * "2013"以外的"process.pid"

    
    
    response = client.eql.search(
      index: 'my-data-stream',
      body: {
        query: "\n    process where (process.name == \"cmd.exe\" and process.pid != 2013)\n  "
      }
    )
    puts response
    
    
    GET /my-data-stream/_eql/search
    {
      "query": """
        process where (process.name == "cmd.exe" and process.pid != 2013)
      """
    }

API 返回以下响应。"hits.events"属性中的匹配事件按时间戳排序，按升序转换为自Unixepoch以来的毫秒。

如果两个或多个事件共享相同的时间戳，则"tiebreaker_field"字段用于按升序对事件进行排序。

    
    
    {
      "is_partial": false,
      "is_running": false,
      "took": 6,
      "timed_out": false,
      "hits": {
        "total": {
          "value": 2,
          "relation": "eq"
        },
        "events": [
          {
            "_index": ".ds-my-data-stream-2099.12.07-000001",
            "_id": "babI3XMBI9IjHuIqU0S_",
            "_source": {
              "@timestamp": "2099-12-06T11:04:05.000Z",
              "event": {
                "category": "process",
                "id": "edwCRnyD",
                "sequence": 1
              },
              "process": {
                "pid": 2012,
                "name": "cmd.exe",
                "executable": "C:\\Windows\\System32\\cmd.exe"
              }
            }
          },
          {
            "_index": ".ds-my-data-stream-2099.12.07-000001",
            "_id": "b6bI3XMBI9IjHuIqU0S_",
            "_source": {
              "@timestamp": "2099-12-07T11:06:07.000Z",
              "event": {
                "category": "process",
                "id": "cMyt5SZ2",
                "sequence": 3
              },
              "process": {
                "pid": 2012,
                "name": "cmd.exe",
                "executable": "C:\\Windows\\System32\\cmd.exe"
              }
            }
          }
        ]
      }
    }

#### 序列查询示例

以下 EQL 搜索请求匹配以下事件序列：

1. 从以下事件开始：

    * An `event.category` of `file`
    * A `file.name` of `cmd.exe`
    * An `process.pid` other than `2013`

2. 之后是以下活动：

    * An `event.category` of `process`
    * A `process.executable` that contains the substring `regsvr32`

这些事件还必须共享相同的"process.pid"值。

    
    
    response = client.eql.search(
      index: 'my-data-stream',
      body: {
        query: "\n    sequence by process.pid\n      [ file where file.name == \"cmd.exe\" and process.pid != 2013 ]\n      [ process where stringContains(process.executable, \"regsvr32\") ]\n  "
      }
    )
    puts response
    
    
    GET /my-data-stream/_eql/search
    {
      "query": """
        sequence by process.pid
          [ file where file.name == "cmd.exe" and process.pid != 2013 ]
          [ process where stringContains(process.executable, "regsvr32") ]
      """
    }

API 返回以下响应。匹配序列包含在"hits.sequences"属性中。"hits.sequences.join_keys"属性包含每个匹配事件的共享"process.pid"值。

    
    
    {
      "is_partial": false,
      "is_running": false,
      "took": 6,
      "timed_out": false,
      "hits": {
        "total": {
          "value": 1,
          "relation": "eq"
        },
        "sequences": [
          {
            "join_keys": [
              2012
            ],
            "events": [
              {
                "_index": ".ds-my-data-stream-2099.12.07-000001",
                "_id": "AtOJ4UjUBAAx3XR5kcCM",
                "_source": {
                  "@timestamp": "2099-12-06T11:04:07.000Z",
                  "event": {
                    "category": "file",
                    "id": "dGCHwoeS",
                    "sequence": 2
                  },
                  "file": {
                    "accessed": "2099-12-07T11:07:08.000Z",
                    "name": "cmd.exe",
                    "path": "C:\\Windows\\System32\\cmd.exe",
                    "type": "file",
                    "size": 16384
                  },
                  "process": {
                    "pid": 2012,
                    "name": "cmd.exe",
                    "executable": "C:\\Windows\\System32\\cmd.exe"
                  }
                }
              },
              {
                "_index": ".ds-my-data-stream-2099.12.07-000001",
                "_id": "OQmfCaduce8zoHT93o4H",
                "_source": {
                  "@timestamp": "2099-12-07T11:07:09.000Z",
                  "event": {
                    "category": "process",
                    "id": "aR3NWVOs",
                    "sequence": 4
                  },
                  "process": {
                    "pid": 2012,
                    "name": "regsvr32.exe",
                    "command_line": "regsvr32.exe  /s /u /i:https://...RegSvr32.sct scrobj.dll",
                    "executable": "C:\\Windows\\System32\\regsvr32.exe"
                  }
                }
              }
            ]
          }
        ]
      }
    }

[« Delete async EQL search API](delete-async-eql-search-api.md) [Get async
EQL search API »](get-async-eql-search-api.md)
