

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning trained model APIs](ml-df-trained-
models-apis.md)

[« Clear trained model deployment cache API](clear-trained-model-deployment-
cache.md) [Create trained model definition part API »](put-trained-model-
definition-part.md)

## 创建或更新训练模型别名API

创建或更新已训练的模型别名。

训练模型别名是用于引用单个训练模型的逻辑名称。

###Request

"把_ml/trained_models/<model_id>/model_aliases/<model_alias>"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

可以使用别名而不是经过训练的模型标识符，以便更轻松地引用模型。例如，您可以在推理聚合和处理器中使用别名。

别名必须是唯一的，并且仅引用单个经过训练的模型。但是，每个训练的模型可以有多个别名。

接口限制：

* 不允许更新别名，使其引用不同的训练模型 ID，并且模型使用不同类型的数据帧分析。例如，如果您有用于回归分析的训练模型和用于分类分析的训练模型，则会出现这种情况;不能将别名从一种类型的训练模型重新分配给另一种类型的训练模型。  * 您无法从"pytorch"模型和数据帧分析模型更新别名。  * 您无法将别名从已部署的"pytorch"模型更新为当前未部署的模型。

如果使用此 API 更新别名，并且模型别名的新旧训练模型之间很少有不常见的输入字段，则 API 会返回警告。

### 路径参数

`model_alias`

     (Required, string) The alias to create or update. This value cannot end in numbers. 
`model_id`

     (Required, string) The identifier for the trained model that the alias refers to. 

### 查询参数

`reassign`

     (Optional, boolean) Specifies whether the alias gets reassigned to the specified trained model if it is already assigned to a different model. If the alias is already assigned and this parameter is `false`, the API returns an error. Defaults to `false`. 

###Examples

#### 创建经过训练的模型别名

以下示例演示如何为经过训练的模型创建别名 ("flight_delay_model")("航班延迟预测-1574775339910")：

    
    
    response = client.ml.put_trained_model_alias(
      model_id: 'flight-delay-prediction-1574775339910',
      model_alias: 'flight_delay_model'
    )
    puts response
    
    
    PUT _ml/trained_models/flight-delay-prediction-1574775339910/model_aliases/flight_delay_model

#### 更新已训练的模型别名

以下示例演示如何将别名 ('flight_delay_model') 重新分配给不同的训练模型 ('flight-delay-prediction-1580004349800')：

    
    
    response = client.ml.put_trained_model_alias(
      model_id: 'flight-delay-prediction-1580004349800',
      model_alias: 'flight_delay_model',
      reassign: true
    )
    puts response
    
    
    PUT _ml/trained_models/flight-delay-prediction-1580004349800/model_aliases/flight_delay_model?reassign=true

[« Clear trained model deployment cache API](clear-trained-model-deployment-
cache.md) [Create trained model definition part API »](put-trained-model-
definition-part.md)
