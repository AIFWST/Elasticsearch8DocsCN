

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Search your
data](search-your-data.md)

[« Sort search results](sort-search-results.md) [Semantic search
»](semantic-search.md)

## k-最近邻 (kNN)搜索

_k最近neighbor_ (kNN) 搜索查找最接近查询向量的 _k_，由相似性指标度量度量。

kNN 的常见用例包括：

* 基于自然语言处理(NLP)算法的相关性排名 * 产品推荐和推荐引擎 * 图像或视频的相似性搜索

###Prerequisites

* 要运行 kNN 搜索，您必须能够将数据转换为有意义的矢量值。您可以在 Elasticsearch 中使用自然语言处理 (NLP) 模型创建这些向量，也可以在 Elasticsearch 之外生成它们。矢量可以作为"dense_vector"字段值添加到文档中。查询表示为具有相同维度的向量。

设计向量，使文档的向量越接近查询向量，基于相似性指标，其匹配度就越好。

* 要完成本指南中的步骤，您必须具有以下索引权限：

    * `create_index` or `manage` to create an index with a `dense_vector` field 
    * `create`, `index`, or `write` to add data to the index you created 
    * `read` to search the index 

### kNN方法

Elasticsearch 支持两种 kNN 搜索方法：

* 使用"knn"搜索选项近似 kNN * 使用带有向量函数的"script_score"查询精确、暴力的 kNN

在大多数情况下，您需要使用近似的 kNN。近似 kNN 提供更低的延迟，但代价是索引速度较慢且准确性不完美。

精确的蛮力 kNN 保证了准确的结果，但不能很好地扩展大型数据集。使用这种方法，"script_score"查询必须扫描每个匹配的文档以计算向量函数，这可能会导致搜索速度变慢。但是，可以通过使用查询来限制传递给函数的匹配文档数来改善延迟。如果将数据筛选为一小部分文档，则可以使用此方法获得良好的搜索性能。

### ApproxkNN

与其他类型的搜索相比，近似 kNN 搜索具有特定的资源要求。特别是，所有矢量数据都必须适合节点的页面缓存才能高效。有关配置和大小调整的重要说明，请参阅近似的 kNN 搜索调谐指南。

要运行近似 kNN 搜索，请使用"knn"选项搜索一个或多个启用了索引的"dense_vector"字段。

1. 显式映射一个或多个"dense_vector"字段。近似 kNN 搜索需要以下映射选项：

    * An `index` value of `true`. 
    * A `similarity` value. This value determines the similarity metric used to score documents based on similarity between the query and document vector. For a list of available metrics, see the [`similarity`](dense-vector.html#dense-vector-similarity) parameter documentation. 
    
        response = client.indices.create(
      index: 'image-index',
      body: {
        mappings: {
          properties: {
            "image-vector": {
              type: 'dense_vector',
              dims: 3,
              index: true,
              similarity: 'l2_norm'
            },
            "title-vector": {
              type: 'dense_vector',
              dims: 5,
              index: true,
              similarity: 'l2_norm'
            },
            title: {
              type: 'text'
            },
            "file-type": {
              type: 'keyword'
            }
          }
        }
      }
    )
    puts response
    
        PUT image-index
    {
      "mappings": {
        "properties": {
          "image-vector": {
            "type": "dense_vector",
            "dims": 3,
            "index": true,
            "similarity": "l2_norm"
          },
          "title-vector": {
            "type": "dense_vector",
            "dims": 5,
            "index": true,
            "similarity": "l2_norm"
          },
          "title": {
            "type": "text"
          },
          "file-type": {
            "type": "keyword"
          }
        }
      }
    }

2. 为数据编制索引。           POST 图像索引/_bulk？刷新=真 { "索引"： { "_id"： "1" } } { "图像矢量"： [1， 5， -20]， "标题矢量"： [12， 50， -10， 0， 1]， "标题"： "驼鹿家族"， "文件类型"： "JPG" } { "索引"： { "_id"： "2" } } { "图像矢量"： [42， 8， -15]， "标题矢量"： [25， 1， 4， -12， 2]， "标题"： "阿尔卑斯湖"， "文件类型"： "PNG" } { "索引"： { "_id"： "3" } } { "图像矢量"： [15， 11， 23]， "标题矢量"： [1， 5， 25， 50， 20]， "标题"： "满月"， "文件类型"： "JPG" } ...

3. 使用"knn"选项运行搜索。           响应 = client.search( index： 'image-index'， body： { knn： { field： 'image-vector'， query_vector： [ -5， 9， -12 ]， k： 10， num_candidates： 100 }， fields： [ 'title'， 'file-type' ] } ) put response POST image-index/_search { "knn"： { "field"： "image-vector"， "query_vector"： [-5， 9， -12]， "k"： 10，       "num_candidates"： 100 }， "字段"： [ "标题"， "文件类型" ] }

文档"_score"由查询和文档向量之间的相似性决定。有关如何计算 kNN 搜索分数的更多信息，请参阅"相似性"。

版本 8.0 中添加了对近似 kNN 搜索的支持。在此之前，"dense_vector"字段不支持在映射中启用"索引"。如果您在 8.0 之前创建了包含"dense_vector"字段的索引，则为了支持近似 kNN 搜索，必须使用设置"index： true"的新字段映射对数据重新编制索引。

#### 调整近似 kNN 以提高速度或准确性

为了收集结果，kNN 搜索 API 在每个分片上查找"num_candidates"个近似最近邻候选者。搜索计算这些候选向量与查询向量的相似性，从每个分片中选择"k"最相似的结果。然后，搜索合并每个分片的结果，以返回全局顶部"k"最近邻。

您可以增加"num_candidates"以获得更准确的结果，但代价是搜索速度较慢。具有高值"num_candidates"的搜索会考虑每个分片中的更多候选项。这需要更多时间，但搜索找到真正的"k"顶最近邻的概率更高。

同样，您可以减少"num_candidates"，以加快搜索速度，结果可能不太准确。

#### 使用字节向量的近似 kNN

近似 kNN 搜索 API 除了支持"浮点"值向量外，还支持"字节"值向量。使用"knn"选项搜索"dense_vector"字段，并将"element_type"设置为"字节"并启用索引。

1. 显式映射一个或多个"dense_vector"字段，并将"element_type"设置为"字节"并启用索引。           响应 = client.indices.create( index： 'byte-image-index'， body： { mappings： { properties： { "byte-image-vector"： { type： 'dense_vector'， element_type： 'byte'， dims： 2， index： true， similarity： 'cosine' }， title： { type： 'text' } } } } ) put response PUT byte-image-index { "mappings"： {       "属性"： { "字节图像矢量"： { "类型"： "dense_vector"， "element_type"： "字节"， "暗淡"： 2， "索引"： 真， "相似性"： "余弦" }， "标题"： { "类型"： "文本" } } }

2. 索引数据，确保所有向量值都是 [-128， 127] 范围内的整数。           响应 = client.bulk( index： 'byte-image-index'， refresh： true， body： [ { index： { _id： '1' } }， { "byte-image-vector"： [ 5， -20 ]， title： 'Moose Family' }， { index： { _id： '2' } }， { "byte-image-vector"： [ 8， -15 ]， title： 'Alpine Lake' }， { index： {           _id： '3' } }， { "byte-image-vector"： [ 11， 23 ]， title： 'Full moon' } ] ) 把响应 POST byte-image-index/_bulk？refresh=true { "index"： { "_id"： "1" } } { "byte-image-vector"： [5， -20]， "title"： "Moose Family" } { "index"： { "_id"： "2" } } { "byte-image-vector"： [8， -15]， "title"： "Alpine Lake" } { "index"： { "_id"： "3" } } { "byte-image-vector"： [11， 23]， "title"： "满月" }

3. 使用"knn"选项运行搜索，确保"query_vector"值是 [-128， 127] 范围内的整数。           响应 = client.search( index： 'byte-image-index'， body： { knn： { field： 'byte-image-vector'， query_vector： [ -5， 9 ]， k： 10， num_candidates： 100 }， fields： [ 'title' ] } ) put response POST byte-image-index/_search { "knn"： { "field"： "byte-image-vector"， "query_vector"： [-5， 9]， "k"： 10， "num_candidates"： 100 }，     "字段"： [ "标题" ] }

#### Filter kNNsearch

kNN 搜索 API 支持使用过滤器限制搜索。搜索将返回与筛选器查询匹配的顶部"k"文档。

以下请求执行按"文件类型"字段过滤的近似 kNN 搜索：

    
    
    response = client.search(
      index: 'image-index',
      body: {
        knn: {
          field: 'image-vector',
          query_vector: [
            54,
            10,
            -2
          ],
          k: 5,
          num_candidates: 50,
          filter: {
            term: {
              "file-type": 'png'
            }
          }
        },
        fields: [
          'title'
        ],
        _source: false
      }
    )
    puts response
    
    
    POST image-index/_search
    {
      "knn": {
        "field": "image-vector",
        "query_vector": [54, 10, -2],
        "k": 5,
        "num_candidates": 50,
        "filter": {
          "term": {
            "file-type": "png"
          }
        }
      },
      "fields": ["title"],
      "_source": false
    }

过滤器在近似 kNN 搜索期间应用，以确保返回"k"匹配文档。这与后过滤方法形成鲜明对比，在后过滤方法中，过滤器在近似kNN搜索完成后**应用。后筛选的缺点是，即使有足够的匹配文档，它有时返回的结果也少于 k 个。

#### 将近似 kNN 与其他特征相结合

您可以通过同时提供"knn"选项和"查询"来执行_hybrid retrieval_：

    
    
    response = client.search(
      index: 'image-index',
      body: {
        query: {
          match: {
            title: {
              query: 'mountain lake',
              boost: 0.9
            }
          }
        },
        knn: {
          field: 'image-vector',
          query_vector: [
            54,
            10,
            -2
          ],
          k: 5,
          num_candidates: 50,
          boost: 0.1
        },
        size: 10
      }
    )
    puts response
    
    
    POST image-index/_search
    {
      "query": {
        "match": {
          "title": {
            "query": "mountain lake",
            "boost": 0.9
          }
        }
      },
      "knn": {
        "field": "image-vector",
        "query_vector": [54, 10, -2],
        "k": 5,
        "num_candidates": 50,
        "boost": 0.1
      },
      "size": 10
    }

此搜索查找全局前 'k = 5' 向量匹配项，将它们与 'match' 查询中的匹配项组合在一起，最后返回 10 个得分最高的结果。"knn"和"query"匹配通过析取组合在一起，就像你在它们之间取了一个布尔_or_一样。顶部的"k"向量结果表示所有索引分片中的全局最近邻。

每次命中的分数是"knn"和"查询"分数的总和。您可以指定一个"提升"值，为总和中的每个分数赋予权重。在上面的示例中，分数将计算为

    
    
    score = 0.9 * match_score + 0.1 * knn_score

"knn"选项也可以与"聚合"一起使用。通常，Elasticsearch 会计算与搜索匹配的所有文档的聚合。因此，对于近似的 kNN搜索，聚合是在前"k"个最近的文档上计算的。如果搜索还包括"查询"，则根据"knn"和"query"匹配的组合集计算聚合。

#### 执行语义搜索

kNN 搜索使您能够使用以前部署的文本嵌入模型执行语义搜索。语义搜索不是对搜索词进行文字匹配，而是根据搜索查询的意图和上下文含义检索结果。

在后台，文本嵌入 NLP 模型从您提供的名为"model_text"的输入查询字符串生成一个密集向量。然后，根据包含使用相同文本嵌入机器学习模型创建的密集向量的索引对其进行搜索。搜索结果在语义上与模型学习的相似。

执行语义搜索：

* 您需要一个包含要搜索的输入数据的密集向量表示的索引， * 您必须使用与从输入数据创建密集向量相同的文本嵌入模型进行搜索， * 必须启动文本嵌入 NLP 模型部署。

在"query_vector_builder"对象中引用已部署的文本嵌入模型或模型部署，并将搜索查询提供为"model_text"：

    
    
    (...)
    {
      "knn": {
        "field": "dense-vector-field",
        "k": 10,
        "num_candidates": 100,
        "query_vector_builder": {
          "text_embedding": { __"model_id": "my-text-embedding-model", __"model_text": "The opposite of blue" __}
        }
      }
    }
    (...)

__

|

要执行的自然语言处理任务。它必须是"text_embedding"。   ---|---    __

|

用于从查询字符串生成密集向量的文本嵌入模型的 ID。使用从搜索索引中的输入文本生成嵌入的相同模型。您可以在"model_id"参数中使用"deployment_id"的值。   __

|

模型从中生成密集矢量表示的查询字符串。   有关如何部署经过训练的模型并使用它来创建文本嵌入的详细信息，请参阅此端到端示例。

#### 搜索多个 kNNn 字段

除了_hybrid retrieval_，您还可以一次搜索多个kNN向量场：

    
    
    response = client.search(
      index: 'image-index',
      body: {
        query: {
          match: {
            title: {
              query: 'mountain lake',
              boost: 0.9
            }
          }
        },
        knn: [
          {
            field: 'image-vector',
            query_vector: [
              54,
              10,
              -2
            ],
            k: 5,
            num_candidates: 50,
            boost: 0.1
          },
          {
            field: 'title-vector',
            query_vector: [
              1,
              20,
              -52,
              23,
              10
            ],
            k: 10,
            num_candidates: 10,
            boost: 0.5
          }
        ],
        size: 10
      }
    )
    puts response
    
    
    POST image-index/_search
    {
      "query": {
        "match": {
          "title": {
            "query": "mountain lake",
            "boost": 0.9
          }
        }
      },
      "knn": [ {
        "field": "image-vector",
        "query_vector": [54, 10, -2],
        "k": 5,
        "num_candidates": 50,
        "boost": 0.1
      },
      {
        "field": "title-vector",
        "query_vector": [1, 20, -52, 23, 10],
        "k": 10,
        "num_candidates": 10,
        "boost": 0.5
      }],
      "size": 10
    }

此搜索查找"图像矢量"的全局顶部"k = 5"向量匹配项和"标题向量"的全局"k = 10"。然后将这些顶级值与"match"查询中的匹配项组合在一起，并返回前 10 个文档。多个"knn"条目和"查询"匹配项通过分离组合在一起，就好像您在它们之间取了一个布尔 _or_ 一样。顶部的"k"向量结果表示所有索引分片中的全局最近邻。

具有上述配置提升的文档的评分为：

    
    
    score = 0.9 * match_score + 0.1 * knn_score_image-vector + 0.5 * knn_score_title-vector

#### 搜索具有预期相似性的 kNN

虽然 kNN 是一个强大的工具，但它总是试图返回"k"最近的邻居。因此，当将"knn"与"过滤器"一起使用时，您可以过滤掉所有相关文档，只剩下不相关的文档进行搜索。在这种情况下，"knn"仍将尽力返回"k"最近的邻居，即使这些邻居在向量空间中可能很远。

为了减轻这种担忧，在"knn"子句中有一个"相似性"参数。此值是将向量视为匹配所需的最小相似性。具有此参数的"knn"搜索流如下所示：

* 应用任何用户提供的"过滤器"查询 * 探索向量空间以获得"k"向量 * 不要返回任何比配置的"相似性"更远的向量

下面是一个示例。在这个例子中，我们搜索给定的'query_vector'作为'k'最近的邻居。但是，应用了"过滤器"并要求找到的向量至少具有它们之间提供的"相似性"。

    
    
    response = client.search(
      index: 'image-index',
      body: {
        knn: {
          field: 'image-vector',
          query_vector: [
            1,
            5,
            -20
          ],
          k: 5,
          num_candidates: 50,
          similarity: 36,
          filter: {
            term: {
              "file-type": 'png'
            }
          }
        },
        fields: [
          'title'
        ],
        _source: false
      }
    )
    puts response
    
    
    POST image-index/_search
    {
      "knn": {
        "field": "image-vector",
        "query_vector": [1, 5, -20],
        "k": 5,
        "num_candidates": 50,
        "similarity": 36,
        "filter": {
          "term": {
            "file-type": "png"
          }
        }
      },
      "fields": ["title"],
      "_source": false
    }

在我们的数据集中，唯一文件类型为"png"的文档的向量为"[42， 8， -15]"。"[42， 8， -15]" 和 '[1， 5，-20]' 之间的"l2_norm"距离为 '41.412'，大于配置的相似性 '36'。这意味着，此搜索不会返回任何命中。

#### 索引注意事项

对于近似的kNN搜索，Elasticsearch将每个段的密集向量值存储为HNSW图。用于近似 kNN 搜索的索引向量可能需要大量时间，因为构建这些图的成本很高。您可能需要增加索引和批量请求的客户端请求超时。近似 kNN 调优指南包含有关索引性能以及索引配置如何影响搜索性能的重要指导。

除了搜索时间调整参数外，HNSW 算法还具有索引时间参数，这些参数在构建图形的成本、搜索速度和准确性之间进行权衡。设置"dense_vector"映射时，可以使用"index_options"参数来调整这些参数：

    
    
    response = client.indices.create(
      index: 'image-index',
      body: {
        mappings: {
          properties: {
            "image-vector": {
              type: 'dense_vector',
              dims: 3,
              index: true,
              similarity: 'l2_norm',
              index_options: {
                type: 'hnsw',
                m: 32,
                ef_construction: 100
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT image-index
    {
      "mappings": {
        "properties": {
          "image-vector": {
            "type": "dense_vector",
            "dims": 3,
            "index": true,
            "similarity": "l2_norm",
            "index_options": {
              "type": "hnsw",
              "m": 32,
              "ef_construction": 100
            }
          }
        }
      }
    }

#### 近似 kNNsearch 的限制

* 您无法对"嵌套"映射中的"dense_vector"字段运行近似 kNN 搜索。  * 在跨集群搜索中使用 kNN 搜索时，不支持"ccs_minimize_roundtrips"选项。  Elasticsearch使用HNSW算法来支持高效的kNN搜索。与大多数 kNN 算法一样，HNSW 是一种近似方法，它牺牲了结果的准确性以提高搜索速度。这意味着返回的结果并不总是真正的 _k_ 最近邻。

近似 kNN 搜索始终使用"dfs_query_then_fetch"搜索类型，以便跨分片收集全局顶级"k"匹配项。运行 kNN 搜索时，无法显式设置"search_type"。

### ExactkNN

要运行精确的 kNN 搜索，请使用带有向量函数的"script_score"查询。

1. 显式映射一个或多个"dense_vector"字段。如果您不打算将该字段用于近似 kNN，请省略"索引"映射选项或将其设置为"false"。这可以显著提高索引速度。           响应 = client.index.create( index： 'product-index'， body： { mappings： { properties： { "product-vector"： { type： 'dense_vector'， dims： 5， index： false }， price： { type： 'long' } } } } ) put response PUT product-index { "mappings"： { "properties"： { "product-vector"： { "type"： "dense_vector"，           "dims"： 5， "index"： false }， "price"： { "type"： "long" } } } }

2. 为数据编制索引。           POST product-index/_bulk？refresh=true { "index"： { "_id"： "1" } } { "product-vector"： [230.0， 300.33， -34.8988， 15.555， -200.0]， "price"： 1599 } { "index"： { "_id"： "2" } } { "product-vector"： [-0.5， 100.0， -13.0， 14.8， -156.0]， "price"： 799 } { "index"： { "_id"： "3" } } { "product-vector"： [0.5， 111.3， -13.0， 14.8， -156.0]， "price"： 1099 } ...

3. 使用搜索 API 运行包含向量函数的"script_score"查询。

要限制传递给矢量函数的匹配文档数，我们建议您在"script_score.query"参数中指定筛选器查询。如果需要，您可以在此参数中使用"match_all"查询来匹配所有文档。但是，匹配所有文档可能会显著增加搜索延迟。

    
        response = client.search(
      index: 'product-index',
      body: {
        query: {
          script_score: {
            query: {
              bool: {
                filter: {
                  range: {
                    price: {
                      gte: 1000
                    }
                  }
                }
              }
            },
            script: {
              source: "cosineSimilarity(params.queryVector, 'product-vector') + 1.0",
              params: {
                "queryVector": [
                  -0.5,
                  90,
                  -10,
                  14.8,
                  -156
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
        POST product-index/_search
    {
      "query": {
        "script_score": {
          "query" : {
            "bool" : {
              "filter" : {
                "range" : {
                  "price" : {
                    "gte": 1000
                  }
                }
              }
            }
          },
          "script": {
            "source": "cosineSimilarity(params.queryVector, 'product-vector') + 1.0",
            "params": {
              "queryVector": [-0.5, 90.0, -10, 14.8, -156.0]
            }
          }
        }
      }
    }

[« Sort search results](sort-search-results.md) [Semantic search
»](semantic-search.md)
