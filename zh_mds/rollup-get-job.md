

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Rollup APIs](rollup-apis.md)

[« Delete rollup jobs API](rollup-delete-job.md) [Get rollup job
capabilities API »](rollup-get-rollup-caps.md)

## 获取汇总作业API

检索汇总作业的配置、统计信息和状态。

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

对于版本 8.5 及更高版本，我们建议对汇总进行缩减采样，以降低时序数据的存储成本。

###Request

"获得_rollup/工作/<job_id>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"、"monitor_rollup"、"管理"或"manage_rollup"集群权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

API 可以返回单个汇总作业或所有汇总作业的详细信息。

此 API 仅返回活动("已启动"和"已停止")作业。如果作业已创建、运行了一段时间，然后被删除，则此 API 不会返回有关该作业的任何详细信息。

有关历史汇总作业的详细信息，汇总功能 API 可能更有用。

### 路径参数

`<job_id>`

     (Optional, string) Identifier for the rollup job. If it is `_all` or omitted, the API returns all rollup jobs. 

### 响应正文

`jobs`

    

(阵列)汇总作业资源的数组。

汇总作业资源的属性

`config`

     (object) Contains the configuration for the rollup job. This information is identical to the configuration that was supplied when creating the job via the [create job API](rollup-put-job.html "Create rollup jobs API"). 
`stats`

     (object) Contains transient statistics about the rollup job, such as how many documents have been processed and how many rollup summary docs have been indexed. These stats are not persisted. If a node is restarted, these stats are reset. 
`status`

    

(对象)包含汇总作业的索引器的当前状态。可能的值及其含义为：

* "停止"表示索引器已暂停，不会处理数据，即使其 cron 间隔触发也是如此。  * "已启动"表示索引器正在运行，但未主动索引数据。当 cron 间隔触发时，作业的索引器将开始处理数据。  * "索引"表示索引器正在主动处理数据并创建新的汇总文档。处于此状态时，将忽略任何后续 cron 间隔触发器，因为作业已使用前一个触发器处于活动状态。  * "中止"是一种瞬态，通常不由用户见证。如果由于某种原因需要关闭任务(作业已被删除，遇到不可恢复的错误等)，则使用它。设置"中止"状态后不久，作业将从群集中删除自身。

###Examples

如果我们已经创建了一个名为"sensor"的汇总作业，则可以使用以下方法检索有关该作业的详细信息：

    
    
    response = client.rollup.get_jobs(
      id: 'sensor'
    )
    puts response
    
    
    GET _rollup/job/sensor

API 生成以下响应：

    
    
    {
      "jobs": [
        {
          "config": {
            "id": "sensor",
            "index_pattern": "sensor-*",
            "rollup_index": "sensor_rollup",
            "cron": "*/30 * * * * ?",
            "groups": {
              "date_histogram": {
                "fixed_interval": "1h",
                "delay": "7d",
                "field": "timestamp",
                "time_zone": "UTC"
              },
              "terms": {
                "fields": [
                  "node"
                ]
              }
            },
            "metrics": [
              {
                "field": "temperature",
                "metrics": [
                  "min",
                  "max",
                  "sum"
                ]
              },
              {
                "field": "voltage",
                "metrics": [
                  "avg"
                ]
              }
            ],
            "timeout": "20s",
            "page_size": 1000
          },
          "status": {
            "job_state": "stopped"
          },
          "stats": {
            "pages_processed": 0,
            "documents_processed": 0,
            "rollups_indexed": 0,
            "trigger_count": 0,
            "index_failures": 0,
            "index_time_in_ms": 0,
            "index_total": 0,
            "search_failures": 0,
            "search_time_in_ms": 0,
            "search_total": 0,
            "processing_time_in_ms": 0,
            "processing_total": 0
          }
        }
      ]
    }

"jobs"数组包含一个作业("id：sensor")，因为我们在端点的 URL 中请求了一个作业。如果我们添加另一个作业，我们可以看到如何处理多作业响应：

    
    
    PUT _rollup/job/sensor2 __{
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
    
    GET _rollup/job/_all __

__

|

我们创建名为"sensor2"的第二个作业 ---|--- __

|

然后使用 GetJobs API 中的"_all"请求所有作业，这将产生以下响应：

    
    
    {
      "jobs": [
        {
          "config": {
            "id": "sensor2",
            "index_pattern": "sensor-*",
            "rollup_index": "sensor_rollup",
            "cron": "*/30 * * * * ?",
            "groups": {
              "date_histogram": {
                "fixed_interval": "1h",
                "delay": "7d",
                "field": "timestamp",
                "time_zone": "UTC"
              },
              "terms": {
                "fields": [
                  "node"
                ]
              }
            },
            "metrics": [
              {
                "field": "temperature",
                "metrics": [
                  "min",
                  "max",
                  "sum"
                ]
              },
              {
                "field": "voltage",
                "metrics": [
                  "avg"
                ]
              }
            ],
            "timeout": "20s",
            "page_size": 1000
          },
          "status": {
            "job_state": "stopped"
          },
          "stats": {
            "pages_processed": 0,
            "documents_processed": 0,
            "rollups_indexed": 0,
            "trigger_count": 0,
            "index_failures": 0,
            "index_time_in_ms": 0,
            "index_total": 0,
            "search_failures": 0,
            "search_time_in_ms": 0,
            "search_total": 0,
            "processing_time_in_ms": 0,
            "processing_total": 0
          }
        },
        {
          "config": {
            "id": "sensor",
            "index_pattern": "sensor-*",
            "rollup_index": "sensor_rollup",
            "cron": "*/30 * * * * ?",
            "groups": {
              "date_histogram": {
                "fixed_interval": "1h",
                "delay": "7d",
                "field": "timestamp",
                "time_zone": "UTC"
              },
              "terms": {
                "fields": [
                  "node"
                ]
              }
            },
            "metrics": [
              {
                "field": "temperature",
                "metrics": [
                  "min",
                  "max",
                  "sum"
                ]
              },
              {
                "field": "voltage",
                "metrics": [
                  "avg"
                ]
              }
            ],
            "timeout": "20s",
            "page_size": 1000
          },
          "status": {
            "job_state": "stopped"
          },
          "stats": {
            "pages_processed": 0,
            "documents_processed": 0,
            "rollups_indexed": 0,
            "trigger_count": 0,
            "index_failures": 0,
            "index_time_in_ms": 0,
            "index_total": 0,
            "search_failures": 0,
            "search_time_in_ms": 0,
            "search_total": 0,
            "processing_time_in_ms": 0,
            "processing_total": 0
          }
        }
      ]
    }

[« Delete rollup jobs API](rollup-delete-job.md) [Get rollup job
capabilities API »](rollup-get-rollup-caps.md)
