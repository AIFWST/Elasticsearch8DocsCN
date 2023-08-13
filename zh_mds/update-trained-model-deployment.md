

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning trained model APIs](ml-df-trained-
models-apis.md)

[« Stop trained model deployment API](stop-trained-model-deployment.md)
[Migration APIs »](migration-api.md)

## 更新训练模型部署接口

更新已训练模型部署的某些属性。

此功能处于测试阶段，可能会发生变化。设计和代码不如官方 GA 功能成熟，并且按原样提供，不提供任何保证。测试版功能不受官方 GA 功能的支持 SLA 的约束。

###Request

"发布_ml/trained_models/<deployment_id>/部署/_update"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

可以更新"assignment_state"已启动"的已训练模型部署。您可以增加或减少此类部署的分配数。

### 路径参数

`<deployment_id>`

     (Required, string) A unique identifier for the deployment of the model. 

### 请求正文

`number_of_allocations`

     (Optional, integer) The total number of allocations this model is assigned across machine learning nodes. Increasing this value generally increases the throughput. 

###Examples

以下示例将"elastic__distilbert-base-uncased-finetuned-conll03-english"训练模型的部署更新为具有 4 个分配：

    
    
    response = client.ml.update_trained_model_deployment(
      model_id: 'elastic__distilbert-base-uncased-finetuned-conll03-english',
      body: {
        number_of_allocations: 4
      }
    )
    puts response
    
    
    POST _ml/trained_models/elastic__distilbert-base-uncased-finetuned-conll03-english/deployment/_update
    {
      "number_of_allocations": 4
    }

API 返回以下结果：

    
    
    {
        "assignment": {
            "task_parameters": {
                "model_id": "elastic__distilbert-base-uncased-finetuned-conll03-english",
                "model_bytes": 265632637,
                "threads_per_allocation" : 1,
                "number_of_allocations" : 4,
                "queue_capacity" : 1024
            },
            "routing_table": {
                "uckeG3R8TLe2MMNBQ6AGrw": {
                    "current_allocations": 1,
                    "target_allocations": 4,
                    "routing_state": "started",
                    "reason": ""
                }
            },
            "assignment_state": "started",
            "start_time": "2022-11-02T11:50:34.766591Z"
        }
    }

[« Stop trained model deployment API](stop-trained-model-deployment.md)
[Migration APIs »](migration-api.md)
