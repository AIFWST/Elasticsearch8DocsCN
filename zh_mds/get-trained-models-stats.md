

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning trained model APIs](ml-df-trained-
models-apis.md)

[« Get trained models API](get-trained-models.md) [Infer trained model API
»](infer-trained-model.md)

## 获取训练模型统计接口

检索已训练模型的使用情况信息。

###Request

"获取_ml/trained_models/_stats"

"获取_ml/trained_models/_all/_stats"

"得到_ml/trained_models<model_id_or_deployment_id>//_stats"

'GET_ml/trained_models<model_id_or_deployment_id>/，<model_id_2_or_deployment_id_2>/_stats"

`GET
_ml/trained_models/<model_id_pattern*_or_deployment_id_pattern*>,<model_id_2_or_deployment_id_2>/_stats`

###Prerequisites

需要"monitor_ml"群集权限。此权限包含在"machine_learning_user"内置角色中。

###Description

您可以使用以逗号分隔的模型 ID、部署 ID 或通配符表达式列表，在单个 API 请求中获取多个已训练模型或已训练模型部署的使用情况信息。

### 路径参数

`<model_id_or_deployment_id>`

     (Optional, string) The unique identifier of the model or the deployment. If a model has multiple deployments, and the ID of one of the deployments matches the model ID, then the model ID takes precedence; the results are returned for all deployments of the model. 

### 查询参数

`allow_no_match`

    

(可选，布尔值)指定在请求时要执行的操作：

* 包含通配符表达式，并且没有匹配的模型。  * 包含"_all"字符串或不包含标识符，并且没有匹配项。  * 包含通配符表达式，并且只有部分匹配。

默认值为"true"，当没有匹配项时返回一个空数组，当存在部分匹配时返回结果子集。如果此参数为"false"，则当没有匹配项或只有部分匹配项时，请求将返回"404"状态代码。

`from`

     (Optional, integer) Skips the specified number of models. The default value is `0`. 
`size`

     (Optional, integer) Specifies the maximum number of models to obtain. The default value is `100`. 

### 响应正文

`count`

     (integer) The total number of trained model statistics that matched the requested ID patterns. Could be higher than the number of items in the `trained_model_stats` array as the size of the array is restricted by the supplied `size` parameter. 
`trained_model_stats`

    

(阵列)一组经过训练的模型统计信息，按"model_id"值升序排序。

已训练模型统计信息的属性

`deployment_stats`

    

(列表)部署统计信息的集合(如果部署了提供的"model_id"值之一)

部署统计信息的属性

`allocation_status`

    

(对象)给定部署配置的详细分配状态。

分配统计信息的属性

`allocation_count`

     (integer) The current number of nodes where the model is allocated. 
`cache_size`

     ([byte value](api-conventions.html#byte-units "Byte size units")) The inference cache size (in memory outside the JVM heap) per node for the model. 
`state`

    

(字符串)与节点相关的详细分配状态。

* "正在启动"：正在尝试分配，但当前没有节点分配模型。  * "已启动"：至少分配了一个节点的模型。  * "fully_allocated"：部署已完全分配并满足"target_allocation_count"。

`target_allocation_count`

     (integer) The desired number of nodes for model allocation. 

`deployment_id`

     A unique identifier for the deployment of the model. 
`error_count`

     (integer) The sum of `error_count` for all nodes in the deployment. 
`inference_count`

     (integer) The sum of `inference_count` for all nodes in the deployment. 
`model_id`

     (string) The unique identifier of the trained model. 
`nodes`

    

(对象数组)当前分配了模型的每个节点的部署统计信息。

节点统计信息的属性

`average_inference_time_ms`

     (double) The average time for each inference call to complete on this node. The average is calculated over the lifetime of the deployment. 
`average_inference_time_ms_excluding_cache_hits`

     (double) The average time to perform inference on the trained model excluding occasions where the response comes from the cache. Cached inference calls return very quickly as the model is not evaluated, by excluding cache hits this value is an accurate measure of the average time taken to evaluate the model. 
`average_inference_time_ms_last_minute`

     (double) The average time for each inference call to complete on this node in the last minute. 
`error_count`

     (integer) The number of errors when evaluating the trained model. 
`inference_cache_hit_count`

     (integer) The total number of inference calls made against this node for this model that were served from the inference cache. 
`inference_cache_hit_count_last_minute`

     (integer) The number of inference calls made against this node for this model in the last minute that were served from the inference cache. 
`inference_count`

     (integer) The total number of inference calls made against this node for this model. 
`last_access`

     (long) The epoch time stamp of the last inference call for the model on this node. 
`node`

    

(对象)与节点有关的信息。

节点的属性

`attributes`

     (object) Lists node attributes such as `ml.machine_memory` or `ml.max_open_jobs` settings. 
`ephemeral_id`

     (string) The ephemeral ID of the node. 
`id`

     (string) The unique identifier of the node. 
`name`

     (string) The node name. 
`transport_address`

     (string) The host and port where transport HTTP connections are accepted. 

`number_of_allocations`

     (integer) The number of allocations assigned to this node. 
`number_of_pending_requests`

     (integer) The number of inference requests queued to be processed. 
`peak_throughput_per_minute`

     (integer) The peak number of requests processed in a 1 minute period. 
`routing_state`

    

(对象)此分配的当前路由状态和当前路由状态的原因。

routing_state的性质

`reason`

     (string) The reason for the current state. Usually only populated when the `routing_state` is `failed`. 
`routing_state`

     (string) The current routing state. 

* "正在启动"：模型正在尝试在此模型上进行分配，推理调用尚未被接受。  * "已启动"：模型已分配并准备好接受推理请求。  * "停止"：模型正在从此节点中释放。  * "停止"：模型从此节点完全释放。  * "失败"：分配尝试失败，请参阅"原因"字段了解潜在原因。

`rejected_execution_count`

     (integer) The number of inference requests that were not processed because the queue was full. 
`start_time`

     (long) The epoch timestamp when the allocation started. 
`threads_per_allocation`

     (integer) The number of threads for each allocation during inference. This value is limited by the number of hardware threads on the node; it might therefore differ from the `threads_per_allocation` value in the [Start trained model deployment](start-trained-model-deployment.html "Start trained model deployment API") API. 
`timeout_count`

     (integer) The number of inference requests that timed out before being processed. 
`throughput_last_minute`

     (integer) The number of requests processed in the last 1 minute. 

`number_of_allocations`

     (integer) The requested number of allocations for the trained model deployment. 
`peak_throughput_per_minute`

     (integer) The peak number of requests processed in a 1 minute period for all nodes in the deployment. This is calculated as the sum of each node's `peak_throughput_per_minute` value. 
`priority`

     (string) The deployment priority. 
`rejected_execution_count`

     (integer) The sum of `rejected_execution_count` for all nodes in the deployment. Individual nodes reject an inference request if the inference queue is full. The queue size is controlled by the `queue_capacity` setting in the [Start trained model deployment](start-trained-model-deployment.html "Start trained model deployment API") API. 
`reason`

     (string) The reason for the current deployment state. Usually only populated when the model is not deployed to a node. 
`start_time`

     (long) The epoch timestamp when the deployment started. 
`state`

    

(字符串)部署的总体状态。这些值可能是：

* "正在启动"：部署最近已启动，但尚未可用，因为模型未在任何节点上分配。  * "已启动"：部署可用，因为至少有一个节点分配了模型。  * "停止"：部署正准备停止并从相关节点中释放模型。

`threads_per_allocation`

     (integer) The number of threads per allocation used by the inference process. 
`timeout_count`

     (integer) The sum of `timeout_count` for all nodes in the deployment. 
`queue_capacity`

     (integer) The number of inference requests that may be queued before new requests are rejected. 

`inference_stats`

    

(对象)推理统计信息字段的集合。

推理统计信息的属性

`missing_all_fields_count`

     (integer) The number of inference calls where all the training features for the model were missing. 
`inference_count`

     (integer) The total number of times the model has been called for inference. This is across all inference contexts, including all pipelines. 
`cache_miss_count`

     (integer) The number of times the model was loaded for inference and was not retrieved from the cache. If this number is close to the `inference_count`, then the cache is not being appropriately used. This can be solved by increasing the cache size or its time-to-live (TTL). See [General machine learning settings](ml-settings.html#general-ml-settings "General machine learning settings") for the appropriate settings. 
`failure_count`

     (integer) The number of failures when using the model for inference. 
`timestamp`

     ([time units](api-conventions.html#time-units "Time units")) The time when the statistics were last updated. 

`ingest`

     (object) A collection of ingest stats for the model across all nodes. The values are summations of the individual node statistics. The format matches the `ingest` section in [Nodes stats](cluster-nodes-stats.html "Nodes stats API"). 
`model_id`

     (string) The unique identifier of the trained model. 
`model_size_stats`

    

(对象)模型大小统计信息字段的集合。

模型大小统计信息的属性

`model_size_bytes`

     (integer) The size of the model in bytes. 
`required_native_memory_bytes`

     (integer) The amount of memory required to load the model in bytes. 

`pipeline_count`

     (integer) The number of ingest pipelines that currently refer to the model. 

### 响应码

"404"(缺少资源)

     If `allow_no_match` is `false`, this code indicates that there are no resources that match the request or only partial matches for the request. 

###Examples

以下示例获取所有已训练模型的使用情况信息：

    
    
    response = client.ml.get_trained_models_stats
    puts response
    
    
    GET _ml/trained_models/_stats

API 返回以下结果：

    
    
    {
      "count": 2,
      "trained_model_stats": [
        {
          "model_id": "flight-delay-prediction-1574775339910",
          "pipeline_count": 0,
          "inference_stats": {
            "failure_count": 0,
            "inference_count": 4,
            "cache_miss_count": 3,
            "missing_all_fields_count": 0,
            "timestamp": 1592399986979
          }
        },
        {
          "model_id": "regression-job-one-1574775307356",
          "pipeline_count": 1,
          "inference_stats": {
            "failure_count": 0,
            "inference_count": 178,
            "cache_miss_count": 3,
            "missing_all_fields_count": 0,
            "timestamp": 1592399986979
          },
          "ingest": {
            "total": {
              "count": 178,
              "time_in_millis": 8,
              "current": 0,
              "failed": 0
            },
            "pipelines": {
              "flight-delay": {
                "count": 178,
                "time_in_millis": 8,
                "current": 0,
                "failed": 0,
                "processors": [
                  {
                    "inference": {
                      "type": "inference",
                      "stats": {
                        "count": 178,
                        "time_in_millis": 7,
                        "current": 0,
                        "failed": 0
                      }
                    }
                  }
                ]
              }
            }
          }
        }
      ]
    }

[« Get trained models API](get-trained-models.md) [Infer trained model API
»](infer-trained-model.md)
