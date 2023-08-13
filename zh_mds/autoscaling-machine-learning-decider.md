

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Autoscaling](xpack-autoscaling.md) ›[Autoscaling deciders](autoscaling-
deciders.md)

[« Frozen existence decider](autoscaling-frozen-existence-decider.md) [Fixed
decider »](autoscaling-fixed-decider.md)

## 机器学习决策程序

机器学习决策程序 ('ml') 计算内存和 CPU 要求以运行机器学习作业和训练的模型。

为管理"ml"节点的策略启用机器学习决策程序。

若要在群集未适当缩放时打开机器学习作业，请将"xpack.ml.max_lazy_ml_nodes"设置为最大可能的机器学习节点数(有关详细信息，请参阅高级机器学习设置)。在 Elasticsearch Service 中，这是自动设置的。

### 配置设置

"num_anomaly_jobs_in_queue"和"num_analytics_jobs_in_queue"都旨在延迟放大事件。如果群集太小，这些设置指示可以从节点取消分配的每种类型的作业数。这两个设置仅考虑在给定当前规模的情况下可以打开的作业。如果作业对于任何节点大小来说都太大，或者如果没有用户干预就无法分配作业(例如，用户针对实时异常情况检测作业调用"_stop")，则会忽略该特定作业的数字。

`num_anomaly_jobs_in_queue`

     (Optional, integer) Specifies the number of queued anomaly detection jobs to allow. Defaults to `0`. 
`num_analytics_jobs_in_queue`

     (Optional, integer) Specifies the number of queued data frame analytics jobs to allow. Defaults to `0`. 
`down_scale_delay`

     (Optional, [time value](api-conventions.html#time-units "Time units")) Specifies the time to delay before scaling down. Defaults to 1 hour. If a scale down is possible for the entire time window, then a scale down is requested. If the cluster requires a scale up during the window, the window is reset. 

###Examples

此示例创建一个名为"my_autoscaling_policy"的自动缩放策略，该策略将替代机器学习决策程序的默认配置。

    
    
    PUT /_autoscaling/policy/my_autoscaling_policy
    {
      "roles" : [ "ml" ],
      "deciders": {
        "ml": {
          "num_anomaly_jobs_in_queue": 5,
          "num_analytics_jobs_in_queue": 3,
          "down_scale_delay": "30m"
        }
      }
    }

API 返回以下结果：

    
    
    {
      "acknowledged": true
    }

[« Frozen existence decider](autoscaling-frozen-existence-decider.md) [Fixed
decider »](autoscaling-fixed-decider.md)
