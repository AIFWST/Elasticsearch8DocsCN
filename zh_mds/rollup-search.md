

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Rollup APIs](rollup-apis.md)

[« Get rollup index capabilities API](rollup-get-rollup-index-caps.md)
[Start rollup jobs API »](rollup-start-job.md)

## 汇总搜索

允许使用标准查询 DSL 搜索汇总数据。

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

对于版本 8.5 及更高版本，我们建议对汇总进行缩减采样，以降低时序数据的存储成本。

###Request

"获取<target>/_rollup_search"

###Description

之所以需要汇总搜索终结点，是因为在内部，汇总文档使用的文档结构与原始数据不同。rollupsearch 终结点将标准查询 DSL 重写为与汇总文档匹配的格式，然后获取响应并将其重写回客户端在给定原始查询时所期望的内容。

### 路径参数

`<target>`

    

(必需，字符串)用于限制请求的数据流和索引的逗号分隔列表。支持通配符表达式 ('*')。

此目标可以包括汇总索引和非汇总索引。

"<target>"参数的规则：

* 必须至少指定一个数据流、索引或通配符表达式。此目标可以包括汇总索引或非汇总索引。对于数据流，流的支持索引只能用作非汇总索引。不允许省略"<target>"参数或使用"_all"。  * 可以指定多个非汇总索引。  * 只能指定一个汇总索引。如果提供了多个，则会发生异常。  * 可以使用通配符表达式，但如果它们与多个汇总索引匹配，则会发生异常。但是，您可以使用表达式来匹配多个非汇总索引或数据流。

### 请求正文

请求正文支持常规搜索 API 中的功能子集。它支持：

* 用于指定 DSL 查询的"query"参数，受某些限制(请参阅汇总搜索限制和汇总聚合限制) * 用于指定聚合的"聚合"参数

不可用的功能：

* "size"：由于汇总处理的是预先聚合的数据，因此无法返回任何搜索命中，因此必须将大小设置为零或完全省略。  *"荧光笔"，"建议器"，"post_filter"，"个人资料"，"解释"：这些同样是不允许的。

###Examples

#### 仅历史搜索示例

假设我们有一个名为"sensor-1"的索引，其中包含原始数据，并且我们使用以下配置创建了一个汇总作业：

    
    
    PUT _rollup/job/sensor
    {
      "index_pattern": "sensor-*",
      "rollup_index": "sensor_rollup",
      "cron": "*/30 * * * * ?",
      "page_size": 1000,
      "groups": {
        "date_histogram": {
          "field": "timestamp",
          "fixed_interval": "1h",
          "delay": "7d"
        },
        "terms": {
          "fields": [ "node" ]
        }
      },
      "metrics": [
        {
          "field": "temperature",
          "metrics": [ "min", "max", "sum" ]
        },
        {
          "field": "voltage",
          "metrics": [ "avg" ]
        }
      ]
    }

这将汇总"传感器-*"模式并将结果存储在"sensor_rollup"中。若要搜索此汇总数据，我们需要使用"_rollup_search"终结点。但是，您会注意到，我们可以使用常规查询 DSL 来搜索汇总的数据：

    
    
    response = client.rollup.rollup_search(
      index: 'sensor_rollup',
      body: {
        size: 0,
        aggregations: {
          max_temperature: {
            max: {
              field: 'temperature'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /sensor_rollup/_rollup_search
    {
      "size": 0,
      "aggregations": {
        "max_temperature": {
          "max": {
            "field": "temperature"
          }
        }
      }
    }

查询以"sensor_rollup"数据为目标，因为它包含在作业中配置的汇总数据。在"温度"字段上使用"max"聚合，产生以下响应：

    
    
    {
      "took" : 102,
      "timed_out" : false,
      "terminated_early" : false,
      "_shards" : ... ,
      "hits" : {
        "total" : {
            "value": 0,
            "relation": "eq"
        },
        "max_score" : 0.0,
        "hits" : [ ]
      },
      "aggregations" : {
        "max_temperature" : {
          "value" : 202.0
        }
      }
    }

响应完全符合常规查询 + 聚合的预期;它提供了有关请求("已获取"、"_shards"等)、搜索命中(对于汇总搜索始终为空)和聚合响应的一些元数据。

汇总搜索仅限于在汇总作业中配置的功能。例如，我们无法计算平均温度，因为"avg"不是"温度"字段的配置指标之一。如果我们尝试执行该搜索：

    
    
    response = client.rollup.rollup_search(
      index: 'sensor_rollup',
      body: {
        size: 0,
        aggregations: {
          avg_temperature: {
            avg: {
              field: 'temperature'
            }
          }
        }
      }
    )
    puts response
    
    
    GET sensor_rollup/_rollup_search
    {
      "size": 0,
      "aggregations": {
        "avg_temperature": {
          "avg": {
            "field": "temperature"
          }
        }
      }
    }
    
    
    {
      "error": {
        "root_cause": [
          {
            "type": "illegal_argument_exception",
            "reason": "There is not a rollup job that has a [avg] agg with name [avg_temperature] which also satisfies all requirements of query.",
            "stack_trace": ...
          }
        ],
        "type": "illegal_argument_exception",
        "reason": "There is not a rollup job that has a [avg] agg with name [avg_temperature] which also satisfies all requirements of query.",
        "stack_trace": ...
      },
      "status": 400
    }

#### 搜索历史汇总和非汇总数据

汇总搜索 API 能够搜索"实时"非汇总数据和聚合汇总数据。这是通过简单地将实时索引添加到 URI 来完成的：

    
    
    response = client.rollup.rollup_search(
      index: 'sensor-1,sensor_rollup',
      body: {
        size: 0,
        aggregations: {
          max_temperature: {
            max: {
              field: 'temperature'
            }
          }
        }
      }
    )
    puts response
    
    
    GET sensor-1,sensor_rollup/_rollup_search __{
      "size": 0,
      "aggregations": {
        "max_temperature": {
          "max": {
            "field": "temperature"
          }
        }
      }
    }

__

|

注意 URI 现在同时搜索"sensor-1"和"sensor_rollup"---|--- 执行搜索时，汇总搜索终结点执行两项操作：

1. 原始请求原封不动地发送到非汇总索引。  2. 原始请求的重写版本将发送到汇总索引。

收到两个响应后，终结点将重写汇总响应并将两者合并在一起。在合并过程中，如果两个响应之间的存储桶有任何重叠，则使用非汇总索引中的存储桶。

对上述查询的响应看起来符合预期，尽管跨越了汇总索引和非汇总索引：

    
    
    {
      "took" : 102,
      "timed_out" : false,
      "terminated_early" : false,
      "_shards" : ... ,
      "hits" : {
        "total" : {
            "value": 0,
            "relation": "eq"
        },
        "max_score" : 0.0,
        "hits" : [ ]
      },
      "aggregations" : {
        "max_temperature" : {
          "value" : 202.0
        }
      }
    }

[« Get rollup index capabilities API](rollup-get-rollup-index-caps.md)
[Start rollup jobs API »](rollup-start-job.md)
