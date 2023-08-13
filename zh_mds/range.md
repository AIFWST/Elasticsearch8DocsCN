

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Point field type](point.md) [Rank feature field type »](rank-
feature.md)

## 范围字段类型

范围字段类型表示上限和下限之间的连续值范围。例如，范围可以用 0 到 9_ October_或_anyinteger表示日期_any。它们使用运算符"gt"或"gte"表示下限，使用"lt"或"lte"表示上限。它们可用于查询，并且对聚合的支持有限。唯一支持的聚合是直方图，基数。

支持以下范围类型：

`integer_range`

|

最小值为"-231"，最大值为"231-1"的有符号 32 位整数范围。   ---|--- "float_range"

|

一系列单精度 32 位 IEEE 754 浮点值。   "long_range"

|

最小值为"-263"，最大值为"263-1"的有符号 64 位整数范围。   "double_range"

|

一系列双精度 64 位 IEEE 754 浮点值。   "date_range"

|

"日期"值的范围。日期范围通过"格式"映射参数支持各种日期格式。无论使用何种格式，日期值都会解析为无符号的 64 位整数，表示自 Unix 纪元 inUTC 以来的毫秒数。不支持包含"now"日期数学表达式的值。   "ip_range"

|

支持 IPv4 或 IPv6(或混合)地址的 IP 值范围。   下面是使用各种范围字段配置映射的示例，后面是索引多个范围类型的示例。

    
    
    response = client.indices.create(
      index: 'range_index',
      body: {
        settings: {
          number_of_shards: 2
        },
        mappings: {
          properties: {
            expected_attendees: {
              type: 'integer_range'
            },
            time_frame: {
              type: 'date_range',
              format: 'yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'range_index',
      id: 1,
      refresh: true,
      body: {
        expected_attendees: {
          gte: 10,
          lt: 20
        },
        time_frame: {
          gte: '2015-10-31 12:00:00',
          lte: '2015-11-01'
        }
      }
    )
    puts response
    
    
    PUT range_index
    {
      "settings": {
        "number_of_shards": 2
      },
      "mappings": {
        "properties": {
          "expected_attendees": {
            "type": "integer_range"
          },
          "time_frame": {
            "type": "date_range", __"format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
          }
        }
      }
    }
    
    PUT range_index/_doc/1?refresh
    {
      "expected_attendees" : { __"gte" : 10,
        "lt" : 20
      },
      "time_frame" : {
        "gte" : "2015-10-31 12:00:00", __"lte" : "2015-11-01"
      }
    }

__

|

"date_range"类型接受由"date"类型定义的相同字段参数。   ---|---    __

|

例如，为包含 10 到 20 名与会者(不包括 20 名与会者)的会议编制索引。   __

|

使用日期时间戳的示例日期范围。   以下是对名为"expected_attendees"的"integer_range"字段的术语查询示例。12 是范围内的值，因此它将匹配。

    
    
    response = client.search(
      index: 'range_index',
      body: {
        query: {
          term: {
            expected_attendees: {
              value: 12
            }
          }
        }
      }
    )
    puts response
    
    
    GET range_index/_search
    {
      "query" : {
        "term" : {
          "expected_attendees" : {
            "value": 12
          }
        }
      }
    }

上述查询生成的结果。

    
    
    {
      "took": 13,
      "timed_out": false,
      "_shards" : {
        "total": 2,
        "successful": 2,
        "skipped" : 0,
        "failed": 0
      },
      "hits" : {
        "total" : {
            "value": 1,
            "relation": "eq"
        },
        "max_score" : 1.0,
        "hits" : [
          {
            "_index" : "range_index",
            "_id" : "1",
            "_score" : 1.0,
            "_source" : {
              "expected_attendees" : {
                "gte" : 10, "lt" : 20
              },
              "time_frame" : {
                "gte" : "2015-10-31 12:00:00", "lte" : "2015-11-01"
              }
            }
          }
        ]
      }
    }

以下是对名为"time_frame"的"date_range"字段的"date_range"查询示例。

    
    
    response = client.search(
      index: 'range_index',
      body: {
        query: {
          range: {
            time_frame: {
              gte: '2015-10-31',
              lte: '2015-11-01',
              relation: 'within'
            }
          }
        }
      }
    )
    puts response
    
    
    GET range_index/_search
    {
      "query" : {
        "range" : {
          "time_frame" : { __"gte" : "2015-10-31",
            "lte" : "2015-11-01",
            "relation" : "within" __}
        }
      }
    }

__

|

范围查询的工作方式与范围查询中所述相同。   ---|---    __

|

对范围字段的范围查询支持"关系"参数，该参数可以是"WITHIN"、"CONTAINS"、"ITSECTS"(默认值)之一。   此查询生成类似的结果：

    
    
    {
      "took": 13,
      "timed_out": false,
      "_shards" : {
        "total": 2,
        "successful": 2,
        "skipped" : 0,
        "failed": 0
      },
      "hits" : {
        "total" : {
            "value": 1,
            "relation": "eq"
        },
        "max_score" : 1.0,
        "hits" : [
          {
            "_index" : "range_index",
            "_id" : "1",
            "_score" : 1.0,
            "_source" : {
              "expected_attendees" : {
                "gte" : 10, "lt" : 20
              },
              "time_frame" : {
                "gte" : "2015-10-31 12:00:00", "lte" : "2015-11-01"
              }
            }
          }
        ]
      }
    }

### 知识产权

除了上述范围格式外，还可以以 CIDR 表示法提供 IP 范围：

    
    
    response = client.indices.put_mapping(
      index: 'range_index',
      body: {
        properties: {
          ip_allowlist: {
            type: 'ip_range'
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'range_index',
      id: 2,
      body: {
        ip_allowlist: '192.168.0.0/16'
      }
    )
    puts response
    
    
    PUT range_index/_mapping
    {
      "properties": {
        "ip_allowlist": {
          "type": "ip_range"
        }
      }
    }
    
    PUT range_index/_doc/2
    {
      "ip_allowlist" : "192.168.0.0/16"
    }

### 范围字段的参数

范围类型接受以下参数：

"胁迫"

|

尝试将字符串转换为数字并截断整数的分数。接受"真"(默认值)和"假"。   ---|--- "索引"

|

该字段是否应可搜索？接受"真"(默认值)和"假"。   "商店"

|

字段值是否应与"_source"字段分开存储和检索。接受"真"或"假"(默认值)。   « 点字段类型 排名特征字段类型 »