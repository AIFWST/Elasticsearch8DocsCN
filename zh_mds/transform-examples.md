

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Roll up or
transform your data](data-rollup-transform.md) ›[Transforming
data](transforms.md)

[« Tutorial: Transforming the eCommerce sample data](ecommerce-
transforms.md) [Painless examples for transforms »](transform-painless-
examples.md)

## 转换示例

这些示例演示如何使用转换从数据中获取有用的见解。所有示例都使用 Kibana 示例数据集之一。有关更详细的分步示例，请参阅教程：转换电子商务示例数据。

* 寻找最佳客户 * 寻找延误最多的航空公司 * 查找可疑客户端 IP * 查找每个 IP 地址的最后一个日志事件 * 查找向服务器发送最多字节的客户端 IP * 通过客户 ID 获取客户名称和电子邮件地址

### 寻找最佳客户

此示例使用电子商务订单示例数据集来查找在假设的网上商店中花费最多的客户。让我们使用"透视"类型的转换，以便目标索引包含订单数、订单总价、唯一产品的数量和每个订单的平均价格，以及每个客户的订购产品总量。

!在 Kibana 中通过转换找到最佳客户

或者，可以使用预览转换和创建转换 API。

接口示例

    
    
    POST _transform/_preview
    {
      "source": {
        "index": "kibana_sample_data_ecommerce"
      },
      "dest" : { __"index" : "sample_ecommerce_orders_by_customer"
      },
      "pivot": {
        "group_by": { __"user": { "terms": { "field": "user" }},
          "customer_id": { "terms": { "field": "customer_id" }}
        },
        "aggregations": {
          "order_count": { "value_count": { "field": "order_id" }},
          "total_order_amt": { "sum": { "field": "taxful_total_price" }},
          "avg_amt_per_order": { "avg": { "field": "taxful_total_price" }},
          "avg_unique_products_per_order": { "avg": { "field": "total_unique_products" }},
          "total_unique_products": { "cardinality": { "field": "products.product_id" }}
        }
      }
    }

__

|

转换的目标索引。它被"_preview"忽略。   ---|---    __

|

选择两个"group_by"字段。这意味着转换包含每个"用户"和"customer_id"组合的唯一行。在此数据集中，这两个字段都是唯一的。通过在转换中包含两者，它可以为最终结果提供更多上下文。   在上面的示例中，使用精简的 JSON 格式使透视对象更易于阅读。

预览转换 API 使你能够提前查看转换的布局，其中填充了一些示例值。例如：

    
    
    {
      "preview" : [
        {
          "total_order_amt" : 3946.9765625,
          "order_count" : 59.0,
          "total_unique_products" : 116.0,
          "avg_unique_products_per_order" : 2.0,
          "customer_id" : "10",
          "user" : "recip",
          "avg_amt_per_order" : 66.89790783898304
        },
        ...
        ]
      }

通过此转换，可以更轻松地回答以下问题：

* 哪些客户花费最多？  * 哪些客户每笔订单花费最多？  * 哪些客户最常订购？  * 哪些客户订购的不同产品数量最少？

仅使用聚合就可以回答这些问题，但是转换允许我们将此数据保存为以客户为中心的索引。这使我们能够大规模分析数据，并更灵活地从以客户为中心的角度探索和导航数据。在某些情况下，它甚至可以使创建可视化变得更加简单。

### 寻找延误最多的航空公司

此示例使用航班示例数据集来找出哪个航空公司的延误最多。首先，使用查询筛选器筛选源数据，使其排除所有取消的航班。然后转换数据以包含不同航班数、延迟分钟数和航空承运人的飞行分钟数总和。最后，使用"bucket_script"来确定实际延误的飞行时间百分比。

    
    
    POST _transform/_preview
    {
      "source": {
        "index": "kibana_sample_data_flights",
        "query": { __"bool": {
            "filter": [
              { "term":  { "Cancelled": false } }
            ]
          }
        }
      },
      "dest" : { __"index" : "sample_flight_delays_by_carrier"
      },
      "pivot": {
        "group_by": { __"carrier": { "terms": { "field": "Carrier" }}
        },
        "aggregations": {
          "flights_count": { "value_count": { "field": "FlightNum" }},
          "delay_mins_total": { "sum": { "field": "FlightDelayMin" }},
          "flight_mins_total": { "sum": { "field": "FlightTimeMin" }},
          "delay_time_percentage": { __"bucket_script": {
              "buckets_path": {
                "delay_time": "delay_mins_total.value",
                "flight_time": "flight_mins_total.value"
              },
              "script": "(params.delay_time / params.flight_time) * 100"
            }
          }
        }
      }
    }

__

|

筛选源数据以仅选择未取消的航班。   ---|---    __

|

转换的目标索引。它被"_preview"忽略。   __

|

数据按包含航空公司名称的"承运人"字段分组。   __

|

此"bucket_script"对聚合返回的结果执行计算。在此特定示例中，它计算延误占用的旅行时间百分比。   预览显示新索引将包含每个运营商的如下数据：

    
    
    {
      "preview" : [
        {
          "carrier" : "ES-Air",
          "flights_count" : 2802.0,
          "flight_mins_total" : 1436927.5130677223,
          "delay_time_percentage" : 9.335543983955839,
          "delay_mins_total" : 134145.0
        },
        ...
      ]
    }

通过此转换，可以更轻松地回答以下问题：

* 哪家航空公司的延误时间占航班时间的百分比最多？

此数据是虚构的，并不反映任何特色目的地或始发机场的实际延误或航班统计数据。

### 查找可疑客户端 IP

此示例使用 Web 日志示例数据集来识别可疑客户端 IP。它转换数据，使新索引包含字节总和以及不同 URL、代理、按位置列出的传入请求的数量以及每个客户端 IP 的地理目标。它还使用筛选器聚合来计算每个客户端 IP 接收的特定类型的 HTTP 响应。最终，下面的示例将 Web 日志数据转换为以实体为中心的索引，其中实体是"clientip"。

    
    
    PUT _transform/suspicious_client_ips
    {
      "source": {
        "index": "kibana_sample_data_logs"
      },
      "dest" : { __"index" : "sample_weblogs_by_clientip"
      },
      "sync" : { __"time": {
          "field": "timestamp",
          "delay": "60s"
        }
      },
      "pivot": {
        "group_by": { __"clientip": { "terms": { "field": "clientip" } }
          },
        "aggregations": {
          "url_dc": { "cardinality": { "field": "url.keyword" }},
          "bytes_sum": { "sum": { "field": "bytes" }},
          "geo.src_dc": { "cardinality": { "field": "geo.src" }},
          "agent_dc": { "cardinality": { "field": "agent.keyword" }},
          "geo.dest_dc": { "cardinality": { "field": "geo.dest" }},
          "responses.total": { "value_count": { "field": "timestamp" }},
          "success" : { __"filter": {
                "term": { "response" : "200"}}
            },
          "error404" : {
             "filter": {
                "term": { "response" : "404"}}
            },
          "error5xx" : {
             "filter": {
                "range": { "response" : { "gte": 500, "lt": 600}}}
            },
          "timestamp.min": { "min": { "field": "timestamp" }},
          "timestamp.max": { "max": { "field": "timestamp" }},
          "timestamp.duration_ms": { __"bucket_script": {
              "buckets_path": {
                "min_time": "timestamp.min.value",
                "max_time": "timestamp.max.value"
              },
              "script": "(params.max_time - params.min_time)"
            }
          }
        }
      }
    }

__

|

转换的目标索引。   ---|---    __

|

将转换配置为连续运行。它使用"时间戳"字段来同步源索引和目标索引。最坏情况下的引入延迟为 60 秒。   __

|

数据按"客户端 ip"字段分组。   __

|

筛选聚合，用于计算"响应"字段中成功 ("200") 响应的出现次数。以下两个聚合("error404"和"error5xx")按错误代码对错误响应进行计数，与精确值或一系列响应代码匹配。   __

|

此"bucket_script"根据聚合结果计算"clientip"访问的持续时间。   创建转换后，必须启动它：

    
    
    response = client.transform.start_transform(
      transform_id: 'suspicious_client_ips'
    )
    puts response
    
    
    POST _transform/suspicious_client_ips/_start

此后不久，第一个结果应该在目标索引中可用：

    
    
    response = client.search(
      index: 'sample_weblogs_by_clientip'
    )
    puts response
    
    
    GET sample_weblogs_by_clientip/_search

搜索结果显示每个客户端 IP 的数据如下：

    
    
        "hits" : [
          {
            "_index" : "sample_weblogs_by_clientip",
            "_id" : "MOeHH_cUL5urmartKj-b5UQAAAAAAAAA",
            "_score" : 1.0,
            "_source" : {
              "geo" : {
                "src_dc" : 2.0,
                "dest_dc" : 2.0
              },
              "success" : 2,
              "error404" : 0,
              "error503" : 0,
              "clientip" : "0.72.176.46",
              "agent_dc" : 2.0,
              "bytes_sum" : 4422.0,
              "responses" : {
                "total" : 2.0
              },
              "url_dc" : 2.0,
              "timestamp" : {
                "duration_ms" : 5.2191698E8,
                "min" : "2020-03-16T07:51:57.333Z",
                "max" : "2020-03-22T08:50:34.313Z"
              }
            }
          }
        ]

与其他 Kibana 示例数据集一样，Web 日志示例数据集包含相对于安装时的时间戳，包括将来的时间戳。连续转换将在数据点过去时拾取它们。如果您在一段时间前安装了 Web 日志示例数据集，则可以卸载并重新安装它，时间戳将更改。

通过此转换，可以更轻松地回答以下问题：

* 哪些客户端 IP 传输的数据量最多？  * 哪些客户端 IP 正在与大量不同的 URL 交互？  * 哪些客户端 IP 的错误率很高？  * 哪些客户端 IP 正在与大量目的地国家/地区进行交互？

### 查找每个 IP 地址的最后一个日志事件

此示例使用 Web 日志示例数据集从 IP 地址查找最后一个日志。让我们在连续模式下使用"最新"类型的转换。它将每个唯一键的最新文档从源索引复制到目标索引，并在新数据进入源索引时更新目标索引。

选择"客户端ip"字段作为唯一键;数据按此字段分组。选择"时间戳"作为按时间顺序对数据进行排序的日期字段。对于连续模式，请指定用于标识新文档的日期字段，以及检查源索引中更改之间的间隔。

!使用 Kibana 中的转换查找每个 IP 地址的最后一个日志事件

假设我们只对日志中最近出现的 IP 地址保留文档感兴趣。您可以定义保留策略并指定用于计算文档期限的日期字段。此示例使用用于对数据进行排序的相同日期字段。然后设置文档的最长期限;早于您设置的值的文档将从目标索引中删除。

!在 Kibana 中定义转换的保留策略

此转换创建目标索引，其中包含每个客户端 IP 的最新登录日期。当转换在连续模式下运行时，目标索引将更新为进入源索引的新数据。最后，由于应用的保留策略，每个超过 30 天的文档都将从目标索引中删除。

接口示例

    
    
    PUT _transform/last-log-from-clientip
    {
      "source": {
        "index": [
          "kibana_sample_data_logs"
        ]
      },
      "latest": {
        "unique_key": [ __"clientip"
        ],
        "sort": "timestamp" __},
      "frequency": "1m", __"dest": {
        "index": "last-log-from-clientip"
      },
      "sync": { __"time": {
          "field": "timestamp",
          "delay": "60s"
        }
      },
      "retention_policy": { __"time": {
          "field": "timestamp",
          "max_age": "30d"
        }
      },
      "settings": {
        "max_page_search_size": 500
      }
    }

__

|

指定用于对数据进行分组的字段。   ---|---    __

|

指定用于对数据进行排序的日期字段。   __

|

设置转换检查源索引中更改的间隔。   __

|

包含用于同步源索引和目标索引的时间字段和延迟设置。   __

|

指定转换的保留策略。早于配置值的文档将从目标索引中删除。   创建转换后，启动它：

    
    
    response = client.transform.start_transform(
      transform_id: 'last-log-from-clientip'
    )
    puts response
    
    
    POST _transform/last-log-from-clientip/_start

转换处理数据后，搜索目标索引：

    
    
    response = client.search(
      index: 'last-log-from-clientip'
    )
    puts response
    
    
    GET last-log-from-clientip/_search

搜索结果显示每个客户端 IP 的数据如下：

    
    
    {
      "_index" : "last-log-from-clientip",
      "_id" : "MOeHH_cUL5urmartKj-b5UQAAAAAAAAA",
      "_score" : 1.0,
      "_source" : {
        "referer" : "http://twitter.com/error/don-lind",
        "request" : "/elasticsearch",
        "agent" : "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)",
        "extension" : "",
        "memory" : null,
        "ip" : "0.72.176.46",
        "index" : "kibana_sample_data_logs",
        "message" : "0.72.176.46 - - [2018-09-18T06:31:00.572Z] \"GET /elasticsearch HTTP/1.1\" 200 7065 \"-\" \"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)\"",
        "url" : "https://www.elastic.co/downloads/elasticsearch",
        "tags" : [
          "success",
          "info"
        ],
        "geo" : {
          "srcdest" : "IN:PH",
          "src" : "IN",
          "coordinates" : {
            "lon" : -124.1127917,
            "lat" : 40.80338889
          },
          "dest" : "PH"
        },
        "utc_time" : "2021-05-04T06:31:00.572Z",
        "bytes" : 7065,
        "machine" : {
          "os" : "ios",
          "ram" : 12884901888
        },
        "response" : 200,
        "clientip" : "0.72.176.46",
        "host" : "www.elastic.co",
        "event" : {
          "dataset" : "sample_web_logs"
        },
        "phpmemory" : null,
        "timestamp" : "2021-05-04T06:31:00.572Z"
      }
    }

通过此转换，可以更轻松地回答以下问题：

* 与特定 IP 地址关联的最近日志事件是什么？

### 查找向服务器发送最多字节的客户端 IP

此示例使用 Web 日志示例数据集查找每小时向服务器发送最多字节的客户端 IP。该示例使用具有"top_metrics"聚合的"透视"转换。

按时间字段上的日期直方图对数据进行分组，间隔为一小时。在"字节"字段上使用最大聚合来获取发送到服务器的最大数据量。如果没有"max"聚合，API 调用仍返回发送最多字节的客户端 IP，但是，不会返回它发送的字节数。在"top_metrics"属性中，指定"clientip"和"geo.src"，然后按"bytes"字段降序对它们进行排序。转换返回发送最大数据的客户端 IP 和相应位置的 2 个字母的 ISO 代码。

    
    
    POST _transform/_preview
    {
      "source": {
        "index": "kibana_sample_data_logs"
      },
      "pivot": {
        "group_by": { __"timestamp": {
            "date_histogram": {
              "field": "timestamp",
              "fixed_interval": "1h"
            }
          }
        },
        "aggregations": {
          "bytes.max": { __"max": {
              "field": "bytes"
            }
          },
          "top": {
            "top_metrics": { __"metrics": [
                {
                  "field": "clientip"
                },
                {
                  "field": "geo.src"
                }
              ],
              "sort": {
                "bytes": "desc"
              }
            }
          }
        }
      }
    }

__

|

数据按时间间隔为一小时的时间字段的日期直方图进行分组。   ---|---    __

|

计算"字节"字段的最大值。   __

|

指定要返回的顶部文档的字段("clientip"和"geo.src")和排序方法(具有最高"字节"值的文档)。   上面的 API 调用返回类似于以下内容的响应：

    
    
    {
      "preview" : [
        {
          "top" : {
            "clientip" : "223.87.60.27",
            "geo.src" : "IN"
          },
          "bytes" : {
            "max" : 6219
          },
          "timestamp" : "2021-04-25T00:00:00.000Z"
        },
        {
          "top" : {
            "clientip" : "99.74.118.237",
            "geo.src" : "LK"
          },
          "bytes" : {
            "max" : 14113
          },
          "timestamp" : "2021-04-25T03:00:00.000Z"
        },
        {
          "top" : {
            "clientip" : "218.148.135.12",
            "geo.src" : "BR"
          },
          "bytes" : {
            "max" : 4531
          },
          "timestamp" : "2021-04-25T04:00:00.000Z"
        },
        ...
      ]
    }

### 通过客户 ID 获取客户名称和电子邮件地址

此示例使用电子商务示例数据集基于客户 ID 创建以实体为中心的索引，并使用"top_metrics"聚合获取客户名称和电子邮件地址。

按"customer_id"对数据进行分组，然后添加"top_metrics"聚合，其中"指标"是"电子邮件"、"customer_first_name.关键字"和"customer_last_name.关键字"字段。按"order_date"降序对"top_metrics"进行排序。API 调用如下所示：

    
    
    POST _transform/_preview
    {
      "source": {
        "index": "kibana_sample_data_ecommerce"
      },
      "pivot": {
        "group_by": { __"customer_id": {
            "terms": {
              "field": "customer_id"
            }
          }
        },
        "aggregations": {
          "last": {
            "top_metrics": { __"metrics": [
                {
                  "field": "email"
                },
                {
                  "field": "customer_first_name.keyword"
                },
                {
                  "field": "customer_last_name.keyword"
                }
              ],
              "sort": {
                "order_date": "desc"
              }
            }
          }
        }
      }
    }

__

|

数据按"customer_id"字段上的"术语"聚合进行分组。   ---|---    __

|

指定要按订单日期降序返回的字段(电子邮件和姓名字段)。   API 返回类似于以下内容的响应：

    
    
     {
      "preview" : [
        {
          "last" : {
            "customer_last_name.keyword" : "Long",
            "customer_first_name.keyword" : "Recip",
            "email" : "recip@long-family.zzz"
          },
          "customer_id" : "10"
        },
        {
          "last" : {
            "customer_last_name.keyword" : "Jackson",
            "customer_first_name.keyword" : "Fitzgerald",
            "email" : "fitzgerald@jackson-family.zzz"
          },
          "customer_id" : "11"
        },
        {
          "last" : {
            "customer_last_name.keyword" : "Cross",
            "customer_first_name.keyword" : "Brigitte",
            "email" : "brigitte@cross-family.zzz"
          },
          "customer_id" : "12"
        },
        ...
      ]
    }

[« Tutorial: Transforming the eCommerce sample data](ecommerce-
transforms.md) [Painless examples for transforms »](transform-painless-
examples.md)
