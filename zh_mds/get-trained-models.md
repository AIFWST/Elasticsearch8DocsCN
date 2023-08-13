

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning trained model APIs](ml-df-trained-
models-apis.md)

[« Delete trained model aliases API](delete-trained-models-aliases.md) [Get
trained models API »](get-trained-models.md)

## 删除训练模型接口

删除现有的训练推理模型。

###Request

"删除_ml/trained_models<model_id>/"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

### 路径参数

`<model_id>`

     (Optional, string) The unique identifier of the trained model. 

### 查询参数

`force`

     (Optional, Boolean) Use to forcefully delete a trained model that is referenced by ingest pipelines or has a started deployment. 

### 响应码

`409`

     The code indicates that the trained model is referenced by an ingest pipeline and cannot be deleted. 

###Examples

以下示例删除"回归作业一-1574775307356"训练模型：

    
    
    response = client.ml.delete_trained_model(
      model_id: 'regression-job-one-1574775307356'
    )
    puts response
    
    
    DELETE _ml/trained_models/regression-job-one-1574775307356

API 返回以下结果：

    
    
    {
      "acknowledged" : true
    }

[« Delete trained model aliases API](delete-trained-models-aliases.md) [Get
trained models API »](get-trained-models.md)
