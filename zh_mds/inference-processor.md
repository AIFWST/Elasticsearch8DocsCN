

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« HTML strip processor](htmlstrip-processor.md) [Join processor »](join-
processor.md)

## 推理处理器

使用预先训练的数据帧分析模型或为自然语言处理任务部署的模型来推断管道中摄取的数据。

**表 27.推理选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'model_id' .

|

yes

|

-

|

(字符串)已训练模型的 ID 或别名，或部署的 ID。   "target_field"

|

no

|

`ml.inference.<processor_tag>`

|

(字符串)添加到传入文档以包含结果对象的字段。   "field_map"

|

no

|

如果定义了模型的默认字段映射

|

(对象)将文档字段名称映射到模型的已知字段名称。此映射优先于模型配置中提供的任何默认映射。   "inference_config"

|

no

|

模型中定义的默认设置

|

(对象)包含推理类型及其选项。   "说明"

|

no

|

-

|

处理器的说明。用于描述处理器的目的或其配置。   "如果"

|

no

|

-

|

有条件地执行处理器。请参阅有条件运行处理器。   "ignore_failure"

|

no

|

`false`

|

忽略处理器的故障。请参阅处理管道故障。   "on_failure"

|

no

|

-

|

处理处理器的故障。请参阅处理管道故障。   "标签"

|

no

|

-

|

处理器的标识符。对于调试和指标很有用。               { "推理"： { "model_id"： "model_deployment_for_inference"， "target_field"： "FlightDelayMin_prediction_infer"， "field_map"： { "your_field"： "my_field" }， "inference_config"： { "回归"： {} } } } }

#### 分类配置选项

用于推理的分类配置。

`num_top_classes`

     (Optional, integer) Specifies the number of top class predictions to return. Defaults to 0. 
`num_top_feature_importance_values`

     (Optional, integer) Specifies the maximum number of [feature importance](/guide/en/machine-learning/8.9/ml-feature-importance.html) values per document. Defaults to 0 which means no feature importance calculation occurs. 
`results_field`

     (Optional, string) The field that is added to incoming documents to contain the inference prediction. Defaults to the `results_field` value of the data frame analytics job that was used to train the model, which defaults to `<dependent_variable>_prediction`. 
`top_classes_results_field`

     (Optional, string) Specifies the field to which the top classes are written. Defaults to `top_classes`. 
`prediction_field_type`

     (Optional, string) Specifies the type of the predicted field to write. Valid values are: `string`, `number`, `boolean`. When `boolean` is provided `1.0` is transformed to `true` and `0.0` to `false`. 

#### 填充掩码配置选项

`num_top_classes`

     (Optional, integer) Specifies the number of top class predictions to return. Defaults to 0. 
`results_field`

     (Optional, string) The field that is added to incoming documents to contain the inference prediction. Defaults to the `results_field` value of the data frame analytics job that was used to train the model, which defaults to `<dependent_variable>_prediction`. 
`tokenization`

    

(可选，对象)指示要执行的标记化和所需的设置。默认标记化配置为"bert"。有效的标记化值为

* 'bert'：用于 BERT 风格的模型 * 'mpnet'：用于 MPNet 风格的模型 * 'roberta'：用于 RoBERTa 风格的和 BART 风格的模型 * [预览] 此功能处于技术预览阶段，可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持约束。 "xlm_roberta"：用于 XLMRoBERTa 样式的模型 * [预览] 此功能处于技术预览状态，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持约束。 "bert_ja"：用于为日语训练的BERT风格模型。

标记化的属性

`bert`

    

(可选，对象)BERT风格的标记化将使用封闭的设置执行。

伯特的性质

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`roberta`

    

(可选，对象)RoBERTa风格的标记化将使用封闭的设置执行。

罗伯塔的属性

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`mpnet`

    

(可选，对象)MPNet样式的标记化将使用封闭的设置执行。

mpnet 的属性

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

#### NER 配置选项

`results_field`

     (Optional, string) The field that is added to incoming documents to contain the inference prediction. Defaults to the `results_field` value of the data frame analytics job that was used to train the model, which defaults to `<dependent_variable>_prediction`. 
`tokenization`

    

(可选，对象)指示要执行的标记化和所需的设置。默认标记化配置为"bert"。有效的标记化值为

* 'bert'：用于 BERT 风格的模型 * 'mpnet'：用于 MPNet 风格的模型 * 'roberta'：用于 RoBERTa 风格的和 BART 风格的模型 * [预览] 此功能处于技术预览阶段，可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持约束。 "xlm_roberta"：用于 XLMRoBERTa 样式的模型 * [预览] 此功能处于技术预览状态，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持约束。 "bert_ja"：用于为日语训练的BERT风格模型。

标记化的属性

`bert`

    

(可选，对象)BERT风格的标记化将使用封闭的设置执行。

伯特的性质

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`roberta`

    

(可选，对象)RoBERTa风格的标记化将使用封闭的设置执行。

罗伯塔的属性

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`mpnet`

    

(可选，对象)MPNet样式的标记化将使用封闭的设置执行。

mpnet 的属性

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

#### 回归配置选项

用于推理的回归配置。

`results_field`

     (Optional, string) The field that is added to incoming documents to contain the inference prediction. Defaults to the `results_field` value of the data frame analytics job that was used to train the model, which defaults to `<dependent_variable>_prediction`. 
`num_top_feature_importance_values`

     (Optional, integer) Specifies the maximum number of [feature importance](/guide/en/machine-learning/8.9/ml-feature-importance.html) values per document. By default, it is zero and no feature importance calculation occurs. 

#### 文本分类配置选项

`classification_labels`

     (Optional, string) An array of classification labels. 
`num_top_classes`

     (Optional, integer) Specifies the number of top class predictions to return. Defaults to 0. 
`results_field`

     (Optional, string) The field that is added to incoming documents to contain the inference prediction. Defaults to the `results_field` value of the data frame analytics job that was used to train the model, which defaults to `<dependent_variable>_prediction`. 
`tokenization`

    

(可选，对象)指示要执行的标记化和所需的设置。默认标记化配置为"bert"。有效的标记化值为

* 'bert'：用于 BERT 风格的模型 * 'mpnet'：用于 MPNet 风格的模型 * 'roberta'：用于 RoBERTa 风格的和 BART 风格的模型 * [预览] 此功能处于技术预览阶段，可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持约束。 "xlm_roberta"：用于 XLMRoBERTa 样式的模型 * [预览] 此功能处于技术预览状态，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持约束。 "bert_ja"：用于为日语训练的BERT风格模型。

标记化的属性

`bert`

    

(可选，对象)BERT风格的标记化将使用封闭的设置执行。

伯特的性质

`span`

    

(可选，整数)当"截断"为"无"时，您可以对较长的文本序列进行分区以进行推理。该值指示每个子序列之间重叠的标记数。

默认值为"-1"，表示不发生窗口或跨越。

当您的典型输入仅略大于"max_sequence_length"时，最好简单地截断;第二个子序列中的信息将很少。

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`roberta`

    

(可选，对象)RoBERTa风格的标记化将使用封闭的设置执行。

罗伯塔的属性

`span`

    

(可选，整数)当"截断"为"无"时，您可以对较长的文本序列进行分区以进行推理。该值指示每个子序列之间重叠的标记数。

默认值为"-1"，表示不发生窗口或跨越。

当您的典型输入仅略大于"max_sequence_length"时，最好简单地截断;第二个子序列中的信息将很少。

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`mpnet`

    

(可选，对象)MPNet样式的标记化将使用封闭的设置执行。

mpnet 的属性

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

#### 文本嵌入配置选项

`results_field`

     (Optional, string) The field that is added to incoming documents to contain the inference prediction. Defaults to the `results_field` value of the data frame analytics job that was used to train the model, which defaults to `<dependent_variable>_prediction`. 
`tokenization`

    

(可选，对象)指示要执行的标记化和所需的设置。默认标记化配置为"bert"。有效的标记化值为

* 'bert'：用于 BERT 风格的模型 * 'mpnet'：用于 MPNet 风格的模型 * 'roberta'：用于 RoBERTa 风格的和 BART 风格的模型 * [预览] 此功能处于技术预览阶段，可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持约束。 "xlm_roberta"：用于 XLMRoBERTa 样式的模型 * [预览] 此功能处于技术预览状态，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持约束。 "bert_ja"：用于为日语训练的BERT风格模型。

标记化的属性

`bert`

    

(可选，对象)BERT风格的标记化将使用封闭的设置执行。

伯特的性质

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`roberta`

    

(可选，对象)RoBERTa风格的标记化将使用封闭的设置执行。

罗伯塔的属性

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`mpnet`

    

(可选，对象)MPNet样式的标记化将使用封闭的设置执行。

mpnet 的属性

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

#### 零镜头分类配置选项

`labels`

     (Optional, array) The labels to classify. Can be set at creation for default labels, and then updated during inference. 
`multi_label`

     (Optional, boolean) Indicates if more than one `true` label is possible given the input. This is useful when labeling text that could pertain to more than one of the input labels. Defaults to `false`. 
`results_field`

     (Optional, string) The field that is added to incoming documents to contain the inference prediction. Defaults to the `results_field` value of the data frame analytics job that was used to train the model, which defaults to `<dependent_variable>_prediction`. 
`tokenization`

    

(可选，对象)指示要执行的标记化和所需的设置。默认标记化配置为"bert"。有效的标记化值为

* 'bert'：用于 BERT 风格的模型 * 'mpnet'：用于 MPNet 风格的模型 * 'roberta'：用于 RoBERTa 风格的和 BART 风格的模型 * [预览] 此功能处于技术预览阶段，可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持约束。 "xlm_roberta"：用于 XLMRoBERTa 样式的模型 * [预览] 此功能处于技术预览状态，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持约束。 "bert_ja"：用于为日语训练的BERT风格模型。

标记化的属性

`bert`

    

(可选，对象)BERT风格的标记化将使用封闭的设置执行。

伯特的性质

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`roberta`

    

(可选，对象)RoBERTa风格的标记化将使用封闭的设置执行。

罗伯塔的属性

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`mpnet`

    

(可选，对象)MPNet样式的标记化将使用封闭的设置执行。

mpnet 的属性

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

#### 推理处理器示例

    
    
    "inference":{
      "model_id": "my_model_id",
      "field_map": {
        "original_fieldname": "expected_fieldname"
      },
      "inference_config": {
        "regression": {
          "results_field": "my_regression"
        }
      }
    }

此配置指定"回归"推理，结果将写入"target_field"结果对象中包含的"my_regression"字段。"field_map"配置将源文档中的字段"original_fieldname"映射到模型所需的字段。

    
    
    "inference":{
      "model_id":"my_model_id"
      "inference_config": {
        "classification": {
          "num_top_classes": 2,
          "results_field": "prediction",
          "top_classes_results_field": "probabilities"
        }
      }
    }

此配置指定"分类"推理。报告预测概率的类别数为 2('num_top_classes')。结果将写入"预测"字段，并将顶级类写入"概率"字段。这两个字段都包含在"target_field"结果对象中。

有关使用自然语言处理训练模型的示例，请参阅将 NLP 推理添加到引入管道。

#### 功能重要性对象映射

要获得聚合和搜索特征重要性的全部好处，请更新特征重要性结果字段的索引映射，如下所示：

    
    
    "ml.inference.feature_importance": {
      "type": "nested",
      "dynamic": true,
      "properties": {
        "feature_name": {
          "type": "keyword"
        },
        "importance": {
          "type": "double"
        }
      }
    }

特征重要性的映射字段名称(在上面的示例中为"ml.inference.feature_importance")组合如下：

`<ml.inference.target_field>`.`<inference.tag>`.`feature_importance`

* "<ml.inference.target_field>"：默认为"ml.inference"。  * "<inference.tag>"：如果处理器定义中未提供，则它不是字段路径的一部分。

例如，如果您在定义中提供标签"foo"，如下所示：

    
    
    {
      "tag": "foo",
      ...
    }

然后，将特征重要性值写入"ml.inference.foo.feature_importance"字段。

您还可以按如下方式指定目标字段：

    
    
    {
      "tag": "foo",
      "target_field": "my_field"
    }

在这种情况下，特征重要性显示在"my_field.foo.feature_important"字段中。

[« HTML strip processor](htmlstrip-processor.md) [Join processor »](join-
processor.md)
