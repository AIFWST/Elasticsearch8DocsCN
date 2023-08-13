

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `store`](mapping-store.md) [`term_vector` »](term-vector.md)

##'子对象'

在为文档编制索引或更新映射时，Elasticsearch 接受名称中包含点的字段，这些字段会扩展为其相应的对象结构。例如，字段"metrics.time.max"被映射为具有父"time"对象的"max"叶字段，该对象属于其父"metrics"对象。

所描述的默认行为在大多数情况下是合理的，但在某些情况下会导致问题，例如字段"metrics.time"也包含值，这在索引指标数据时很常见。同时保存"metrics.time.max"和"metrics.time"值的文档被拒绝，因为"time"需要是一个叶字段来保存一个值，以及一个对象来保存一个"max"子字段。

"子对象"设置只能应用于顶级映射定义和"对象"字段，它禁用了对象保存更多子对象的能力，并使得存储字段名称包含点并共享公共前缀的文档成为可能。从上面的例子中，如果对象容器"度量"将"子对象"设置为"false"，它可以直接保存"time"和"time.max"的值，而无需任何中间对象，因为字段名称中的点被保留。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            metrics: {
              type: 'object',
              subobjects: false
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 'metric_1',
      body: {
        "metrics.time": 100,
        "metrics.time.min": 10,
        "metrics.time.max": 900
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 'metric_2',
      body: {
        metrics: {
          time: 100,
          "time.min": 10,
          "time.max": 900
        }
      }
    )
    puts response
    
    response = client.indices.get_mapping(
      index: 'my-index-000001'
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "metrics": {
            "type":  "object",
            "subobjects": false __}
        }
      }
    }
    
    PUT my-index-000001/_doc/metric_1
    {
      "metrics.time" : 100, __"metrics.time.min" : 10,
      "metrics.time.max" : 900
    }
    
    PUT my-index-000001/_doc/metric_2
    {
      "metrics" : {
        "time" : 100, __"time.min" : 10,
        "time.max" : 900
      }
    }
    
    GET my-index-000001/_mapping
    
    
    {
      "my-index-000001" : {
        "mappings" : {
          "properties" : {
            "metrics" : {
              "subobjects" : false,
              "properties" : {
                "time" : {
                  "type" : "long"
                },
                "time.min" : { __"type" : "long"
                },
                "time.max" : {
                  "type" : "long"
                }
              }
            }
          }
        }
      }
    }

__

|

"指标"字段不能容纳其他对象。   ---|---    __

|

包含平面路径的示例文档 __

|

保存对象(配置为不保存子对象)及其叶子字段 __ 的示例文档

|

保留字段名称中的点的结果映射 整个映射可能配置为不支持子对象，在这种情况下，文档只能包含叶子字段：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          subobjects: false
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 'metric_1',
      body: {
        time: '100ms',
        "time.min": '10ms',
        "time.max": '900ms'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "subobjects": false __}
    }
    
    PUT my-index-000001/_doc/metric_1
    {
      "time" : "100ms", __"time.min" : "10ms",
      "time.max" : "900ms"
    }

__

|

整个映射配置为不支持对象。   ---|---    __

|

文档不支持对象 无法更新现有字段和顶级映射定义的"子对象"设置。

[« `store`](mapping-store.md) [`term_vector` »](term-vector.md)
