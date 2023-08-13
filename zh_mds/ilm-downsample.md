

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md) ›[Index lifecycle actions](ilm-actions.md)

[« Rollover](ilm-rollover.md) [Searchable snapshot »](ilm-searchable-
snapshot.md)

##Downsample

允许的阶段：热，暖，冷。

聚合时间序列 (TSDS) 索引，并存储按配置的时间间隔分组的每个指标字段的预先计算的统计摘要("最小"、"最大值"、"总和"、"value_count"和"平均值")。例如，包含每 10 秒采样一次的指标的 TSDS 索引可以缩减采样为每小时索引。一小时间隔内的所有文档都将汇总并存储为单个文档，并存储在缩减采样索引中。

此操作对应于缩减采样 API。

生成的下采样索引的名称是"下采样-<original-index-name>-<random-uuid>"。如果 ILM 对数据流的后备索引执行"下采样"操作，则下采样索引将成为同一流的后备索引，并且源索引将被删除。

要在"热"阶段使用"下采样"操作，必须存在"翻转"操作**。如果未配置滚动更新操作，ILM 将拒绝该策略。

###Options

`fixed_interval`

     (Required, string) The [fixed time interval](rollup-understanding-groups.html#rollup-understanding-group-intervals "Calendar vs fixed time intervals") into which the data will be downsampled. 

###Example

    
    
    response = client.ilm.put_lifecycle(
      policy: 'datastream_policy',
      body: {
        policy: {
          phases: {
            hot: {
              actions: {
                rollover: {
                  max_docs: 1
                },
                downsample: {
                  fixed_interval: '1h'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT _ilm/policy/datastream_policy
    {
      "policy": {
        "phases": {
          "hot": {
            "actions": {
              "rollover": {
                "max_docs": 1
              },
              "downsample": {
      	          "fixed_interval": "1h"
      	      }
            }
          }
        }
      }
    }

[« Rollover](ilm-rollover.md) [Searchable snapshot »](ilm-searchable-
snapshot.md)
