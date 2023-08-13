

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning trained model APIs](ml-df-trained-
models-apis.md)

[« Start trained model deployment API](start-trained-model-deployment.md)
[Update trained model deployment API »](update-trained-model-deployment.md)

## 停止训练模型部署API

停止已训练的模型部署。

###Request

"发布_ml/trained_models/<deployment_id>/部署/_stop"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

只有具有 PyTorch'model_type' 的训练模型才需要部署。

### 路径参数

`<deployment_id>`

     (Required, string) A unique identifier for the deployment of the model. 

### 查询参数

`allow_no_match`

    

(可选，布尔值)指定在请求时要执行的操作：

* 包含通配符表达式，并且没有匹配的部署。  * 包含"_all"字符串或不包含标识符，并且没有匹配项。  * 包含通配符表达式，并且只有部分匹配。

默认值为"true"，当没有匹配项时返回一个空数组，当存在部分匹配时返回结果子集。如果此参数为"false"，则当没有匹配项或只有部分匹配项时，请求将返回"404"状态代码。

`force`

     (Optional, Boolean) If true, the deployment is stopped even if it or one of its model aliases is referenced by ingest pipelines. You can't use these pipelines until you restart the model deployment. 

###Examples

以下示例停止"my_model_for_search"部署：

    
    
    POST _ml/trained_models/my_model_for_search/deployment/_stop

[« Start trained model deployment API](start-trained-model-deployment.md)
[Update trained model deployment API »](update-trained-model-deployment.md)
