

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning trained model APIs](ml-df-trained-
models-apis.md)

[« Create trained model vocabulary API](put-trained-model-vocabulary.md)
[Delete trained models API »](delete-trained-models.md)

## 删除训练好的模型别名API

删除已训练的模型别名。

###Request

"删除_ml/trained_models/<model_id>/model_aliases<model_alias>/"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

此 API 删除引用已训练模型的现有模型别名。

如果模型别名缺失或引用的模型不是由"model_id"标识的模型，则此 API 将返回错误。

### 路径参数

`model_alias`

     (Required, string) The model alias to delete. 
`model_id`

     (Required, string) The trained model ID to which the model alias refers. 

###Examples

以下示例演示如何删除已训练模型 ID 的模型别名 ("flight_delay_model")("航班延迟预测-1574775339910")：

    
    
    response = client.ml.delete_trained_model_alias(
      model_id: 'flight-delay-prediction-1574775339910',
      model_alias: 'flight_delay_model'
    )
    puts response
    
    
    DELETE _ml/trained_models/flight-delay-prediction-1574775339910/model_aliases/flight_delay_model

[« Create trained model vocabulary API](put-trained-model-vocabulary.md)
[Delete trained models API »](delete-trained-models.md)
