

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Search your
data](search-your-data.md)

[« Near real-time search](near-real-time.md) [Retrieve inner hits »](inner-
hits.md)

## 分页搜索结果

默认情况下，搜索返回前 10 个匹配命中。若要分页浏览更大的结果集，可以使用搜索 API 的"发件人"和"大小"参数。"from"参数定义要跳过的命中数，默认为"0"。"size"参数是要返回的最大命中数。这两个参数共同定义一页结果。

    
    
    response = client.search(
      body: {
        from: 5,
        size: 20,
        query: {
          match: {
            "user.id": 'kimchy'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "from": 5,
    	  "size": 20,
    	  "query": {
    	    "match": {
    	      "user.id": "kimchy"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "from": 5,
      "size": 20,
      "query": {
        "match": {
          "user.id": "kimchy"
        }
      }
    }

避免使用"from"和"size"来分页太深或一次请求太多结果。搜索请求通常跨越多个分片。每个分片必须将其请求的命中数和任何先前页面的命中数加载到内存中。对于深层页面或大型结果集，这些操作可能会显著增加内存和 CPU 使用率，从而导致性能下降或节点故障。

默认情况下，您不能使用"发件人"和"大小"来浏览超过 10，000 次点击。此限制是由"index.max_result_window"索引设置设置的保护措施。如果您需要翻阅超过 10，000 次点击，请改用"search_after"参数。

Elasticsearch使用Lucene的内部文档ID作为决胜局。这些内部文档 ID 在相同数据的副本之间可能完全不同。当搜索命中分页时，您可能偶尔会看到具有相同排序值的文档的排序不一致。

### 搜索后

您可以使用"search_after"参数检索下一页的命中，使用上一页中的一组排序值。

使用"search_after"需要具有相同"查询"和"排序"值的多个搜索请求。第一步是运行初始请求。以下示例按两个字段("日期"和"tie_breaker_id")对结果进行排序：

    
    
    response = client.search(
      index: 'twitter',
      body: {
        query: {
          match: {
            title: 'elasticsearch'
          }
        },
        sort: [
          {
            date: 'asc'
          },
          {
            tie_breaker_id: 'asc'
          }
        ]
      }
    )
    puts response
    
    
    GET twitter/_search
    {
        "query": {
            "match": {
                "title": "elasticsearch"
            }
        },
        "sort": [
            {"date": "asc"},
            {"tie_breaker_id": "asc"}      __]
    }

__

|

启用了"doc_values"---|的"_id"字段的副本--- 搜索响应包括每个匹配的"排序"值数组：

    
    
    {
      "took" : 17,
      "timed_out" : false,
      "_shards" : ...,
      "hits" : {
        "total" : ...,
        "max_score" : null,
        "hits" : [
          ...
          {
            "_index" : "twitter",
            "_id" : "654322",
            "_score" : null,
            "_source" : ...,
            "sort" : [
              1463538855,
              "654322"
            ]
          },
          {
            "_index" : "twitter",
            "_id" : "654323",
            "_score" : null,
            "_source" : ...,
            "sort" : [                                __1463538857,
              "654323"
            ]
          }
        ]
      }
    }

__

|

对上次返回的命中值进行排序。   ---|--- 要检索下一页结果，请重复请求，从上次命中中获取"sort"值，并将其插入到"search_after"数组中：

    
    
    response = client.search(
      index: 'twitter',
      body: {
        query: {
          match: {
            title: 'elasticsearch'
          }
        },
        search_after: [
          1_463_538_857,
          '654323'
        ],
        sort: [
          {
            date: 'asc'
          },
          {
            tie_breaker_id: 'asc'
          }
        ]
      }
    )
    puts response
    
    
    GET twitter/_search
    {
        "query": {
            "match": {
                "title": "elasticsearch"
            }
        },
        "search_after": [1463538857, "654323"],
        "sort": [
            {"date": "asc"},
            {"tie_breaker_id": "asc"}
        ]
    }

通过每次检索新结果页时更新"search_after"数组来重复此过程。如果在这些请求之间发生刷新，则结果的顺序可能会更改，从而导致页面之间的结果不一致。若要防止出现这种情况，可以创建一个时间点 (PIT) 来保留搜索的当前索引状态。

    
    
    response = client.open_point_in_time(
      index: 'my-index-000001',
      keep_alive: '1m'
    )
    puts response
    
    
    POST /my-index-000001/_pit?keep_alive=1m

API 返回一个 PIT ID。

    
    
    {
      "id": "46ToAwMDaWR5BXV1aWQyKwZub2RlXzMAAAAAAAAAACoBYwADaWR4BXV1aWQxAgZub2RlXzEAAAAAAAAAAAEBYQADaWR5BXV1aWQyKgZub2RlXzIAAAAAAAAAAAwBYgACBXV1aWQyAAAFdXVpZDEAAQltYXRjaF9hbGw_gAAAAA=="
    }

要获取结果的第一页，请提交带有"sort"参数的搜索请求。如果使用 PIT，请在"pit.id"参数中指定 PIT ID，并从请求路径中省略目标数据流或索引。

所有 PIT 搜索请求都会添加一个名为"_shard_doc"的隐式排序仲裁字段，该字段也可以显式提供。如果您无法使用 PIT，我们建议您在"排序"中包含仲裁字段。此仲裁器字段应包含每个文档的唯一值。如果未包含仲裁字段，则分页结果可能会错过或重复命中。

请求后搜索具有优化，可在排序顺序为"_shard_doc"且未跟踪总命中数时使其更快。如果要循环访问所有文档而不考虑顺序，这是最有效的选项。

如果"sort"字段在某些目标数据流或索引中是"日期"，但在其他目标中是"date_nanos"字段，请使用"numeric_type"参数将值转换为单个分辨率，并使用"format"参数为"sort"字段指定日期格式。否则，Elasticsearch 将无法在每个请求中正确解释参数之后的搜索。

    
    
    GET /_search
    {
      "size": 10000,
      "query": {
        "match" : {
          "user.id" : "elkbee"
        }
      },
      "pit": {
        "id":  "46ToAwMDaWR5BXV1aWQyKwZub2RlXzMAAAAAAAAAACoBYwADaWR4BXV1aWQxAgZub2RlXzEAAAAAAAAAAAEBYQADaWR5BXV1aWQyKgZub2RlXzIAAAAAAAAAAAwBYgACBXV1aWQyAAAFdXVpZDEAAQltYXRjaF9hbGw_gAAAAA==", __"keep_alive": "1m"
      },
      "sort": [ __{"@timestamp": {"order": "asc", "format": "strict_date_optional_time_nanos", "numeric_type" : "date_nanos" }}
      ]
    }

__

|

用于搜索的 PIT ID。   ---|---    __

|

对搜索的命中进行排序，并在"_shard_doc"升序上隐含的抢七。   搜索响应包括每个匹配的"排序"值数组。如果您使用了 PIT，则每个命中的最后一个"排序"值将包含仲裁。这个名为"_shard_doc"的仲裁系统会自动添加到每个使用 PIT 的搜索请求上。"_shard_doc"值是 PIT 中的分片索引和 Lucene 的内部文档 ID 的组合，它是 PIT 中唯一的文档和常量。您还可以在搜索请求中显式添加仲裁规则以自定义顺序：

    
    
    GET /_search
    {
      "size": 10000,
      "query": {
        "match" : {
          "user.id" : "elkbee"
        }
      },
      "pit": {
        "id":  "46ToAwMDaWR5BXV1aWQyKwZub2RlXzMAAAAAAAAAACoBYwADaWR4BXV1aWQxAgZub2RlXzEAAAAAAAAAAAEBYQADaWR5BXV1aWQyKgZub2RlXzIAAAAAAAAAAAwBYgACBXV1aWQyAAAFdXVpZDEAAQltYXRjaF9hbGw_gAAAAA==", __"keep_alive": "1m"
      },
      "sort": [ __{"@timestamp": {"order": "asc", "format": "strict_date_optional_time_nanos"}},
        {"_shard_doc": "desc"}
      ]
    }

__

|

用于搜索的 PIT ID。   ---|---    __

|

对搜索的命中进行排序，并在"_shard_doc"降序上显式平局。               { "pit_id" ： "46ToAwMDaWR5BXV1aWQyKwZub2RlXzMAAAAAAAAAACoBYwADaWR4BXV1aWQxAgZub2RlXzEAAAAAAAAAAAEBYQADaWR5BXV1aWQyKgZub2RlXzIAAAAAAAAAAAwBYgACBXV1aWQyAAAFdXVpZDEAAQltYXRjaF9hbGw_gAAAAA=="， __"采取" ： 17， "timed_out" ： 假， "_shards" ： ...， "命中" ： { "总计" ： ...， "max_score" ： 空， "命中" ： [ ...         { "_index" ： "my-index-000001"， "_id" ： "FaslK3QBySSL_rrj9zM5"， "_score" ： null， "_source" ： ...， "sort" ： [ __"2021-05-20T05：30：04.832Z"， 4294967298 __] } ]     }    }

__

|

更新了时间点的"id"。   ---|---    __

|

对上次返回的命中值进行排序。   __

|

仲裁符值，在"pit_id"中每个文档都是唯一的。   若要获取下一页结果，请使用 lasthit 的排序值(包括仲裁符)作为"search_after"参数重新运行上一个搜索。如果使用 PIT 参数，请在"pit.id"参数中使用最新的 PIT ID。搜索的"查询"和"排序"参数必须保持不变。如果提供，"from"参数必须是"0"(默认值)或"-1"。

    
    
    GET /_search
    {
      "size": 10000,
      "query": {
        "match" : {
          "user.id" : "elkbee"
        }
      },
      "pit": {
        "id":  "46ToAwMDaWR5BXV1aWQyKwZub2RlXzMAAAAAAAAAACoBYwADaWR4BXV1aWQxAgZub2RlXzEAAAAAAAAAAAEBYQADaWR5BXV1aWQyKgZub2RlXzIAAAAAAAAAAAwBYgACBXV1aWQyAAAFdXVpZDEAAQltYXRjaF9hbGw_gAAAAA==", __"keep_alive": "1m"
      },
      "sort": [
        {"@timestamp": {"order": "asc", "format": "strict_date_optional_time_nanos"}}
      ],
      "search_after": [ __"2021-05-20T05:30:04.832Z",
        4294967298
      ],
      "track_total_hits": false __}

__

|

上一次搜索返回的 PIT ID。   ---|---    __

|

对上一次搜索的上次命中值进行排序。   __

|

禁用对总点击量的跟踪以加快分页速度。   您可以重复此过程以获取其他结果页面。如果使用 aPIT，则可以使用每个搜索请求的"keep_alive"参数延长 PIT 的保留期。

完成后，应删除 PIT。

    
    
    response = client.close_point_in_time(
      body: {
        id: '46ToAwMDaWR5BXV1aWQyKwZub2RlXzMAAAAAAAAAACoBYwADaWR4BXV1aWQxAgZub2RlXzEAAAAAAAAAAAEBYQADaWR5BXV1aWQyKgZub2RlXzIAAAAAAAAAAAwBYgACBXV1aWQyAAAFdXVpZDEAAQltYXRjaF9hbGw_gAAAAA=='
      }
    )
    puts response
    
    
    DELETE /_pit
    {
        "id" : "46ToAwMDaWR5BXV1aWQyKwZub2RlXzMAAAAAAAAAACoBYwADaWR4BXV1aWQxAgZub2RlXzEAAAAAAAAAAAEBYQADaWR5BXV1aWQyKgZub2RlXzIAAAAAAAAAAAwBYgACBXV1aWQyAAAFdXVpZDEAAQltYXRjaF9hbGw_gAAAAA=="
    }

### 滚动搜索结果

我们不再建议使用滚动 API 进行深度分页。如果需要在分页超过 10，000 次命中时保留索引状态，请将"search_after"参数与时间点 (PIT) 一起使用。

虽然"搜索"请求返回单个"页面"结果，但"滚动"API 可用于从单个搜索请求中检索大量结果(甚至所有结果)，其方式与在传统数据库上使用游标的方式大致相同。

滚动不是用于实时用户请求，而是用于处理大量数据，例如，为了将 onedata 流的内容重新索引或索引为具有不同配置的新数据流或索引。

**客户端支持滚动和重新索引**

一些官方支持的客户端提供了帮助程序来帮助进行滚动搜索和重新索引：

Perl

     See [Search::Elasticsearch::Client::5_0::Bulk](https://metacpan.org/pod/Search::Elasticsearch::Client::5_0::Bulk) and [Search::Elasticsearch::Client::5_0::Scroll](https://metacpan.org/pod/Search::Elasticsearch::Client::5_0::Scroll)
Python

     See [elasticsearch.helpers.*](https://elasticsearch-py.readthedocs.org/en/master/helpers.html)
JavaScript

     See [client.helpers.*](/guide/en/elasticsearch/client/javascript-api/current/client-helpers.html)

从滚动请求返回的结果反映了发出初始"搜索"请求时数据流或索引的状态，就像时间快照一样。对文档的后续更改(索引、更新或删除)只会影响以后的搜索请求。

为了使用滚动，初始搜索请求应该在查询字符串中指定 'scroll' 参数，它告诉 Elasticsearch 它应该让"搜索上下文"保持活动多长时间(参见保持搜索上下文处于活动状态)，例如 '？scroll=1m'。

    
    
    response = client.search(
      index: 'my-index-000001',
      scroll: '1m',
      body: {
        size: 100,
        query: {
          match: {
            message: 'foo'
          }
        }
      }
    )
    puts response
    
    
    POST /my-index-000001/_search?scroll=1m
    {
      "size": 100,
      "query": {
        "match": {
          "message": "foo"
        }
      }
    }

上述请求的结果包括一个"_scroll_id"，应将其传递给"滚动"API，以便检索下一批结果。

    
    
    res, err := es.Scroll(
    	es.Scroll.WithBody(strings.NewReader(`{
    	  "scroll": "1m",
    	  "scroll_id": "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAD4WYm9laVYtZndUQlNsdDcwakFMNjU1QQ=="
    	}`)),
    	es.Scroll.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    POST /_search/scroll                                                               __{
      "scroll" : "1m", __"scroll_id" : "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAD4WYm9laVYtZndUQlNsdDcwakFMNjU1QQ==" __}

__

|

可以使用"GET"或"POST"，并且URL不应包含"索引"名称 - 这是在原始"搜索"请求中指定的。   ---|---    __

|

"scroll"参数告诉Elasticsearch保持搜索上下文打开另一个"1m"。   __

|

"scroll_id"参数 "size"参数允许您配置每批结果返回的最大命中数。每次调用"滚动"API 都会返回下一批结果，直到没有更多结果要返回，即"hits"数组为空。

初始搜索请求和每个后续滚动请求都返回 a'_scroll_id'。虽然"_scroll_id"可能会在请求之间发生变化，但它并不总是改变——无论如何，只应使用最近收到的"_scroll_id"。

如果请求指定聚合，则只有初始搜索响应将包含聚合结果。

滚动请求具有优化功能，可在排序顺序为"_doc"时使其更快。如果要遍历所有文档而不考虑顺序，这是最有效的选项：

    
    
    $params = [
        'body' => [
            'sort' => [
                '_doc',
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(scroll="1m", body={"sort": ["_doc"]})
    print(resp)
    
    
    response = client.search(
      scroll: '1m',
      body: {
        sort: [
          '_doc'
        ]
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "sort": [
    	    "_doc"
    	  ]
    	}`)),
    	es.Search.WithScroll(time.Duration(60000000000)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      scroll: '1m',
      body: {
        sort: [
          '_doc'
        ]
      }
    })
    console.log(response)
    
    
    GET /_search?scroll=1m
    {
      "sort": [
        "_doc"
      ]
    }

#### 保持搜索上下文处于活动状态

滚动返回在初始搜索请求时与搜索匹配的所有文档。它忽略对这些文档的任何后续更改。"scroll_id"标识一个_search context_，它跟踪 Elasticsearch 返回正确文档所需的所有内容。搜索上下文由初始请求创建，并由后续请求保持活动状态。

"scroll"参数(传递给"搜索"请求和每个"scroll"请求)告诉Elasticsearch应该保持搜索上下文存活多长时间。它的值(例如"1m"，请参阅时间单位)不需要足够长来处理所有数据 - 它只需要足够长来处理前一批结果。每个"滚动"请求(带有"scroll"参数)都会设置新的到期时间。如果"scroll"请求未传入"scroll"参数，则搜索上下文将作为_that_"scroll"请求的一部分被释放。

通常，后台合并过程通过将较小的段合并在一起以创建新的较大段来优化索引。一旦不再需要较小的段，它们就会被删除。此过程在滚动过程中继续，但打开的搜索上下文可防止删除旧段，因为它们仍在使用中。

保持较旧的段处于活动状态意味着需要更多的磁盘空间和文件句柄。确保已将节点配置为具有足够的可用文件句柄。请参阅文件描述符。

此外，如果区段包含已删除或更新的文档，则搜索上下文必须跟踪区段中的每个文档在初始搜索请求时是否处于活动状态。如果索引上有许多打开的滚动，并且需要持续删除或更新，请确保节点具有足够的堆空间。

为了防止因打开的卷轴过多而导致的问题，不允许用户打开超过特定限制的卷轴。默认情况下，打开卷轴的最大数量为 500。可以使用"搜索.max_打开_滚动_上下文"群集设置更新此限制。

您可以使用节点统计信息 API 检查打开了多少个搜索上下文：

    
    
    $params = [
        'metric' => 'indices',
        'index_metric' => 'search',
    ];
    $response = $client->nodes()->stats($params);
    
    
    resp = client.nodes.stats(metric="indices", index_metric="search")
    print(resp)
    
    
    response = client.nodes.stats(
      metric: 'indices',
      index_metric: 'search'
    )
    puts response
    
    
    res, err := es.Nodes.Stats(
    	es.Nodes.Stats.WithMetric([]string{"indices"}...),
    	es.Nodes.Stats.WithIndexMetric([]string{"search"}...),
    )
    fmt.Println(res, err)
    
    
    const response = await client.nodes.stats({
      metric: 'indices',
      index_metric: 'search'
    })
    console.log(response)
    
    
    GET /_nodes/stats/indices/search

#### 清除滚动

当超过"滚动"超时时，将自动删除搜索上下文。但是，保持滚动打开是有代价的，如上一节所述，因此一旦不再使用滚动，应使用"清除滚动"API 显式清除滚动：

    
    
    response = client.clear_scroll(
      body: {
        scroll_id: 'DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAD4WYm9laVYtZndUQlNsdDcwakFMNjU1QQ=='
      }
    )
    puts response
    
    
    res, err := es.ClearScroll(
    	es.ClearScroll.WithBody(strings.NewReader(`{
    	  "scroll_id": "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAD4WYm9laVYtZndUQlNsdDcwakFMNjU1QQ=="
    	}`)),
    )
    fmt.Println(res, err)
    
    
    DELETE /_search/scroll
    {
      "scroll_id" : "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAD4WYm9laVYtZndUQlNsdDcwakFMNjU1QQ=="
    }

多个滚动 ID 可以作为数组传递：

    
    
    response = client.clear_scroll(
      body: {
        scroll_id: [
          'DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAD4WYm9laVYtZndUQlNsdDcwakFMNjU1QQ==',
          'DnF1ZXJ5VGhlbkZldGNoBQAAAAAAAAABFmtSWWRRWUJrU2o2ZExpSGJCVmQxYUEAAAAAAAAAAxZrUllkUVlCa1NqNmRMaUhiQlZkMWFBAAAAAAAAAAIWa1JZZFFZQmtTajZkTGlIYkJWZDFhQQAAAAAAAAAFFmtSWWRRWUJrU2o2ZExpSGJCVmQxYUEAAAAAAAAABBZrUllkUVlCa1NqNmRMaUhiQlZkMWFB'
        ]
      }
    )
    puts response
    
    
    res, err := es.ClearScroll(
    	es.ClearScroll.WithBody(strings.NewReader(`{
    	  "scroll_id": [
    	    "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAD4WYm9laVYtZndUQlNsdDcwakFMNjU1QQ==",
    	    "DnF1ZXJ5VGhlbkZldGNoBQAAAAAAAAABFmtSWWRRWUJrU2o2ZExpSGJCVmQxYUEAAAAAAAAAAxZrUllkUVlCa1NqNmRMaUhiQlZkMWFBAAAAAAAAAAIWa1JZZFFZQmtTajZkTGlIYkJWZDFhQQAAAAAAAAAFFmtSWWRRWUJrU2o2ZExpSGJCVmQxYUEAAAAAAAAABBZrUllkUVlCa1NqNmRMaUhiQlZkMWFB"
    	  ]
    	}`)),
    )
    fmt.Println(res, err)
    
    
    DELETE /_search/scroll
    {
      "scroll_id" : [
        "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAD4WYm9laVYtZndUQlNsdDcwakFMNjU1QQ==",
        "DnF1ZXJ5VGhlbkZldGNoBQAAAAAAAAABFmtSWWRRWUJrU2o2ZExpSGJCVmQxYUEAAAAAAAAAAxZrUllkUVlCa1NqNmRMaUhiQlZkMWFBAAAAAAAAAAIWa1JZZFFZQmtTajZkTGlIYkJWZDFhQQAAAAAAAAAFFmtSWWRRWUJrU2o2ZExpSGJCVmQxYUEAAAAAAAAABBZrUllkUVlCa1NqNmRMaUhiQlZkMWFB"
      ]
    }

可以使用"_all"参数清除所有搜索上下文：

    
    
    $params = [
        'scroll_id' => '_all',
    ];
    $response = $client->clearScroll($params);
    
    
    resp = client.clear_scroll(scroll_id="_all")
    print(resp)
    
    
    response = client.clear_scroll(
      scroll_id: '_all'
    )
    puts response
    
    
    res, err := es.ClearScroll(
    	es.ClearScroll.WithScrollID("_all"),
    )
    fmt.Println(res, err)
    
    
    const response = await client.clearScroll({
      scroll_id: '_all'
    })
    console.log(response)
    
    
    DELETE /_search/scroll/_all

"scroll_id"也可以作为查询字符串参数或在请求正文中传递。多个滚动 ID 可以作为逗号分隔值传递：

    
    
    $params = [
        'scroll_id' => 'DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAD4WYm9laVYtZndUQlNsdDcwakFMNjU1QQ==,DnF1ZXJ5VGhlbkZldGNoBQAAAAAAAAABFmtSWWRRWUJrU2o2ZExpSGJCVmQxYUEAAAAAAAAAAxZrUllkUVlCa1NqNmRMaUhiQlZkMWFBAAAAAAAAAAIWa1JZZFFZQmtTajZkTGlIYkJWZDFhQQAAAAAAAAAFFmtSWWRRWUJrU2o2ZExpSGJCVmQxYUEAAAAAAAAABBZrUllkUVlCa1NqNmRMaUhiQlZkMWFB',
    ];
    $response = $client->clearScroll($params);
    
    
    resp = client.clear_scroll(
        scroll_id=[
            "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAD4WYm9laVYtZndUQlNsdDcwakFMNjU1QQ==",
            "DnF1ZXJ5VGhlbkZldGNoBQAAAAAAAAABFmtSWWRRWUJrU2o2ZExpSGJCVmQxYUEAAAAAAAAAAxZrUllkUVlCa1NqNmRMaUhiQlZkMWFBAAAAAAAAAAIWa1JZZFFZQmtTajZkTGlIYkJWZDFhQQAAAAAAAAAFFmtSWWRRWUJrU2o2ZExpSGJCVmQxYUEAAAAAAAAABBZrUllkUVlCa1NqNmRMaUhiQlZkMWFB",
        ],
    )
    print(resp)
    
    
    response = client.clear_scroll(
      scroll_id: 'DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAD4WYm9laVYtZndUQlNsdDcwakFMNjU1QQ==,DnF1ZXJ5VGhlbkZldGNoBQAAAAAAAAABFmtSWWRRWUJrU2o2ZExpSGJCVmQxYUEAAAAAAAAAAxZrUllkUVlCa1NqNmRMaUhiQlZkMWFBAAAAAAAAAAIWa1JZZFFZQmtTajZkTGlIYkJWZDFhQQAAAAAAAAAFFmtSWWRRWUJrU2o2ZExpSGJCVmQxYUEAAAAAAAAABBZrUllkUVlCa1NqNmRMaUhiQlZkMWFB'
    )
    puts response
    
    
    res, err := es.ClearScroll(
    	es.ClearScroll.WithScrollID("DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAD4WYm9laVYtZndUQlNsdDcwakFMNjU1QQ==", "DnF1ZXJ5VGhlbkZldGNoBQAAAAAAAAABFmtSWWRRWUJrU2o2ZExpSGJCVmQxYUEAAAAAAAAAAxZrUllkUVlCa1NqNmRMaUhiQlZkMWFBAAAAAAAAAAIWa1JZZFFZQmtTajZkTGlIYkJWZDFhQQAAAAAAAAAFFmtSWWRRWUJrU2o2ZExpSGJCVmQxYUEAAAAAAAAABBZrUllkUVlCa1NqNmRMaUhiQlZkMWFB"),
    )
    fmt.Println(res, err)
    
    
    const response = await client.clearScroll({
      scroll_id: 'DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAD4WYm9laVYtZndUQlNsdDcwakFMNjU1QQ==,DnF1ZXJ5VGhlbkZldGNoBQAAAAAAAAABFmtSWWRRWUJrU2o2ZExpSGJCVmQxYUEAAAAAAAAAAxZrUllkUVlCa1NqNmRMaUhiQlZkMWFBAAAAAAAAAAIWa1JZZFFZQmtTajZkTGlIYkJWZDFhQQAAAAAAAAAFFmtSWWRRWUJrU2o2ZExpSGJCVmQxYUEAAAAAAAAABBZrUllkUVlCa1NqNmRMaUhiQlZkMWFB'
    })
    console.log(response)
    
    
    DELETE /_search/scroll/DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAD4WYm9laVYtZndUQlNsdDcwakFMNjU1QQ==,DnF1ZXJ5VGhlbkZldGNoBQAAAAAAAAABFmtSWWRRWUJrU2o2ZExpSGJCVmQxYUEAAAAAAAAAAxZrUllkUVlCa1NqNmRMaUhiQlZkMWFBAAAAAAAAAAIWa1JZZFFZQmtTajZkTGlIYkJWZDFhQQAAAAAAAAAFFmtSWWRRWUJrU2o2ZExpSGJCVmQxYUEAAAAAAAAABBZrUllkUVlCa1NqNmRMaUhiQlZkMWFB

#### 切片滚动

在分页浏览大量文档时，将搜索拆分为多个切片以独立使用它们会很有帮助：

    
    
    response = client.search(
      index: 'my-index-000001',
      scroll: '1m',
      body: {
        slice: {
          id: 0,
          max: 2
        },
        query: {
          match: {
            message: 'foo'
          }
        }
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      scroll: '1m',
      body: {
        slice: {
          id: 1,
          max: 2
        },
        query: {
          match: {
            message: 'foo'
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search?scroll=1m
    {
      "slice": {
        "id": 0,                      __"max": 2 __},
      "query": {
        "match": {
          "message": "foo"
        }
      }
    }
    GET /my-index-000001/_search?scroll=1m
    {
      "slice": {
        "id": 1,
        "max": 2
      },
      "query": {
        "match": {
          "message": "foo"
        }
      }
    }

__

|

切片的 id ---|--- __

|

最大切片数 第一个请求返回属于第一个切片的文档的结果 (id： 0) 和第二个请求返回属于第二个切片的文档的结果。由于最大切片数设置为2，因此两个请求的结果相当于没有切片的滚动查询的结果。默认情况下，拆分首先在分片上完成，然后使用"_id"字段在每个分片上本地完成。局部拆分遵循公式"slice(doc) = floorMod(hashCode(doc._id)， max))"。

每个滚动都是独立的，可以像任何滚动请求一样并行处理。

如果切片数大于分片数，则切片过滤器在第一次调用时非常慢，其复杂性为 O(N)，内存成本等于每个切片 N 位，其中 N 是分片中的文档总数。在几次调用后，筛选器应缓存，后续调用应更快，但应限制并行执行的切片查询数，以避免内存爆炸。

时间点 API 支持更高效的分区策略，并且不会出现此问题。如果可能，建议使用切片而不是滚动的时间点搜索。

避免这种高成本的另一种方法是使用另一个字段的"doc_values"进行切片。该字段必须具有以下属性：

* 该字段为数字。  * 在该字段上启用了"doc_values" * 每个文档都应包含一个值。如果文档的指定字段有多个值，则使用第一个值。  * 每个文档的值应在创建文档时设置一次，并且永远不会更新。这可确保每个切片获得确定性结果。  * 字段的基数应很高。这可确保每个切片获得大致相同数量的文档。

    
    
    response = client.search(
      index: 'my-index-000001',
      scroll: '1m',
      body: {
        slice: {
          field: '@timestamp',
          id: 0,
          max: 10
        },
        query: {
          match: {
            message: 'foo'
          }
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_search?scroll=1m
    {
      "slice": {
        "field": "@timestamp",
        "id": 0,
        "max": 10
      },
      "query": {
        "match": {
          "message": "foo"
        }
      }
    }

对于仅追加基于时间的索引，可以安全地使用"时间戳"字段。

[« Near real-time search](near-real-time.md) [Retrieve inner hits »](inner-
hits.md)
