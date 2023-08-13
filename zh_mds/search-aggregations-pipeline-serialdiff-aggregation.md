

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Pipeline aggregations](search-
aggregations-pipeline.md)

[« Percentiles bucket aggregation](search-aggregations-pipeline-percentiles-
bucket-aggregation.md) [Stats bucket aggregation »](search-aggregations-
pipeline-stats-bucket-aggregation.md)

## 串行差异聚合

序列差分是一种技术，其中在不同的时间滞后或周期中从自身中减去时间序列中的值。例如，数据点 f(x) = f(xt) - f(xt-n)，其中 n 是正在使用的周期。

周期 1 相当于没有时间归一化的导数：它只是从一个点到下一个点的变化。单个周期对于消除恒定的线性趋势很有用。

单个周期对于将数据转换为平稳序列也很有用。在此示例中，道琼斯指数绘制在 ~250 天内。原始数据不是静止的，这使得某些技术难以使用。

通过计算第一个差值，我们对数据进行去趋势化(例如，删除不恒定的线性趋势)。我们可以看到数据成为一个平稳序列(例如，第一个差值随机分布在零附近，并且似乎没有表现出任何模式/行为)。转换显示数据集遵循随机游走;该值是前一个值 +/- 随机量。这种洞察力允许选择更多的分析工具。

![dow](images/pipeline_serialdiff/dow.png)

图7.道琼斯绘制并用第一差分使静止

较大的周期可用于消除季节性/周期性行为。在这个例子中，旅鼠群是用正弦波+恒定线性趋势+随机噪声合成生成的。正弦波的周期为 30 天。

第一个差值消除了恒定趋势，只留下一个正弦波。然后将第 30 个差值应用于第一个差值以消除循环行为，留下一个适合其他分析的平稳序列。

![lemmings](images/pipeline_serialdiff/lemmings.png)

图8.绘制的旅鼠数据使具有第 1 和第 30 个差值的静止

###Syntax

"serial_diff"聚合单独如下所示：

    
    
    {
      "serial_diff": {
        "buckets_path": "the_sum",
        "lag": 7
      }
    }

**表 77.'serial_diff' 参数**

参数名称 |描述 |必填 |默认值 ---|---|---|--- 'buckets_path'

|

感兴趣指标的路径(有关详细信息，请参阅"buckets_path"语法

|

Required

|   "滞后"

|

要从当前值中减去的历史存储桶。例如，滞后 7 将从 7 个存储桶前的值中减去当前值。必须是正的、非零的整数

|

Optional

|

"1" "gap_policy"

|

确定在遇到数据间隙时应发生的情况。

|

Optional

|

"insert_zeros"格式"

|

十进制格式模式的输出值。如果指定，则在聚合的"value_as_string"属性中返回格式化值

|

Optional

|

"空""serial_diff"聚合必须嵌入到"直方图"或"date_histogram"聚合中：

    
    
    response = client.search(
      body: {
        size: 0,
        aggregations: {
          my_date_histo: {
            date_histogram: {
              field: 'timestamp',
              calendar_interval: 'day'
            },
            aggregations: {
              the_sum: {
                sum: {
                  field: 'lemmings'
                }
              },
              thirtieth_difference: {
                serial_diff: {
                  buckets_path: 'the_sum',
                  lag: 30
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
                "field": "timestamp",
                "calendar_interval": "day"
             },
             "aggs": {
                "the_sum": {
                   "sum": {
                      "field": "lemmings" __}
                },
                "thirtieth_difference": {
                   "serial_diff": { __"buckets_path": "the_sum",
                      "lag" : 30
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

"总和"指标用于计算字段的总和。这可以是任何度量(总和、最小值、最大值等)__

|

最后，我们指定一个"serial_diff"聚合，该聚合使用"the_sum"指标作为输入。   序列差异是通过首先在字段上指定"直方图"或"date_histogram"来构建的。然后，您可以选择在该直方图内添加普通指标，例如"总和"。最后，"serial_diff"嵌入在直方图中。然后，使用"buckets_path"参数"指向"直方图中的同级指标之一(有关"buckets_path"语法的说明，请参阅"buckets_path"语法。

[« Percentiles bucket aggregation](search-aggregations-pipeline-percentiles-
bucket-aggregation.md) [Stats bucket aggregation »](search-aggregations-
pipeline-stats-bucket-aggregation.md)
