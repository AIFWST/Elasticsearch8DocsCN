

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Date field type](date.md) [Dense vector field type »](dense-vector.md)

## 日期纳秒字段类型

此数据类型是对"日期"数据类型的补充。然而，两者之间有一个重要的区别。现有的"日期"数据类型以毫秒分辨率存储日期。"date_nanos"数据类型存储以纳秒分辨率存储日期，这限制了其日期范围，从大约 1970 年到 2262 年，因为日期仍然存储为表示自纪元以来的纳秒的长整型。

纳秒查询在内部转换为此长表示形式的范围查询，聚合和存储字段的结果将转换回字符串，具体取决于与字段关联的日期格式。

可以自定义日期格式，但如果未指定"格式"，则使用默认值：

    
    
        "strict_date_optional_time_nanos||epoch_millis"

例如：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            date: {
              type: 'date_nanos'
            }
          }
        }
      }
    )
    puts response
    
    response = client.bulk(
      index: 'my-index-000001',
      refresh: true,
      body: [
        {
          index: {
            _id: '1'
          }
        },
        {
          date: '2015-01-01'
        },
        {
          index: {
            _id: '2'
          }
        },
        {
          date: '2015-01-01T12:10:30.123456789Z'
        },
        {
          index: {
            _id: '3'
          }
        },
        {
          date: 1_420_070_400_000
        }
      ]
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        sort: {
          date: 'asc'
        },
        runtime_mappings: {
          date_has_nanos: {
            type: 'boolean',
            script: "emit(doc['date'].value.nano != 0)"
          }
        },
        fields: [
          {
            field: 'date',
            format: 'strict_date_optional_time_nanos'
          },
          {
            field: 'date_has_nanos'
          }
        ]
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "date": {
            "type": "date_nanos" __}
        }
      }
    }
    
    PUT my-index-000001/_bulk?refresh
    { "index" : { "_id" : "1" } }
    { "date": "2015-01-01" } __{ "index" : { "_id" : "2" } }
    { "date": "2015-01-01T12:10:30.123456789Z" } __{ "index" : { "_id" : "3" } }
    { "date": 1420070400000 } __GET my-index-000001/_search
    {
      "sort": { "date": "asc"}, __"runtime_mappings": {
        "date_has_nanos": {
          "type": "boolean",
          "script": "emit(doc['date'].value.nano != 0)" __}
      },
      "fields": [
        {
          "field": "date",
          "format": "strict_date_optional_time_nanos" __},
        {
          "field": "date_has_nanos"
        }
      ]
    }

__

|

"日期"字段使用默认的"格式"。   ---|---    __

|

本文档使用纯日期。   __

|

本文档包括一个时间。   __

|

本文档使用自纪元以来的毫秒。   __

|

请注意，返回的"sort"值均以自纪元以来的纳秒为单位。   __

|

在脚本中使用".nano"返回日期的纳秒部分。   __

|

您可以在使用"fields"参数获取数据时指定格式。使用"strict_date_optional_time_nanos"，否则您将获得四舍五入的结果。   您还可以指定由"||`.可以使用与"日期"字段相同的映射参数。

日期纳秒将接受带有小数点的数字，例如"{"date"：1618249875.123456}"，但在某些情况下(#70085)，我们会在这些日期上失去精度，因此应避免使用它们。

###Limitations

聚合仍以毫秒级分辨率运行，即使使用"date_nanos"字段也是如此。此限制也会影响转换。

* * *

### 合成的"_source"

合成"_source"仅对 TSDB 索引(将"index.mode"设置为"time_series"的索引)正式发布。对于其他指数，合成"_source"处于技术预览状态。技术预览版中的功能可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

"date_nanos"字段在其默认配置中支持合成"_source"。合成"_source"不能与"copy_to"、"ignore_malformed"设置为 true 或禁用"doc_values"一起使用。

合成源始终对"date_nanos"字段进行排序。例如：

    
    
    response = client.indices.create(
      index: 'idx',
      body: {
        mappings: {
          _source: {
            mode: 'synthetic'
          },
          properties: {
            date: {
              type: 'date_nanos'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'idx',
      id: 1,
      body: {
        date: [
          '2015-01-01T12:10:30.000Z',
          '2014-01-01T12:10:30.000Z'
        ]
      }
    )
    puts response
    
    
    PUT idx
    {
      "mappings": {
        "_source": { "mode": "synthetic" },
        "properties": {
          "date": { "type": "date_nanos" }
        }
      }
    }
    PUT idx/_doc/1
    {
      "date": ["2015-01-01T12:10:30.000Z", "2014-01-01T12:10:30.000Z"]
    }

将成为：

    
    
    {
      "date": ["2014-01-01T12:10:30.000Z", "2015-01-01T12:10:30.000Z"]
    }

[« Date field type](date.md) [Dense vector field type »](dense-vector.md)
