

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning trained model APIs](ml-df-trained-
models-apis.md)

[« Get trained models statistics API](get-trained-models-stats.md) [Start
trained model deployment API »](start-trained-model-deployment.md)

## 推断训练模型API

评估已训练的模型。该模型可以是任何通过数据帧分析训练或导入的监督模型。

对于启用了缓存的模型部署，可以直接从推理缓存返回结果。

###Request

"发布_ml/trained_models/<model_id>/_infer" "POST_ml/trained_models/<deployment_id>/_infer"

### 路径参数

`<model_id>`

     (Optional, string) The unique identifier of the trained model or a model alias. 

如果在 API 调用中指定"model_id"，并且模型具有多个部署，则将使用随机部署。如果"model_id"与其中一个部署的 ID 匹配，则将使用该部署。

`<deployment_id>`

     (Optional, string) A unique identifier for the deployment of the model. 

### 查询参数

`timeout`

     (Optional, time) Controls the amount of time to wait for inference results. Defaults to 10 seconds. 

### 请求正文

`docs`

     (Required, array) An array of objects to pass to the model for inference. The objects should contain the fields matching your configured trained model input. Typically for NLP models, the field name is `text_field`. 

`inference_config`

    

(可选，对象)推理的默认配置。这可以是："回归"、"分类"、"fill_mask"、"ner"、"question_answering"、"text_classification"、"text_embedding"或"zero_shot_classification"。如果是"回归"或"分类"，它必须与底层"definition.trained_model"的"target_type"匹配。如果是"fill_mask"、"ner"、"question_answering"、"text_classification"或"text_embedding";"model_type"必须是"PyTorch"。如果未指定，则使用创建模型时的"inference_config"。

"inference_config"的属性

`classification`

    

(可选，对象)用于推理的分类配置。

分类推理的属性

`num_top_classes`

     (Optional, integer) Specifies the number of top class predictions to return. Defaults to 0. 
`num_top_feature_importance_values`

     (Optional, integer) Specifies the maximum number of [feature importance](/guide/en/machine-learning/8.9/ml-feature-importance.html) values per document. Defaults to 0 which means no feature importance calculation occurs. 
`prediction_field_type`

     (Optional, string) Specifies the type of the predicted field to write. Valid values are: `string`, `number`, `boolean`. When `boolean` is provided `1.0` is transformed to `true` and `0.0` to `false`. 
`results_field`

     (Optional, string) The field that is added to incoming documents to contain the inference prediction. Defaults to `predicted_value`. 
`top_classes_results_field`

     (Optional, string) Specifies the field to which the top classes are written. Defaults to `top_classes`. 

`fill_mask`

    

(可选，对象)fill_mask自然语言处理 (NLP) 任务的配置。fill_mask任务适用于针对填充蒙版操作优化的模型。例如，对于BERT模型，可能会提供以下文本："法国的首都是[MASK]。响应指示最有可能替换"[MASK]"的值。在这种情况下，最可能的代币是"巴黎"。

fill_mask推理的属性

`num_top_classes`

     (Optional, integer) Number of top predicted tokens to return for replacing the mask token. Defaults to `0`. 
`results_field`

     (Optional, string) The field that is added to incoming documents to contain the inference prediction. Defaults to `predicted_value`. 
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

`xlm_roberta`

    

(可选，对象) [预览] 此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的支持 SLA 的约束。 XLMRoBERTa风格的标记化将使用随附的设置执行。

xlm_roberta的性质

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`bert_ja`

    

(可选，对象) [预览] 此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的支持 SLA 的约束。 日语文本的BERT样式标记化将使用随附的设置执行。

bert_ja的性质

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`ner`

    

(可选，对象)配置命名实体识别 (NER) 任务。NER是令牌分类的一个特例。序列中的每个标记都根据提供的分类标签进行分类。目前，NER 任务需要"classification_labels"内-外-开始 (IOB) 格式标签。仅支持人员、组织、位置和杂项。

ner推理的属性

`results_field`

     (Optional, string) The field that is added to incoming documents to contain the inference prediction. Defaults to `predicted_value`. 
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

`xlm_roberta`

    

(可选，对象) [预览] 此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的支持 SLA 的约束。 XLMRoBERTa风格的标记化将使用随附的设置执行。

xlm_roberta的性质

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`bert_ja`

    

(可选，对象) [预览] 此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的支持 SLA 的约束。 日语文本的BERT样式标记化将使用随附的设置执行。

bert_ja的性质

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`pass_through`

    

(可选，对象)配置"pass_through"任务。此任务对于调试非常有用，因为不会对推理输出进行后处理，并且原始池层结果将返回给调用方。

pass_through推理的属性

`results_field`

     (Optional, string) The field that is added to incoming documents to contain the inference prediction. Defaults to `predicted_value`. 
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

`xlm_roberta`

    

(可选，对象) [预览] 此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的支持 SLA 的约束。 XLMRoBERTa风格的标记化将使用随附的设置执行。

xlm_roberta的性质

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`bert_ja`

    

(可选，对象) [预览] 此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的支持 SLA 的约束。 日语文本的BERT样式标记化将使用随附的设置执行。

bert_ja的性质

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`question_answering`

    

(可选，对象)配置问答自然语言处理 (NLP) 任务。问答对于从大量文本语料库中提取某些问题的答案非常有用。

question_answering推理的属性

`max_answer_length`

     (Optional, integer) The maximum amount of words in the answer. Defaults to `15`. 
`num_top_classes`

     (Optional, integer) The number the top found answers to return. Defaults to `0`, meaning only the best found answer is returned. 
`question`

     (Required, string) The question to use when extracting an answer 
`results_field`

     (Optional, string) The field that is added to incoming documents to contain the inference prediction. Defaults to `predicted_value`. 
`tokenization`

    

(可选，对象)指示要执行的标记化和所需的设置。默认标记化配置为"bert"。有效的标记化值为

* 'bert'：用于 BERT 风格的模型 * 'mpnet'：用于 MPNet 风格的模型 * 'roberta'：用于 RoBERTa 风格的和 BART 风格的模型 * [预览] 此功能处于技术预览阶段，可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持约束。 "xlm_roberta"：用于 XLMRoBERTa 样式的模型 * [预览] 此功能处于技术预览状态，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持约束。 "bert_ja"：用于为日语训练的BERT风格模型。

建议将"max_sequence_length"设置为"386"，并将"span"设置为"128"，并将"截断"设置为"none"。

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

`span`

    

(可选，整数)当"截断"为"无"时，您可以对较长的文本序列进行分区以进行推理。该值指示每个子序列之间重叠的标记数。

默认值为"-1"，表示不发生窗口或跨越。

当您的典型输入仅略大于"max_sequence_length"时，最好简单地截断;第二个子序列中的信息将很少。

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`xlm_roberta`

    

(可选，对象) [预览] 此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的支持 SLA 的约束。 XLMRoBERTa风格的标记化将使用随附的设置执行。

xlm_roberta的性质

`span`

    

(可选，整数)当"截断"为"无"时，您可以对较长的文本序列进行分区以进行推理。该值指示每个子序列之间重叠的标记数。

默认值为"-1"，表示不发生窗口或跨越。

当您的典型输入仅略大于"max_sequence_length"时，最好简单地截断;第二个子序列中的信息将很少。

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`bert_ja`

    

(可选，对象) [预览] 此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的支持 SLA 的约束。 日语文本的BERT样式标记化将使用随附的设置执行。

bert_ja的性质

`span`

    

(可选，整数)当"截断"为"无"时，您可以对较长的文本序列进行分区以进行推理。该值指示每个子序列之间重叠的标记数。

默认值为"-1"，表示不发生窗口或跨越。

当您的典型输入仅略大于"max_sequence_length"时，最好简单地截断;第二个子序列中的信息将很少。

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`regression`

    

(可选，对象)用于推理的回归配置。

回归推理的属性

`num_top_feature_importance_values`

     (Optional, integer) Specifies the maximum number of [feature importance](/guide/en/machine-learning/8.9/ml-feature-importance.html) values per document. By default, it is zero and no feature importance calculation occurs. 
`results_field`

     (Optional, string) The field that is added to incoming documents to contain the inference prediction. Defaults to `predicted_value`. 

`text_classification`

    

(可选，对象)文本分类任务。文本分类将提供的文本序列分类为以前已知的目标类。这方面的一个具体示例是情绪分析，它返回可能的目标类指示文本情绪，例如"悲伤"、"快乐"或"愤怒"。

text_classification推理的属性

`classification_labels`

     (Optional, string) An array of classification labels. 
`num_top_classes`

     (Optional, integer) Specifies the number of top class predictions to return. Defaults to all classes (-1). 
`results_field`

     (Optional, string) The field that is added to incoming documents to contain the inference prediction. Defaults to `predicted_value`. 
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

`span`

    

(可选，整数)当"截断"为"无"时，您可以对较长的文本序列进行分区以进行推理。该值指示每个子序列之间重叠的标记数。

默认值为"-1"，表示不发生窗口或跨越。

当您的典型输入仅略大于"max_sequence_length"时，最好简单地截断;第二个子序列中的信息将很少。

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`xlm_roberta`

    

(可选，对象) [预览] 此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的支持 SLA 的约束。 XLMRoBERTa风格的标记化将使用随附的设置执行。

xlm_roberta的性质

`span`

    

(可选，整数)当"截断"为"无"时，您可以对较长的文本序列进行分区以进行推理。该值指示每个子序列之间重叠的标记数。

默认值为"-1"，表示不发生窗口或跨越。

当您的典型输入仅略大于"max_sequence_length"时，最好简单地截断;第二个子序列中的信息将很少。

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`bert_ja`

    

(可选，对象) [预览] 此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的支持 SLA 的约束。 日语文本的BERT样式标记化将使用随附的设置执行。

bert_ja的性质

`span`

    

(可选，整数)当"截断"为"无"时，您可以对较长的文本序列进行分区以进行推理。该值指示每个子序列之间重叠的标记数。

默认值为"-1"，表示不发生窗口或跨越。

当您的典型输入仅略大于"max_sequence_length"时，最好简单地截断;第二个子序列中的信息将很少。

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`text_embedding`

    

(对象，可选)文本嵌入采用输入序列并将其转换为数字向量。这些嵌入不仅捕获了令牌，还捕获了语义含义和上下文。这些嵌入可用于密集向量场以获得强大的见解。

text_embedding推理的属性

`results_field`

     (Optional, string) The field that is added to incoming documents to contain the inference prediction. Defaults to `predicted_value`. 
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

`xlm_roberta`

    

(可选，对象) [预览] 此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的支持 SLA 的约束。 XLMRoBERTa风格的标记化将使用随附的设置执行。

xlm_roberta的性质

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`bert_ja`

    

(可选，对象) [预览] 此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的支持 SLA 的约束。 日语文本的BERT样式标记化将使用随附的设置执行。

bert_ja的性质

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`text_similarity`

    

(对象，可选)文本相似性采用一个输入序列并将其与另一个输入序列进行比较。这通常称为交叉编码。此任务对于在将文档文本与其他提供的文本输入进行比较时对其进行排名非常有用。

text_similarity推理的属性

`span_score_combination_function`

    

(可选，字符串)标识当提供的文本段落长度超过"max_sequence_length"并且必须自动分隔以进行多次调用时，如何合并生成的相似性分数。这仅适用于"截断"为"无"且"span"为非负数的情况。默认值为"最大值"。可用选项包括：

* "max"：返回所有跨度的最高分。  * "mean"：返回所有跨度的平均分数。

`text`

     (Required, string) This is the text with which to compare all document provided text inputs. 
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

`with_special_tokens`

    

(可选，布尔值)使用特殊令牌进行标记化。BERT 样式标记化中通常包含的令牌包括：

* "[CLS]"：要分类的序列的第一个标记。  * "[SEP]"：表示序列分离。

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

`span`

    

(可选，整数)当"截断"为"无"时，您可以对较长的文本序列进行分区以进行推理。该值指示每个子序列之间重叠的标记数。

默认值为"-1"，表示不发生窗口或跨越。

当您的典型输入仅略大于"max_sequence_length"时，最好简单地截断;第二个子序列中的信息将很少。

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`xlm_roberta`

    

(可选，对象) [预览] 此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的支持 SLA 的约束。 XLMRoBERTa风格的标记化将使用随附的设置执行。

xlm_roberta的性质

`span`

    

(可选，整数)当"截断"为"无"时，您可以对较长的文本序列进行分区以进行推理。该值指示每个子序列之间重叠的标记数。

默认值为"-1"，表示不发生窗口或跨越。

当您的典型输入仅略大于"max_sequence_length"时，最好简单地截断;第二个子序列中的信息将很少。

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`bert_ja`

    

(可选，对象) [预览] 此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的支持 SLA 的约束。 日语文本的BERT样式标记化将使用随附的设置执行。

bert_ja的性质

`span`

    

(可选，整数)当"截断"为"无"时，您可以对较长的文本序列进行分区以进行推理。该值指示每个子序列之间重叠的标记数。

默认值为"-1"，表示不发生窗口或跨越。

当您的典型输入仅略大于"max_sequence_length"时，最好简单地截断;第二个子序列中的信息将很少。

`with_special_tokens`

     (Optional, boolean) Tokenize with special tokens if `true`. 

`zero_shot_classification`

    

(对象，可选)配置零镜头分类任务。零镜头分类允许在没有预先确定的标签的情况下进行文本分类。在推理时，可以调整标签进行分类。这使得这种类型的模型和任务异常灵活。

如果始终对相同的标签进行分类，则最好使用微调的文本分类模型。

zero_shot_classification推理的属性

`labels`

     (Optional, array) The labels to classify. Can be set at creation for default labels, and then updated during inference. 
`multi_label`

     (Optional, boolean) Indicates if more than one `true` label is possible given the input. This is useful when labeling text that could pertain to more than one of the input labels. Defaults to `false`. 
`results_field`

     (Optional, string) The field that is added to incoming documents to contain the inference prediction. Defaults to `predicted_value`. 
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

`xlm_roberta`

    

(可选，对象) [预览] 此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的支持 SLA 的约束。 XLMRoBERTa风格的标记化将使用随附的设置执行。

xlm_roberta的性质

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

`bert_ja`

    

(可选，对象) [预览] 此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的支持 SLA 的约束。 日语文本的BERT样式标记化将使用随附的设置执行。

bert_ja的性质

`truncate`

    

(可选，字符串)指示令牌在超过"max_sequence_length"时如何截断。默认值为"第一"。

* "无"：不发生截断;推理请求收到错误。  * "first"：仅截断第一个序列。  * "second"：只有第二个序列被截断。如果只有一个序列，则该序列将被截断。

对于"zero_shot_classification"，假设序列始终是第二个序列。因此，在这种情况下不要使用"second"。

###Examples

响应取决于模型的类型。

例如，对于语言识别，响应是预测的语言和分数：

    
    
    response = client.ml.infer_trained_model(
      model_id: 'lang_ident_model_1',
      body: {
        docs: [
          {
            text: 'The fool doth think he is wise, but the wise man knows himself to be a fool.'
          }
        ]
      }
    )
    puts response
    
    
    POST _ml/trained_models/lang_ident_model_1/_infer
    {
      "docs":[{"text": "The fool doth think he is wise, but the wise man knows himself to be a fool."}]
    }

以下是以高概率预测英语的结果。

    
    
    {
      "inference_results": [
        {
          "predicted_value": "en",
          "prediction_probability": 0.9999658805366392,
          "prediction_score": 0.9999658805366392
        }
      ]
    }

当它是文本分类模型时，响应是分数和预测分类。

例如：

    
    
    response = client.ml.infer_trained_model(
      model_id: 'model2',
      body: {
        docs: [
          {
            text_field: 'The movie was awesome!!'
          }
        ]
      }
    )
    puts response
    
    
    POST _ml/trained_models/model2/_infer
    {
    	"docs": [{"text_field": "The movie was awesome!!"}]
    }

API 返回预测的标签和置信度。

    
    
    {
      "inference_results": [{
        "predicted_value" : "POSITIVE",
        "prediction_probability" : 0.9998667964092964
      }]
    }

对于命名实体识别 (NER) 模型，响应包含批注文本输出和识别的实体。

    
    
    response = client.ml.infer_trained_model(
      model_id: 'model2',
      body: {
        docs: [
          {
            text_field: 'Hi my name is Josh and I live in Berlin'
          }
        ]
      }
    )
    puts response
    
    
    POST _ml/trained_models/model2/_infer
    {
    	"docs": [{"text_field": "Hi my name is Josh and I live in Berlin"}]
    }

在这种情况下，API 返回：

    
    
    {
      "inference_results": [{
        "predicted_value" : "Hi my name is [Josh](PER&Josh) and I live in [Berlin](LOC&Berlin)",
        "entities" : [
          {
            "entity" : "Josh",
            "class_name" : "PER",
            "class_probability" : 0.9977303419824,
            "start_pos" : 14,
            "end_pos" : 18
          },
          {
            "entity" : "Berlin",
            "class_name" : "LOC",
            "class_probability" : 0.9992474323902818,
            "start_pos" : 33,
            "end_pos" : 39
          }
        ]
      }]
    }

零样本分类模型需要额外的配置来定义类标签。这些标签在零镜头推理配置中传递。

    
    
    response = client.ml.infer_trained_model(
      model_id: 'model2',
      body: {
        docs: [
          {
            text_field: 'This is a very happy person'
          }
        ],
        inference_config: {
          zero_shot_classification: {
            labels: [
              'glad',
              'sad',
              'bad',
              'rad'
            ],
            multi_label: false
          }
        }
      }
    )
    puts response
    
    
    POST _ml/trained_models/model2/_infer
    {
      "docs": [
        {
          "text_field": "This is a very happy person"
        }
      ],
      "inference_config": {
        "zero_shot_classification": {
          "labels": [
            "glad",
            "sad",
            "bad",
            "rad"
          ],
          "multi_label": false
        }
      }
    }

API 返回预测的标签和置信度，以及顶级类：

    
    
    {
      "inference_results": [{
        "predicted_value" : "glad",
        "top_classes" : [
          {
            "class_name" : "glad",
            "class_probability" : 0.8061155063386439,
            "class_score" : 0.8061155063386439
          },
          {
            "class_name" : "rad",
            "class_probability" : 0.18218006158387956,
            "class_score" : 0.18218006158387956
          },
          {
            "class_name" : "bad",
            "class_probability" : 0.006325615787634201,
            "class_score" : 0.006325615787634201
          },
          {
            "class_name" : "sad",
            "class_probability" : 0.0053788162898424545,
            "class_score" : 0.0053788162898424545
          }
        ],
        "prediction_probability" : 0.8061155063386439
      }]
    }

问答模型需要额外的配置来定义要回答的问题。

    
    
    response = client.ml.infer_trained_model(
      model_id: 'model2',
      body: {
        docs: [
          {
            text_field: '<long text to extract answer>'
          }
        ],
        inference_config: {
          question_answering: {
            question: '<question to be answered>'
          }
        }
      }
    )
    puts response
    
    
    POST _ml/trained_models/model2/_infer
    {
      "docs": [
        {
          "text_field": "<long text to extract answer>"
        }
      ],
      "inference_config": {
        "question_answering": {
          "question": "<question to be answered>"
        }
      }
    }

API 返回类似于以下内容的响应：

    
    
    {
        "predicted_value": <string subsection of the text that is the answer>,
        "start_offset": <character offset in document to start>,
        "end_offset": <character offset end of the answer,
        "prediction_probability": <prediction score>
    }

文本相似性模型至少需要两个文本序列进行比较。可以提供多个文本字符串以与其他文本序列进行比较：

    
    
    POST _ml/trained_models/cross-encoder__ms-marco-tinybert-l-2-v2/_infer
    {
      "docs":[{ "text_field": "Berlin has a population of 3,520,031 registered inhabitants in an area of 891.82 square kilometers."}, {"text_field": "New York City is famous for the Metropolitan Museum of Art."}],
      "inference_config": {
        "text_similarity": {
          "text": "How many people live in Berlin?"
        }
      }
    }

响应包含与"text_similarity."text"字段中提供的文本进行比较的每个字符串的预测：

    
    
    {
      "inference_results": [
        {
          "predicted_value": 7.235751628875732
        },
        {
          "predicted_value": -11.562295913696289
        }
      ]
    }

调用 API 时，可以覆盖标记化截断选项：

    
    
    response = client.ml.infer_trained_model(
      model_id: 'model2',
      body: {
        docs: [
          {
            text_field: 'The Amazon rainforest covers most of the Amazon basin in South America'
          }
        ],
        inference_config: {
          ner: {
            tokenization: {
              bert: {
                truncate: 'first'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST _ml/trained_models/model2/_infer
    {
      "docs": [{"text_field": "The Amazon rainforest covers most of the Amazon basin in South America"}],
      "inference_config": {
        "ner": {
          "tokenization": {
            "bert": {
              "truncate": "first"
            }
          }
        }
      }
    }

当输入由于模型的"max_sequence_length"施加的限制而被截断时，响应中将显示"is_truncated"字段。

    
    
    {
      "inference_results": [{
        "predicted_value" : "The [Amazon](LOC&Amazon) rainforest covers most of the [Amazon](LOC&Amazon) basin in [South America](LOC&South+America)",
        "entities" : [
          {
            "entity" : "Amazon",
            "class_name" : "LOC",
            "class_probability" : 0.9505460915724254,
            "start_pos" : 4,
            "end_pos" : 10
          },
          {
            "entity" : "Amazon",
            "class_name" : "LOC",
            "class_probability" : 0.9969992804311777,
            "start_pos" : 41,
            "end_pos" : 47
          }
        ],
        "is_truncated" : true
      }]
    }

[« Get trained models statistics API](get-trained-models-stats.md) [Start
trained model deployment API »](start-trained-model-deployment.md)
