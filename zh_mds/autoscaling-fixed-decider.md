

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Autoscaling](xpack-autoscaling.md) ›[Autoscaling deciders](autoscaling-
deciders.md)

[« Machine learning decider](autoscaling-machine-learning-decider.md)
[Monitor a cluster »](monitor-elasticsearch-cluster.md)

## 固定决策程序

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

固定决策程序仅用于测试。不要在生产中使用此决策程序。

"固定"决策程序以固定的所需容量进行响应。默认情况下不启用它，但可以通过显式配置它为任何策略启用它。

### 配置设置

`storage`

     (Optional, [byte value](api-conventions.html#byte-units "Byte size units")) Required amount of node-level storage. Defaults to `-1` (disabled). 
`memory`

     (Optional, [byte value](api-conventions.html#byte-units "Byte size units")) Required amount of node-level memory. Defaults to `-1` (disabled). 
`processors`

     (Optional, float) Required number of processors. Defaults to disabled. 
`nodes`

     (Optional, integer) Number of nodes to use when calculating capacity. Defaults to `1`. 

###Examples

此示例放置一个名为"my_autoscaling_policy"的自动缩放策略，启用和配置固定决策程序。

    
    
    PUT /_autoscaling/policy/my_autoscaling_policy
    {
      "roles" : [ "data_hot" ],
      "deciders": {
        "fixed": {
          "storage": "1tb",
          "memory": "32gb",
          "processors": 2.3,
          "nodes": 8
        }
      }
    }

API 返回以下结果：

    
    
    {
      "acknowledged": true
    }

[« Machine learning decider](autoscaling-machine-learning-decider.md)
[Monitor a cluster »](monitor-elasticsearch-cluster.md)
