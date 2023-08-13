

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Time series aggregation](search-aggregations-bucket-time-series-
aggregation.md) [Subtleties of bucketing range fields »](search-
aggregations-bucket-range-field-note.md)

## 可变宽度直方图聚合

这是一个类似于直方图的多存储桶聚合。但是，未指定每个存储桶的宽度。相反，提供目标数量的存储桶，并根据文档分发动态确定存储桶间隔。这是使用简单的单程文档聚类算法完成的，该算法旨在获得桶质心之间的低距离。与其他多存储桶聚合不同，间隔不一定具有均匀的宽度。

返回的存储桶数将始终小于或等于目标数量。

请求目标为 2 个存储桶。

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          prices: {
            variable_width_histogram: {
              field: 'price',
              buckets: 2
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "prices": {
          "variable_width_histogram": {
            "field": "price",
            "buckets": 2
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "prices": {
          "buckets": [
            {
              "min": 10.0,
              "key": 30.0,
              "max": 50.0,
              "doc_count": 2
            },
            {
              "min": 150.0,
              "key": 185.0,
              "max": 200.0,
              "doc_count": 5
            }
          ]
        }
      }
    }

此聚合当前不能嵌套在从多个存储桶收集的任何聚合下。

### 聚类算法

每个分片获取第一个"initial_buffer"文档并将它们存储在内存中。缓冲区已满后，这些文档将被分类并线性分成"3/4 * shard_size桶"。接下来，将剩余的每个文档收集到最近的存储桶中，或者如果它与所有现有文档相距甚远，则将其放入新存储桶中。最多创建"shard_size"个总存储桶。

在 reduce 步骤中，协调节点按质心对所有分片中的存储桶进行排序。然后，重复合并具有最接近质心的两个存储桶，直到达到目标数量的存储桶。这种合并过程是聚集分层聚类的一种形式。

分片可以返回少于"shard_size"存储桶，但不能返回更多存储桶。

### 分片大小

"shard_size"参数指定协调节点将从每个分片请求的存储桶数。较高的"shard_size"会导致每个分片产生更小的存储桶。这降低了减少步骤后存储桶重叠的可能性。增加"shard_size"将提高直方图的准确性，但它也会使计算最终结果的成本更高，因为更大的优先级队列将不得不在分片级别进行管理，并且节点和客户端之间的数据传输将更大。

参数"存储桶"、"shard_size"和"initial_buffer"是可选的。默认情况下，"存储桶 = 10"、"shard_size = 存储桶 * 50"和"initial_buffer =min(10 * shard_size， 50000)"。

### 初始缓冲区

"initial_buffer"参数可用于指定在运行初始分桶算法之前将存储在分片内存中的单个文档的数量。存储桶分配是使用此"initial_buffer"文档样本确定的。因此，尽管较高的"initial_buffer"将使用更多内存，但它将导致更具代表性的集群。

### 存储桶边界是近似值

在归约步骤中，主节点不断将两个存储桶与最近的质心合并。如果两个存储桶具有重叠的边界但远质心，则它们可能不会合并。因此，在减少后，某个区间的最大值("max")可能大于后续存储桶中的最小值("最小")。为了减少此错误的影响，当发生此类重叠时，这些间隔之间的边界调整为"(最大 + 最小)/2"。

存储桶边界对异常值非常敏感

[« Time series aggregation](search-aggregations-bucket-time-series-
aggregation.md) [Subtleties of bucketing range fields »](search-
aggregations-bucket-range-field-note.md)
