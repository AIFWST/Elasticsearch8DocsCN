

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md)

[« Find structure API](find-structure.md) [Index APIs »](indices.md)

## 图探索API

图形探索 API 使您能够提取和汇总有关 Elasticsearch 数据流或索引中的文档和术语的信息。

了解此 API 行为的最简单方法是使用图形 UI 来浏览连接。您可以从"**上次请求**"面板查看提交到"_explore"终结点的最新请求。有关更多信息，请参阅图形入门。

有关使用探索 API 的其他信息，请参阅 Graph 故障排除和限制主题。

默认情况下，图形探索 API 处于启用状态。要禁用对 graphexplore API 和 Kibana Graph UI 的访问，请将"xpack.graph.enabled： false"添加到"elasticsearch.yml"。

###Request

"发布<target>/_graph/探索"

###Description

对"_explore"API 的初始请求包含一个种子查询，该查询标识感兴趣的文档并指定定义要包含在图形中的顶点和连接的字段。后续的"_explore"请求使您能够从另一个感兴趣的顶点_spider out_。您可以排除已返回的折点。

### 请求正文

query

    

标识相关文档的种子查询。可以是任何有效的弹性搜索查询。例如：

    
    
    "query": {
      "bool": {
        "must": {
          "match": {
            "query.raw": "midi"
          }
        },
        "filter": [
          {
            "range": {
              "query_time": {
                "gte": "2015-10-01 00:00:00"
              }
            }
          }
        ]
      }
    }

vertices

    

指定一个或多个字段，这些字段包含要作为顶点包含在图表中的术语。例如：

    
    
    "vertices": [
      {
        "field": "product"
        }
    ]

"顶点"的属性

field

     Identifies a field in the documents of interest. 
include

     Identifies the terms of interest that form the starting points from which you want to spider out. You do not have to specify a seed query if you specify an include clause. The include clause implicitly queries for documents that contain any of the listed terms listed. In addition to specifying a simple array of strings, you can also pass objects with `term` and `boost` values to boost matches on particular terms. 
exclude

     The `exclude` clause prevents the specified terms from being included in the results. 
size

     Specifies the maximum number of vertex terms returned for each field. Defaults to 5. 
min_doc_count

     Specifies how many documents must contain a pair of terms before it is considered to be a useful connection. This setting acts as a certainty threshold. Defaults to 3. 
shard_min_doc_count

     This advanced setting controls how many documents on a particular shard have to contain a pair of terms before the connection is returned for global consideration. Defaults to 2. 

connections

    

指定要从中提取与指定折点关联的项的一个或多个字段。例如：

    
    
    "connections": {  __"vertices": [
        {
          "field": "query.raw"
        }
      ]
    }

连接可以嵌套在"连接"对象中，以探索数据中的其他关系。每个嵌套级别都被认为是a_hop_的，图中的邻近性通常用_hopdepth_来描述。

"连接"的属性

query

     An optional _guiding query_ that constrains the Graph API as it explores connected terms. For example, you might want to direct the Graph API to ignore older data by specifying a query that identifies recent documents. 
vertices

    

包含您感兴趣的字段。例如：

    
    
    "vertices": [
      {
        "field": "query.raw",
        "size": 5,
        "min_doc_count": 10,
        "shard_min_doc_count": 3
      }
    ]

controls

    

指导图形 API 如何构建图形。

"控件"的属性

use_significance

     The `use_significance` flag filters associated terms so only those that are significantly associated with your query are included. For information about the algorithm used to calculate significance, see the [significant_terms aggregation](/guide/en/elasticsearch/reference/8.9/search-aggregations-bucket-significantterms-aggregation.html). Defaults to `true`. 
sample_size

     Each _hop_ considers a sample of the best-matching documents on each shard. Using samples improves the speed of execution and keeps exploration focused on meaningfully-connected terms. Very small values (less than 50) might not provide sufficient weight-of-evidence to identify significant connections between terms. Very large sample sizes can dilute the quality of the results and increase execution times. Defaults to 100 documents. 
timeout

     The length of time in milliseconds after which exploration will be halted and the results gathered so far are returned. This timeout is honored on a best-effort basis. Execution might overrun this timeout if, for example, a long pause is encountered while FieldData is loaded for a field. 
sample_diversity

    

为了避免顶级匹配文档样本由单一结果源主导，有时需要请求样本中的多样性。为此，您可以选择单值字段，并为该字段设置每个值的最大文档数。例如：

    
    
    "sample_diversity": {
      "field": "category.raw",
      "max_docs_per_value": 500
    }

###Examples

#### 基础探索

初始搜索通常从查询开始，以识别强相关的术语。

    
    
    POST clicklogs/_graph/explore
    {
      "query": {                  __"match": {
          "query.raw": "midi"
        }
      },
      "vertices": [ __{
          "field": "product"
        }
      ],
      "connections": { __"vertices": [
          {
            "field": "query.raw"
          }
        ]
      }
    }

__

|

使用查询为探索设定种子。此示例正在搜索搜索术语"midi"的用户的点击日志。   ---|---    __

|

标识要包含在图形中的顶点。此示例查找与搜索"midi"显著关联的产品代码。   __

|

找到连接。此示例查找引导用户单击与搜索"midi"关联的产品的其他搜索词。   来自探索 API 的响应如下所示：

    
    
    {
       "took": 0,
       "timed_out": false,
       "failures": [],
       "vertices": [ __{
             "field": "query.raw",
             "term": "midi cable",
             "weight": 0.08745858139552132,
             "depth": 1
          },
          {
             "field": "product",
             "term": "8567446",
             "weight": 0.13247784285434397,
             "depth": 0
          },
          {
             "field": "product",
             "term": "1112375",
             "weight": 0.018600718471158982,
             "depth": 0
          },
          {
             "field": "query.raw",
             "term": "midi keyboard",
             "weight": 0.04802242866755111,
             "depth": 1
          }
       ],
       "connections": [ __{
             "source": 0,
             "target": 1,
             "weight": 0.04802242866755111,
             "doc_count": 13
          },
          {
             "source": 2,
             "target": 3,
             "weight": 0.08120623870976627,
             "doc_count": 23
          }
       ]
    }

__

|

已发现的所有顶点的数组。顶点是索引术语，因此提供了字段和术语值。"权重"属性指定显著性分数。"depth"属性指定首次遇到该术语的跃点级别。   ---|---    __

|

数组中顶点之间的连接。"源"和"目标"属性被索引到顶点数组中，并指示哪个顶点在探索过程中被命名为另一个顶点。"doc_count"值指示样本集中有多少文档包含此术语对(这不是数据流或索引中所有文档的全局计数)。   #### 可选控件编辑

默认设置配置为删除嘈杂数据并从数据中获取"大局"。此示例演示如何指定其他参数以影响图形的构建方式。

有关调整设置以进行更详细的取证评估的提示，其中每个文档都可能感兴趣，请参阅故障排除指南。

    
    
    POST clicklogs/_graph/explore
    {
      "query": {
        "match": {
          "query.raw": "midi"
        }
      },
      "controls": {
        "use_significance": false,        __"sample_size": 2000, __"timeout": 2000, __"sample_diversity": { __"field": "category.raw",
          "max_docs_per_value": 500
        }
      },
      "vertices": [
        {
          "field": "product",
          "size": 5, __"min_doc_count": 10, __"shard_min_doc_count": 3 __}
      ],
      "connections": {
        "query": { __"bool": {
            "filter": [
              {
                "range": {
                  "query_time": {
                    "gte": "2015-10-01 00:00:00"
                  }
                }
              }
            ]
          }
        },
        "vertices": [
          {
            "field": "query.raw",
            "size": 5,
            "min_doc_count": 10,
            "shard_min_doc_count": 3
          }
        ]
      }
    }

__

|

禁用"use_significance"以包含所有关联的术语，而不仅仅是与查询显著关联的术语。   ---|---    __

|

增加样本大小以考虑每个分片上的一组更大的文档。   __

|

限制图形请求在返回结果之前运行的时间。   __

|

通过对特定单值字段(如类别字段)中每个值的文档数设置限制，确保样本的多样性。   __

|

控制为每个字段返回的最大顶点项数。   __

|

设置一个确定性阈值，指定在我们认为它是有用的连接之前，必须包含一对术语的文档数量。   __

|

指定在返回连接以供全局考虑之前，分片上必须包含一对术语的文档数。   __

|

限制在浏览相关术语时考虑哪些文档。   #### 爬取操作编辑

初始搜索后，您通常希望选择感兴趣的折点，并查看连接了哪些其他折点。用图形术语来说，此操作称为"爬虫"。通过提交一系列请求，您可以逐步构建相关信息的图表。

要爬出，您需要指定两件事：

* 要为其查找其他连接的顶点集 * 您已经知道的要从爬取操作结果中排除的顶点集。

您可以使用"包含"和"排除"子句指定此信息。例如，以下请求以产品"1854873"和 spidersout 开头，以查找与该产品关联的其他搜索词。术语"midi"、"midi 键盘"和"合成器"从结果中排除。

    
    
    POST clicklogs/_graph/explore
    {
       "vertices": [
          {
             "field": "product",
             "include": [ "1854873" ] __}
       ],
       "connections": {
          "vertices": [
             {
                "field": "query.raw",
                "exclude": [ __"midi keyboard",
                   "midi",
                   "synth"
                ]
             }
          ]
       }
    }

__

|

要从中开始的顶点在"include"子句中指定为项数组。   ---|---    __

|

"排除"子句可防止您已经知道的术语包含在结果中。   « 查找结构 API 索引 API »