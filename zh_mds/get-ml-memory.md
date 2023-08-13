

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning APIs](ml-apis.md)

[« Get machine learning info API](get-ml-info.md) [Set upgrade mode API
»](ml-set-upgrade-mode.md)

## 获取机器学习内存统计信息API

返回有关机器学习如何使用内存的信息。

###Request

"获取_ml/内存/_stats" "获取_ml/内存/<node_id>/_stats"

###Prerequisites

需要"monitor_ml"群集权限。此权限包含在"machine_learning_user"内置角色中。

###Description

获取有关机器学习作业和训练模型如何在每个节点上使用内存的信息，包括 JVM 堆内和 JVM 外部的本机内存。

### 路径参数

`<node_id>`

     (Optional, string) The names of particular nodes in the cluster to target. For example, `nodeId1,nodeId2` or `ml:true`. For node selection options, see [Node specification](cluster.html#cluster-nodes "Node specification"). 

### 查询参数

`human`

     Specify this query parameter to include the fields with units in the response. Otherwise only the `_in_bytes` sizes are returned in the response. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 响应正文

`_nodes`

    

(对象)包含有关请求选择的节点数的统计信息。

"_nodes"的属性

`failed`

     (integer) Number of nodes that rejected the request or failed to respond. If this value is not `0`, a reason for the rejection or failure is included in the response. 
`successful`

     (integer) Number of nodes that responded successfully to the request. 
`total`

     (integer) Total number of nodes selected by the request. 

`cluster_name`

     (string) Name of the cluster. Based on the [cluster.name](important-settings.html#cluster-name "Cluster name setting") setting. 
`nodes`

    

(对象)包含请求选择的节点的统计信息。

"节点"的属性

`<node_id>`

    

(对象)包含节点的统计信息。

""的属性<node_id>

`attributes`

     (object) Lists node attributes such as `ml.machine_memory` or `ml.max_open_jobs` settings. 
`ephemeral_id`

     (string) The ephemeral ID of the node. 
`jvm`

    

(对象)包含节点的 Java 虚拟机 (JVM) 统计信息。

"jvm"的属性

`heap_max`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Maximum amount of memory available for use by the heap. 
`heap_max_in_bytes`

     (integer) Maximum amount of memory, in bytes, available for use by the heap. 
`java_inference`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Amount of Java heap currently being used for caching inference models. 
`java_inference_in_bytes`

     (integer) Amount of Java heap, in bytes, currently being used for caching inference models. 
`java_inference_max`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Maximum amount of Java heap to be used for caching inference models. 
`java_inference_max_in_bytes`

     (integer) Maximum amount of Java heap, in bytes, to be used for caching inference models. 

`mem`

    

(对象)包含有关节点内存使用情况的统计信息。

"mem"的属性

`adjusted_total`

     ([byte value](api-conventions.html#byte-units "Byte size units")) If the amount of physical memory has been overridden using the `es.total_memory_bytes` system property then this reports the overridden value. Otherwise it reports the same value as `total`. 
`adjusted_total_in_bytes`

     (integer) If the amount of physical memory has been overridden using the `es.total_memory_bytes` system property then this reports the overridden value in bytes. Otherwise it reports the same value as `total_in_bytes`. 
`ml`

    

(对象)包含有关机器学习在节点上使用本机内存的统计信息。

"ml"的性质

`anomaly_detectors`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Amount of native memory set aside for anomaly detection jobs. 
`anomaly_detectors_in_bytes`

     (integer) Amount of native memory, in bytes, set aside for anomaly detection jobs. 
`data_frame_analytics`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Amount of native memory set aside for data frame analytics jobs. 
`data_frame_analytics_in_bytes`

     (integer) Amount of native memory, in bytes, set aside for data frame analytics jobs. 
`max`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Maximum amount of native memory (separate to the JVM heap) that may be used by machine learning native processes. 
`max_in_bytes`

     (integer) Maximum amount of native memory (separate to the JVM heap), in bytes, that may be used by machine learning native processes. 
`native_code_overhead`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Amount of native memory set aside for loading machine learning native code shared libraries. 
`native_code_overhead_in_bytes`

     (integer) Amount of native memory, in bytes, set aside for loading machine learning native code shared libraries. 
`native_inference`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Amount of native memory set aside for trained models that have a PyTorch `model_type`. 
`native_inference_in_bytes`

     (integer) Amount of native memory, in bytes, set aside for trained models that have a PyTorch `model_type`. 

`total`

     ([byte value](api-conventions.html#byte-units "Byte size units")) Total amount of physical memory. 
`total_in_bytes`

     (integer) Total amount of physical memory in bytes. 

`name`

     (string) Human-readable identifier for the node. Based on the [Node name setting](important-settings.html#node-name "Node name setting") setting. 
`roles`

     (array of strings) Roles assigned to the node. See [Node](modules-node.html "Node"). 
`transport_address`

     (string) The host and port where transport HTTP connections are accepted. 

###Examples

    
    
    response = client.ml.get_memory_stats(
      human: true
    )
    puts response
    
    
    GET _ml/memory/_stats?human

这是一个可能的响应：

    
    
    {
      "_nodes": {
        "total": 1,
        "successful": 1,
        "failed": 0
      },
      "cluster_name": "my_cluster",
      "nodes": {
        "pQHNt5rXTTWNvUgOrdynKg": {
          "name": "node-0",
          "ephemeral_id": "ITZ6WGZnSqqeT_unfit2SQ",
          "transport_address": "127.0.0.1:9300",
          "attributes": {
            "ml.machine_memory": "68719476736",
            "ml.max_jvm_size": "536870912"
          },
          "roles": [
            "data",
            "data_cold",
            "data_content",
            "data_frozen",
            "data_hot",
            "data_warm",
            "ingest",
            "master",
            "ml",
            "remote_cluster_client",
            "transform"
          ],
          "mem": {
            "total": "64gb",
            "total_in_bytes": 68719476736,
            "adjusted_total": "64gb",
            "adjusted_total_in_bytes": 68719476736,
            "ml": {
              "max": "19.1gb",
              "max_in_bytes": 20615843020,
              "native_code_overhead": "0b",
              "native_code_overhead_in_bytes": 0,
              "anomaly_detectors": "0b",
              "anomaly_detectors_in_bytes": 0,
              "data_frame_analytics": "0b",
              "data_frame_analytics_in_bytes": 0,
              "native_inference": "0b",
              "native_inference_in_bytes": 0
            }
          },
          "jvm": {
            "heap_max": "512mb",
            "heap_max_in_bytes": 536870912,
            "java_inference_max": "204.7mb",
            "java_inference_max_in_bytes": 214748364,
            "java_inference": "0b",
            "java_inference_in_bytes": 0
          }
        }
      }
    }

[« Get machine learning info API](get-ml-info.md) [Set upgrade mode API
»](ml-set-upgrade-mode.md)
