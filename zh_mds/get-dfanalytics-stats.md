

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning data frame analytics APIs](ml-df-
analytics-apis.md)

[« Get data frame analytics jobs API](get-dfanalytics.md) [Preview data
frame analytics API »](preview-dfanalytics.md)

## 获取数据帧分析作业统计API

检索数据框分析作业的使用情况信息。

###Request

"获取_ml/data_frame/分析/<data_frame_analytics_id>/_stats"

'GET_ml/data_frame/analytics/<data_frame_analytics_id>，<data_frame_analytics_id>/_stats'

"获取_ml/data_frame/分析/_stats"

"获取_ml/data_frame/分析/_all/_stats"

"获取_ml/data_frame/分析/*/_stats"

###Prerequisites

需要"monitor_ml"群集权限。此权限包含在"machine_learning_user"内置角色中。

### 路径参数

`<data_frame_analytics_id>`

     (Optional, string) Identifier for the data frame analytics job. If you do not specify this option, the API returns information for the first hundred data frame analytics jobs. 

### 查询参数

`allow_no_match`

    

(可选，布尔值)指定在请求时要执行的操作：

* 包含通配符表达式，并且没有匹配的数据框分析作业。  * 包含"_all"字符串或不包含标识符，并且没有匹配项。  * 包含通配符表达式，并且只有部分匹配。

默认值为"true"，当没有匹配项时返回空的"data_frame_analytics"数组，当存在部分匹配时返回结果子集。如果此参数为"false"，则当没有匹配项或只有部分匹配项时，请求将返回"404"状态代码。

`from`

     (Optional, integer) Skips the specified number of data frame analytics jobs. The default value is `0`. 
`size`

     (Optional, integer) Specifies the maximum number of data frame analytics jobs to obtain. The default value is `100`. 
`verbose`

     (Optional, Boolean) Defines whether the stats response should be verbose. The default value is `false`. 

### 响应正文

`data_frame_analytics`

    

(阵列)包含数据帧分析作业的使用信息的对象数组，这些作业按"id"值升序排序。

数据框分析作业使用资源的属性

`analysis_stats`

    

(对象)包含有关分析作业的信息的对象。

"analysis_stats"的属性

`classification_stats`

    

(对象)包含有关分类分析作业的信息的对象。

"classification_stats"的属性

`hyperparameters`

    

(对象)包含分类分析作业参数的对象。

"超参数"的属性

`alpha`

     (double) Advanced configuration option. Machine learning uses loss guided tree growing, which means that the decision trees grow where the regularized loss decreases most quickly. This parameter affects loss calculations by acting as a multiplier of the tree depth. Higher alpha values result in shallower trees and faster training times. By default, this value is calculated during hyperparameter optimization. It must be greater than or equal to zero. 
`class_assignment_objective`

     (string) Defines the objective to optimize when assigning class labels: `maximize_accuracy` or `maximize_minimum_recall`. When maximizing accuracy, class labels are chosen to maximize the number of correct predictions. When maximizing minimum recall, labels are chosen to maximize the minimum recall for any class. Defaults to `maximize_minimum_recall`. 
`downsample_factor`

     (double) Advanced configuration option. Controls the fraction of data that is used to compute the derivatives of the loss function for tree training. A small value results in the use of a small fraction of the data. If this value is set to be less than 1, accuracy typically improves. However, too small a value may result in poor convergence for the ensemble and so require more trees. For more information about shrinkage, refer to [this wiki article](https://en.wikipedia.org/wiki/Gradient_boosting#Stochastic_gradient_boosting). By default, this value is calculated during hyperparameter optimization. It must be greater than zero and less than or equal to 1. 
`eta`

     (double) Advanced configuration option. The shrinkage applied to the weights. Smaller values result in larger forests which have a better generalization error. However, larger forests cause slower training. For more information about shrinkage, refer to [this wiki article](https://en.wikipedia.org/wiki/Gradient_boosting#Shrinkage). By default, this value is calculated during hyperparameter optimization. It must be a value between 0.001 and 1. 
`eta_growth_rate_per_tree`

     (double) Advanced configuration option. Specifies the rate at which `eta` increases for each new tree that is added to the forest. For example, a rate of 1.05 increases `eta` by 5% for each extra tree. By default, this value is calculated during hyperparameter optimization. It must be between 0.5 and 2. 
`feature_bag_fraction`

     (double) Advanced configuration option. Defines the fraction of features that will be used when selecting a random bag for each candidate split. By default, this value is calculated during hyperparameter optimization. 
`gamma`

     (double) Advanced configuration option. Regularization parameter to prevent overfitting on the training data set. Multiplies a linear penalty associated with the size of individual trees in the forest. A high gamma value causes training to prefer small trees. A small gamma value results in larger individual trees and slower training. By default, this value is calculated during hyperparameter optimization. It must be a nonnegative value. 
`lambda`

     (double) Advanced configuration option. Regularization parameter to prevent overfitting on the training data set. Multiplies an L2 regularization term which applies to leaf weights of the individual trees in the forest. A high lambda value causes training to favor small leaf weights. This behavior makes the prediction function smoother at the expense of potentially not being able to capture relevant relationships between the features and the dependent variable. A small lambda value results in large individual trees and slower training. By default, this value is calculated during hyperparameter optimization. It must be a nonnegative value. 
`max_attempts_to_add_tree`

     (integer) If the algorithm fails to determine a non-trivial tree (more than a single leaf), this parameter determines how many of such consecutive failures are tolerated. Once the number of attempts exceeds the threshold, the forest training stops. 
`max_optimization_rounds_per_hyperparameter`

     (integer) Advanced configuration option. A multiplier responsible for determining the maximum number of hyperparameter optimization steps in the Bayesian optimization procedure. The maximum number of steps is determined based on the number of undefined hyperparameters times the maximum optimization rounds per hyperparameter. By default, this value is calculated during hyperparameter optimization. 
`max_trees`

     (integer) Advanced configuration option. Defines the maximum number of decision trees in the forest. The maximum value is 2000. By default, this value is calculated during hyperparameter optimization. 
`num_folds`

     (integer) The maximum number of folds for the cross-validation procedure. 
`num_splits_per_feature`

     (integer) Determines the maximum number of splits for every feature that can occur in a decision tree when the tree is trained. 
`soft_tree_depth_limit`

     (double) Advanced configuration option. Machine learning uses loss guided tree growing, which means that the decision trees grow where the regularized loss decreases most quickly. This soft limit combines with the `soft_tree_depth_tolerance` to penalize trees that exceed the specified depth; the regularized loss increases quickly beyond this depth. By default, this value is calculated during hyperparameter optimization. It must be greater than or equal to 0. 
`soft_tree_depth_tolerance`

     (double) Advanced configuration option. This option controls how quickly the regularized loss increases when the tree depth exceeds `soft_tree_depth_limit`. By default, this value is calculated during hyperparameter optimization. It must be greater than or equal to 0.01. 

`iteration`

     (integer) The number of iterations on the analysis. 
`timestamp`

     (date) The timestamp when the statistics were reported in milliseconds since the epoch. 

`timing_stats`

    

(对象)包含有关数据框分析作业的时间统计信息的对象。

"timing_stats"的属性

`elapsed_time`

     (integer) Runtime of the analysis in milliseconds. 
`iteration_time`

     (integer) Runtime of the latest iteration of the analysis in milliseconds. 

`validation_loss`

    

(对象)包含有关验证丢失的信息的对象。

"validation_loss"的属性

`fold_values`

     Validation loss values for every added decision tree during the forest growing procedure. 
`loss_type`

     (string) The type of the loss metric. For example, `binomial_logistic`. 

`outlier_detection_stats`

    

(对象)包含有关异常值检测作业的信息的对象。

"outlier_detection_stats"的属性

`parameters`

    

(对象)由用户指定或由算法启发式确定的作业参数列表。

"参数"的属性

`compute_feature_influence`

     (Boolean) Specifies whether the feature influence calculation is enabled. Defaults to `true`. 
`feature_influence_threshold`

     (double) The minimum outlier score that a document needs to have in order to calculate its feature influence score. Value range: 0-1 (`0.1` by default). 
`method`

     (string) The method that outlier detection uses. Available methods are `lof`, `ldof`, `distance_kth_nn`, `distance_knn`, and `ensemble`. The default value is `ensemble`, which means that outlier detection uses an ensemble of different methods and normalises and combines their individual outlier scores to obtain the overall outlier score. 
`n_neighbors`

     (integer) Defines the value for how many nearest neighbors each method of outlier detection uses to calculate its outlier score. When the value is not set, different values are used for different ensemble members. This default behavior helps improve the diversity in the ensemble; only override it if you are confident that the value you choose is appropriate for the data set. 
`outlier_fraction`

     (double) The proportion of the data set that is assumed to be outlying prior to outlier detection. For example, 0.05 means it is assumed that 5% of values are real outliers and 95% are inliers. 
`standardization_enabled`

     (Boolean) If `true`, the following operation is performed on the columns before computing outlier scores: (x_i - mean(x_i)) / sd(x_i). Defaults to `true`. For more information about this concept, see [Wikipedia](https://en.wikipedia.org/wiki/Feature_scaling#Standardization_\(Z-score_Normalization\)). 

`timestamp`

     (date) The timestamp when the statistics were reported in milliseconds since the epoch. 

`timing_stats`

    

(对象)包含有关数据框分析作业的时间统计信息的对象。

"timing_stats"的属性

`elapsed_time`

     (integer) Runtime of the analysis in milliseconds. 

`regression_stats`

    

(对象)包含有关回归分析作业的信息的对象。

"regression_stats"的属性

`hyperparameters`

    

(对象)包含回归分析作业参数的对象。

"超参数"的属性

`alpha`

     (double) Advanced configuration option. Machine learning uses loss guided tree growing, which means that the decision trees grow where the regularized loss decreases most quickly. This parameter affects loss calculations by acting as a multiplier of the tree depth. Higher alpha values result in shallower trees and faster training times. By default, this value is calculated during hyperparameter optimization. It must be greater than or equal to zero. 
`downsample_factor`

     (double) Advanced configuration option. Controls the fraction of data that is used to compute the derivatives of the loss function for tree training. A small value results in the use of a small fraction of the data. If this value is set to be less than 1, accuracy typically improves. However, too small a value may result in poor convergence for the ensemble and so require more trees. For more information about shrinkage, refer to [this wiki article](https://en.wikipedia.org/wiki/Gradient_boosting#Stochastic_gradient_boosting). By default, this value is calculated during hyperparameter optimization. It must be greater than zero and less than or equal to 1. 
`eta`

     (double) Advanced configuration option. The shrinkage applied to the weights. Smaller values result in larger forests which have a better generalization error. However, larger forests cause slower training. For more information about shrinkage, refer to [this wiki article](https://en.wikipedia.org/wiki/Gradient_boosting#Shrinkage). By default, this value is calculated during hyperparameter optimization. It must be a value between 0.001 and 1. 
`eta_growth_rate_per_tree`

     (double) Advanced configuration option. Specifies the rate at which `eta` increases for each new tree that is added to the forest. For example, a rate of 1.05 increases `eta` by 5% for each extra tree. By default, this value is calculated during hyperparameter optimization. It must be between 0.5 and 2. 
`feature_bag_fraction`

     (double) Advanced configuration option. Defines the fraction of features that will be used when selecting a random bag for each candidate split. By default, this value is calculated during hyperparameter optimization. 
`gamma`

     (double) Advanced configuration option. Regularization parameter to prevent overfitting on the training data set. Multiplies a linear penalty associated with the size of individual trees in the forest. A high gamma value causes training to prefer small trees. A small gamma value results in larger individual trees and slower training. By default, this value is calculated during hyperparameter optimization. It must be a nonnegative value. 
`lambda`

     (double) Advanced configuration option. Regularization parameter to prevent overfitting on the training data set. Multiplies an L2 regularization term which applies to leaf weights of the individual trees in the forest. A high lambda value causes training to favor small leaf weights. This behavior makes the prediction function smoother at the expense of potentially not being able to capture relevant relationships between the features and the dependent variable. A small lambda value results in large individual trees and slower training. By default, this value is calculated during hyperparameter optimization. It must be a nonnegative value. 
`max_attempts_to_add_tree`

     (integer) If the algorithm fails to determine a non-trivial tree (more than a single leaf), this parameter determines how many of such consecutive failures are tolerated. Once the number of attempts exceeds the threshold, the forest training stops. 
`max_optimization_rounds_per_hyperparameter`

     (integer) Advanced configuration option. A multiplier responsible for determining the maximum number of hyperparameter optimization steps in the Bayesian optimization procedure. The maximum number of steps is determined based on the number of undefined hyperparameters times the maximum optimization rounds per hyperparameter. By default, this value is calculated during hyperparameter optimization. 
`max_trees`

     (integer) Advanced configuration option. Defines the maximum number of decision trees in the forest. The maximum value is 2000. By default, this value is calculated during hyperparameter optimization. 
`num_folds`

     (integer) The maximum number of folds for the cross-validation procedure. 
`num_splits_per_feature`

     (integer) Determines the maximum number of splits for every feature that can occur in a decision tree when the tree is trained. 
`soft_tree_depth_limit`

     (double) Advanced configuration option. Machine learning uses loss guided tree growing, which means that the decision trees grow where the regularized loss decreases most quickly. This soft limit combines with the `soft_tree_depth_tolerance` to penalize trees that exceed the specified depth; the regularized loss increases quickly beyond this depth. By default, this value is calculated during hyperparameter optimization. It must be greater than or equal to 0. 
`soft_tree_depth_tolerance`

     (double) Advanced configuration option. This option controls how quickly the regularized loss increases when the tree depth exceeds `soft_tree_depth_limit`. By default, this value is calculated during hyperparameter optimization. It must be greater than or equal to 0.01. 

`iteration`

     (integer) The number of iterations on the analysis. 
`timestamp`

     (date) The timestamp when the statistics were reported in milliseconds since the epoch. 

`timing_stats`

    

(对象)包含有关数据框分析作业的时间统计信息的对象。

"timing_stats"的普罗珀蒂斯

`elapsed_time`

     (integer) Runtime of the analysis in milliseconds. 
`iteration_time`

     (integer) Runtime of the latest iteration of the analysis in milliseconds. 

`validation_loss`

    

(对象)包含有关验证丢失的信息的对象。

"validation_loss"的属性

`fold_values`

     (array of strings) Validation loss values for every added decision tree during the forest growing procedure. 
`loss_type`

     (string) The type of the loss metric. For example, `binomial_logistic`. 

`assignment_explanation`

     (string) For running jobs only, contains messages relating to the selection of a node to run the job. 

`data_counts`

    

(对象)一个对象，它提供跳过的文档数量、用于训练的文档数或可用于测试的文档数。

"data_counts"的属性

`skipped_docs_count`

     (integer) The number of documents that are skipped during the analysis because they contained values that are not supported by the analysis. For example, outlier detection does not support missing fields so it skips documents with missing fields. Likewise, all types of analysis skip documents that contain arrays with more than one element. 
`test_docs_count`

     (integer) The number of documents that are not used for training the model and can be used for testing. 
`training_docs_count`

     (integer) The number of documents that are used for training the model. 

`id`

     (string) The unique identifier of the data frame analytics job. 
`memory_usage`

    

(可选，对象)描述分析的内存使用情况的对象。它仅在启动作业并报告内存使用情况后存在。

"memory_usage"的属性

`memory_reestimate_bytes`

     (long) This value is present when the `status` is `hard_limit` and it is a new estimate of how much memory the job needs. 
`peak_usage_bytes`

     (long) The number of bytes used at the highest peak of memory usage. 
`status`

    

(字符串)内存使用状态。可能具有以下值之一：

* "确定"：使用量保持在限制以下。  * "hard_limit"：使用量超过配置的内存限制。

`timestamp`

     (date) The timestamp when memory usage was calculated. 

`node`

    

(对象)包含运行作业的节点的属性。此信息仅适用于正在运行的作业。

"节点"的属性

`attributes`

     (object) Lists node attributes such as `ml.machine_memory` or `ml.max_open_jobs` settings. 
`ephemeral_id`

     (string) The ephemeral ID of the node. 
`id`

     (string) The unique identifier of the node. 
`name`

     (string) The node name. 
`transport_address`

     (string) The host and port where transport HTTP connections are accepted. 

`progress`

    

(阵列)按阶段划分的数据框分析作业的进度报告。

相位对象的属性

`phase`

    

(字符串)定义数据框分析作业的阶段。可能的阶段：

* "重新索引"、* "loading_data"、"computing_outliers"(仅用于异常值检测)、* "feature_selection"(仅用于回归和分类)、* "coarse_parameter_search"(仅用于回归和分类)、* "fine_tuning_parameters"(仅用于回归和分类)、* "final_training"(仅用于回归和分类)、* "writing_results"、"* 推理"(仅用于回归和分类)。

要了解有关不同阶段的更多信息，请参阅数据框分析作业的工作原理。

`progress_percent`

     (integer) The progress that the data frame analytics job has made expressed in percentage. 

`state`

     (string) The status of the data frame analytics job, which can be one of the following values: `failed`, `started`, `starting`,`stopping`, `stopped`. 

### 响应码

"404"(缺少资源)

     If `allow_no_match` is `false`, this code indicates that there are no resources that match the request or only partial matches for the request. 

###Examples

以下 API 检索异常值检测数据帧分析作业示例的使用情况信息：

    
    
    response = client.ml.get_data_frame_analytics_stats(
      id: 'weblog-outliers'
    )
    puts response
    
    
    GET _ml/data_frame/analytics/weblog-outliers/_stats
    
    
    {
      "count" : 1,
      "data_frame_analytics" : [
        {
          "id" : "weblog-outliers",
          "state" : "stopped",
          "progress" : [
            {
              "phase" : "reindexing",
              "progress_percent" : 100
            },
            {
              "phase" : "loading_data",
              "progress_percent" : 100
            },
            {
              "phase" : "computing_outliers",
              "progress_percent" : 100
            },
            {
              "phase" : "writing_results",
              "progress_percent" : 100
            }
          ],
          "data_counts" : {
            "training_docs_count" : 1001,
            "test_docs_count" : 0,
            "skipped_docs_count" : 0
          },
          "memory_usage" : {
            "timestamp" : 1626264770206,
            "peak_usage_bytes" : 328011,
            "status" : "ok"
          },
          "analysis_stats" : {
            "outlier_detection_stats" : {
              "timestamp" : 1626264770206,
              "parameters" : {
                "n_neighbors" : 0,
                "method" : "ensemble",
                "compute_feature_influence" : true,
                "feature_influence_threshold" : 0.1,
                "outlier_fraction" : 0.05,
                "standardization_enabled" : true
              },
              "timing_stats" : {
                "elapsed_time" : 32
              }
            }
          }
        }
      ]
    }

[« Get data frame analytics jobs API](get-dfanalytics.md) [Preview data
frame analytics API »](preview-dfanalytics.md)
