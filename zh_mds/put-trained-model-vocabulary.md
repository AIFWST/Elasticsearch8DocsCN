

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning trained model APIs](ml-df-trained-
models-apis.md)

[« Create trained models API](put-trained-models.md) [Delete trained model
aliases API »](delete-trained-models-aliases.md)

## 创建训练模型词汇接口

创建经过训练的模型词汇表。这仅适用于自然语言处理 (NLP) 模型。

###Request

"输入_ml/trained_models/<model_id>/词汇/"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

词汇表存储在索引中，如训练模型定义的"inference_config.*.vocabulary"中所述。

### 路径参数

`<model_id>`

     (Required, string) The unique identifier of the trained model. 

### 请求正文

`vocabulary`

     (array) The model vocabulary. Must not be empty. 
`merges`

     (Optional, array) The model merges used in byte-pair encoding. The merges must be sub-token pairs, space delimited, and in order of preference. Example: ["f o", "fo o"]. Must be provided for RoBERTa and BART style models. 
`scores`

     (Optional, array) Vocabulary value scores used by sentence-piece tokenization. Must have the same length as `vocabulary`. Required for unigram sentence-piece tokenized models like XLMRoberta and T5. 

###Examples

以下示例演示如何为以前存储的训练模型配置创建模型词汇表。

    
    
    PUT _ml/trained_models/elastic__distilbert-base-uncased-finetuned-conll03-english/vocabulary
    {
      "vocabulary": [
        "[PAD]",
        "[unused0]",
        ...
      ]
    }

API 返回以下结果：

    
    
    {
        "acknowledged": true
    }

[« Create trained models API](put-trained-models.md) [Delete trained model
aliases API »](delete-trained-models-aliases.md)
