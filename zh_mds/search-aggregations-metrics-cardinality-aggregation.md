

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« Boxplot aggregation](search-aggregations-metrics-boxplot-aggregation.md)
[Extended stats aggregation »](search-aggregations-metrics-extendedstats-
aggregation.md)

## 基数聚合

一种"单值"指标聚合，用于计算非重复值的近似计数。

假设您正在为实体店销售额编制索引，并希望计算与查询匹配的已售产品的唯一数量：

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          type_count: {
            cardinality: {
              field: 'type'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "type_count": {
          "cardinality": {
            "field": "type"
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "type_count": {
          "value": 3
        }
      }
    }

### 精度控制

此聚合还支持"precision_threshold"选项：

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          type_count: {
            cardinality: {
              field: 'type',
              precision_threshold: 100
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "type_count": {
          "cardinality": {
            "field": "type",
            "precision_threshold": 100 __}
        }
      }
    }

__

|

"precision_threshold"选项允许以内存换取准确性，并定义一个唯一计数，低于该计数的计数预期接近准确。高于此值，计数可能会变得更加模糊。支持的最大值为 40000，阈值高于此数字将与阈值 40000 具有相同的效果。默认值为"3000"。   ---|--- ### 计数是近似编辑

计算精确计数需要将值加载到哈希集中并返回其大小。在处理高基数集和/或大型值时，这不会扩展，因为所需的内存使用量以及在节点之间通信这些分片集的需求会占用集群的太多资源。

这种"基数"聚合基于 HyperLogLog++算法，该算法基于具有一些有趣属性的值的哈希进行计数：

* 可配置的精度，决定如何用内存换取精度， * 低基数集的出色精度， * 固定内存使用量：无论有数十个还是数十亿个唯一值，内存使用量仅取决于配置的精度。

对于精度阈值"c"，我们使用的实现需要大约"c * 8"字节。

下图显示了阈值前后误差的变化情况：

基数错误

对于所有 3 个阈值，计数一直精确到配置的阈值。虽然不能保证，但情况很可能如此。准确性不实践取决于所讨论的数据集。通常，大多数数据集始终表现出良好的准确性。另请注意，即使阈值低至 100，即使在计算数百万个项目时，误差仍然非常低(如上图所示为 1-6%)。

HyperLogLog++ 算法依赖于哈希值的前导零，数据集中哈希的精确分布会影响基数的准确性。

### 预计算哈希

在具有高基数的字符串字段上，将字段值的哈希存储在索引中，然后在此字段上运行基数聚合可能会更快。这可以通过从客户端提供哈希值来完成，也可以通过使用"mapper-murmur3"插件让 Elasticsearch 为您计算哈希值来完成。

预计算哈希通常只对非常大和/或高基数字段有用，因为它可以节省 CPU 和内存。但是，在数值字段上，哈希非常快，存储原始值需要与存储哈希一样多或更少的内存。这在低基数字符串字段上也是如此，特别是考虑到这些字符串字段进行了优化，以确保每个段的每个唯一值最多计算一次哈希。

###Script

如果需要两个字段组合的基数，请创建将它们组合在一起并聚合它的运行时字段。

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        runtime_mappings: {
          type_and_promoted: {
            type: 'keyword',
            script: "emit(doc['type'].value + ' ' + doc['promoted'].value)"
          }
        },
        aggregations: {
          type_promoted_count: {
            cardinality: {
              field: 'type_and_promoted'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "runtime_mappings": {
        "type_and_promoted": {
          "type": "keyword",
          "script": "emit(doc['type'].value + ' ' + doc['promoted'].value)"
        }
      },
      "aggs": {
        "type_promoted_count": {
          "cardinality": {
            "field": "type_and_promoted"
          }
        }
      }
    }

### 缺失值

"missing"参数定义应如何处理缺少值的文档。默认情况下，它们将被忽略，但也可以将它们视为具有值。

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          tag_cardinality: {
            cardinality: {
              field: 'tag',
              missing: 'N/A'
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "tag_cardinality": {
          "cardinality": {
            "field": "tag",
            "missing": "N/A" __}
        }
      }
    }

__

|

"标签"字段中没有值的文档将与值为"N/A"的文档属于同一存储桶。   ---|--- ### 执行提示编辑

您可以使用不同的机制运行基数聚合：

* 直接使用字段值("直接") * 使用字段的全局序号并在完成分片后解析这些值 ("global_ordinals") * 使用段序号值并在每个段后解析这些值 ("segment_ordinals")

此外，还有两种"基于启发式"的模式。这些模式将导致 Elasticsearch 使用一些关于索引状态的数据来选择合适的执行方法。两种启发式方法是：

* 'save_time_heuristic' \- 这是 Elasticsearch 8.4 及更高版本中的默认值。  * 'save_memory_heuristic' \- 这是 Elasticsearch 8.3 及更早版本中的默认值

如果未指定，Elasticsearch 将应用启发式方法来选择适当的模式。另请注意，对于某些数据(非序数字段)，"direct"是唯一的选项，在这些情况下将忽略提示。通常，不需要设置此值。

[« Boxplot aggregation](search-aggregations-metrics-boxplot-aggregation.md)
[Extended stats aggregation »](search-aggregations-metrics-extendedstats-
aggregation.md)
