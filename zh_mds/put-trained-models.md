

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning trained model APIs](ml-df-trained-
models-apis.md)

[« Create or update trained model aliases API](put-trained-models-
aliases.md) [Create trained models API »](put-trained-models.md)

## 创建训练模型定义部分API

创建已训练模型定义的一部分。

###Request

'把_ml/trained_models/<model_id>/定义/<part_num>'

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

### 路径参数

`<model_id>`

     (Required, string) The unique identifier of the trained model. 
`<part>`

     (Required, number) The definition part number. When the definition is loaded for inference the definition parts will be streamed in order of their `part_num`. The first part must be `0` and the final part must be `total_parts - 1`. 

### 请求正文

`definition`

     (Required, string) The definition part for the model. Must be a base64 encoded string. 
`total_definition_length`

     (Required, number) The total uncompressed definition length in bytes. Not base64 encoded. 
`total_parts`

     (Required, number) The total number of parts that will be uploaded. Must be greater than 0. 

###Examples

下面的示例为以前存储的模型配置创建模型定义部件。定义部分存储在由"location.index.name"配置的索引中。

"definition"对象的值从示例中省略，因为它是一个非常大的base64编码字符串。

    
    
    PUT _ml/trained_models/elastic__distilbert-base-uncased-finetuned-conll03-english/definition/0
    {
        "definition": "...",
        "total_definition_length": 265632637,
        "total_parts": 64
    }

API 返回以下结果：

    
    
    {
        "acknowledged": true
    }

[« Create or update trained model aliases API](put-trained-models-
aliases.md) [Create trained models API »](put-trained-models.md)
