

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning data frame analytics APIs](ml-df-
analytics-apis.md)

[« Machine learning data frame analytics APIs](ml-df-analytics-apis.md)
[Delete data frame analytics jobs API »](delete-dfanalytics.md)

## 创建数据帧分析作业API

实例化数据框分析作业。

###Request

"放置_ml/data_frame/分析/<data_frame_analytics_id>"

###Prerequisites

需要以下权限：

* 集群："manage_ml"("machine_learning_admin"内置角色授予此权限) * 源索引："读取"、"view_index_metadata" * 目标索引："读取"、"create_index"、"管理"和"索引"

数据框分析作业会记住创建数据框分析作业的用户在创建时具有哪些角色。启动作业时，它将使用相同的角色执行分析。如果提供辅助授权标头，则会改用这些凭据。

###Description

此 API 创建一个数据框分析作业，该作业对源索引执行分析并将结果存储在目标索引中。

如果目标索引不存在，则会在启动作业时自动创建该索引。请参阅启动数据框分析作业。

如果仅提供回归或分类参数的子集，则会发生超参数优化。它为每个未定义的参数确定一个值。

### 路径参数

`<data_frame_analytics_id>`

     (Required, string) Identifier for the data frame analytics job. This identifier can contain lowercase alphanumeric characters (a-z and 0-9), hyphens, and underscores. It must start and end with alphanumeric characters. 

### 请求正文

`allow_lazy_start`

     (Optional, Boolean) Specifies whether this job can start when there is insufficient machine learning node capacity for it to be immediately assigned to a node. The default is `false`; if a machine learning node with capacity to run the job cannot immediately be found, the API returns an error. However, this is also subject to the cluster-wide `xpack.ml.max_lazy_ml_nodes` setting. See [Advanced machine learning settings](ml-settings.html#advanced-ml-settings "Advanced machine learning settings"). If this option is set to `true`, the API does not return an error and the job waits in the `starting` state until sufficient machine learning node capacity is available. 

`analysis`

    

(必填，对象)分析配置，其中包含执行以下分析类型之一所需的信息：分类、异常值检测或回归。

"分析"的属性

`classification`

    

(必填*，对象)执行分类所需的配置信息。

高级参数用于微调分类分析。它们由超参数优化自动设置，以提供最小的验证错误。强烈建议使用默认值，除非您完全了解这些参数的功能。

"分类"的属性

`alpha`

     (Optional, double) Advanced configuration option. Machine learning uses loss guided tree growing, which means that the decision trees grow where the regularized loss decreases most quickly. This parameter affects loss calculations by acting as a multiplier of the tree depth. Higher alpha values result in shallower trees and faster training times. By default, this value is calculated during hyperparameter optimization. It must be greater than or equal to zero. 
`class_assignment_objective`

     (Optional, string) Defines the objective to optimize when assigning class labels: `maximize_accuracy` or `maximize_minimum_recall`. When maximizing accuracy, class labels are chosen to maximize the number of correct predictions. When maximizing minimum recall, labels are chosen to maximize the minimum recall for any class. Defaults to `maximize_minimum_recall`. 
`dependent_variable`

    

(必需，字符串)

定义要预测文档的哪个字段。此参数由字段名称提供，并且必须与索引中用于训练的字段之一匹配。如果文档中缺少此字段，则该文档将不会用于训练，但会为其生成具有已训练模型的预测。它也被称为连续目标变量。

字段的数据类型必须是数字("整数"、"短"、"长"、"字节")、分类("ip"或"关键字")或布尔值。此字段中的不同值不得超过 100 个。

`downsample_factor`

     (Optional, double) Advanced configuration option. Controls the fraction of data that is used to compute the derivatives of the loss function for tree training. A small value results in the use of a small fraction of the data. If this value is set to be less than 1, accuracy typically improves. However, too small a value may result in poor convergence for the ensemble and so require more trees. For more information about shrinkage, refer to [this wiki article](https://en.wikipedia.org/wiki/Gradient_boosting#Stochastic_gradient_boosting). By default, this value is calculated during hyperparameter optimization. It must be greater than zero and less than or equal to 1. 
`early_stopping_enabled`

     (Optional, Boolean) Advanced configuration option. Specifies whether the training process should finish if it is not finding any better performing models. If disabled, the training process can take significantly longer and the chance of finding a better performing model is unremarkable. By default, early stoppping is enabled. 
`eta`

     (Optional, double) Advanced configuration option. The shrinkage applied to the weights. Smaller values result in larger forests which have a better generalization error. However, larger forests cause slower training. For more information about shrinkage, refer to [this wiki article](https://en.wikipedia.org/wiki/Gradient_boosting#Shrinkage). By default, this value is calculated during hyperparameter optimization. It must be a value between 0.001 and 1. 
`eta_growth_rate_per_tree`

     (Optional, double) Advanced configuration option. Specifies the rate at which `eta` increases for each new tree that is added to the forest. For example, a rate of 1.05 increases `eta` by 5% for each extra tree. By default, this value is calculated during hyperparameter optimization. It must be between 0.5 and 2. 
`feature_bag_fraction`

     (Optional, double) Advanced configuration option. Defines the fraction of features that will be used when selecting a random bag for each candidate split. By default, this value is calculated during hyperparameter optimization. 
`feature_processors`

    

(可选，列表)高级配置选项。修改一个或多个包含字段的功能预处理器的集合。分析使用生成的一个或多个要素，而不是原始文档字段。但是，这些功能是短暂的;它们不存储在目标索引中。多个"feature_processors"条目可以引用相同的文档字段。对于自定义处理器未处理或具有分类值的字段，仍会发生自动分类特征编码。仅当要覆盖指定字段的自动要素编码时，才使用此属性。请参阅数据帧分析功能处理器以了解更多信息。

"feature_processors"的属性

`frequency_encoding`

    

(对象)执行频率编码所需的配置信息。

"frequency_encoding"的属性

`feature_name`

     (Required, string) The resulting feature name. 
`field`

     (Required, string) The name of the field to encode. 
`frequency_map`

     (Required, object) The resulting frequency map for the field value. If the field value is missing from the `frequency_map`, the resulting value is `0`. 

`multi_encoding`

    

(对象)执行多重编码所需的配置信息。它允许一起更改多个处理器。这样，处理器的输出就可以作为输入传递给另一个处理器。

"multi_encoding"的属性

`processors`

     (Required, array) The ordered array of custom processors to execute. Must be more than 1. 

`n_gram_encoding`

    

(对象)执行 n 元语法编码所需的配置信息。此编码器创建的要素具有以下名称格式："<feature_prefix>。<ngram><弦位置>"。例如，如果"feature_prefix"是"f"，则字符串中第二个 unigram 的特征名称是"f.11"。

"n_gram_encoding"的属性

`feature_prefix`

     (Optional, string) The feature name prefix. Defaults to `ngram_<start>_<length>`. 
`field`

     (Required, string) The name of the text field to encode. 
`length`

     (Optional, integer) Specifies the length of the n-gram substring. Defaults to `50`. Must be greater than `0`. 
`n_grams`

     (Required, array) Specifies which n-grams to gather. It’s an array of integer values where the minimum value is 1, and a maximum value is 5. 
`start`

     (Optional, integer) Specifies the zero-indexed start of the n-gram substring. Negative values are allowed for encoding n-grams of string suffixes. Defaults to `0`. 

`one_hot_encoding`

    

(对象)执行一次热编码所需的配置信息。

"one_hot_encoding"的属性

`field`

     (Required, string) The name of the field to encode. 
`hot_map`

     (Required, string) The one hot map mapping the field value with the column name. 

`target_mean_encoding`

    

(对象)执行目标均值编码所需的配置信息。

"target_mean_encoding"的属性

`default_value`

     (Required, integer) The default value if field value is not found in the `target_map`. 
`feature_name`

     (Required, string) The resulting feature name. 
`field`

     (Required, string) The name of the field to encode. 
`target_map`

     (Required, object) The field value to target mean transition map. 

`gamma`

     (Optional, double) Advanced configuration option. Regularization parameter to prevent overfitting on the training data set. Multiplies a linear penalty associated with the size of individual trees in the forest. A high gamma value causes training to prefer small trees. A small gamma value results in larger individual trees and slower training. By default, this value is calculated during hyperparameter optimization. It must be a nonnegative value. 
`lambda`

     (Optional, double) Advanced configuration option. Regularization parameter to prevent overfitting on the training data set. Multiplies an L2 regularization term which applies to leaf weights of the individual trees in the forest. A high lambda value causes training to favor small leaf weights. This behavior makes the prediction function smoother at the expense of potentially not being able to capture relevant relationships between the features and the dependent variable. A small lambda value results in large individual trees and slower training. By default, this value is calculated during hyperparameter optimization. It must be a nonnegative value. 
`max_optimization_rounds_per_hyperparameter`

     (Optional, integer) Advanced configuration option. A multiplier responsible for determining the maximum number of hyperparameter optimization steps in the Bayesian optimization procedure. The maximum number of steps is determined based on the number of undefined hyperparameters times the maximum optimization rounds per hyperparameter. By default, this value is calculated during hyperparameter optimization. 
`max_trees`

     (Optional, integer) Advanced configuration option. Defines the maximum number of decision trees in the forest. The maximum value is 2000. By default, this value is calculated during hyperparameter optimization. 
`num_top_classes`

    

(可选，整数)定义报告预测概率的类别数。它必须是非负数或 -1。如果它大于类别总数 -1 或大于，则报告所有类别的概率;如果有大量类别，则可能会对目标索引的大小产生重大影响。默认值为 2。

要使用 AUC ROC 评估方法，"num_top_classes"必须设置为"-1"或大于或等于类别总数的值。

`num_top_feature_importance_values`

     (Optional, integer) Advanced configuration option. Specifies the maximum number of [feature importance](/guide/en/machine-learning/8.9/ml-feature-importance.html) values per document to return. By default, it is zero and no feature importance calculation occurs. 
`prediction_field_name`

     (Optional, string) Defines the name of the prediction field in the results. Defaults to `<dependent_variable>_prediction`. 
`randomize_seed`

     (Optional, long) Defines the seed for the random generator that is used to pick training data. By default, it is randomly generated. Set it to a specific value to use the same training data each time you start a job (assuming other related parameters such as `source` and `analyzed_fields` are the same). 
`soft_tree_depth_limit`

     (Optional, double) Advanced configuration option. Machine learning uses loss guided tree growing, which means that the decision trees grow where the regularized loss decreases most quickly. This soft limit combines with the `soft_tree_depth_tolerance` to penalize trees that exceed the specified depth; the regularized loss increases quickly beyond this depth. By default, this value is calculated during hyperparameter optimization. It must be greater than or equal to 0. 
`soft_tree_depth_tolerance`

     (Optional, double) Advanced configuration option. This option controls how quickly the regularized loss increases when the tree depth exceeds `soft_tree_depth_limit`. By default, this value is calculated during hyperparameter optimization. It must be greater than or equal to 0.01. 
`training_percent`

     (Optional, integer) Defines what percentage of the eligible documents that will be used for training. Documents that are ignored by the analysis (for example those that contain arrays with more than one value) won’t be included in the calculation for used percentage. Defaults to `100`. 

`outlier_detection`

    

(必填*，对象)执行异常值检测所需的配置信息：

"outlier_detection"的属性

`compute_feature_influence`

     (Optional, Boolean) Specifies whether the feature influence calculation is enabled. Defaults to `true`. 
`feature_influence_threshold`

     (Optional, double) The minimum outlier score that a document needs to have in order to calculate its feature influence score. Value range: 0-1 (`0.1` by default). 
`method`

     (Optional, string) The method that outlier detection uses. Available methods are `lof`, `ldof`, `distance_kth_nn`, `distance_knn`, and `ensemble`. The default value is `ensemble`, which means that outlier detection uses an ensemble of different methods and normalises and combines their individual outlier scores to obtain the overall outlier score. 
`n_neighbors`

     (Optional, integer) Defines the value for how many nearest neighbors each method of outlier detection uses to calculate its outlier score. When the value is not set, different values are used for different ensemble members. This default behavior helps improve the diversity in the ensemble; only override it if you are confident that the value you choose is appropriate for the data set. 
`outlier_fraction`

     (Optional, double) The proportion of the data set that is assumed to be outlying prior to outlier detection. For example, 0.05 means it is assumed that 5% of values are real outliers and 95% are inliers. 
`standardization_enabled`

     (Optional, Boolean) If `true`, the following operation is performed on the columns before computing outlier scores: (x_i - mean(x_i)) / sd(x_i). Defaults to `true`. For more information about this concept, see [Wikipedia](https://en.wikipedia.org/wiki/Feature_scaling#Standardization_\(Z-score_Normalization\)). 

`regression`

    

(必填*，对象)执行回归所需的配置信息。

高级参数用于微调回归分析。它们由超参数优化自动设置，以提供最小的验证错误。强烈建议使用默认值，除非您完全了解这些参数的功能。

"回归"的属性

`alpha`

     (Optional, double) Advanced configuration option. Machine learning uses loss guided tree growing, which means that the decision trees grow where the regularized loss decreases most quickly. This parameter affects loss calculations by acting as a multiplier of the tree depth. Higher alpha values result in shallower trees and faster training times. By default, this value is calculated during hyperparameter optimization. It must be greater than or equal to zero. 
`dependent_variable`

    

(必需，字符串)

定义要预测文档的哪个字段。此参数由字段名称提供，并且必须与索引中用于训练的字段之一匹配。如果文档中缺少此字段，则该文档将不会用于训练，但会为其生成具有已训练模型的预测。它也被称为连续目标变量。

字段的数据类型必须是数字。

`downsample_factor`

     (Optional, double) Advanced configuration option. Controls the fraction of data that is used to compute the derivatives of the loss function for tree training. A small value results in the use of a small fraction of the data. If this value is set to be less than 1, accuracy typically improves. However, too small a value may result in poor convergence for the ensemble and so require more trees. For more information about shrinkage, refer to [this wiki article](https://en.wikipedia.org/wiki/Gradient_boosting#Stochastic_gradient_boosting). By default, this value is calculated during hyperparameter optimization. It must be greater than zero and less than or equal to 1. 
`early_stopping_enabled`

     (Optional, Boolean) Advanced configuration option. Specifies whether the training process should finish if it is not finding any better performing models. If disabled, the training process can take significantly longer and the chance of finding a better performing model is unremarkable. By default, early stoppping is enabled. 
`eta`

     (Optional, double) Advanced configuration option. The shrinkage applied to the weights. Smaller values result in larger forests which have a better generalization error. However, larger forests cause slower training. For more information about shrinkage, refer to [this wiki article](https://en.wikipedia.org/wiki/Gradient_boosting#Shrinkage). By default, this value is calculated during hyperparameter optimization. It must be a value between 0.001 and 1. 
`eta_growth_rate_per_tree`

     (Optional, double) Advanced configuration option. Specifies the rate at which `eta` increases for each new tree that is added to the forest. For example, a rate of 1.05 increases `eta` by 5% for each extra tree. By default, this value is calculated during hyperparameter optimization. It must be between 0.5 and 2. 
`feature_bag_fraction`

     (Optional, double) Advanced configuration option. Defines the fraction of features that will be used when selecting a random bag for each candidate split. By default, this value is calculated during hyperparameter optimization. 
`feature_processors`

     (Optional, list) Advanced configuration option. A collection of feature preprocessors that modify one or more included fields. The analysis uses the resulting one or more features instead of the original document field. However, these features are ephemeral; they are not stored in the destination index. Multiple `feature_processors` entries can refer to the same document fields. Automatic categorical [feature encoding](/guide/en/machine-learning/8.9/ml-feature-encoding.html) still occurs for the fields that are unprocessed by a custom processor or that have categorical values. Use this property only if you want to override the automatic feature encoding of the specified fields. Refer to [data frame analytics feature processors](/guide/en/machine-learning/8.9/ml-feature-processors.html) to learn more. 
`gamma`

     (Optional, double) Advanced configuration option. Regularization parameter to prevent overfitting on the training data set. Multiplies a linear penalty associated with the size of individual trees in the forest. A high gamma value causes training to prefer small trees. A small gamma value results in larger individual trees and slower training. By default, this value is calculated during hyperparameter optimization. It must be a nonnegative value. 
`lambda`

     (Optional, double) Advanced configuration option. Regularization parameter to prevent overfitting on the training data set. Multiplies an L2 regularization term which applies to leaf weights of the individual trees in the forest. A high lambda value causes training to favor small leaf weights. This behavior makes the prediction function smoother at the expense of potentially not being able to capture relevant relationships between the features and the dependent variable. A small lambda value results in large individual trees and slower training. By default, this value is calculated during hyperparameter optimization. It must be a nonnegative value. 
`loss_function`

     (Optional, string) The loss function used during regression. Available options are `mse` (mean squared error), `msle` (mean squared logarithmic error), `huber` (Pseudo-Huber loss). Defaults to `mse`. Refer to [Loss functions for regression analyses](/guide/en/machine-learning/8.9/dfa-regression-lossfunction.html) to learn more. 
`loss_function_parameter`

     (Optional, double) A positive number that is used as a parameter to the `loss_function`. 
`max_optimization_rounds_per_hyperparameter`

     (Optional, integer) Advanced configuration option. A multiplier responsible for determining the maximum number of hyperparameter optimization steps in the Bayesian optimization procedure. The maximum number of steps is determined based on the number of undefined hyperparameters times the maximum optimization rounds per hyperparameter. By default, this value is calculated during hyperparameter optimization. 
`max_trees`

     (Optional, integer) Advanced configuration option. Defines the maximum number of decision trees in the forest. The maximum value is 2000. By default, this value is calculated during hyperparameter optimization. 
`num_top_feature_importance_values`

     (Optional, integer) Advanced configuration option. Specifies the maximum number of [feature importance](/guide/en/machine-learning/8.9/ml-feature-importance.html) values per document to return. By default, it is zero and no feature importance calculation occurs. 
`prediction_field_name`

     (Optional, string) Defines the name of the prediction field in the results. Defaults to `<dependent_variable>_prediction`. 
`randomize_seed`

     (Optional, long) Defines the seed for the random generator that is used to pick training data. By default, it is randomly generated. Set it to a specific value to use the same training data each time you start a job (assuming other related parameters such as `source` and `analyzed_fields` are the same). 
`soft_tree_depth_limit`

     (Optional, double) Advanced configuration option. Machine learning uses loss guided tree growing, which means that the decision trees grow where the regularized loss decreases most quickly. This soft limit combines with the `soft_tree_depth_tolerance` to penalize trees that exceed the specified depth; the regularized loss increases quickly beyond this depth. By default, this value is calculated during hyperparameter optimization. It must be greater than or equal to 0. 
`soft_tree_depth_tolerance`

     (Optional, double) Advanced configuration option. This option controls how quickly the regularized loss increases when the tree depth exceeds `soft_tree_depth_limit`. By default, this value is calculated during hyperparameter optimization. It must be greater than or equal to 0.01. 
`training_percent`

     (Optional, integer) Defines what percentage of the eligible documents that will be used for training. Documents that are ignored by the analysis (for example those that contain arrays with more than one value) won’t be included in the calculation for used percentage. Defaults to `100`. 

`analyzed_fields`

    

(可选，对象)指定"包含"和/或"排除"模式以选择将包含在分析中的字段。"排除"中指定的模式最后应用，因此"排除"优先。换句话说，如果在"包含"和"排除"中指定了相同的字段，则该字段将不会包含在分析中。

每种分析类型支持的字段如下所示：

* 异常值检测需要数值或布尔数据进行分析。这些算法不支持缺失值，因此将忽略数据类型不是数值或布尔值的字段。包含的字段包含缺失值、空值或数组的文档也会被忽略。因此，"目标"索引可能包含没有异常值分数的文档。  * 回归支持数字、"布尔值"、"文本"、"关键字"和"ip"字段。它还容忍缺失值。支持的字段包含在分析中，其他字段将被忽略。包含的字段包含具有两个或更多值的数组的文档也会被忽略。"目标"索引中不包含结果字段的文档不包括在回归分析中。  * 分类支持数字、"布尔"、"文本"、"关键字"和"ip"字段。它还容忍缺失值。支持的字段包含在分析中，其他字段将被忽略。包含的字段包含具有两个或更多值的数组的文档也会被忽略。"目标"索引中不包含结果字段的文档不包括在分类分析中。通过将序号变量值映射到单个数字，可以改进分类分析。例如，对于年龄范围，您可以将值建模为"0-14"= 0、"15-24"= 1、"25-34"= 2，依此类推。

如果未设置"analyzed_fields"，则仅包含相关字段。例如，用于异常值检测的所有数值字段。有关字段选择的详细信息，请参阅数据框分析说明。

"analyzed_fields"的属性

`excludes`

     (Optional, array) An array of strings that defines the fields that will be excluded from the analysis. You do not need to add fields with unsupported data types to `excludes`, these fields are excluded from the analysis automatically. 
`includes`

     (Optional, array) An array of strings that defines the fields that will be included in the analysis. 

`description`

     (Optional, string) A description of the job. 
`dest`

    

(必填，对象)目标配置，由"索引"和可选的"results_field"(默认为"ml")组成。

"目标"的属性

`index`

     (Required, string) Defines the _destination index_ to store the results of the data frame analytics job. 
`results_field`

     (Optional, string) Defines the name of the field in which to store the results of the analysis. Defaults to `ml`. 

`max_num_threads`

     (Optional, integer) The maximum number of threads to be used by the analysis. The default value is `1`. Using more threads may decrease the time necessary to complete the analysis at the cost of using more CPU. Note that the process may use additional threads for operational functionality other than the analysis itself. 
`_meta`

     (Optional, object) Advanced configuration option. Contains custom metadata about the job. For example, it can contain custom URL information. 
`model_memory_limit`

     (Optional, string) The approximate maximum amount of memory resources that are permitted for analytical processing. The default value for data frame analytics jobs is `1gb`. If you specify a value for the `xpack.ml.max_model_memory_limit` setting, an error occurs when you try to create jobs that have `model_memory_limit` values greater than that setting value. For more information, see [Machine learning settings](ml-settings.html "Machine learning settings in Elasticsearch"). 
`source`

    

(对象)如何获取分析数据的配置。它需要一个"索引"。(可选)可以指定"查询"、"runtime_mappings"和"_source"。

"源"的属性

`index`

    

(必需，字符串或数组)要对其执行分析的一个或多个索引。它可以是单个索引或索引模式，也可以是索引或模式数组。

如果源索引包含具有相同 ID 的文档，则只有最后编制索引的文档才会显示在目标索引中。

`query`

     (Optional, object) The Elasticsearch query domain-specific language ([DSL](query-dsl.html "Query DSL")). This value corresponds to the query object in an Elasticsearch search POST body. All the options that are supported by Elasticsearch can be used, as this object is passed verbatim to Elasticsearch. By default, this property has the following value: `{"match_all": {}}`. 
`runtime_mappings`

     (Optional, object) Definitions of runtime fields that will become part of the mapping of the destination index. 
`_source`

    

(可选，对象)指定"包含"和/或"排除"模式以选择目标中将存在的字段。排除的字段不能包含在分析中。

"_source"的属性

`includes`

     (array) An array of strings that defines the fields that will be included in the destination. 
`excludes`

     (array) An array of strings that defines the fields that will be excluded from the destination. 

###Examples

#### 预处理操作示例

以下示例演示如何将分析范围限制为某些字段，在目标索引中指定排除的字段，以及如何在分析之前使用查询筛选数据。

    
    
    PUT _ml/data_frame/analytics/model-flight-delays-pre
    {
      "source": {
        "index": [
          "kibana_sample_data_flights" __],
        "query": { __"range": {
            "DistanceKilometers": {
              "gt": 0
            }
          }
        },
        "_source": { __"includes": [],
          "excludes": [
            "FlightDelay",
            "FlightDelayType"
          ]
        }
      },
      "dest": { __"index": "df-flight-delays",
        "results_field": "ml-results"
      },
      "analysis": {
      "regression": {
        "dependent_variable": "FlightDelayMin",
        "training_percent": 90
        }
      },
      "analyzed_fields": { __"includes": [],
        "excludes": [
          "FlightNum"
        ]
      },
      "model_memory_limit": "100mb"
    }

__

|

要分析的源索引。   ---|---    __

|

此查询筛选出目标索引中不存在的整个文档。   __

|

"_source"对象定义数据集中将包含或排除在目标索引中的字段。   __

|

定义目标索引，该索引包含分析结果和"_source"对象中指定的源索引的字段。还定义了"results_field"的名称。   __

|

指定要包含在分析中或从分析中排除的字段。这不会影响字段是否存在于目标索引中，而只会影响它们是否在分析中使用。   在这个例子中，我们可以看到源索引的所有字段都包含在目标索引中，除了"FlightDelay"和"FlightDelayType"，因为这些字段被"_source"对象的"excludes"参数定义为排除字段。"FlightNum"字段包含在目的地索引中，但它不包括在分析中，因为它被"analyzed_fields"对象的"excludes"参数显式指定为排除字段。

#### 异常值检测示例

以下示例创建"loganalytics"数据帧分析作业，分析类型为"outlier_detection"：

    
    
    PUT _ml/data_frame/analytics/loganalytics
    {
      "description": "Outlier detection on log data",
      "source": {
        "index": "logdata"
      },
      "dest": {
        "index": "logdata_out"
      },
      "analysis": {
        "outlier_detection": {
          "compute_feature_influence": true,
          "outlier_fraction": 0.05,
          "standardization_enabled": true
        }
      }
    }

API 返回以下结果：

    
    
    {
      "id" : "loganalytics",
      "create_time" : 1656364565517,
      "version" : "8.4.0",
      "authorization" : {
        "roles" : [
          "superuser"
        ]
      },
      "description" : "Outlier detection on log data",
      "source" : {
        "index" : [
          "logdata"
        ],
        "query" : {
          "match_all" : { }
        }
      },
      "dest" : {
        "index" : "logdata_out",
        "results_field" : "ml"
      },
      "analysis" : {
        "outlier_detection" : {
          "compute_feature_influence" : true,
          "outlier_fraction" : 0.05,
          "standardization_enabled" : true
        }
      },
      "model_memory_limit" : "1gb",
      "allow_lazy_start" : false,
      "max_num_threads" : 1
    }

#### 回归示例

以下示例创建"house_price_regression_analysis"数据帧分析作业，分析类型为"回归"：

    
    
    PUT _ml/data_frame/analytics/house_price_regression_analysis
    {
      "source": {
        "index": "houses_sold_last_10_yrs"
      },
      "dest": {
        "index": "house_price_predictions"
      },
      "analysis":
        {
          "regression": {
            "dependent_variable": "price"
          }
        }
    }

API 返回以下结果：

    
    
    {
      "id" : "house_price_regression_analysis",
      "create_time" : 1656364845151,
      "version" : "8.4.0",
      "authorization" : {
        "roles" : [
          "superuser"
        ]
      },
      "source" : {
        "index" : [
          "houses_sold_last_10_yrs"
        ],
        "query" : {
          "match_all" : { }
        }
      },
      "dest" : {
        "index" : "house_price_predictions",
        "results_field" : "ml"
      },
      "analysis" : {
        "regression" : {
          "dependent_variable" : "price",
          "prediction_field_name" : "price_prediction",
          "training_percent" : 100.0,
          "randomize_seed" : -3578554885299300212,
          "loss_function" : "mse",
          "early_stopping_enabled" : true
        }
      },
      "model_memory_limit" : "1gb",
      "allow_lazy_start" : false,
      "max_num_threads" : 1
    }

以下示例创建一个作业并指定训练百分比：

    
    
    PUT _ml/data_frame/analytics/student_performance_mathematics_0.3
    {
     "source": {
       "index": "student_performance_mathematics"
     },
     "dest": {
       "index":"student_performance_mathematics_reg"
     },
     "analysis":
       {
         "regression": {
           "dependent_variable": "G3",
           "training_percent": 70,  __"randomize_seed": 19673948271 __}
       }
    }

__

|

用于训练模型的数据集的百分比。   ---|---    __

|

用于随机选择用于训练的数据的种子。   以下示例使用自定义特征处理器，使用单热、目标均值和频率编码技术将"DestWeather"的分类值转换为数值：

    
    
    PUT _ml/data_frame/analytics/flight_prices
    {
      "source": {
        "index": [
          "kibana_sample_data_flights"
        ]
      },
      "dest": {
        "index": "kibana_sample_flight_prices"
      },
      "analysis": {
        "regression": {
          "dependent_variable": "AvgTicketPrice",
          "num_top_feature_importance_values": 2,
          "feature_processors": [
            {
              "frequency_encoding": {
                "field": "DestWeather",
                "feature_name": "DestWeather_frequency",
                "frequency_map": {
                  "Rain": 0.14604811155570188,
                  "Heavy Fog": 0.14604811155570188,
                  "Thunder & Lightning": 0.14604811155570188,
                  "Cloudy": 0.14604811155570188,
                  "Damaging Wind": 0.14604811155570188,
                  "Hail": 0.14604811155570188,
                  "Sunny": 0.14604811155570188,
                  "Clear": 0.14604811155570188
                }
              }
            },
            {
              "target_mean_encoding": {
                "field": "DestWeather",
                "feature_name": "DestWeather_targetmean",
                "target_map": {
                  "Rain": 626.5588814585794,
                  "Heavy Fog": 626.5588814585794,
                  "Thunder & Lightning": 626.5588814585794,
                  "Hail": 626.5588814585794,
                  "Damaging Wind": 626.5588814585794,
                  "Cloudy": 626.5588814585794,
                  "Clear": 626.5588814585794,
                  "Sunny": 626.5588814585794
                },
                "default_value": 624.0249512020454
              }
            },
            {
              "one_hot_encoding": {
                "field": "DestWeather",
                "hot_map": {
                  "Rain": "DestWeather_Rain",
                  "Heavy Fog": "DestWeather_Heavy Fog",
                  "Thunder & Lightning": "DestWeather_Thunder & Lightning",
                  "Cloudy": "DestWeather_Cloudy",
                  "Damaging Wind": "DestWeather_Damaging Wind",
                  "Hail": "DestWeather_Hail",
                  "Clear": "DestWeather_Clear",
                  "Sunny": "DestWeather_Sunny"
                }
              }
            }
          ]
        }
      },
      "analyzed_fields": {
        "includes": [
          "AvgTicketPrice",
          "Cancelled",
          "DestWeather",
          "FlightDelayMin",
          "DistanceMiles"
        ]
      },
      "model_memory_limit": "30mb"
    }

这些自定义功能处理器是可选的;对于所有分类要素，自动特征编码仍然发生。

#### 分类示例

以下示例创建"loan_classification"数据框分析作业，分析类型为"分类"：

    
    
    PUT _ml/data_frame/analytics/loan_classification
    {
      "source" : {
        "index": "loan-applicants"
      },
      "dest" : {
        "index": "loan-applicants-classified"
      },
      "analysis" : {
        "classification": {
          "dependent_variable": "label",
          "training_percent": 75,
          "num_top_classes": 2
        }
      }
    }

[« Machine learning data frame analytics APIs](ml-df-analytics-apis.md)
[Delete data frame analytics jobs API »](delete-dfanalytics.md)
