

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Search your
data](search-your-data.md) ›[Semantic search](semantic-search.md)

[« Semantic search](semantic-search.md) [Query DSL »](query-dsl.md)

## 教程：使用 ELSER 进行语义搜索

Elastic Learned Sparse EncodeR (或 ELSER )是由 Elastic 训练的 NLP 模型，使您能够使用稀疏向量表示来执行语义搜索。语义搜索不是对搜索词进行文字匹配，而是根据搜索查询的意图和上下文含义检索结果。

本教程中的说明介绍如何使用 ELSER 对数据执行语义搜索。

在使用 ELSER v1 进行语义搜索期间，仅考虑每个字段的前 512 个提取标记。有关详细信息，请参阅此页面。

####Requirements

要使用 ELSER 执行语义搜索，必须在群集中部署 NLP 模型。请参阅 ELSER文档，了解如何下载和部署模型。

如果部署自动缩放已关闭，则在 Elasticsearch Service 中，用于部署和使用 ELSER 模型的最小专用 ML 节点大小为 4 GB。建议启用自动缩放，因为它允许部署根据需求动态调整资源。通过使用更多分配或每个分配的更多线程可以实现更好的性能，这需要更大的 ML 节点。自动缩放在需要时提供更大的节点。如果自动缩放已关闭，则必须自行提供适当大小的节点。

#### 创建索引映射

首先，必须创建目标索引(包含模型基于文本创建的令牌的索引)的映射。目标索引必须具有具有"rank_features"字段类型的字段才能为 ELSER输出编制索引。

ELSER 输出必须摄取到字段类型为"rank_features"的字段中。否则，Elasticsearch 会将令牌权重对解释为文档中的大量字段。如果您收到类似于以下内容的错误"添加新字段时超出了总计字段 [1000] 的限制"，则 ELSERoutput 字段未正确映射，并且其字段类型不同于"rank_features"。

    
    
    PUT my-index
    {
      "mappings": {
        "properties": {
          "ml.tokens": { __"type": "rank_features" __},
          "text": { __"type": "text" __}
        }
      }
    }

__

|

包含生成的令牌的字段的名称。   ---|---    __

|

包含令牌的字段是"rank_features"字段。   __

|

要从中创建稀疏矢量表示的字段的名称。在此示例中，字段的名称为"text"。   __

|

在此示例中为文本的字段类型。   若要了解如何优化空间，请参阅通过从文档源中排除 ELSER 令牌来节省磁盘空间部分。

#### 使用推理处理器创建采集管道

使用推理处理器创建引入管道，以使用 ELSER 对管道中摄取的数据进行推理。

    
    
    PUT _ingest/pipeline/elser-v1-test
    {
      "processors": [
        {
          "inference": {
            "model_id": ".elser_model_1",
            "target_field": "ml",
            "field_map": { __"text": "text_field"
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

"field_map"对象将输入文档字段名称(在此示例中为"文本")映射到模型所需的字段名称(始终为"text_field")。   ---|---    __

|

"text_expansion"推理类型需要在推理摄取处理器中使用。   #### 加载数据编辑

在此步骤中，您将加载稍后在推理摄取管道中使用的数据，以便从中提取令牌。

使用"msmarco-passagetest2019-top1000"数据集，该数据集是MS MARCO Passage Ranking数据集的子集。它由 200 个查询组成，每个查询都附有相关文本段落的列表。所有独特的段落及其ID都已从该数据集中提取并编译到atsv文件中。

下载文件并使用机器学习 UI 中的数据可视化工具将其上传到群集。将名称"id"分配给第一列，将名称"text"分配给第二列。索引名称为"测试数据"。上传完成后，您可以看到一个名为"test-data"的索引，其中包含 182469 个文档。

#### 通过推理摄取管道摄取数据

通过使用 ELSER 作为推理模型的推理管道重新索引数据，从文本创建令牌。

    
    
    POST _reindex?wait_for_completion=false
    {
      "source": {
        "index": "test-data",
        "size": 50 __},
      "dest": {
        "index": "my-index",
        "pipeline": "elser-v1-test"
      }
    }

__

|

重新编制索引的默认批大小为 1000。将"大小"减小到较小的数字可以加快重新索引过程的更新，从而使您能够密切跟踪进度并及早发现错误。   ---|--- 调用返回任务 ID 以监视进度：

    
    
    GET _tasks/<task_id>

还可以打开"已训练的模型"UI，选择"ELSER"下的"管道"选项卡以跟踪进度。完成该过程可能需要几分钟。

#### 使用"text_expansion"查询进行语义搜索

若要执行语义搜索，请使用"text_expansion"查询，并提供查询文本和 ELSER 模型 ID。下面的示例使用查询文本"如何避免跑步后肌肉酸痛？"，"ml-tokens"字段包含生成的 ELSER 输出：

    
    
    GET my-index/_search
    {
       "query":{
          "text_expansion":{
             "ml.tokens":{
                "model_id":".elser_model_1",
                "model_text":"How to avoid muscle soreness after running?"
             }
          }
       }
    }

结果是"my-index"索引中含义最接近查询文本的前 10 个文档，这些文档按其相关性排序。结果还包含每个相关搜索结果的提取令牌及其权重。

    
    
    "hits":[
       {
          "_index":"my-index",
          "_id":"978UAYgBKCQMet06sLEy",
          "_score":18.612831,
          "_ignored":[
             "text.keyword"
          ],
          "_source":{
             "id":7361587,
             "text":"For example, if you go for a run, you will mostly use the muscles in your lower body. Give yourself 2 days to rest those muscles so they have a chance to heal before you exercise them again. Not giving your muscles enough time to rest can cause muscle damage, rather than muscle development.",
             "ml":{
                "tokens":{
                   "muscular":0.075696334,
                   "mostly":0.52380747,
                   "practice":0.23430172,
                   "rehab":0.3673556,
                   "cycling":0.13947526,
                   "your":0.35725075,
                   "years":0.69484913,
                   "soon":0.005317828,
                   "leg":0.41748235,
                   "fatigue":0.3157955,
                   "rehabilitation":0.13636169,
                   "muscles":1.302141,
                   "exercises":0.36694175,
                   (...)
                },
                "model_id":".elser_model_1"
             }
          }
       },
       (...)
    ]

要了解如何优化"text_expansion"查询，请参阅优化text_expansion查询的搜索效果。

#### 将语义搜索与其他查询相结合

您可以将"text_expansion"与复合查询中的其他查询结合使用。例如，在布尔值中使用过滤器子句或全文查询，该查询可能会也可能不会使用与"text_expansion"查询相同的查询文本。这使您能够合并来自两个查询的搜索结果。

来自"text_expansion"查询的搜索命中率往往高于另一个 Elasticsearch 查询。通过使用"boost"参数增加或减少每个查询的相关性分数，可以对这些分数进行正则化。在"text_expansion"查询的回想度可能很高，其中有一条长尾的不相关结果。使用"min_score"参数修剪那些不太相关的文档。

    
    
    GET my-index/_search
    {
      "query": {
        "bool": { __"should": [
            {
              "text_expansion": {
                "ml.tokens": {
                  "model_text": "How to avoid muscle soreness after running?",
                  "model_id": ".elser_model_1",
                  "boost": 1 __}
              }
            },
            {
              "query_string": {
                "query": "toxins",
                "boost": 4 __}
            }
          ]
        }
      },
      "min_score": 10 __}

__

|

"text_expansion"和"query_string"查询都在"bool"查询的"should"子句中。   ---|---    __

|

对于默认值，"text_expansion"查询的"提升"值为"1"。这意味着不会提高此查询结果的相关度分数。   __

|

对于"query_string"查询，"boost"值为"4"。此查询结果的相关性分数增加，导致它们在搜索结果中的排名更高。   __

|

仅显示分数等于或高于"10"的结果。   ### 优化性能编辑

#### 通过从文档源中排除 ELSER 令牌来节省磁盘空间

ELSER 生成的令牌必须编制索引才能在text_expansionquery中使用。但是，没有必要在文档源中保留这些术语。通过使用源排除映射从文档源中删除 ELSER 术语，可以节省磁盘空间。

重新索引使用文档源填充目标索引。一旦从源中排除了 ELSER 术语，就无法通过重新索引来恢复这些术语。从源中排除令牌是一种节省空间的优化，仅当您确定将来不需要重新索引时才应应用！请务必仔细考虑这种权衡，并确保从源中排除 ELSER 术语符合您的特定要求和用例。

从"_source"字段中排除"ml.tokens"的映射可以通过以下 API 调用创建：

    
    
    PUT my-index
    {
      "mappings": {
        "_source": {
          "excludes": [
            "ml.tokens"
          ]
        },
        "properties": {
          "ml.tokens": {
            "type": "rank_features"
          },
          "text": {
            "type": "text"
          }
        }
      }
    }

#### 延伸阅读

* 如何下载和部署 ELSER * ELSER v1 限制 * 改进 Elastic 堆栈中的信息检索：引入我们的新检索模型 Elastic Learned 稀疏编码器

[« Semantic search](semantic-search.md) [Query DSL »](query-dsl.md)
