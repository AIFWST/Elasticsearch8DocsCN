

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `index_prefixes`](index-prefixes.md) [`fields` »](multi-fields.md)

##'元'

附加到字段的元数据。此元数据对 Elasticsearch 是不透明的，它仅对处理相同索引的多个应用程序有用，以共享有关字段(如单位)的元信息

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            latency: {
              type: 'long',
              meta: {
                unit: 'ms'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "latency": {
            "type": "long",
            "meta": {
              "unit": "ms"
            }
          }
        }
      }
    }

字段元数据强制实施最多 5 个条目，键的长度小于或等于 20，值是长度小于或等于 50 的字符串。

字段元数据可通过提交映射更新进行更新。更新的元数据将覆盖现有字段的元数据。

对象或嵌套字段不支持字段元数据。

弹性产品对字段使用以下标准元数据条目。您可以遵循这些相同的元数据约定，以获得更好的开箱即用数据体验。

unit

     The unit associated with a numeric field: `"percent"`, `"byte"` or a [time unit](api-conventions.html#time-units "Time units"). By default, a field does not have a unit. Only valid for numeric fields. The convention for percents is to use value `1` to mean `100%`. 
metric_type

     The metric type of a numeric field: `"gauge"` or `"counter"`. A gauge is a single-value measurement that can go up or down over time, such as a temperature. A counter is a single-value cumulative counter that only goes up, such as the number of requests processed by a web server, or resets to 0 (zero). By default, no metric type is associated with a field. Only valid for numeric fields. 

[« `index_prefixes`](index-prefixes.md) [`fields` »](multi-fields.md)
