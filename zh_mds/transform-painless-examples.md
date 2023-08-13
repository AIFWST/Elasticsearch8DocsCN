

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Roll up or
transform your data](data-rollup-transform.md) ›[Transforming
data](transforms.md)

[« Transform examples](transform-examples.md) [Transform limitations
»](transform-limitations.md)

## 转换的无痛示例

这些示例演示了如何在转换中使用无痛。您可以在无痛指南中了解有关无痛脚本语言的更多信息。

* 使用脚本化指标聚合获取热门 * 使用聚合获取时间要素 * 使用存储桶脚本获取持续时间 * 使用脚本化指标聚合对 HTTP 响应进行计数 * 使用脚本化指标聚合比较索引 * 使用脚本化指标聚合获取 Web 会话详细信息

* 虽然以下示例的上下文是转换用例，但以下代码段中的 Painless 脚本也可以在其他 Elasticsearch 搜索聚合中使用。  * 以下所有示例都使用脚本，当脚本创建字段时，转换无法推断输出字段的映射。转换不会在目标索引中为这些字段创建任何映射，这意味着它们会被动态映射。在开始转换之前创建目标索引，以防需要显式映射。

### 使用脚本化指标聚合获取热门

此代码段显示如何查找最新文档，换句话说，具有最新时间戳的文档。从技术角度来看，它通过在提供指标输出的转换中使用脚本化指标聚合来帮助实现热门命中的功能。

    
    
    "aggregations": {
      "latest_doc": {
        "scripted_metric": {
          "init_script": "state.timestamp_latest = 0L; state.last_doc = ''", __"map_script": """ __def current_date = doc['@timestamp'].getValue().toInstant().toEpochMilli();
            if (current_date > state.timestamp_latest)
            {state.timestamp_latest = current_date;
            state.last_doc = new HashMap(params['_source']);}
          """,
          "combine_script": "return state", __"reduce_script": """ __def last_doc = '';
            def timestamp_latest = 0L;
            for (s in states) {if (s.timestamp_latest > (timestamp_latest))
            {timestamp_latest = s.timestamp_latest; last_doc = s.last_doc;}}
            return last_doc
          """
        }
      }
    }

__

|

"init_script"在"state"对象中创建长类型"timestamp_latest"和字符串类型"last_doc"。   ---|---    __

|

"map_script"根据文档的时间戳定义"current_date"，然后将"current_date"与"state.timestamp_latest"进行比较，最后从分片返回"state.last_doc"。通过使用"新哈希图(...)' 复制源文档，每当您想要将 fullsource 对象从一个阶段传递到下一个阶段时，这一点很重要。   __

|

"combine_script"从每个分片返回"状态"。   __

|

"reduce_script"遍历每个分片返回的"s.timestamp_latest"值，并返回具有最新时间戳("last_doc")的文档。在响应中，排名靠前的命中(换句话说，"latest_doc")嵌套在"latest_doc"字段下方。   检查脚本的范围，以获取有关相应脚本的详细说明。

您可以通过类似的方式检索最后一个值：

    
    
    "aggregations": {
      "latest_value": {
        "scripted_metric": {
          "init_script": "state.timestamp_latest = 0L; state.last_value = ''",
          "map_script": """
            def current_date = doc['@timestamp'].getValue().toInstant().toEpochMilli();
            if (current_date > state.timestamp_latest)
            {state.timestamp_latest = current_date;
            state.last_value = params['_source']['value'];}
          """,
          "combine_script": "return state",
          "reduce_script": """
            def last_value = '';
            def timestamp_latest = 0L;
            for (s in states) {if (s.timestamp_latest > (timestamp_latest))
            {timestamp_latest = s.timestamp_latest; last_value = s.last_value;}}
            return last_value
          """
        }
      }
    }

##### 使用存储脚本获取热门

您还可以使用存储脚本的强大功能来获取最新值。存储的脚本可缩短编译时间，加快搜索速度，并且可更新。

1. 创建存储的脚本： POST _scripts/last-value-map-init { "script"： { "lang"： "painless"， "source"： """ state.timestamp_latest = 0L;state.last_value = '' """ } } POST _scripts/last-value-map { "script"： { "lang"： "painless"， "source"： """ def current_date = doc['@timestamp'].getValue().toInstant().toEpochMilli();           如果 (current_date > state.timestamp_latest) {state.timestamp_latest = current_date;           state.last_value = doc[params['key']].value;}       """ } } POST _scripts/last-value-combine { "script"： { "lang"： "painless"， "source"： """ return state """ } } POST _scripts/last-value-reduce { "script"： { "lang"： "painless"， "source"： """ def last_value = '';           定义 timestamp_latest = 0L;           for (s in states) {if (s.timestamp_latest > (timestamp_latest)) {timestamp_latest = s.timestamp_latest; last_value = s.last_value;}}           返回 last_value """ } }

2. 在脚本化指标聚合中使用存储的脚本。           "aggregations"：{ "latest_value"：{ "scripted_metric"：{ "init_script"：{ "id"："last-value-map-init" }， "map_script"：{ "id"："last-value-map"， "params"：{ "key"："field_with_last_value" __} }， "combine_script"：{ "id"："last-value-combine" }， "reduce_script"：{ "id"："last-value-reduce" }

__

|

参数"field_with_last_value"可以设置为您想要最新值的任何字段。   ---|---   

### 使用聚合获取时间特征

此代码片段显示了如何在转换中使用无痛提取基于时间的特征。代码段使用索引，其中"@timestamp"定义为"日期"类型字段。

    
    
    "aggregations": {
      "avg_hour_of_day": { __"avg":{
          "script": { __"source": """
              ZonedDateTime date =  doc['@timestamp'].value; __return date.getHour(); __"""
          }
        }
      },
      "avg_month_of_year": { __"avg":{
          "script": { __"source": """
              ZonedDateTime date =  doc['@timestamp'].value; __return date.getMonthValue(); __"""
          }
        }
      },
     ...
    }

__

|

聚合的名称。   ---|---    __

|

包含返回一天中的小时数的无痛脚本。   __

|

根据文档的时间戳设置"日期"。   __

|

返回"date"中的小时值。   __

|

聚合的名称。   __

|

包含返回一年中月份的无痛脚本。   __

|

根据文档的时间戳设置"日期"。   __

|

返回"日期"中的月份值。   ### 使用存储桶脚本编辑获取持续时间

此示例说明如何使用存储桶脚本从数据日志中按客户端 IP 获取会话的持续时间。该示例使用 Kibana 示例 Web 日志数据集。

    
    
    PUT _transform/data_log
    {
      "source": {
        "index": "kibana_sample_data_logs"
      },
      "dest": {
        "index": "data-logs-by-client"
      },
      "pivot": {
        "group_by": {
          "machine.os": {"terms": {"field": "machine.os.keyword"}},
          "machine.ip": {"terms": {"field": "clientip"}}
        },
        "aggregations": {
          "time_frame.lte": {
            "max": {
              "field": "timestamp"
            }
          },
          "time_frame.gte": {
            "min": {
              "field": "timestamp"
            }
          },
          "time_length": { __"bucket_script": {
              "buckets_path": { __"min": "time_frame.gte.value",
                "max": "time_frame.lte.value"
              },
              "script": "params.max - params.min" __}
          }
        }
      }
    }

__

|

为了定义会话的长度，我们使用存储桶脚本。   ---|---    __

|

存储桶路径是脚本变量及其关联路径的映射，指向要用于该变量的存储桶。在这种特殊情况下，"min"和"max"是映射到"time_frame.gte.value"和"time_frame.lte.value"的变量。   __

|

最后，脚本从结束日期中减去会话的开始日期，这会导致会话的持续时间。   ### 使用脚本化指标聚合对 HTTP 响应进行计数编辑

您可以通过使用脚本化指标聚合作为转换的一部分来计算 Web 日志数据集中的不同 HTTP 响应类型。您可以使用过滤器聚合实现类似的功能，有关详细信息，请查看查找可疑客户端 IP 示例。

下面的示例假定 HTTP 响应代码作为关键字存储在文档的"响应"字段中。

    
    
    "aggregations": { __"responses.counts": { __"scripted_metric": { __"init_script": "state.responses = ['error':0L,'success':0L,'other':0L]", __"map_script": """ __def code = doc['response.keyword'].value;
            if (code.startsWith('5') || code.startsWith('4')) {
              state.responses.error += 1 ;
            } else if(code.startsWith('2')) {
              state.responses.success += 1;
            } else {
              state.responses.other += 1;
            }
            """,
          "combine_script": "state.responses", __"reduce_script": """ __def counts = ['error': 0L, 'success': 0L, 'other': 0L];
            for (responses in states) {
              counts.error += responses['error'];
              counts.success += responses['success'];
              counts.other += responses['other'];
            }
            return counts;
            """
          }
        },
      ...
    }

__

|

包含所有聚合的转换的"聚合"对象。   ---|---    __

|

"scripted_metric"聚合的对象。   __

|

此"scripted_metric"对 Web 日志数据执行分布式操作，以计算特定类型的 HTTP 响应(错误、成功和其他)。   __

|

"init_script"在"状态"对象中创建一个"响应"数组，该数组具有长数据类型的三个属性("错误"、"成功"、"其他")。   __

|

"map_script"根据文档的"response.keyword"值定义"代码"，然后根据响应的第一个数字计算错误、成功和其他响应。   __

|

"combine_script"从每个分片返回"state.responses"。   __

|

"reduce_script"创建一个具有"错误"、"成功"和"其他"属性的"counts"数组，然后遍历每个分片返回的"响应"值，并将不同的响应类型分配给"counts"对象的适当属性;对错误计数的错误响应、对成功计数的成功响应以及对其他计数的其他响应。最后，返回包含响应计数的"counts"数组。   ### 使用脚本化指标聚合比较索引编辑

此示例演示如何通过使用脚本化指标聚合的转换来比较两个索引的内容。

    
    
    POST _transform/_preview
    {
      "id" : "index_compare",
      "source" : { __"index" : [
          "index1",
          "index2"
        ],
        "query" : {
          "match_all" : { }
        }
      },
      "dest" : { __"index" : "compare"
      },
      "pivot" : {
        "group_by" : {
          "unique-id" : {
            "terms" : {
              "field" : " <unique-id-field>" __}
          }
        },
        "aggregations" : {
          "compare" : { __"scripted_metric" : {
              "map_script" : "state.doc = new HashMap(params['_source'])", __"combine_script" : "return state", __"reduce_script" : """ __if (states.size() != 2) {
                  return "count_mismatch"
                }
                if (states.get(0).equals(states.get(1))) {
                  return "match"
                } else {
                  return "mismatch"
                }
                """
            }
          }
        }
      }
    }

__

|

"源"对象中引用的索引相互比较。   ---|---    __

|

"dest"索引包含比较结果。   __

|

"group_by"字段需要是每个文档的唯一标识符。   __

|

"scripted_metric"聚合的对象。   __

|

"map_script"在状态对象中定义"doc"。通过使用'newHashMap(...)' 复制源文档，每当您想要将完整的源对象从一个阶段传递到下一个阶段时，这一点很重要。   __

|

"combine_script"从每个分片返回"状态"。   __

|

"reduce_script"检查索引的大小是否相等。如果它们不相等，则报告"count_mismatch"。然后，它遍历两个指数的所有值并进行比较。如果值相等，则返回"匹配"，否则返回"不匹配"。   ### 使用脚本化指标聚合编辑获取 Web 会话详细信息

此示例演示如何从单个事务派生多个特征。让我们从数据中看一下示例源文档：

源文档

    
    
    {
      "_index":"apache-sessions",
      "_type":"_doc",
      "_id":"KvzSeGoB4bgw0KGbE3wP",
      "_score":1.0,
      "_source":{
        "@timestamp":1484053499256,
        "apache":{
          "access":{
            "sessionid":"571604f2b2b0c7b346dc685eeb0e2306774a63c2",
            "url":"http://www.leroymerlin.fr/v3/search/search.do?keyword=Carrelage%20salle%20de%20bain",
            "path":"/v3/search/search.do",
            "query":"keyword=Carrelage%20salle%20de%20bain",
            "referrer":"http://www.leroymerlin.fr/v3/p/produits/carrelage-parquet-sol-souple/carrelage-sol-et-mur/decor-listel-et-accessoires-carrelage-mural-l1308217717?resultOffset=0&resultLimit=51&resultListShape=MOSAIC&priceStyle=SALEUNIT_PRICE",
            "user_agent":{
              "original":"Mobile Safari 10.0 Mac OS X (iPad) Apple Inc.",
              "os_name":"Mac OS X (iPad)"
            },
            "remote_ip":"0337b1fa-5ed4-af81-9ef4-0ec53be0f45d",
            "geoip":{
              "country_iso_code":"FR",
              "location":{
                "lat":48.86,
                "lon":2.35
              }
            },
            "response_code":200,
            "method":"GET"
          }
        }
      }
    }
    ...

通过使用"sessionid"作为分组依据字段，您可以通过会话枚举事件，并使用脚本化度量聚合获取会话的更多详细信息。

    
    
    POST _transform/_preview
    {
      "source": {
        "index": "apache-sessions"
      },
      "pivot": {
        "group_by": {
          "sessionid": { __"terms": {
              "field": "apache.access.sessionid"
            }
          }
        },
        "aggregations": { __"distinct_paths": {
            "cardinality": {
              "field": "apache.access.path"
            }
          },
          "num_pages_viewed": {
            "value_count": {
              "field": "apache.access.url"
            }
          },
          "session_details": {
            "scripted_metric": {
              "init_script": "state.docs = []", __"map_script": """ __Map span = [
                  '@timestamp':doc['@timestamp'].value,
                  'url':doc['apache.access.url'].value,
                  'referrer':doc['apache.access.referrer'].value
                ];
                state.docs.add(span)
              """,
              "combine_script": "return state.docs;", __"reduce_script": """ __def all_docs = [];
                for (s in states) {
                  for (span in s) {
                    all_docs.add(span);
                  }
                }
                all_docs.sort((HashMap o1, HashMap o2)- >o1['@timestamp'].toEpochMilli().compareTo(o2['@timestamp'].toEpochMilli()));
                def size = all_docs.size();
                def min_time = all_docs[0]['@timestamp'];
                def max_time = all_docs[size-1]['@timestamp'];
                def duration = max_time.toEpochMilli() - min_time.toEpochMilli();
                def entry_page = all_docs[0]['url'];
                def exit_path = all_docs[size-1]['url'];
                def first_referrer = all_docs[0]['referrer'];
                def ret = new HashMap();
                ret['first_time'] = min_time;
                ret['last_time'] = max_time;
                ret['duration'] = duration;
                ret['entry_page'] = entry_page;
                ret['exit_path'] = exit_path;
                ret['first_referrer'] = first_referrer;
                return ret;
              """
            }
          }
        }
      }
    }

__

|

数据按"会话 ID"分组。   ---|---    __

|

聚合计算路径数，并在会话期间枚举查看的页面。   __

|

"init_script"在"状态"对象中创建数组类型"doc"。   __

|

"map_script"定义了一个"span"数组，其中包含时间戳，URL和基于文档相应值的引用值，然后将"span"数组的值添加到"doc"对象中。   __

|

"combine_script"从每个分片返回"state.docs"。   __

|

"reduce_script"根据文档字段定义各种对象，如"min_time"、"max_time"和"持续时间"，然后声明一个"ret"对象，并使用"new HashMap ()"复制源文档。接下来，脚本根据之前定义的对应对象定义 'ret' 对象内的 'first_time'、'last_time'、'duration' 等字段，最后返回 'ret'。   API 调用会产生类似的响应：

    
    
    {
      "num_pages_viewed" : 2.0,
      "session_details" : {
        "duration" : 100300001,
        "first_referrer" : "https://www.bing.com/",
        "entry_page" : "http://www.leroymerlin.fr/v3/p/produits/materiaux-menuiserie/porte-coulissante-porte-interieure-escalier-et-rambarde/barriere-de-securite-l1308218463",
        "first_time" : "2017-01-10T21:22:52.982Z",
        "last_time" : "2017-01-10T21:25:04.356Z",
        "exit_path" : "http://www.leroymerlin.fr/v3/p/produits/materiaux-menuiserie/porte-coulissante-porte-interieure-escalier-et-rambarde/barriere-de-securite-l1308218463?__result-wrapper?pageTemplate=Famille%2FMat%C3%A9riaux+et+menuiserie&resultOffset=0&resultLimit=50&resultListShape=PLAIN&nomenclatureId=17942&priceStyle=SALEUNIT_PRICE&fcr=1&*4294718806=4294718806&*14072=14072&*4294718593=4294718593&*17942=17942"
      },
      "distinct_paths" : 1.0,
      "sessionid" : "000046f8154a80fd89849369c984b8cc9d795814"
    },
    {
      "num_pages_viewed" : 10.0,
      "session_details" : {
        "duration" : 343100405,
        "first_referrer" : "https://www.google.fr/",
        "entry_page" : "http://www.leroymerlin.fr/",
        "first_time" : "2017-01-10T16:57:39.937Z",
        "last_time" : "2017-01-10T17:03:23.049Z",
        "exit_path" : "http://www.leroymerlin.fr/v3/p/produits/porte-de-douche-coulissante-adena-e168578"
      },
      "distinct_paths" : 8.0,
      "sessionid" : "000087e825da1d87a332b8f15fa76116c7467da6"
    }
    ...

[« Transform examples](transform-examples.md) [Transform limitations
»](transform-limitations.md)
