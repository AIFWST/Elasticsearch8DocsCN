

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Autoscaling](xpack-autoscaling.md) ›[Autoscaling deciders](autoscaling-
deciders.md)

[« Reactive storage decider](autoscaling-reactive-storage-decider.md)
[Frozen shards decider »](autoscaling-frozen-shards-decider.md)

## 主动预防性存储决策程序

主动存储决策程序 ("proactive_storage") 计算包含当前数据集所需的存储以及估计的预期附加数据量。

为管理具有"data_hot"角色的节点的所有策略启用主动存储决策程序。

对预期额外数据的估计基于"forecast_window"中发生的过去索引。只有索引到数据流中才能达到估计值。

### 配置设置

`forecast_window`

     (Optional, [time value](api-conventions.html#time-units "Time units")) The window of time to use for forecasting. Defaults to 30 minutes. 

###Examples

此示例将名为"my_autoscaling_policy"的自动缩放策略覆盖主动决策程序的"forecast_window"为 10 分钟。

    
    
    PUT /_autoscaling/policy/my_autoscaling_policy
    {
      "roles" : [ "data_hot" ],
      "deciders": {
        "proactive_storage": {
          "forecast_window": "10m"
        }
      }
    }

API 返回以下结果：

    
    
    {
      "acknowledged": true
    }

[« Reactive storage decider](autoscaling-reactive-storage-decider.md)
[Frozen shards decider »](autoscaling-frozen-shards-decider.md)
