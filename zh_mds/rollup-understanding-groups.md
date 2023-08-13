

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Roll up or
transform your data](data-rollup-transform.md) ›[Rolling up historical
data](xpack-rollup.md)

[« Getting started with rollups](rollup-getting-started.md) [Rollup
aggregation limitations »](rollup-agg-limitations.md)

## 理解组

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

对于版本 8.5 及更高版本，我们建议对汇总进行缩减采样，以降低时序数据的存储成本。

为了保持灵活性，汇总作业是根据将来查询可能需要如何使用数据来定义的。传统上，系统会强制管理员决定汇总哪些指标以及汇总时间间隔。例如，每小时"cpu_time"的平均值。这是有限的;如果将来管理员希望每小时看到"cpu_time"的平均值_and_partitioned"host_name"，他们就不走运了。

当然，管理员可以决定每小时汇总"[小时，主机]"元组，但随着分组键数量的增加，管理员需要配置的元组数量也会增加。此外，这些"[小时，主机]"元组仅对每小时汇总有用...每日、每周或每月汇总都需要新配置。

Elasticsearch 的汇总作业不是强制管理员提前决定应该汇总哪些单独的元组，而是根据哪些组可能对未来的查询有用来配置。例如，此配置：

    
    
    "groups" : {
      "date_histogram": {
        "field": "timestamp",
        "fixed_interval": "1h",
        "delay": "7d"
      },
      "terms": {
        "fields": ["hostname", "datacenter"]
      },
      "histogram": {
        "fields": ["load", "net_in", "net_out"],
        "interval": 5
      }
    }

允许在"时间戳"字段上使用"date_histogram"，在"主机名"和"数据中心"字段上使用"术语"聚合，以及在任何"加载"、"net_in"、"net_out"字段中使用"直方图"。

重要的是，这些 aggs/字段可以任意组合使用。此聚合：

    
    
    "aggs" : {
      "hourly": {
        "date_histogram": {
          "field": "timestamp",
          "fixed_interval": "1h"
        },
        "aggs": {
          "host_names": {
            "terms": {
              "field": "hostname"
            }
          }
        }
      }
    }

与此聚合一样有效：

    
    
    "aggs" : {
      "hourly": {
        "date_histogram": {
          "field": "timestamp",
          "fixed_interval": "1h"
        },
        "aggs": {
          "data_center": {
            "terms": {
              "field": "datacenter"
            }
          },
          "aggs": {
            "host_names": {
              "terms": {
                "field": "hostname"
              }
            },
            "aggs": {
              "load_values": {
                "histogram": {
                  "field": "load",
                  "interval": 5
                }
              }
            }
          }
        }
      }
    }

您会注意到，第二个聚合不仅要大得多，而且还交换了术语聚合在"主机名"上的位置，说明了聚合的顺序对汇总无关紧要。同样，虽然汇总数据需要"date_histogram"，但在查询时不需要(尽管经常使用)。例如，这是要执行的汇总搜索的有效聚合：

    
    
    "aggs" : {
      "host_names": {
        "terms": {
          "field": "hostname"
        }
      }
    }

最终，在为作业配置"组"时，请考虑将来如何对查询中的数据进行分区......然后将这些包含在配置中。由于汇总搜索允许分组字段的任何顺序或组合，因此您只需确定字段是否对以后聚合有用，以及您可能希望如何使用它(术语、直方图等)。

### 日历与固定时间间隔

每个汇总作业都必须具有具有已定义间隔的日期直方图组。Elasticsearch可以理解日历和固定的时间间隔。固定的时间间隔相当容易理解;"60s"表示 60 秒。但是"1M"是什么意思？一个月的时间取决于我们在谈论哪个月，有些月份比其他月份长或短。这是日历时间的一个示例，该单元的持续时间取决于上下文。日历单位还受到闰秒、闰年等的影响。

这一点很重要，因为汇总生成的存储桶采用日历或固定间隔，这限制了您以后查询它们的方式。SeeRequests必须是配置的倍数。

我们建议坚持使用固定的时间间隔，因为它们更易于理解，并且在查询时更灵活。它将在闰事件期间引入一些数据漂移，您将不得不考虑固定数量(30 天)的月份，而不是实际的日历长度。但是，它通常比在查询时处理日历单位更容易。

单位的倍数始终是"固定的"。例如，"2h"始终是固定数量的"7200"秒。单个单位可以是固定的或日历的，具体取决于单位：

单位 |日历 |固定---|---|---毫秒

|

NA

|

"1ms"、"10ms"等秒

|

NA

|

"1s"、"10s"等分钟

|

`1m`

|

"2m"、"10m"等小时

|

`1h`

|

"2h"、"10h"等天

|

`1d`

|

"2d"、"10d"等周

|

`1w`

|

不适用月份

|

`1M`

|

北美季度

|

`1q`

|

不适用年份

|

`1y`

|

NA 对于同时存在固定单位和日历的某些单位，您可能需要用下一个较小的单位来表示数量。例如，如果您想要固定的一天(不是日历日)，则应指定"24h"而不是"1d"。同样，如果需要固定小时数，请指定"60m"而不是"1h"。这是因为单个数量需要日历时间，并且限制您将来按日历时间进行查询。

### 异构索引的分组限制

以前，Rollup 处理具有异构映射(多个不相关/非重叠映射)的索引的方式存在限制。当时的建议是为每个数据"类型"配置一个单独的作业。例如，您可以为已启用的每个 Beats 模块配置一个单独的作业(一个用于"进程"，另一个用于"文件系统"等)。

此建议由内部实现详细信息驱动，如果使用单个"合并"作业，则会导致文档计数可能不正确。

此后，这一限制得到了缓解。从 6.4.0 开始，现在认为最佳做法是将所有汇总配置合并到一个作业中。

例如，如果您的索引有两种类型的文档：

    
    
    {
      "timestamp": 1516729294000,
      "temperature": 200,
      "voltage": 5.2,
      "node": "a"
    }

and

    
    
    {
      "timestamp": 1516729294000,
      "price": 123,
      "title": "Foo"
    }

最佳做法是将它们合并到涵盖这两种文档类型的单个汇总作业中，如下所示：

    
    
    PUT _rollup/job/combined
    {
      "index_pattern": "data-*",
      "rollup_index": "data_rollup",
      "cron": "*/30 * * * * ?",
      "page_size": 1000,
      "groups": {
        "date_histogram": {
          "field": "timestamp",
          "fixed_interval": "1h",
          "delay": "7d"
        },
        "terms": {
          "fields": [ "node", "title" ]
        }
      },
      "metrics": [
        {
          "field": "temperature",
          "metrics": [ "min", "max", "sum" ]
        },
        {
          "field": "price",
          "metrics": [ "avg" ]
        }
      ]
    }

### 文档计数和重叠作业

以前，"重叠"作业配置上的文档计数存在问题，由相同的内部实现细节驱动。如果有两个汇总作业保存到同一索引，其中一个作业是另一个作业的"子集"，则对于某些聚合安排，文档计数可能不正确。

此问题在 6.4.0 中也已消除。

[« Getting started with rollups](rollup-getting-started.md) [Rollup
aggregation limitations »](rollup-agg-limitations.md)
