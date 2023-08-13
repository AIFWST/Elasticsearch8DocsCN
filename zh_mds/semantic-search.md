

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Search your
data](search-your-data.md)

[« k-nearest neighbor (kNN) search](knn-search.md) [Tutorial: semantic
search with ELSER »](semantic-search-elser.md)

## 语义搜索

语义搜索是一种搜索方法，可帮助您根据搜索查询的意图和上下文含义查找数据，而不是查询词的匹配(词法搜索)。

Elasticsearch使用自然语言处理(NLP)和矢量搜索提供语义搜索功能。将 NLP 模型部署到 Elasticsearch 使其能够从文本中提取文本嵌入。嵌入是提供文本数字表示形式的向量。具有相似含义的内容片段具有相似的表示形式。

!编码文本概念作为向量的简化表示

图6.编码文本概念作为向量的简化表示

在查询时，Elasticsearch 可以使用相同的 NLP 模型将查询转换为嵌入，使您能够查找具有类似文本嵌入的文档。

本指南向您展示如何使用 Elasticsearch 实现语义搜索，从选择 NLP 模型到编写查询。

### 选择自然语言处理模型

Elasticsearch提供了广泛的NLP模型的使用，包括密集和稀疏矢量模型。语言模型的选择对于成功实现语义搜索至关重要。

虽然可以引入自己的文本嵌入模型，但通过模型调整获得良好的搜索结果具有挑战性。从我们的第三方模型列表中选择合适的模型是第一步。使用您自己的数据训练模型对于确保比仅使用 BM25 更好的搜索结果至关重要。但是，模型训练过程需要数据科学家和 ML 专家团队，因此成本高昂且耗时。

为了解决这个问题，Elastic 提供了一个预先训练的表征模型，称为 Elastic Learned Sparse EncodeR (ELSER)。ELSER，目前仅适用于英语，是一种不需要微调的域外稀疏向量模型。这种适应性使其适用于开箱即用的各种 NLP 用例。除非您有 ML 专家团队，否则强烈建议使用 ELSER 模型。

在稀疏向量表示的情况下，向量主要由零值组成，只有一小部分包含非零值。此表示形式通常用于文本数据。在 ELSER 的情况下，索引中的每个文档和查询文本本身都由高维稀疏向量表示。向量的每个非零元素对应于模型词汇表中的一个项。ELSER 词汇表包含大约 30000 个术语，因此 ELSER 创建的稀疏向量包含大约 30000 个值，其中大部分为零。实际上，ELSER 模型正在将原始查询中的术语替换为已学习到存在于文档中的其他术语，这些术语与训练数据集中的原始搜索词最匹配，并加权以控制每个术语的重要性。

### 部署模型

确定要用于实现语义搜索的模型后，需要在 Elasticsearch 中部署模型。

埃尔瑟密集矢量模型

要部署 ELSER，请参阅下载并部署 ELSER。

要部署第三方文本嵌入模型，请参阅部署文本嵌入模型。

### 映射文本嵌入的字段

在开始使用已部署的模型基于输入文本生成嵌入之前，需要先准备索引映射。索引的映射取决于模型的类型。

埃尔瑟密集矢量模型

ELSER 生成令牌权重对作为输入文本和查询的输出。Elasticsearch 'rank_features' 字段类型可以将这些令牌权重对存储为数字特征向量。索引必须具有"rank_features"字段类型的字段，才能为 ELSER 生成的令牌编制索引。

若要为 ELSER 索引创建映射，请参阅本教程的创建索引映射部分。该示例演示如何为"my-index"创建索引映射，该映射将"my_embeddings.tokens"字段(将包含 ELSER 输出)定义为"rank_features"字段。

    
    
    PUT my-index
    {
      "mappings": {
        "properties": {
          "my_embeddings.tokens": { __"type": "rank_features" __},
          "my_text_field": { __"type": "text" __}
        }
      }
    }

__

|

将包含 ELSER 生成的令牌的字段的名称。   ---|---    __

|

包含令牌的字段必须是"rank_features"字段。   __

|

要从中创建稀疏矢量表示的字段的名称。在此示例中，字段的名称为"my_text_field"。   __

|

在此示例中，字段类型为"文本"。   与Elasticsearch NLP兼容的模型生成密集向量作为输出。"dense_vector"字段类型适用于存储数值的密集向量。索引必须具有"dense_vector"字段类型的字段，才能为所选支持的第三方模型生成的嵌入编制索引。请记住，该模型生成具有一定数量维度的嵌入。"dense_vector"字段必须使用"dims"选项配置相同数量的维度。请参阅相应的模型文档以获取有关嵌入维度数的信息。

要查看 NLP 模型的索引映射，请参阅本教程的将文本嵌入模型添加到引入推理管道部分中的映射代码片段。该示例演示如何创建一个索引映射，该映射将"my_embeddings.predicted_value"字段(将包含模型输出)定义为"dense_vector"字段。

    
    
    PUT my-index
    {
      "mappings": {
        "properties": {
          "my_embeddings.predicted_value": { __"type": "dense_vector", __"dims": 384, __"index": true,
            "similarity": "cosine"
          },
          "my_text_field": { __"type": "text" __}
        }
      }
    }

__

|

将包含模型生成的嵌入的字段的名称。   ---|---    __

|

包含嵌入的字段必须是"dense_vector"字段。   __

|

该模型生成具有一定数量维度的嵌入。"dense_vector"字段必须通过"dims"选项配置相同数量的维度。请参阅相应的模型文档以获取有关嵌入维度数的信息。   __

|

要从中创建密集矢量表示的字段的名称。在此示例中，字段的名称为"my_text_field"。   __

|

在此示例中，字段类型为"文本"。   ### 生成文本嵌入编辑

为索引创建映射后，可以从输入文本生成文本嵌入。这可以通过将摄取管道与推理处理器结合使用来完成。引入管道处理输入数据并将其索引到目标索引中。在索引时，推理摄取处理器使用经过训练的模型来推理通过管道引入的数据。使用推理处理器创建摄取管道后，您可以通过它摄取数据以生成模型输出。

埃尔瑟密集矢量模型

以下是使用 ELSER 模型的引入管道的创建方式：

    
    
    PUT _ingest/pipeline/my-text-embeddings-pipeline
    {
      "description": "Text embedding pipeline",
      "processors": [
        {
          "inference": {
            "model_id": ".elser_model_1",
            "target_field": "my_embeddings",
            "field_map": { __"my_text_field": "text_field"
            },
            "inference_config": {
              "text_expansion": { __"results_field": "tokens"
              }
            }
          }
        }
      ]
    }

__

|

"field_map"对象将输入文档字段名称(在此示例中为"my_text_field")映射到模型期望的字段名称(始终为"text_field")。   ---|---    __

|

"text_expansion"推理类型需要在推理摄取处理器中使用。   要通过管道引入数据以使用 ELSER 生成令牌，请参阅本教程的通过推理引入管道引入数据部分。使用管道成功引入文档后，索引将包含 ELSER 生成的令牌。

以下是使用文本嵌入模型的摄取管道的创建方式：

    
    
    PUT _ingest/pipeline/my-text-embeddings-pipeline
    {
      "description": "Text embedding pipeline",
      "processors": [
        {
          "inference": {
            "model_id": "sentence-transformers__msmarco-minilm-l-12-v3", __"target_field": "my_embeddings",
            "field_map": { __"my_text_field": "text_field"
            }
          }
        }
      ]
    }

__

|

要使用的文本嵌入模型的模型 ID。   ---|---    __

|

"field_map"对象将输入文档字段名称(在此示例中为"my_text_field")映射到模型期望的字段名称(始终为"text_field")。   若要通过管道引入数据以使用所选模型生成文本嵌入，请参阅将文本嵌入模型添加到推理管道部分。该示例演示如何使用推理处理器创建管道，并通过管道重新索引数据。使用管道成功引入文档后，索引将包含模型生成的文本嵌入。

现在是时候执行语义搜索了！

### 搜索数据

根据已部署的模型类型，您可以使用文本扩展查询查询排名要素，也可以使用 kNN 搜索查询密集向量。

埃尔瑟密集矢量模型

可以使用文本扩展查询查询 ELSER 文本嵌入。文本扩展查询使您能够通过提供 NLP 模型的模型 ID 和查询文本来查询排名特征字段：

    
    
    GET my-index/_search
    {
       "query":{
          "text_expansion":{
             "my_embeddings.tokens":{ __"model_id":".elser_model_1",
                "model_text":"the query string"
             }
          }
       }
    }

__

|

类型为"rank_features"的字段。   ---|--- 密集向量模型生成的文本嵌入可以使用 kNNsearch 进行查询。在"knn"子句中，提供密集向量字段的名称，并提供包含模型 ID 和查询文本的"query_vector_builder"子句。

    
    
    GET my-index/_search
    {
      "knn": {
        "field": "my_embeddings.predicted_value",
        "k": 10,
        "num_candidates": 100,
        "query_vector_builder": {
          "text_embedding": {
            "model_id": "sentence-transformers__msmarco-minilm-l-12-v3",
            "model_text": "the query string"
          }
        }
      }
    }

### 使用混合搜索超越语义搜索

在某些情况下，词法搜索可能比语义搜索性能更好。例如，在搜索单个单词或 ID(如产品编号)时。

使用倒数排名融合将语义和词汇搜索组合到一个混合搜索请求中，可提供两全其美的效果。不仅如此，使用倒数秩融合的混合搜索已被证明总体上表现更好。

埃尔瑟密集矢量模型

语义查询和词法查询之间的混合搜索可以通过在搜索请求中使用"sub_searches"子句来实现。在"sub_searches"子句中，提供"text_expansion"查询和全文查询。在"sub_searches"子句旁边，还提供带有"rrf"参数的"rank"子句，以使用倒数融合对文档进行排名。

    
    
    GET my-index/_search
    {
      "sub_searches": [
        {
          "query": {
            "match": {
              "my_text_field": "the query string"
            }
          }
        },
        {
          "query": {
            "text_expansion": {
              "my_embeddings.tokens": {
                "model_id": ".elser_model_1",
                "model_text": "the query string"
              }
            }
          }
        }
      ],
      "rank": {
        "rrf": {}
      }
    }

语义查询和词法查询之间的混合搜索可以通过以下方式实现：

* 全文查询的"查询"子句;  * 带有 kNN 搜索的 'knn' 子句，用于查询密集向量场;  * 以及带有"RRF"参数的"rank"子句，用于使用倒数排名融合对文档进行排名。

    
    
    GET my-index/_search
    {
      "query": {
        "match": {
          "my_text_field": "the query string"
        }
      },
      "knn": {
        "field": "text_embedding.predicted_value",
        "k": 10,
        "num_candidates": 100,
        "query_vector_builder": {
          "text_embedding": {
            "model_id": "sentence-transformers__msmarco-minilm-l-12-v3",
            "model_text": "the query string"
          }
        }
      },
      "rank": {
        "rrf": {}
      }
    }

### 阅读更多

*教程：

    * [Semantic search with ELSER](semantic-search-elser.html "Tutorial: semantic search with ELSER")
    * [Semantic search with the msmarco-MiniLM-L-12-v3 sentence-transformer model](/guide/en/machine-learning/8.9/ml-nlp-text-emb-vector-search-example.html)

* 博客：

    * [Introducing Elastic Learned Sparse Encoder: Elastic's AI model for semantic search](/blog/may-2023-launch-sparse-encoder-ai-model)
    * [How to get the best of lexical and AI-powered search with Elastic's vector database](/blog/lexical-ai-powered-search-elastic-vector-database)
    * Information retrieval blog series:

      * [Part 1: Steps to improve search relevance](/blog/improving-information-retrieval-elastic-stack-search-relevance)
      * [Part 2: Benchmarking passage retrieval](/blog/improving-information-retrieval-elastic-stack-benchmarking-passage-retrieval)
      * [Part 3: Introducing Elastic Learned Sparse Encoder, our new retrieval model](/blog/may-2023-launch-information-retrieval-elasticsearch-ai-model)
      * [Part 4: Hybrid retrieval](/blog/improving-information-retrieval-elastic-stack-hybrid)

[« k-nearest neighbor (kNN) search](knn-search.md) [Tutorial: semantic
search with ELSER »](semantic-search-elser.md)
