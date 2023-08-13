

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Pipeline aggregations](search-
aggregations-pipeline.md)

[« Min bucket aggregation](search-aggregations-pipeline-min-bucket-
aggregation.md) [Moving percentiles aggregation »](search-aggregations-
pipeline-moving-percentiles-aggregation.md)

## 移动函数聚合

给定一系列有序的数据，移动函数聚合将在数据上滑动一个窗口，并允许用户指定在每个数据窗口上执行的自定义脚本。为方便起见，预定义了许多常用函数，例如最小值/最大值、移动平均线等。

###Syntax

"moving_fn"聚合单独如下所示：

    
    
    {
      "moving_fn": {
        "buckets_path": "the_sum",
        "window": 10,
        "script": "MovingFunctions.min(values)"
      }
    }

**表 64.'moving_fn' 参数**

参数名称 |描述 |必填 |默认值 ---|---|---|--- 'buckets_path'

|

感兴趣指标的路径(有关详细信息，请参阅"buckets_path"语法

|

Required

|   "窗口"

|

要在直方图上"滑动"的窗口大小。

|

Required

|   "脚本"

|

应在每个数据窗口上执行的脚本

|

Required

|   "gap_policy"

|

在数据中发现差距时要应用的策略。请参阅处理数据中的差距。

|

Optional

|

"跳过""转移"

|

窗口位置的移动。

|

Optional

|

0 "moving_fn"聚合必须嵌入"直方图"或"date_histogram"聚合中。它们可以像任何其他指标聚合一样嵌入：

    
    
    response = client.search(
      body: {
        size: 0,
        aggregations: {
          my_date_histo: {
            date_histogram: {
              field: 'date',
              calendar_interval: '1M'
            },
            aggregations: {
              the_sum: {
                sum: {
                  field: 'price'
                }
              },
              the_movfn: {
                moving_fn: {
                  buckets_path: 'the_sum',
                  window: 10,
                  script: 'MovingFunctions.unweightedAvg(values)'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /_search
    {
      "size": 0,
      "aggs": {
        "my_date_histo": {                  __"date_histogram": {
            "field": "date",
            "calendar_interval": "1M"
          },
          "aggs": {
            "the_sum": {
              "sum": { "field": "price" } __},
            "the_movfn": {
              "moving_fn": {
                "buckets_path": "the_sum", __"window": 10,
                "script": "MovingFunctions.unweightedAvg(values)"
              }
            }
          }
        }
      }
    }

__

|

在"时间戳"字段上构造一个名为"my_date_histo"的"date_histogram"，间隔为一天---|---__

|

"总和"指标用于计算字段的总和。这可以是任何数字度量(总和、最小值、最大值等)__

|

最后，我们指定一个"moving_fn"聚合，该聚合使用"the_sum"指标作为输入。   移动平均线是通过首先在字段上指定"直方图"或"date_histogram"来构建的。然后，您可以选择在该直方图内添加数值指标，例如"总和"。最后，"moving_fn"嵌入在直方图中。然后，使用"buckets_path"参数"指向"直方图中的同级指标之一(有关"buckets_path"语法的说明，请参阅"buckets_path"语法。

来自上述聚合的示例响应可能如下所示：

    
    
    {
       "took": 11,
       "timed_out": false,
       "_shards": ...,
       "hits": ...,
       "aggregations": {
          "my_date_histo": {
             "buckets": [
                 {
                     "key_as_string": "2015/01/01 00:00:00",
                     "key": 1420070400000,
                     "doc_count": 3,
                     "the_sum": {
                        "value": 550.0
                     },
                     "the_movfn": {
                        "value": null
                     }
                 },
                 {
                     "key_as_string": "2015/02/01 00:00:00",
                     "key": 1422748800000,
                     "doc_count": 2,
                     "the_sum": {
                        "value": 60.0
                     },
                     "the_movfn": {
                        "value": 550.0
                     }
                 },
                 {
                     "key_as_string": "2015/03/01 00:00:00",
                     "key": 1425168000000,
                     "doc_count": 2,
                     "the_sum": {
                        "value": 375.0
                     },
                     "the_movfn": {
                        "value": 305.0
                     }
                 }
             ]
          }
       }
    }

### 自定义用户脚本

移动函数聚合允许用户指定任意脚本来定义自定义逻辑。每次收集新的数据窗口时都会调用该脚本。这些值在"值"变量中提供给脚本。然后，脚本应执行某种计算并发出单个"double"作为结果。不允许发射"null"，但允许发出"NaN"和+/- "Inf"。

例如，此脚本将仅返回窗口中的第一个值，如果没有可用值，则返回"NaN"：

    
    
    response = client.search(
      body: {
        size: 0,
        aggregations: {
          my_date_histo: {
            date_histogram: {
              field: 'date',
              calendar_interval: '1M'
            },
            aggregations: {
              the_sum: {
                sum: {
                  field: 'price'
                }
              },
              the_movavg: {
                moving_fn: {
                  buckets_path: 'the_sum',
                  window: 10,
                  script: 'return values.length > 0 ? values[0] : Double.NaN'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    POST /_search
    {
      "size": 0,
      "aggs": {
        "my_date_histo": {
          "date_histogram": {
            "field": "date",
            "calendar_interval": "1M"
          },
          "aggs": {
            "the_sum": {
              "sum": { "field": "price" }
            },
            "the_movavg": {
              "moving_fn": {
                "buckets_path": "the_sum",
                "window": 10,
                "script": "return values.length > 0 ? values[0] : Double.NaN"
              }
            }
          }
        }
      }
    }

### 移位参数

默认情况下("shift = 0")，用于计算的窗口是不包括当前存储桶的最后一个"n"值。将"移位"增加 1 将起始窗口位置向右移动"1"。

* 要将当前存储桶包含在窗口中，请使用"shift = 1"。  * 对于中心对齐(当前存储桶前后的"n / 2"值)，请使用"shift = window / 2"。  * 对于右对齐(当前存储桶后的"n"值)，请使用"shift = 窗口"。

如果窗口边缘中的任何一个移动到数据系列的边框之外，窗口将收缩以仅包含可用值。

### 预构建函数

为方便起见，许多函数已预先构建，并在"moving_fn"脚本上下文中可用：

* 'max()' * 'min()' * 'sum()' * 'stdDev()' * 'unweightedAvg()' * 'linearWeightedAvg()' * 'ewma()' * 'holt()' * 'holtWinters()'

这些函数可从"移动函数"命名空间获得。例如'MovingFunctions.max()'

#### maxFunction

此函数接受双精度的集合，并返回该窗口中的最大值。"null"和"NaN"值将被忽略;最大值仅根据实际值计算。如果窗口为空，或者所有值均为"null"/"NaN"，则返回"NaN"作为结果。

**表 65.'max(double[] 值)' 参数**

参数名称 |描述 ---|--- "值"

|

查找最大响应的值窗口 = client.search( body： { size： 0， aggregations： { my_date_histo： { date_histogram： { field： 'date'， calendar_interval： '1M' }， 聚合： { the_sum： { 总和： { 字段： '价格' } }， the_moving_max： { moving_fn： { buckets_path： 'the_sum'， 窗口： 10， 脚本： '移动函数.max(值)' } } } } } } } ) 放置响应 POST /_search { "size"： 0， "aggs"： { "my_date_histo"： { "date_histogram"： { "field"： "date"， "calendar_interval"： "1M" }， "aggs"： { "the_sum"： { "sum"： { "field"： "price" } }，           "the_moving_max"： { "moving_fn"： { "buckets_path"： "the_sum"， "窗口"： 10， "脚本"： "MovingFunctions.max(values)" } } } } } }

#### 最小函数

此函数接受双精度的集合，并返回该窗口中的最小值。"null"和"NaN"值将被忽略;最小值仅根据实际值计算。如果窗口为空，或者所有值均为"null"/"NaN"，则返回"NaN"作为结果。

**表 66.'min(double[] 值)' 参数**

参数名称 |描述 ---|--- "值"

|

查找最小响应的值窗口 = client.search( body： { size： 0， aggregations： { my_date_histo： { date_histogram： { field： 'date'， calendar_interval： '1M' }， 聚合： { the_sum： { 总和： { 字段： '价格' } }， the_moving_min： { moving_fn： { buckets_path： 'the_sum'， 窗口： 10， 脚本： 'MovingFunctions.min(values)' } } } ) 放置响应 POST /_search { "size"： 0， "aggs"： { "my_date_histo"： { "date_histogram"： { "field"： "date"， "calendar_interval"： "1M" }， "aggs"： { "the_sum"： { "sum"： { "field"： "price" } }，           "the_moving_min"： { "moving_fn"： { "buckets_path"： "the_sum"， "窗口"： 10， "脚本"： "MovingFunctions.min(values)" } } } } } }

#### 求和函数

此函数接受双精度的集合，并返回该窗口中值的总和。"null"和"NaN"值将被忽略;总和仅根据实际值计算。如果窗口为空，或者所有值均为"null"/"NaN"，则返回"0.0"作为结果。

表 67.'sum(double[] 值)' 参数**

参数名称 |描述 ---|--- "值"

|

用于查找响应总和的值窗口 = client.search( body： { size： 0， aggregations： { my_date_histo： { date_histogram： { field： 'date'， calendar_interval： '1M' }， 聚合： { the_sum： { 总和： { 字段： 'price' } }， the_moving_sum： { moving_fn： { buckets_path： 'the_sum'， 窗口： 10， 脚本： 'MovingFunctions.sum(values)' } } } } ) 放置响应 POST /_search { "size"： 0， "aggs"： { "my_date_histo"： { "date_histogram"： { "field"： "date"， "calendar_interval"： "1M" }， "aggs"： { "the_sum"： { "总和"： { "字段"： "价格" } }，           "the_moving_sum"： { "moving_fn"： { "buckets_path"： "the_sum"， "窗口"： 10， "script"： "MovingFunctions.sum(values)" } } } }

#### 标准开发函数

此函数接受双精度值和平均值的集合，然后返回该窗口中值的标准偏差。忽略"空"和"NaN"值;总和仅根据实际值计算。如果窗口为空，或者所有值均为"null"/"NaN"，则返回"0.0"作为结果。

表 68.'stdDev(double[] 值)' 参数**

参数名称 |描述 ---|--- "值"

|

用于查找"avg"标准偏差的值窗口

|

窗口响应的平均值 = client.search( body： { size： 0， aggregations： { my_date_histo： { date_histogram： { field： 'date'， calendar_interval： '1M' }， 聚合： { the_sum： { sum： { field： 'price' } }， the_moving_sum： { moving_fn： { buckets_path： 'the_sum'，                 window： 10， script： 'MovingFunctions.stdDev(values， MovingFunctions.unweightedAvg(values))' } } } } } ) 把响应 POST /_search { "size"： 0， "aggs"： { "my_date_histo"： { "date_histogram"： { "field"： "date"， "calendar_interval"： "1M" }， "aggs"： { "the_sum"： { "sum"： { "field"： "price" }           }， "the_moving_sum"： { "moving_fn"： { "buckets_path"： "the_sum"， "window"： 10， "script"： "MovingFunctions.stdDev(values， MovingFunctions.unweightedAvg(values))" } } } } } }

必须向标准差函数提供"avg"参数，因为可以在窗口上计算不同样式的平均值(简单、线性加权等)。下面详述的各种移动平均线可用于计算标准差函数的平均值。

#### 未加权平均函数

"unweightedAvg"函数计算窗口中所有值的总和，然后除以窗口的大小。它实际上是窗口的简单算术平均值。简单移动平均线不执行任何随时间变化的加权，这意味着"简单"移动平均线的值往往"滞后"于实际数据。

"null"和"NaN"值将被忽略;平均值仅根据其值计算。如果窗口为空，或者所有值均为"null"/"NaN"，则返回"NaN"作为结果。这意味着平均计算中使用的计数是非"空"，非"NaN"值的计数。

**表 69.'未加权平均值(双精度[] 值)' 参数**

参数名称 |描述 ---|--- "值"

|

用于查找响应总和的值窗口 = client.search( body： { size： 0， aggregations： { my_date_histo： { date_histogram： { field： 'date'， calendar_interval： '1M' }， 聚合： { the_sum： { 总和： { 字段： '价格' } }， the_movavg： { moving_fn： { buckets_path： 'the_sum'， 窗口： 10， 脚本： 'MovingFunctions.unweightedAvg(values)' } } } } } } ) 放置响应 POST /_search { "size"： 0， "aggs"： { "my_date_histo"： { "date_histogram"： { "field"： "date"， "calendar_interval"： "1M" }， "aggs"： { "the_sum"： { "sum"： { "field"： "price" } }，           "the_movavg"： { "moving_fn"： { "buckets_path"： "the_sum"， "窗口"： 10， "script"： "MovingFunctions.unweightedAvg(values)" } } } }

### 线性加权平均函数

"linearWeightedAvg"函数为序列中的点分配线性权重，使得"较旧"的数据点(例如窗口开头的数据点)对总平均值的贡献线性较小。线性加权有助于减少数据平均值后面的"滞后"，因为较旧的点影响较小。

如果窗口为空，或者所有值均为"null"/"NaN"，则返回"NaN"作为结果。

**表 70.'线性加权平均(双精度[] 值)' 参数**

参数名称 |描述 ---|--- "值"

|

用于查找响应总和的值窗口 = client.search( body： { size： 0， aggregations： { my_date_histo： { date_histogram： { field： 'date'， calendar_interval： '1M' }， 聚合： { the_sum： { 总和： { 字段： '价格' } }， the_movavg： { moving_fn： { buckets_path： 'the_sum'， 窗口： 10， 脚本： 'MovingFunctions.linearWeightedAvg(values)' } } } } } ) 把响应 POST /_search { "size"： 0， "aggs"： { "my_date_histo"： { "date_histogram"： { "field"： "date"， "calendar_interval"： "1M" }， "aggs"： { "the_sum"： { "sum"： { "field"： "price" } }，           "the_movavg"： { "moving_fn"： { "buckets_path"： "the_sum"， "window"： 10， "script"： "MovingFunctions.linearWeightedAvg(values)" } } } } }

### ewmaFunction

"ewma"函数(又名"单指数")类似于"linearMovAvg"函数，只是较旧的数据点变得指数级不那么重要，而不是线性降低重要性。重要性衰减的速度可以通过"alpha"设置来控制。较小的值会使权重衰减缓慢，从而提供更大的平滑度，并考虑窗口的较大部分。较大的值会使权重快速衰减，从而减少旧值对移动平均线的影响。这往往会使移动平均线更紧密地跟踪数据，但平滑度较低。

"null"和"NaN"值将被忽略;平均值仅根据其值计算。如果窗口为空，或者所有值均为"null"/"NaN"，则返回"NaN"作为结果。这意味着平均计算中使用的计数是非"空"，非"NaN"值的计数。

**表 71.'ewma(double[] 值，双字母)" 参数**

参数名称 |描述 ---|--- "值"

|

用于查找"alpha"之和的值窗口

|

指数衰减响应 = client.search( body： { size： 0， aggregations： { my_date_histo： { date_histogram： { field： 'date'， calendar_interval： '1M' }， 聚合： { the_sum： { 总和： { 字段： '价格' } }， the_movavg： { moving_fn： { buckets_path： 'the_sum'，                 窗口： 10， 脚本： 'MovingFunctions.ewma(values， 0.3)' } } } } ) 放置响应 POST /_search { "size"： 0， "aggs"： { "my_date_histo"： { "date_histogram"： { "field"： "date"， "calendar_interval"： "1M" }， "aggs"： { "the_sum"： { "总和"： { "字段"： "价格" } }， "the_movavg"： {             "moving_fn"： { "buckets_path"： "the_sum"， "窗口"： 10， "脚本"： "MovingFunctions.ewma(values， 0.3)" } } } } }

### 霍尔特函数

"holt"函数(又名"双指数")包含一个跟踪数据趋势的第二指数项。当数据具有基础线性趋势时，单个指数表现不佳。双指数模型在内部计算两个值："水平"和"趋势"。

级别计算类似于"ewma"，并且是数据的指数加权视图。不同之处在于使用先前平滑的值而不是原始值，这允许它保持接近原始系列。趋势计算着眼于当前值和最后一个值之间的差异(例如，平滑数据的斜率或趋势)。趋势值也是指数加权的。

值是通过乘以水平和趋势分量生成的。

"null"和"NaN"值将被忽略;平均值仅根据其值计算。如果窗口为空，或者所有值均为"null"/"NaN"，则返回"NaN"作为结果。这意味着平均计算中使用的计数是非"空"，非"NaN"值的计数。

**表 72.'holt(double[] 值，双字母)' 参数**

参数名称 |描述 ---|--- "值"

|

用于查找"alpha"之和的值窗口

|

电平衰减值"贝塔"

|

趋势衰减值响应 = client.search( body： { size： 0， 聚合： { my_date_histo： { date_histogram： { field： 'date'， calendar_interval： '1M' }， 聚合： { the_sum： { 总和： { 字段： '价格' } }， the_movavg： { moving_fn： { buckets_path： 'the_sum'，                 窗口： 10， 脚本： 'MovingFunctions.holt(values， 0.3， 0.1)' } } } } ) 放置响应 POST /_search { "size"： 0， "aggs"： { "my_date_histo"： { "date_histogram"： { "field"： "date"， "calendar_interval"： "1M" }， "aggs"： { "the_sum"： { "sum"： { "field"： "price" } }， "the_movavg"： {             "moving_fn"： { "buckets_path"： "the_sum"， "窗口"： 10， "script"： "MovingFunctions.holt(values， 0.3， 0.1)" } }

实际上，"alpha"值在"holtMovAvg"中的行为与"ewmaMovAvg"非常相似：较小的值会产生更多的平滑和更多的滞后，而较大的值会产生更紧密的跟踪和更少的滞后。"beta"的价值通常很难看到。较小的值强调长期趋势(例如整个序列中的恒定线性趋势)，而较大的值强调短期趋势。

### holtWintersFunction

"holtWinters"函数(又名"三重指数")包含一个第三个指数项，用于跟踪数据的季节性方面。因此，这种聚合基于三个组成部分进行平滑："水平"、"趋势"和"季节性"。

水平和趋势计算与"holt"相同 季节性计算着眼于当前点与较早的点数周期之间的差异。

霍尔特-温特斯比其他移动平均值需要更多的把手。您需要指定数据的"周期性"：例如，如果您的数据每 7 天有一次周期趋势，则可以设置"周期 = 7"。同样，如果有月度趋势，您可以将其设置为"30"。目前没有周期性检测，尽管计划在未来的增强功能中这样做。

"null"和"NaN"值将被忽略;平均值仅根据其值计算。如果窗口为空，或者所有值均为"null"/"NaN"，则返回"NaN"作为结果。这意味着平均计算中使用的计数是非"空"，非"NaN"值的计数。

**表 73.'霍尔特温特斯(双倍[] 值，双阿尔法)' 参数**

参数名称 |描述 ---|--- "值"

|

用于查找"alpha"之和的值窗口

|

电平衰减值"贝塔"

|

趋势衰减值"伽马"

|

季节性衰减值"周期"

|

数据"乘法"的周期性

|

如果您希望使用乘法 holt-winters，则为 true，如果使用加法响应为 false，则为 client.search( body： { size： 0， aggregations： { my_date_histo： { date_histogram： { field： 'date'， calendar_interval： '1M' }， aggregations： { the_sum： { sum： { field： 'price' } }， the_movavg： { moving_fn： {                 buckets_path： 'the_sum'， 窗口： 10， 脚本： 'if (values.length > 5*2) {MovingFunctions.holtWinters(values， 0.3， 0.1， 0.1， 5， false)}' } ) put response POST /_search { "size"： 0， "aggs"： { "my_date_histo"： { "date_histogram"： { "field"： "date"， "calendar_interval"： "1M" }， "aggs"： {           "the_sum"： { "sum"： { "field"： "price" } }， "the_movavg"： { "moving_fn"： { "buckets_path"： "the_sum"， "window"： 10， "script"： "if (values.length > 5*2) {MovingFunctions.holtWinters(values， 0.3， 0.1， 0.1， 0.1， 5， false)}" } }

乘法霍尔特-温特斯的工作原理是将每个数据点除以季节性值。如果任何数据为零，或者数据中存在间隙(因为这会导致除以零)，则这是有问题的。为了解决这个问题，"多"Holt-Winters 将所有值填充非常小的量 (1*10-10)，以便所有值都不为零。这会影响结果，但影响很小。如果你的数据不为零，或者你更喜欢在遇到零时看到"NaN"，你可以用"pad：false"禁用此行为

#### "冷启动"

不幸的是，由于Holt-Winters的性质，它需要两个周期的数据来"引导"算法。这意味着您的"窗口"必须始终至少是月经大小的两倍。如果不是，将引发异常。这也意味着霍尔特-温特斯不会为第一个"2 * 周期"存储桶发出值;当前算法不会回播。

您会注意到，在上面的示例中，我们有一个"if ()"语句检查值的大小。这是检查以确保在调用holt-winters函数之前我们有两个周期的数据('5 * 2'，其中5是'holtWintersMovAvg'函数中指定的周期)。

[« Min bucket aggregation](search-aggregations-pipeline-min-bucket-
aggregation.md) [Moving percentiles aggregation »](search-aggregations-
pipeline-moving-percentiles-aggregation.md)
