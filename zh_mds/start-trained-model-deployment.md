

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning trained model APIs](ml-df-trained-
models-apis.md)

[« Infer trained model API](infer-trained-model.md) [Stop trained model
deployment API »](stop-trained-model-deployment.md)

## 启动训练模型部署API

启动新的训练模型部署。

###Request

"发布_ml/trained_models/<model_id>/部署/_start"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

目前仅支持"pytorch"模型进行部署。部署模型后，推理处理器可以在采集管道中使用模型，也可以直接在推断训练模型 API 中使用。

可以使用部署 ID 多次部署模型。部署 ID 必须是唯一的，并且不应与任何其他部署 ID 或模型 ID 匹配，除非它与正在部署的模型的 ID 相同。如果未设置"deployment_id"，则默认为"model_id"。

可以通过设置参数"number_of_allocations"和"threads_per_allocation"来实现扩展推理性能。

增加"threads_per_allocation"意味着在节点上处理推理请求时使用的线程更多。这可以提高某些模型的推理速度。它还可能导致吞吐量的提高。

增加"number_of_allocations"意味着使用更多线程并行处理多个推理请求，从而提高吞吐量。每个模型分配都使用由"threads_per_allocation"定义的多个线程。

模型分配分布在机器学习节点上。分配给节点的所有分配在内存中共享模型的相同副本。为了避免对性能不利的线程超额订阅，模型分配的分布方式使使用的线程总数不超过节点分配的处理器数。

### 路径参数

`<model_id>`

     (Required, string) The unique identifier of the trained model. 

### 查询参数

`cache_size`

     (Optional, [byte value](api-conventions.html#byte-units "Byte size units")) The inference cache size (in memory outside the JVM heap) per node for the model. The default value is the size of the model as reported by the `model_size_bytes` field in the [Get trained models stats](get-trained-models-stats.html "Get trained models statistics API"). To disable the cache, `0b` can be provided. 
`deployment_id`

     (Optional, string) A unique identifier for the deployment of the model. 

默认为"model_id"。

`number_of_allocations`

     (Optional, integer) The total number of allocations this model is assigned across machine learning nodes. Increasing this value generally increases the throughput. Defaults to 1. 
`priority`

    

(可选，字符串)部署的优先级。默认值为"正常"。有两个优先级设置：

* "正常"：将其用于生产中的部署。部署分配是分布式的，以便节点处理器不会超额订阅。  * "低"：用于测试模型功能。目的是不会向这些部署发送大量输入。部署需要只有一个线程的单个分配。可以在已利用其所有处理器的节点上分配低优先级部署，但将获得比正常部署更低的 CPU 优先级。可以取消分配低优先级部署，以满足正常优先级部署的更多分配。

大量使用低优先级部署可能会影响正常优先级部署的性能。

`queue_capacity`

     (Optional, integer) Controls how many inference requests are allowed in the queue at a time. Every machine learning node in the cluster where the model can be allocated has a queue of this size; when the number of requests exceeds the total value, new requests are rejected with a 429 error. Defaults to 1024. Max allowed value is 1000000. 
`threads_per_allocation`

     (Optional, integer) Sets the number of threads used by each model allocation during inference. This generally increases the speed per inference request. The inference process is a compute-bound process; `threads_per_allocations` must not exceed the number of available allocated processors per node. Defaults to 1. Must be a power of 2. Max allowed value is 32. 
`timeout`

     (Optional, time) Controls the amount of time to wait for the model to deploy. Defaults to 30 seconds. 
`wait_for`

     (Optional, string) Specifies the allocation status to wait for before returning. Defaults to `started`. The value `starting` indicates deployment is starting but not yet on any node. The value `started` indicates the model has started on at least one node. The value `fully_allocated` indicates the deployment has started on all valid nodes. 

###Examples

以下示例为"elastic__distilbert-base-uncased-finetuned-conll03-english"训练模型启动新部署：

    
    
    POST _ml/trained_models/elastic__distilbert-base-uncased-finetuned-conll03-english/deployment/_start?wait_for=started&timeout=1m

API 返回以下结果：

    
    
    {
        "assignment": {
            "task_parameters": {
                "model_id": "elastic__distilbert-base-uncased-finetuned-conll03-english",
                "model_bytes": 265632637,
                "threads_per_allocation" : 1,
                "number_of_allocations" : 1,
                "queue_capacity" : 1024,
                "priority": "normal"
            },
            "routing_table": {
                "uckeG3R8TLe2MMNBQ6AGrw": {
                    "routing_state": "started",
                    "reason": ""
                }
            },
            "assignment_state": "started",
            "start_time": "2022-11-02T11:50:34.766591Z"
        }
    }

#### 使用部署 ID

以下示例为 ID 为"my_model_for_ingest"的"my_model"训练模型启动新部署。部署 ID 用于推理 API 调用或推理处理器。

    
    
    POST _ml/trained_models/my_model/deployment/_start?deployment_id=my_model_for_ingest

可以使用不同的 ID 再次部署"my_model"训练的模型：

    
    
    POST _ml/trained_models/my_model/deployment/_start?deployment_id=my_model_for_search

[« Infer trained model API](infer-trained-model.md) [Stop trained model
deployment API »](stop-trained-model-deployment.md)
