

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Parent aggregation](search-aggregations-bucket-parent-aggregation.md)
[Range aggregation »](search-aggregations-bucket-range-aggregation.md)

## 随机采样器聚合

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

"random_sampler"聚合是单个存储桶聚合，它在聚合结果中随机包含文档。采样以牺牲准确性为代价显著提高了速度。

采样是通过在分片中提供整个文档集的随机子集来完成的。如果在搜索请求中提供了筛选器查询，则该筛选器将应用于采样的子集。因此，如果筛选器具有限制性，则很少有文档匹配;因此，统计数据可能不那么准确。

不要将此聚合与采样器聚合混淆。采样器聚合不是在所有文档上;相反，它会对与查询匹配的前 n 个文档进行采样。

    
    
    response = client.search(
      index: 'kibana_sample_data_ecommerce',
      size: 0,
      track_total_hits: false,
      body: {
        aggregations: {
          sampling: {
            random_sampler: {
              probability: 0.1
            },
            aggregations: {
              price_percentiles: {
                percentiles: {
                  field: 'taxful_total_price'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET kibana_sample_data_ecommerce/_search?size=0&track_total_hits=false
    {
      "aggregations": {
        "sampling": {
          "random_sampler": {
            "probability": 0.1
          },
          "aggs": {
            "price_percentiles": {
              "percentiles": {
                "field": "taxful_total_price"
              }
            }
          }
        }
      }
    }

### 顶级参数forrandom_sampler

`probability`

     (Required, float) The probability that a document will be included in the aggregated data. Must be greater than 0, less than `0.5`, or exactly `1`. The lower the probability, the fewer documents are matched. 
`seed`

     (Optional, integer) The seed to generate the random sampling of documents. When a seed is provided, the random subset of documents is the same between calls. 

### 采样是如何工作的？

聚合是索引中所有文档的随机样本。换句话说，采样是在背景文档集上进行的。如果提供了查询，则如果文档与查询匹配并且文档在随机抽样中，则返回文档。不会对匹配的文档进行采样。

考虑一组文档"[1， 2， 3， 4， 5]"。您的查询与"[1， 3，5]"匹配，随机抽样集为"[2， 4， 5]"。在这种情况下，返回的文档将为"[5]"。

这种类型的采样提供了与采样减少文档集大小的量相关的查询延迟几乎线性的改进：

!按采样因子划分的中位数加速比图

此图是 6300 万个文档的测试数据集的大多数聚合速度的典型特征。确切的常数将取决于数据集大小和分片数量，但加速和概率之间的关系形式广泛存在。对于某些聚合，速度可能没有那么显着。这些聚合具有一些与查看的文档数无关的恒定开销。即使对于这些聚合，速度的提高也可能是显着的。

样本集是通过使用几何分布('(1-p)^(k-1)*p')跳过文档生成的，成功概率是提供的"概率"(分布方程中的"p")。从分布返回的值指示要在后台跳过的文档数。这相当于随机统一选择文档。因此，成功前的预期失败次数为"(1-p)/p"。例如，如果"概率"：0.01，则预期失败次数(或跳过的平均文档数)将为"99"，方差为"9900"。因此，如果您的索引中只有 80 个文档或与过滤器匹配，则很可能不会收到任何结果。

!按采样概率和文档数划分的相对误差图

在上图中，"p"是提供给聚合的概率，"n"是与提供的任何查询匹配的文档数。您可以看到异常值对"总和"和"平均值"的影响，但是当许多文档仍以较高的采样率匹配时，相对误差仍然很低。

这表示针对典型的正偏态APM数据集进行聚合的结果，该数据集的上尾也有异常值。发现相对误差对样本数量的线性依赖性广泛存在，但斜率取决于聚合量的变化。因此，您自己的数据中的方差可能会导致相对错误率以不同的速率增加或减少。

### 随机抽样特殊情况

随机采样器聚合返回的所有计数都将缩放为简化可视化和计算。例如，在随机采样日期直方图聚合时，每个存储桶的每个"doc_count"值都按random_sampler"概率"值的倒数进行缩放。因此，如果存储桶的"doc_count"为"10，000"且"概率：0.1"，则聚合的实际文档数为"1，000"。

一个例外是基数聚合。唯一项目计数不适合自动缩放。解释基数计数时，请将其与random_sampler聚合中顶级"doc_count"中提供的采样文档数进行比较。它使您可以了解唯一值占总值的百分比。但是，它可能无法反映给定字段的唯一值的确切数量。

[« Parent aggregation](search-aggregations-bucket-parent-aggregation.md)
[Range aggregation »](search-aggregations-bucket-range-aggregation.md)
