

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Rollup APIs](rollup-apis.md)

[« Get rollup job capabilities API](rollup-get-rollup-caps.md) [Rollup
search »](rollup-search.md)

## 获取汇总索引功能API

返回汇总索引内所有作业的汇总功能(例如，存储汇总数据的索引)。

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

对于版本 8.5 及更高版本，我们建议对汇总进行缩减采样，以降低时序数据的存储成本。

###Request

"获取<target>/_rollup/数据"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则必须对存储汇总结果的索引具有任何"读取"、"view_index_metadata"或"管理"索引权限。有关详细信息，请参阅安全权限。

###Description

单个汇总索引可以存储多个汇总作业的数据，并且可能具有多种功能，具体取决于这些作业。

此 API 将允许您确定：

1. 索引(或通过模式指定的索引)中存储了哪些作业？  2. 汇总了哪些目标索引，这些汇总中使用了哪些字段，以及可以对每个作业执行哪些聚合？

### 路径参数

`<target>`

     (Required, string) Data stream or index to check for rollup capabilities. Wildcard (`*`) expressions are supported. 

###Examples

想象一下，我们有一个名为"sensor-1"的索引，里面装满了原始数据。我们知道数据会随着时间的推移而增长，所以会有"传感器-2"、"传感器-3"等。让我们创建一个汇总作业，将其数据存储在"sensor_rollup"中：

    
    
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

如果以后我们想确定在"sensor_rollup"索引中还原了哪些作业和功能，则可以使用 get rollup index API：

    
    
    response = client.rollup.get_rollup_index_caps(
      index: 'sensor_rollup'
    )
    puts response
    
    
    GET /sensor_rollup/_rollup/data

请注意我们如何请求具体的汇总索引名称 ('sensor_rollup') 作为 URL 的第一部分。这将产生以下响应：

    
    
    {
      "sensor_rollup" : {
        "rollup_jobs" : [
          {
            "job_id" : "sensor",
            "rollup_index" : "sensor_rollup",
            "index_pattern" : "sensor-*",
            "fields" : {
              "node" : [
                {
                  "agg" : "terms"
                }
              ],
              "temperature" : [
                {
                  "agg" : "min"
                },
                {
                  "agg" : "max"
                },
                {
                  "agg" : "sum"
                }
              ],
              "timestamp" : [
                {
                  "agg" : "date_histogram",
                  "time_zone" : "UTC",
                  "fixed_interval" : "1h",
                  "delay": "7d"
                }
              ],
              "voltage" : [
                {
                  "agg" : "avg"
                }
              ]
            }
          }
        ]
      }
    }

返回的响应包含与原始汇总配置类似的信息，但格式不同。首先，有一些内务管理细节：汇总作业 ID、保存滚动数据的索引、作业所针对的索引模式。

接下来，它显示包含符合汇总搜索条件的数据的字段列表。在这里，我们看到四个字段："节点"，"温度"，"时间戳"和"电压"。其中每个字段都列出了可能的聚合。例如，您可以在"温度"字段上使用最小值、最大值或总和聚合，但在"时间戳"上只能使用"date_histogram"。

请注意，"rollup_jobs"元素是一个数组;可以为单个索引或索引模式配置多个独立的作业。其中每个作业可能具有不同的配置，因此 API 返回所有可用配置的列表。

与其他与索引交互的 API 一样，您可以指定索引模式而不是显式索引：

    
    
    response = client.rollup.get_rollup_index_caps(
      index: '*_rollup'
    )
    puts response
    
    
    GET /*_rollup/_rollup/data

[« Get rollup job capabilities API](rollup-get-rollup-caps.md) [Rollup
search »](rollup-search.md)
