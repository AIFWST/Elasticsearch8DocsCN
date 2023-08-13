

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Search your
data](search-your-data.md)

[« Search your data](search-your-data.md) [Filter search results »](filter-
search-results.md)

## 折叠搜索结果

您可以使用"折叠"参数根据字段值折叠搜索结果。折叠是通过仅选择每个折叠键排序最高的文档来完成的。

例如，以下搜索按"user.id"折叠结果，并按"http.response.bytes"对结果进行排序。

    
    
    GET my-index-000001/_search
    {
      "query": {
        "match": {
          "message": "GET /search"
        }
      },
      "collapse": {
        "field": "user.id"         __},
      "sort": [
        {
          "http.response.bytes": { __"order": "desc"
          }
        }
      ],
      "from": 0 __}

__

|

使用"user.id"字段折叠结果集 ---|--- __

|

按"http.response.bytes"__对结果进行排序

|

定义第一个折叠结果的偏移量 响应中的总命中数表示未折叠的匹配文档数。不同组的总数未知。

用于折叠的字段必须是激活了"doc_values"的单值"关键字"或"数字"字段。

折叠仅应用于排名靠前的点击，不会影响聚合。

### 展开折叠结果

也可以使用"inner_hits"选项展开每个折叠的热门歌曲。

    
    
    GET /my-index-000001/_search
    {
      "query": {
        "match": {
          "message": "GET /search"
        }
      },
      "collapse": {
        "field": "user.id",                       __"inner_hits": {
          "name": "most_recent", __"size": 5, __"sort": [ { "@timestamp": "desc" } ] __},
        "max_concurrent_group_searches": 4 __},
      "sort": [
        {
          "http.response.bytes": {
            "order": "desc"
          }
        }
      ]
    }

__

|

使用"user.id"字段折叠结果集 ---|--- __

|

响应 __ 中用于内部命中部分的名称

|

每个折叠键要检索的"inner_hits"数 __

|

如何对每个组中的文档进行排序 __

|

允许检索每个组的"inner_hits"的并发请求数 有关支持的选项的完整列表和响应格式，请参阅内部命中。

也可以为每个折叠的命中请求多个"inner_hits"。当您想要获取折叠命中的多个表示形式时，这可能很有用。

    
    
    GET /my-index-000001/_search
    {
      "query": {
        "match": {
          "message": "GET /search"
        }
      },
      "collapse": {
        "field": "user.id",                   __"inner_hits": [
          {
            "name": "largest_responses", __"size": 3,
            "sort": [
              {
                "http.response.bytes": {
                  "order": "desc"
                }
              }
            ]
          },
          {
            "name": "most_recent", __"size": 3,
            "sort": [
              {
                "@timestamp": {
                  "order": "desc"
                }
              }
            ]
          }
        ]
      },
      "sort": [
        "http.response.bytes"
      ]
    }

__

|

使用"user.id"字段折叠结果集 ---|--- __

|

返回用户 __ 的三个最大的 HTTP 响应

|

为用户返回三个最新的 HTTP 响应 组的扩展是通过为响应中返回的每个折叠命中为每个"inner_hit"请求发送一个额外的查询来完成的。如果您有太多组或"inner_hit"请求，这可能会显着减慢您的搜索速度。

"max_concurrent_group_searches"请求参数可用于控制此阶段允许的最大并发搜索数。默认值基于数据节点数和默认搜索线程池大小。

"折叠"不能与滚动或分数一起使用。

### 折叠与"search_after"

字段折叠可以与"search_after"参数一起使用。仅当在同一字段上进行排序和折叠时，才支持使用"search_after"。也不允许二次排序。例如，我们可以在"user.id"上折叠和排序，同时使用"search_after"对结果进行分页：

    
    
    GET /my-index-000001/_search
    {
      "query": {
        "match": {
          "message": "GET /search"
        }
      },
      "collapse": {
        "field": "user.id"
      },
      "sort": [ "user.id" ],
      "search_after": ["dd5ce1ad"]
    }

### 第二级崩溃

还支持第二级折叠，并应用于"inner_hits"。

例如，以下搜索按"geo.country_name"折叠结果。在每个"geo.country_name"中，内部命中被"user.id"折叠。

第二级崩溃不允许"inner_hits"。

    
    
    GET /my-index-000001/_search
    {
      "query": {
        "match": {
          "message": "GET /search"
        }
      },
      "collapse": {
        "field": "geo.country_name",
        "inner_hits": {
          "name": "by_location",
          "collapse": { "field": "user.id" },
          "size": 3
        }
      }
    }
    
    
    {
      "hits" : {
        "hits" : [
          {
            "_index" : "my-index-000001",
            "_id" : "oX9uXXoB0da05OCR3adK",
            "_score" : 0.5753642,
            "_source" : {
              "@timestamp" : "2099-11-15T14:12:12",
              "geo" : {
                "country_name" : "Amsterdam"
              },
              "http" : {
                "request" : {
                  "method" : "get"
                },
                "response" : {
                  "bytes" : 1070000,
                  "status_code" : 200
                },
                "version" : "1.1"
              },
              "message" : "GET /search HTTP/1.1 200 1070000",
              "source" : {
                "ip" : "127.0.0.1"
              },
              "user" : {
                "id" : "kimchy"
              }
            },
            "fields" : {
              "geo.country_name" : [
                "Amsterdam"
              ]
            },
            "inner_hits" : {
              "by_location" : {
                "hits" : {
                  "total" : {
                    "value" : 1,
                    "relation" : "eq"
                  },
                  "max_score" : null,
                  "hits" : [
                    {
                      "_index" : "my-index-000001",
                      "_id" : "oX9uXXoB0da05OCR3adK",
                      "_score" : 0.5753642,
                      "_source" : {
                        "@timestamp" : "2099-11-15T14:12:12",
                        "geo" : {
                          "country_name" : "Amsterdam"
                        },
                        "http" : {
                          "request" : {
                            "method" : "get"
                          },
                          "response" : {
                            "bytes" : 1070000,
                            "status_code" : 200
                          },
                          "version" : "1.1"
                        },
                        "message" : "GET /search HTTP/1.1 200 1070000",
                        "source" : {
                          "ip" : "127.0.0.1"
                        },
                        "user" : {
                          "id" : "kimchy"
                        }
                      },
                      "fields" : {
                        "user.id" : [
                          "kimchy"
                        ]
                      }
                    }
                  ]
                }
              }
            }
          }
        ]
      }
    }

[« Search your data](search-your-data.md) [Filter search results »](filter-
search-results.md)
