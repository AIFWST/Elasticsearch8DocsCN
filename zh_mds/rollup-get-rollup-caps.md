

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Rollup APIs](rollup-apis.md)

[« Get rollup jobs API](rollup-get-job.md) [Get rollup index capabilities
API »](rollup-get-rollup-index-caps.md)

## 获取汇总作业功能API

返回已为特定索引或索引模式配置的任何汇总作业的功能。

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

对于版本 8.5 及更高版本，我们建议对汇总进行缩减采样，以降低时序数据的存储成本。

###Request

"获取_rollup/数据/<index>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"、"monitor_rollup"、"管理"或"manage_rollup"集群权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

此 API 非常有用，因为汇总作业通常配置为仅汇总源索引中的字段子集。此外，仅为各种字段配置某些聚合扫描，从而导致功能子集有限，具体取决于该配置。

此 API 使您能够检查索引并确定：

1. 此索引是否在群集中的某个位置具有关联的汇总数据？  2. 如果第一个问题是肯定的，则汇总了哪些字段，可以执行哪些聚合，数据位于何处？

### 路径参数

`<index>`

     (string) Index, indices or index-pattern to return rollup capabilities for. `_all` may be used to fetch rollup capabilities from all jobs. 

###Examples

想象一下，我们有一个名为"sensor-1"的索引，里面装满了原始数据。我们知道数据会随着时间的推移而增长，所以会有"传感器-2"、"传感器-3"等。让我们创建一个以索引模式"sensor-*"为目标的汇总作业，以适应将来的扩展：

    
    
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

然后，我们可以通过以下命令检索该索引模式('sensor-*')的汇总功能：

    
    
    response = client.rollup.get_rollup_caps(
      id: 'sensor-*'
    )
    puts response
    
    
    GET _rollup/data/sensor-*

这将产生以下响应：

    
    
    {
      "sensor-*" : {
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

返回的响应包含与原始汇总配置类似的信息，但格式不同。首先，有一些内务管理详细信息：汇总作业 ID、保存滚动数据的索引以及作业所针对的索引模式。

接下来，它显示包含符合汇总搜索条件的数据的字段列表。在这里，我们看到四个字段："节点"，"温度"，"时间戳"和"电压"。其中每个字段都列出了可能的聚合。例如，您可以在"温度"字段上使用最小值、最大值或总和聚合，但只能在"时间戳"上使用"date_histogram"。

请注意，"rollup_jobs"元素是一个数组;可以为单个索引或索引模式配置多个独立的作业。其中每个作业可能具有不同的配置，因此 API 返回所有可用配置的列表。

我们还可以通过请求"_all"来检索相同的信息：

    
    
    response = client.rollup.get_rollup_caps(
      id: '_all'
    )
    puts response
    
    
    GET _rollup/data/_all

但请注意，如果我们使用具体的索引名称("sensor-1")，我们将检索到无汇总功能：

    
    
    response = client.rollup.get_rollup_caps(
      id: 'sensor-1'
    )
    puts response
    
    
    GET _rollup/data/sensor-1
    
    
    {
    
    }

这是为什么呢？原始汇总作业是针对特定索引模式("传感器-*")而不是具体索引("传感器-1")配置的。因此，虽然索引属于模式，但汇总作业仅对整个模式有效，而不仅仅是其中一个包含索引。因此，出于这个原因，get 汇总功能 API 仅根据最初配置的索引名称或模式返回信息。

[« Get rollup jobs API](rollup-get-job.md) [Get rollup index capabilities
API »](rollup-get-rollup-index-caps.md)
