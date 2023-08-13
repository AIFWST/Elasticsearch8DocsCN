

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Date nanoseconds field type](date_nanos.md) [Flattened field type
»](flattened.md)

## 密集向量字段类型

"dense_vector"字段类型存储数值的密集向量。密集向量字段主要用于 k 最近邻 (kNN) 搜索搜索")。

"dense_vector"类型不支持聚合或排序。

默认情况下，您可以添加"dense_vector"字段作为基于"element_type"的数值数组，并带有"float"：

    
    
    response = client.indices.create(
      index: 'my-index',
      body: {
        mappings: {
          properties: {
            my_vector: {
              type: 'dense_vector',
              dims: 3
            },
            my_text: {
              type: 'keyword'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index',
      id: 1,
      body: {
        my_text: 'text1',
        my_vector: [
          0.5,
          10,
          6
        ]
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index',
      id: 2,
      body: {
        my_text: 'text2',
        my_vector: [
          -0.5,
          10,
          10
        ]
      }
    )
    puts response
    
    
    PUT my-index
    {
      "mappings": {
        "properties": {
          "my_vector": {
            "type": "dense_vector",
            "dims": 3
          },
          "my_text" : {
            "type" : "keyword"
          }
        }
      }
    }
    
    PUT my-index/_doc/1
    {
      "my_text" : "text1",
      "my_vector" : [0.5, 10, 6]
    }
    
    PUT my-index/_doc/2
    {
      "my_text" : "text2",
      "my_vector" : [-0.5, 10, 10]
    }

与大多数其他数据类型不同，密集向量始终是单值的。不可能在一个"dense_vector"字段中存储多个值。

### kNNsearch 的索引向量

_k最近neighbor_ (kNN) 搜索查找最接近查询向量的 _k_，由相似性指标度量度量。

密集向量字段可用于对"script_score"查询中的文档进行排名。这使您可以通过扫描所有文档并按相似性对它们进行排名来执行暴力 kNN 搜索。

在许多情况下，暴力 kNN 搜索效率不够高。因此，"dense_vector"类型支持将向量索引为专用数据结构，以支持通过搜索 API 中的"knn"选项进行快速 kNN 检索

用于近似kNN搜索的索引向量是一个昂贵的过程。摄取包含启用了"索引"的向量字段的文档可能需要大量时间。请参阅 k 最近邻 (kNN) 搜索以了解有关内存要求的更多信息。

您可以通过设置"index"参数来启用索引：

    
    
    response = client.indices.create(
      index: 'my-index-2',
      body: {
        mappings: {
          properties: {
            my_vector: {
              type: 'dense_vector',
              dims: 3,
              index: true,
              similarity: 'dot_product'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-2
    {
      "mappings": {
        "properties": {
          "my_vector": {
            "type": "dense_vector",
            "dims": 3,
            "index": true,
            "similarity": "dot_product" __}
        }
      }
    }

__

|

启用"index"后，您必须定义要在 kNNsearch 中使用的向量相似性 ---|--- Elasticsearch 使用 HNSW 算法来支持高效的 kNN 搜索。与大多数 kNN 算法一样，HNSW 是一种近似方法，它牺牲了结果精度以提高速度。

如果密集向量字段位于"嵌套"映射内，则无法对其进行索引。

### 密集向量场的参数

接受以下映射参数：

`element_type`

     (Optional, string) The data type used to encode vectors. The supported data types are `float` (default) and `byte`. `float` indexes a 4-byte floating-point value per dimension. `byte` indexes a 1-byte integer value per dimension. Using `byte` can result in a substantially smaller index size with the trade off of lower precision. Vectors using `byte` require dimensions with integer values between -128 to 127, inclusive for both indexing and searching. 
`dims`

    

(必需，整数)矢量维度数。索引向量不能超过"1024"("index"：true)，非索引向量不能超过"2048"。

[预览] 此功能处于技术预览状态，可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。 索引向量的维数可以扩展到"2048"。

`index`

     (Optional, Boolean) If `true`, you can search this field using the [kNN search API](knn-search-api.html "kNN search API"). Defaults to `false`. 

`similarity`

    

(必填*，字符串)要在 kNN 搜索中使用的向量相似性指标。文档按其向量字段与查询向量的相似性进行排名。每个文档的"_score"将从相似性中得出，以确保分数是积极的，并且较大的分数对应于更高的排名。

* 如果"索引"为"true"，则此参数是必需的。

"相似性"的有效值

`l2_norm`

     Computes similarity based on the L2 distance (also known as Euclidean distance) between the vectors. The document `_score` is computed as `1 / (1 + l2_norm(query, vector)^2)`. 
`dot_product`

    

计算两个向量的点积。此选项提供了一种执行余弦相似性的优化方法。约束和计算分数由"element_type"定义。

当"element_type"为"float"时，所有向量都必须为单位长度，包括文档和查询向量。文档"_score"计算为"(1 +dot_product(查询，向量))/ 2"。

当"element_type"为"字节"时，所有向量必须具有相同的长度，包括文档和查询向量，否则结果将不准确。文档"_score"计算为"0.5 + (dot_product(查询，矢量)/(32768 * dims))"，其中"dims"是每个矢量的维度数。

`cosine`

     Computes the cosine similarity. Note that the most efficient way to perform cosine similarity is to normalize all vectors to unit length, and instead use `dot_product`. You should only use `cosine` if you need to preserve the original vectors and cannot normalize them in advance. The document `_score` is computed as `(1 + cosine(query, vector)) / 2`. The `cosine` similarity does not allow vectors with zero magnitude, since cosine is not defined in this case. 

尽管它们在概念上是相关的，但"相似性"参数与"文本"字段"相似性"不同，并接受一组不同的选项。

`index_options`

    

(可选，对象)配置 kNN 索引算法的可选部分。HNSW 算法有两个内部参数，它们会影响数据结构的构建方式。可以调整这些以提高结果的准确性，但代价是索引速度较慢。提供"index_options"时，必须定义其所有属性。

"index_options"的属性

`type`

     (Required, string) The type of kNN algorithm to use. Currently only `hnsw` is supported. 
`m`

     (Required, integer) The number of neighbors each node will be connected to in the HNSW graph. Defaults to `16`. 
`ef_construction`

     (Required, integer) The number of candidates to track while assembling the list of nearest neighbors for each new node. Defaults to `100`. 

### 合成的"_source"

合成"_source"仅对 TSDB 索引(将"index.mode"设置为"time_series"的索引)正式发布。对于其他指数，合成"_source"处于技术预览状态。技术预览版中的功能可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

"dense_vector"字段支持合成"_source"。

[« Date nanoseconds field type](date_nanos.md) [Flattened field type
»](flattened.md)
