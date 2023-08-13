

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Runtime fields](runtime.md)

[« Runtime fields](runtime.md) [Define runtime fields in a search request
»](runtime-search-request.md)

## 映射运行时字段

您可以通过在映射定义下添加"运行时"部分并定义无痛脚本来映射运行时字段。此脚本可以访问文档的整个上下文，包括通过"params._source"的原始"_source"和任何映射字段及其值。在查询时，脚本将运行并为查询所需的每个脚本化字段生成值。

**发出运行时字段值**

定义用于运行时字段的无痛脚本时，必须包含"emit"方法以发出计算值。

例如，以下请求中的脚本根据定义为"日期"类型的"@timestamp"字段计算星期几。该脚本根据"时间戳"的值计算星期几，并使用"发出"返回计算值。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          runtime: {
            day_of_week: {
              type: 'keyword',
              script: {
                source: "emit(doc['@timestamp'].value.dayOfWeekEnum.getDisplayName(TextStyle.FULL, Locale.ROOT))"
              }
            }
          },
          properties: {
            "@timestamp": {
              type: 'date'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/
    {
      "mappings": {
        "runtime": {
          "day_of_week": {
            "type": "keyword",
            "script": {
              "source": "emit(doc['@timestamp'].value.dayOfWeekEnum.getDisplayName(TextStyle.FULL, Locale.ROOT))"
            }
          }
        },
        "properties": {
          "@timestamp": {"type": "date"}
        }
      }
    }

"运行时"部分可以是以下任何数据类型：

* "布尔值" * "复合" * "日期" * "双精度" * "geo_point" * "IP" * "关键字" * "长" * "查找"

"类型"为"date"的运行时字段可以完全接受"format"参数作为"date"字段类型。

具有"查找"类型"的运行时字段允许从相关索引中检索字段。请参阅"从相关索引中检索字段"。

如果在将"dynamic"参数设置为"运行时"的情况下启用了动态字段映射，则新字段将自动作为运行时字段添加到索引映射中：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          dynamic: 'runtime',
          properties: {
            "@timestamp": {
              type: 'date'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "dynamic": "runtime",
        "properties": {
          "@timestamp": {
            "type": "date"
          }
        }
      }
    }

### 定义不带脚本的运行时字段

运行时字段通常包括以某种方式操作数据的无痛脚本。但是，在某些情况下，您可以定义运行时field_without_脚本。例如，如果要从"_source"中检索单个字段而不进行更改，则不需要脚本。您可以只创建一个没有脚本的运行时字段，例如"day_of_week"：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          runtime: {
            day_of_week: {
              type: 'keyword'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/
    {
      "mappings": {
        "runtime": {
          "day_of_week": {
            "type": "keyword"
          }
        }
      }
    }

当未提供脚本时，Elasticsearch 会在查询时间_source中隐式查找与运行时字段同名的字段，如果存在，则返回 avalue。如果不存在同名字段，则响应不包含该运行时字段的任何值。

在大多数情况下，尽可能通过"doc_values"检索字段值。由于数据是从 Lucene 加载的方式，使用运行时字段访问"doc_values"比从"_source"检索值更快。

但是，在某些情况下，需要从"_source"中检索字段。例如，默认情况下，"文本"字段没有可用的"doc_values"，因此您必须从"_source"中检索值。在其他情况下，您可以选择在特定字段上禁用"doc_values"。

您也可以在要检索其值的字段前面加上"params._source"(例如"params._source.day_of_week")。为简单起见，建议尽可能在映射定义中定义运行时字段而不使用脚本。

### 忽略运行时字段上的脚本错误

脚本可能会在运行时抛出错误，例如，在访问文档中缺失或无效的值时，或者由于执行无效操作。发生这种情况时，"on_script_error"参数可用于控制错误行为。将此参数设置为"continue"将具有静默忽略此运行时字段上的所有错误的效果。默认的"fail"值将导致分片失败，该故障将在搜索响应中报告。

### 更新和删除运行时字段

您可以随时更新或删除运行时字段。要替换现有的运行时字段，请将新的运行时字段添加到具有相同名称的映射中。要从映射中删除运行时字段，请将运行时字段的值设置为"null"：

    
    
    response = client.indices.put_mapping(
      index: 'my-index-000001',
      body: {
        runtime: {
          day_of_week: nil
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_mapping
    {
     "runtime": {
       "day_of_week": null
     }
    }

**下游影响**

在相关查询运行时更新或删除运行时字段可能会返回不一致的结果。每个分片可能有权访问脚本的不同版本，具体取决于映射更改何时生效。

如果您删除或更新 Kibana 中依赖于运行时字段的现有查询或可视化可能会失败。例如，如果类型更改为"布尔值"或删除运行时字段，则使用类型为"ip"的运行时字段的条形图可视化将失败。

[« Runtime fields](runtime.md) [Define runtime fields in a search request
»](runtime-search-request.md)
