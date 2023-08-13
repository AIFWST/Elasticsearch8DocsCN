

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning trained model APIs](ml-df-trained-
models-apis.md)

[« Machine learning trained model APIs](ml-df-trained-models-apis.md)
[Create or update trained model aliases API »](put-trained-models-
aliases.md)

## 清除经过训练的模型部署缓存

清除分配了部署的所有节点上的推理缓存。

###Request

"POST _ml/trained_models/<deployment_id>/deployment/cache/_clear"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

经过训练的模型部署可能启用了推理缓存。由于请求由每个分配的节点处理，因此它们的响应可能会缓存在该单个节点上。调用此 API 会清除缓存，而无需重新启动部署。

### 路径参数

`deployment_id`

     (Required, string) A unique identifier for the deployment of the model. 

###Examples

以下示例清除了"elastic__distilbert-base-uncased-finetuned-conll03-english"训练模型的新部署的缓存：

    
    
    response = client.ml.clear_trained_model_deployment_cache(
      model_id: 'elastic__distilbert-base-uncased-finetuned-conll03-english'
    )
    puts response
    
    
    POST _ml/trained_models/elastic__distilbert-base-uncased-finetuned-conll03-english/deployment/cache/_clear

API 返回以下结果：

    
    
    {
       "cleared": true
    }

[« Machine learning trained model APIs](ml-df-trained-models-apis.md)
[Create or update trained model aliases API »](put-trained-models-
aliases.md)
