

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md)

[« API conventions](api-conventions.md) [REST API compatibility »](rest-api-
compatibility.md)

## 常用选项

所有 Elasticsearch REST API 都支持以下选项。

### 漂亮结果

当将"？pretty=true"附加到任何请求时，返回的JSON将非常格式化(仅用于调试！另一种选择是设置'？format=yaml'，这将导致结果以(有时)更具可读性的yaml格式返回。

### 人类可读输出

统计信息以适合人类(例如"exists_time"："1h"或"大小"："1kb"")和计算机(例如""exists_time_in_millis"：3600000"或"size_in_bytes"：1024")的格式返回。可以通过向查询字符串添加"？human=false"来关闭人类可读值。当统计结果被监控工具使用而不是供人类使用时，这是有道理的。"人类"标志的默认值为"假"。

### 日期数学

大多数接受格式化日期值的参数(例如"gt"和"lt"in 'range' 查询，或"daterange' 聚合中的 'from' 和 'to' — 都能理解日期数学。

表达式以锚定日期开头，定位日期可以是"now"，也可以是以"||`.可以选择此定位日期后跟一个或多个数学表达式：

* "+1h"：加一小时 * "-1d"：减去一天 * "/d"：向下舍入到最接近的日期

支持的时间单位与持续时间的时间单位支持的时间单位不同。支持的单位包括：

`y`

|

年份 ---|--- 'M'

|

月'w'

|

周 'd'

|

天 'h'

|

小时 'H'

|

小时 'm'

|

分钟's'

|

秒 假设"now"是"2001-01-01 12：00：00"，一些示例如下：

`now+1h`

|

"现在"以毫秒加一小时为单位。解析为： '2001-01-01 13：00：00' ---|--- 'now-1h'

|

"现在"以毫秒减去一小时为单位。解析为： '2001-01-01 11：00：00' '现在-1h/d'

|

"now"以毫秒减去一小时为单位，向下舍入为 UTC 00：00。解析为："2001-01-01 00：00：00" '2001.02.01\|\|+1M/d'

|

"2001-02-01"以毫秒加一个月为单位。解析为："2001-03-0100：00：00" ### 响应筛选编辑

所有 REST API 都接受一个"filter_path"参数，该参数可用于减少 Elasticsearch 返回的响应。此参数采用逗号分隔的过滤器列表，以点表示法表示：

    
    
    response = client.search(
      q: 'kimchy',
      filter_path: 'took,hits.hits._id,hits.hits._score'
    )
    puts response
    
    
    GET /_search?q=kimchy&filter_path=took,hits.hits._id,hits.hits._score

Responds:

    
    
    {
      "took" : 3,
      "hits" : {
        "hits" : [
          {
            "_id" : "0",
            "_score" : 1.6375021
          }
        ]
      }
    }

它还支持"*"通配符来匹配任何字段或字段名称的一部分：

    
    
    $response = $client->cluster()->state();
    
    
    resp = client.cluster.state(filter_path="metadata.indices.*.stat*")
    print(resp)
    
    
    response = client.cluster.state(
      filter_path: 'metadata.indices.*.stat*'
    )
    puts response
    
    
    res, err := es.Cluster.State(
    	es.Cluster.State.WithFilterPath("metadata.indices.*.stat*"),
    )
    fmt.Println(res, err)
    
    
    const response = await client.cluster.state({
      filter_path: 'metadata.indices.*.stat*'
    })
    console.log(response)
    
    
    GET /_cluster/state?filter_path=metadata.indices.*.stat*

Responds:

    
    
    {
      "metadata" : {
        "indices" : {
          "my-index-000001": {"state": "open"}
        }
      }
    }

"**"通配符可用于包含字段，而无需知道字段的确切路径。例如，我们可以使用此请求返回每个分片的状态：

    
    
    $response = $client->cluster()->state();
    
    
    resp = client.cluster.state(filter_path="routing_table.indices.**.state")
    print(resp)
    
    
    response = client.cluster.state(
      filter_path: 'routing_table.indices.**.state'
    )
    puts response
    
    
    res, err := es.Cluster.State(
    	es.Cluster.State.WithFilterPath("routing_table.indices.**.state"),
    )
    fmt.Println(res, err)
    
    
    const response = await client.cluster.state({
      filter_path: 'routing_table.indices.**.state'
    })
    console.log(response)
    
    
    GET /_cluster/state?filter_path=routing_table.indices.**.state

Responds:

    
    
    {
      "routing_table": {
        "indices": {
          "my-index-000001": {
            "shards": {
              "0": [{"state": "STARTED"}, {"state": "UNASSIGNED"}]
            }
          }
        }
      }
    }

也可以通过在过滤器前面加上字符"-"来排除一个或多个字段：

    
    
    $response = $client->count();
    
    
    resp = client.count(filter_path="-_shards")
    print(resp)
    
    
    response = client.count(
      filter_path: '-_shards'
    )
    puts response
    
    
    res, err := es.Count(
    	es.Count.WithFilterPath("-_shards"),
    	es.Count.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.count({
      filter_path: '-_shards'
    })
    console.log(response)
    
    
    GET /_count?filter_path=-_shards

Responds:

    
    
    {
      "count" : 5
    }

为了更好地控制，可以在同一表达式中组合包含和排除筛选器。在这种情况下，将首先应用独占筛选器，然后使用非独占筛选器再次筛选结果：

    
    
    $response = $client->cluster()->state();
    
    
    resp = client.cluster.state(
        filter_path=[
            "metadata.indices.*.state",
            "-metadata.indices.logstash-*",
        ],
    )
    print(resp)
    
    
    response = client.cluster.state(
      filter_path: 'metadata.indices.*.state,-metadata.indices.logstash-*'
    )
    puts response
    
    
    res, err := es.Cluster.State(
    	es.Cluster.State.WithFilterPath("metadata.indices.*.state,-metadata.indices.logstash-*"),
    )
    fmt.Println(res, err)
    
    
    const response = await client.cluster.state({
      filter_path: 'metadata.indices.*.state,-metadata.indices.logstash-*'
    })
    console.log(response)
    
    
    GET /_cluster/state?filter_path=metadata.indices.*.state,-metadata.indices.logstash-*

Responds:

    
    
    {
      "metadata" : {
        "indices" : {
          "my-index-000001" : {"state" : "open"},
          "my-index-000002" : {"state" : "open"},
          "my-index-000003" : {"state" : "open"}
        }
      }
    }

请注意，Elasticsearch 有时会直接返回字段的原始值，例如"_source"字段。如果要过滤"_source"字段，应考虑将现有的"_source"参数(有关更多详细信息，请参阅 GetAPI)与"filter_path"参数组合在一起，如下所示：

    
    
    $params = [
        'index' => 'library',
        'body' => [
            'title' => 'Book #1',
            'rating' => 200.1,
        ],
    ];
    $response = $client->index($params);
    $params = [
        'index' => 'library',
        'body' => [
            'title' => 'Book #2',
            'rating' => 1.7,
        ],
    ];
    $response = $client->index($params);
    $params = [
        'index' => 'library',
        'body' => [
            'title' => 'Book #3',
            'rating' => 0.1,
        ],
    ];
    $response = $client->index($params);
    $response = $client->search();
    
    
    resp = client.index(
        index="library",
        refresh=True,
        body={"title": "Book #1", "rating": 200.1},
    )
    print(resp)
    
    resp = client.index(
        index="library",
        refresh=True,
        body={"title": "Book #2", "rating": 1.7},
    )
    print(resp)
    
    resp = client.index(
        index="library",
        refresh=True,
        body={"title": "Book #3", "rating": 0.1},
    )
    print(resp)
    
    resp = client.search(
        filter_path="hits.hits._source", _source="title", sort="rating:desc",
    )
    print(resp)
    
    
    response = client.index(
      index: 'library',
      refresh: true,
      body: {
        title: 'Book #1',
        rating: 200.1
      }
    )
    puts response
    
    response = client.index(
      index: 'library',
      refresh: true,
      body: {
        title: 'Book #2',
        rating: 1.7
      }
    )
    puts response
    
    response = client.index(
      index: 'library',
      refresh: true,
      body: {
        title: 'Book #3',
        rating: 0.1
      }
    )
    puts response
    
    response = client.search(
      filter_path: 'hits.hits._source',
      _source: 'title',
      sort: 'rating:desc'
    )
    puts response
    
    
    {
    	res, err := es.Index(
    		"library",
    		strings.NewReader(`{
    	  "title": "Book #1",
    	  "rating": 200.1
    	}`),
    		es.Index.WithRefresh("true"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Index(
    		"library",
    		strings.NewReader(`{
    	  "title": "Book #2",
    	  "rating": 1.7
    	}`),
    		es.Index.WithRefresh("true"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Index(
    		"library",
    		strings.NewReader(`{
    	  "title": "Book #3",
    	  "rating": 0.1
    	}`),
    		es.Index.WithRefresh("true"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Search(
    		es.Search.WithSource("title"),
    		es.Search.WithFilterPath("hits.hits._source"),
    		es.Search.WithSort("rating:desc"),
    		es.Search.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    
    const response0 = await client.index({
      index: 'library',
      refresh: true,
      body: {
        title: 'Book #1',
        rating: 200.1
      }
    })
    console.log(response0)
    
    const response1 = await client.index({
      index: 'library',
      refresh: true,
      body: {
        title: 'Book #2',
        rating: 1.7
      }
    })
    console.log(response1)
    
    const response2 = await client.index({
      index: 'library',
      refresh: true,
      body: {
        title: 'Book #3',
        rating: 0.1
      }
    })
    console.log(response2)
    
    const response3 = await client.search({
      filter_path: 'hits.hits._source',
      _source: 'title',
      sort: 'rating:desc'
    })
    console.log(response3)
    
    
    POST /library/_doc?refresh
    {"title": "Book #1", "rating": 200.1}
    POST /library/_doc?refresh
    {"title": "Book #2", "rating": 1.7}
    POST /library/_doc?refresh
    {"title": "Book #3", "rating": 0.1}
    GET /_search?filter_path=hits.hits._source&_source=title&sort=rating:desc
    
    
    {
      "hits" : {
        "hits" : [ {
          "_source":{"title":"Book #1"}
        }, {
          "_source":{"title":"Book #2"}
        }, {
          "_source":{"title":"Book #3"}
        } ]
      }
    }

### 平面设置

"flat_settings"标志会影响设置列表的呈现。当"flat_settings"标志为"true"时，设置以平面格式返回：

    
    
    response = client.indices.get_settings(
      index: 'my-index-000001',
      flat_settings: true
    )
    puts response
    
    
    GET my-index-000001/_settings?flat_settings=true

Returns:

    
    
    {
      "my-index-000001" : {
        "settings": {
          "index.number_of_replicas": "1",
          "index.number_of_shards": "1",
          "index.creation_date": "1474389951325",
          "index.uuid": "n6gzFZTgS664GUfx0Xrpjw",
          "index.version.created": ...,
          "index.routing.allocation.include._tier_preference" : "data_content",
          "index.provided_name" : "my-index-000001"
        }
      }
    }

当"flat_settings"标志为"false"时，设置将以更易于阅读的结构化格式返回：

    
    
    response = client.indices.get_settings(
      index: 'my-index-000001',
      flat_settings: false
    )
    puts response
    
    
    GET my-index-000001/_settings?flat_settings=false

Returns:

    
    
    {
      "my-index-000001" : {
        "settings" : {
          "index" : {
            "number_of_replicas": "1",
            "number_of_shards": "1",
            "creation_date": "1474389951325",
            "uuid": "n6gzFZTgS664GUfx0Xrpjw",
            "version": {
              "created": ...
            },
            "routing": {
              "allocation": {
                "include": {
                  "_tier_preference": "data_content"
                }
              }
            },
            "provided_name" : "my-index-000001"
          }
        }
      }
    }

默认情况下，"flat_settings"设置为"false"。

###Fuzziness

一些查询和 API 支持参数，以允许使用"模糊性"参数进行不精确的 _fuzzy_ 匹配。

当查询"文本"或"关键字"字段时，"模糊性"被解释为一个Levenshtein EditDistance——需要对一个字符串进行一个字符更改的数量，以使其与另一个字符串相同。

"模糊度"参数可以指定为：

'0', '1', '2'

|

允许的最大编辑距离(或编辑次数)---|---"自动"

|

根据术语的长度生成编辑距离。可以选择提供低距离和高距离参数"自动：[低]，[高]"。如果未指定，则默认值为 3 和 6，相当于"AUTO：3，6"，表示长度：

`0..2`

     Must match exactly 
`3..5`

     One edit allowed 
`>5`

     Two edits allowed 

"AUTO"通常应该是"模糊性"的首选值。   ### 启用堆栈跟踪编辑

默认情况下，当请求返回错误时，Elasticsearch 不包括错误的堆栈跟踪。您可以通过将"error_trace"url 参数设置为"true"来启用该行为。例如，默认情况下，当您向"_search"API 发送无效的"size"参数时：

    
    
    POST /my-index-000001/_search?size=surprise_me

响应如下所示：

    
    
    {
      "error" : {
        "root_cause" : [
          {
            "type" : "illegal_argument_exception",
            "reason" : "Failed to parse int parameter [size] with value [surprise_me]"
          }
        ],
        "type" : "illegal_argument_exception",
        "reason" : "Failed to parse int parameter [size] with value [surprise_me]",
        "caused_by" : {
          "type" : "number_format_exception",
          "reason" : "For input string: \"surprise_me\""
        }
      },
      "status" : 400
    }

但是，如果您设置"error_trace=true"：

    
    
    POST /my-index-000001/_search?size=surprise_me&error_trace=true

响应如下所示：

    
    
    {
      "error": {
        "root_cause": [
          {
            "type": "illegal_argument_exception",
            "reason": "Failed to parse int parameter [size] with value [surprise_me]",
            "stack_trace": "Failed to parse int parameter [size] with value [surprise_me]]; nested: IllegalArgumentException..."
          }
        ],
        "type": "illegal_argument_exception",
        "reason": "Failed to parse int parameter [size] with value [surprise_me]",
        "stack_trace": "java.lang.IllegalArgumentException: Failed to parse int parameter [size] with value [surprise_me]\n    at org.elasticsearch.rest.RestRequest.paramAsInt(RestRequest.java:175)...",
        "caused_by": {
          "type": "number_format_exception",
          "reason": "For input string: \"surprise_me\"",
          "stack_trace": "java.lang.NumberFormatException: For input string: \"surprise_me\"\n    at java.lang.NumberFormatException.forInputString(NumberFormatException.java:65)..."
        }
      },
      "status": 400
    }

[« API conventions](api-conventions.md) [REST API compatibility »](rest-api-
compatibility.md)
