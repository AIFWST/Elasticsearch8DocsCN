

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning data frame analytics APIs](ml-df-
analytics-apis.md)

[« Delete data frame analytics jobs API](delete-dfanalytics.md) [Explain
data frame analytics API »](explain-dfanalytics.md)

## 评估数据帧分析API

评估带批注索引的数据框分析。

###Request

"发布 _ml/data_frame/_evaluate"

###Prerequisites

需要以下权限：

* 集群："monitor_ml"("machine_learning_user"内置角色授予此权限) * 目标索引："读取"

###Description

API 将各种类型的机器学习功能的常用评估指标打包在一起。这设计用于由数据帧分析创建的索引。评估需要同时存在真实地面字段和分析结果字段。

### 请求正文

`evaluation`

    

(必填，对象)定义要执行的评估类型。请参阅数据帧分析评估资源。

可用的评估类型：

* "outlier_detection" * "回归" * "分类"

`index`

     (Required, object) Defines the `index` in which the evaluation will be performed. 
`query`

     (Optional, object) A query clause that retrieves a subset of data from the source index. See [Query DSL](query-dsl.html "Query DSL"). 

### 数据帧分析评估资源

#### 异常值检测评估对象

异常值检测评估异常值检测分析的结果，该分析输出每个文档为异常值的概率。

`actual_field`

     (Required, string) The field of the `index` which contains the `ground truth`. The data type of this field can be boolean or integer. If the data type is integer, the value has to be either `0` (false) or `1` (true). 
`predicted_probability_field`

     (Required, string) The field of the `index` that defines the probability of whether the item belongs to the class in question or not. It's the field that contains the results of the analysis. 
`metrics`

    

(可选，对象)指定用于评估的指标。如果未指定指标，则默认返回以下内容：

* 'auc_roc' ('include_curve'： false)， * 'precision' ('at'： [0.25， 0.5， 0.75])， * 'recall' ('at'： [0.25， 0.5， 0.75])， * 'confusion_matrix' ('at'： [0.25， 0.5， 0.75])。

`auc_roc`

     (Optional, object) The AUC ROC (area under the curve of the receiver operating characteristic) score and optionally the curve. Default value is {"include_curve": false}. 
`confusion_matrix`

     (Optional, object) Set the different thresholds of the outlier score at where the metrics (`tp` \- true positive, `fp` \- false positive, `tn` \- true negative, `fn` \- false negative) are calculated. Default value is {"at": [0.25, 0.50, 0.75]}. 
`precision`

     (Optional, object) Set the different thresholds of the outlier score at where the metric is calculated. Default value is {"at": [0.25, 0.50, 0.75]}. 
`recall`

     (Optional, object) Set the different thresholds of the outlier score at where the metric is calculated. Default value is {"at": [0.25, 0.50, 0.75]}. 

#### 回归评估对象

回归评估评估输出值预测的回归分析的结果。

`actual_field`

     (Required, string) The field of the `index` which contains the `ground truth`. The data type of this field must be numerical. 
`predicted_field`

     (Required, string) The field in the `index` that contains the predicted value, in other words the results of the regression analysis. 
`metrics`

    

(可选，对象)指定用于评估的指标。有关"mse"、"msle"和"huber"的更多信息，请参阅 Jupyter 笔记本关于回归损失函数。如果未指定指标，则默认返回以下内容：

* 'MSE'， * 'r_squared'， * 'huber' ('delta'： 1.0).

`mse`

     (Optional, object) Average squared difference between the predicted values and the actual (`ground truth`) value. For more information, read [this wiki article](https://en.wikipedia.org/wiki/Mean_squared_error). 
`msle`

    

(可选，对象)预测值的对数与实际("基本事实")值的对数之间的平均平方差。

`offset`

     (Optional, double) Defines the transition point at which you switch from minimizing quadratic error to minimizing quadratic log error. Defaults to `1`. 

`huber`

    

(可选，对象)伪胡贝尔损失函数。有关更多信息，请阅读此维基文章。

`delta`

     (Optional, double) Approximates 1/2 (prediction - actual)2 for values much less than delta and approximates a straight line with slope delta for values much larger than delta. Defaults to `1`. Delta needs to be greater than `0`. 

`r_squared`

     (Optional, object) Proportion of the variance in the dependent variable that is predictable from the independent variables. For more information, read [this wiki article](https://en.wikipedia.org/wiki/Coefficient_of_determination). 

### 分类评估对象

分类评估评估分类分析的结果，它输出一个预测，用于标识每个文档属于哪个类。

`actual_field`

     (Required, string) The field of the `index` which contains the `ground truth`. The data type of this field must be categorical. 
`predicted_field`

     (Optional, string) The field in the `index` which contains the predicted value, in other words the results of the classification analysis. 
`top_classes_field`

     (Optional, string) The field of the `index` which is an array of documents of the form `{ "class_name": XXX, "class_probability": YYY }`. This field must be defined as `nested` in the mappings. 
`metrics`

    

(可选，对象)指定用于评估的指标。如果没有特定的指标，则默认返回以下内容：

* "准确性"， * "multiclass_confusion_matrix"， * "精度"， * "召回"。

`accuracy`

     (Optional, object) Accuracy of predictions (per-class and overall). 
`auc_roc`

    

(可选，对象)AUC ROC(受试者工作特性曲线下的面积)评分和可选的曲线。它是针对被视为阳性的非特定类别(以"class_name"提供)计算的。

`class_name`

     (Required, string) Name of the only class that is treated as positive during AUC ROC calculation. Other classes are treated as negative ("one-vs-all" strategy). All the evaluated documents must have `class_name` in the list of their top classes. 
`include_curve`

     (Optional, Boolean) Whether or not the curve should be returned in addition to the score. Default value is false. 

`multiclass_confusion_matrix`

    

(可选，对象)多类混淆矩阵。

`size`

     (Optional, double) Specifies the size of the multiclass confusion matrix. Defaults to `10` which results in a matrix of size 10x10. 

`precision`

     (Optional, object) Precision of predictions (per-class and average). 
`recall`

     (Optional, object) Recall of predictions (per-class and average). 

###Examples

#### 异常值检测

    
    
    response = client.ml.evaluate_data_frame(
      body: {
        index: 'my_analytics_dest_index',
        evaluation: {
          outlier_detection: {
            actual_field: 'is_outlier',
            predicted_probability_field: 'ml.outlier_score'
          }
        }
      }
    )
    puts response
    
    
    POST _ml/data_frame/_evaluate
    {
      "index": "my_analytics_dest_index",
      "evaluation": {
        "outlier_detection": {
          "actual_field": "is_outlier",
          "predicted_probability_field": "ml.outlier_score"
        }
      }
    }

API 返回以下结果：

    
    
    {
      "outlier_detection": {
        "auc_roc": {
          "value": 0.92584757746414444
        },
        "confusion_matrix": {
          "0.25": {
              "tp": 5,
              "fp": 9,
              "tn": 204,
              "fn": 5
          },
          "0.5": {
              "tp": 1,
              "fp": 5,
              "tn": 208,
              "fn": 9
          },
          "0.75": {
              "tp": 0,
              "fp": 4,
              "tn": 209,
              "fn": 10
          }
        },
        "precision": {
            "0.25": 0.35714285714285715,
            "0.5": 0.16666666666666666,
            "0.75": 0
        },
        "recall": {
            "0.25": 0.5,
            "0.5": 0.1,
            "0.75": 0
        }
      }
    }

####Regression

    
    
    response = client.ml.evaluate_data_frame(
      body: {
        index: 'house_price_predictions',
        query: {
          bool: {
            filter: [
              {
                term: {
                  "ml.is_training": false
                }
              }
            ]
          }
        },
        evaluation: {
          regression: {
            actual_field: 'price',
            predicted_field: 'ml.price_prediction',
            metrics: {
              r_squared: {},
              mse: {},
              msle: {
                offset: 10
              },
              huber: {
                delta: 1.5
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST _ml/data_frame/_evaluate
    {
      "index": "house_price_predictions", __"query": {
          "bool": {
            "filter": [
              { "term":  { "ml.is_training": false } } __]
          }
      },
      "evaluation": {
        "regression": {
          "actual_field": "price", __"predicted_field": "ml.price_prediction", __"metrics": {
            "r_squared": {},
            "mse": {},
            "msle": {"offset": 10},
            "huber": {"delta": 1.5}
          }
        }
      }
    }

__

|

数据框分析回归分析的输出目标索引。   ---|---    __

|

在此示例中，为回归分析定义了测试/训练拆分 ("training_percent")。此查询将评估限制为仅对测试拆分执行。   __

|

实际房价的地面真实值。这是评估结果所必需的。   __

|

通过回归分析计算的房价预测值。   以下示例计算训练误差：

    
    
    response = client.ml.evaluate_data_frame(
      body: {
        index: 'student_performance_mathematics_reg',
        query: {
          term: {
            "ml.is_training": {
              value: true
            }
          }
        },
        evaluation: {
          regression: {
            actual_field: 'G3',
            predicted_field: 'ml.G3_prediction',
            metrics: {
              r_squared: {},
              mse: {},
              msle: {},
              huber: {}
            }
          }
        }
      }
    )
    puts response
    
    
    POST _ml/data_frame/_evaluate
    {
      "index": "student_performance_mathematics_reg",
      "query": {
        "term": {
          "ml.is_training": {
            "value": true __}
        }
      },
      "evaluation": {
        "regression": {
          "actual_field": "G3", __"predicted_field": "ml.G3_prediction", __"metrics": {
            "r_squared": {},
            "mse": {},
            "msle": {},
            "huber": {}
          }
        }
      }
    }

__

|

在此示例中，为回归分析定义了测试/训练拆分 ("training_percent")。此查询将评估限制为仅在训练拆分上执行。这意味着将计算训练误差。   ---|---    __

|

包含实际学生表现的地面实况值的字段。这是评估结果所必需的。   __

|

包含由回归分析计算的学生表现预测值的字段。   下一个示例计算测试误差。与前面的示例相比，唯一的区别是这次将"ml.is_training"设置为"false"，因此查询从评估中排除了训练拆分。

    
    
    response = client.ml.evaluate_data_frame(
      body: {
        index: 'student_performance_mathematics_reg',
        query: {
          term: {
            "ml.is_training": {
              value: false
            }
          }
        },
        evaluation: {
          regression: {
            actual_field: 'G3',
            predicted_field: 'ml.G3_prediction',
            metrics: {
              r_squared: {},
              mse: {},
              msle: {},
              huber: {}
            }
          }
        }
      }
    )
    puts response
    
    
    POST _ml/data_frame/_evaluate
    {
      "index": "student_performance_mathematics_reg",
      "query": {
        "term": {
          "ml.is_training": {
            "value": false __}
        }
      },
      "evaluation": {
        "regression": {
          "actual_field": "G3", __"predicted_field": "ml.G3_prediction", __"metrics": {
            "r_squared": {},
            "mse": {},
            "msle": {},
            "huber": {}
          }
        }
      }
    }

__

|

在此示例中，为回归分析定义了测试/训练拆分 ("training_percent")。此查询将评估限制为仅对测试拆分执行。这意味着将计算测试误差。   ---|---    __

|

包含实际学生表现的地面实况值的字段。这是评估结果所必需的。   __

|

包含由回归分析计算的学生表现预测值的字段。   ####Classificationedit

    
    
    response = client.ml.evaluate_data_frame(
      body: {
        index: 'animal_classification',
        evaluation: {
          classification: {
            actual_field: 'animal_class',
            predicted_field: 'ml.animal_class_prediction',
            metrics: {
              multiclass_confusion_matrix: {}
            }
          }
        }
      }
    )
    puts response
    
    
    POST _ml/data_frame/_evaluate
    {
       "index": "animal_classification",
       "evaluation": {
          "classification": { __"actual_field": "animal_class", __"predicted_field": "ml.animal_class_prediction", __"metrics": {
               "multiclass_confusion_matrix" : {} __}
          }
       }
    }

__

|

评估类型。   ---|---    __

|

包含实际动物分类的地面实况值的字段。这是评估结果所必需的。   __

|

包含通过分类分析进行动物分类的预测值的字段。   __

|

指定用于评估的指标。   API 返回以下结果：

    
    
    {
       "classification" : {
          "multiclass_confusion_matrix" : {
             "confusion_matrix" : [
             {
                "actual_class" : "cat", __"actual_class_doc_count" : 12, __"predicted_classes" : [ __{
                    "predicted_class" : "cat",
                    "count" : 12 __},
                  {
                    "predicted_class" : "dog",
                    "count" : 0 __}
                ],
                "other_predicted_class_doc_count" : 0 __},
              {
                "actual_class" : "dog",
                "actual_class_doc_count" : 11,
                "predicted_classes" : [
                  {
                    "predicted_class" : "dog",
                    "count" : 7
                  },
                  {
                    "predicted_class" : "cat",
                    "count" : 4
                  }
                ],
                "other_predicted_class_doc_count" : 0
              }
            ],
            "other_actual_class_count" : 0
          }
        }
      }

__

|

分析尝试预测的实际类的名称。   ---|---    __

|

索引中属于"actual_class"的文档数。   __

|

此对象包含预测类的列表以及与该类关联的预测数。   __

|

数据集中正确标识为猫的猫的数量。   __

|

数据集中被错误分类为狗的猫的数量。   __

|

分类为未列为"predicted_class"类的文档数。               响应 = client.ml.evaluate_data_frame( 正文： { 索引： 'animal_classification'， 评估： { 分类： { actual_field： 'animal_class'， 指标： { auc_roc： { class_name： 'dog' } } } } ) 放置响应 POST _ml/data_frame/_evaluate { "索引"： "animal_classification"， "评估"： { "分类"： { __"actual_field"： "animal_class"， __"metrics"： { "auc_roc" ： { __"class_name"： "dog" __} } } } }

__

|

评估类型。   ---|---    __

|

包含实际动物分类的地面实况值的字段。这是评估结果所必需的。   __

|

指定用于评估的指标。   __

|

指定在求值期间被视为正数的类名，所有其他类都被视为负数。   API 返回以下结果：

    
    
    {
      "classification" : {
        "auc_roc" : {
          "value" : 0.8941788639536681
        }
      }
    }

[« Delete data frame analytics jobs API](delete-dfanalytics.md) [Explain
data frame analytics API »](explain-dfanalytics.md)
