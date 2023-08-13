

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Document APIs](docs.md)

[« Reindex API](docs-reindex.md) [Multi term vectors API »](docs-multi-
termvectors.md)

## 术语向量API

检索特定文档字段中术语的信息和统计信息。

    
    
    response = client.termvectors(
      index: 'my-index-000001',
      id: 1
    )
    puts response
    
    
    GET /my-index-000001/_termvectors/1

###Request

"获取/<index>/_termvectors/<_id>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则必须对目标索引或索引别名具有"读取"索引权限。

###Description

您可以检索存储在索引中的文档的术语向量，也可以检索请求正文中传递for_artificial_文档的术语向量。

您可以通过"fields"参数指定您感兴趣的字段，也可以通过将字段添加到请求正文来指定。

    
    
    response = client.termvectors(
      index: 'my-index-000001',
      id: 1,
      fields: 'message'
    )
    puts response
    
    
    GET /my-index-000001/_termvectors/1?fields=message

可以使用通配符指定字段，类似于多重匹配查询。

默认情况下，术语向量是实时的，而不是近实时的。这可以通过将"实时"参数设置为"false"来更改。

您可以请求三种类型的值：_term information_、_term statistics_and _field statistics_。默认情况下，将为所有字段返回所有术语信息和字段统计信息，但排除术语统计信息。

#### 术语信息

* 字段中的术语频率(始终返回) * 术语位置("位置"：真) * 开始和结束偏移量("偏移量"：真) * 术语有效负载("有效负载"：真)，作为 base64 编码字节

如果请求的信息未存储在索引中，则如果可能，将对其进行计算。此外，可以为索引中甚至不存在的文档计算术语向量，而是由用户提供。

开始和结束偏移假定正在使用 UTF-16 编码。如果要使用这些偏移量来获取生成此标记的原始文本，则应确保获取子字符串的字符串也使用 UTF-16 进行编码。

#### 术语统计

将"term_statistics"设置为"true"(默认值为"false")将返回

* 总术语频率(术语在所有文档中出现的频率)

* 文档频率(包含当前术语的文档数量)

默认情况下，不返回这些值，因为术语统计信息可能会对性能产生严重影响。

#### 字段统计

将"field_statistics"设置为"false"(默认值为"true")将省略：

* 文档计数(包含此字段的文档数) * 文档频率总和(此字段中所有术语的文档频率总和) * 总术语频率总和(此字段中每个术语的总术语频率之和)

#### 术语筛选

使用参数"filter"，返回的术语也可以根据其 tf-idf 分数进行过滤。这对于找出文档的良好特征向量可能很有用。此功能的工作方式与"更像此查询"的第二阶段类似。有关用法，请参阅示例 5。

支持以下子参数：

`max_num_terms`

|

每个字段必须返回的最大术语数。默认为"25"。   ---|--- "min_term_freq"

|

忽略源文档中频率低于此频率的单词。默认为"1"。   "max_term_freq"

|

忽略源文档中频率超过此频率的单词。 默认值为无界。   "min_doc_freq"

|

忽略至少在这么多文档中没有出现的术语。默认为"1"。   "max_doc_freq"

|

忽略在超过这么多文档中出现的单词。默认为无界。   "min_word_length"

|

将忽略的最小字长。默认为"0"。   "max_word_length"

|

将忽略单词的最大字长。默认值为无界 ('0')。   ###Behaviouredit

术语和字段统计信息不准确。删除的文档不考虑在内。仅检索所请求文档所在的分片的信息。因此，术语和字段统计仅作为相对度量有用，而绝对数字在这种情况下没有意义。默认情况下，当请求人工文档的术语向量时，会随机选择一个用于获取统计信息的分片。仅使用"路由"来命中特定的分片。

### 路径参数

`<index>`

     (Required, string) Name of the index that contains the document. 
`<_id>`

     (Optional, string) Unique identifier of the document. 

### 查询参数

`fields`

    

(可选，字符串)要包含在统计信息中的字段的逗号分隔列表或通配符表达式。

用作默认列表，除非在"completion_fields"或"fielddata_fields"参数中提供了特定的字段列表。

`field_statistics`

     (Optional, Boolean) If `true`, the response includes the document count, sum of document frequencies, and sum of total term frequencies. Defaults to `true`. 
`<offsets>`

     (Optional, Boolean) If `true`, the response includes term offsets. Defaults to `true`. 
`payloads`

     (Optional, Boolean) If `true`, the response includes term payloads. Defaults to `true`. 
`positions`

     (Optional, Boolean) If `true`, the response includes term positions. Defaults to `true`. 
`preference`

     (Optional, string) Specifies the node or shard the operation should be performed on. Random by default. 
`routing`

     (Optional, string) Custom value used to route operations to a specific shard. 
`realtime`

     (Optional, Boolean) If `true`, the request is real-time as opposed to near-real-time. Defaults to `true`. See [Realtime](docs-get.html#realtime "Realtime"). 
`term_statistics`

     (Optional, Boolean) If `true`, the response includes term frequency and document frequency. Defaults to `false`. 
`version`

     (Optional, Boolean) If `true`, returns the document version as part of a hit. 
`version_type`

     (Optional, enum) Specific version type: `external`, `external_gte`. 

###Examples

#### 返回存储的术语向量

首先，我们创建一个存储术语向量、有效负载等的索引。:

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            text: {
              type: 'text',
              term_vector: 'with_positions_offsets_payloads',
              store: true,
              analyzer: 'fulltext_analyzer'
            },
            fullname: {
              type: 'text',
              term_vector: 'with_positions_offsets_payloads',
              analyzer: 'fulltext_analyzer'
            }
          }
        },
        settings: {
          index: {
            number_of_shards: 1,
            number_of_replicas: 0
          },
          analysis: {
            analyzer: {
              fulltext_analyzer: {
                type: 'custom',
                tokenizer: 'whitespace',
                filter: [
                  'lowercase',
                  'type_as_payload'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001
    { "mappings": {
        "properties": {
          "text": {
            "type": "text",
            "term_vector": "with_positions_offsets_payloads",
            "store" : true,
            "analyzer" : "fulltext_analyzer"
           },
           "fullname": {
            "type": "text",
            "term_vector": "with_positions_offsets_payloads",
            "analyzer" : "fulltext_analyzer"
          }
        }
      },
      "settings" : {
        "index" : {
          "number_of_shards" : 1,
          "number_of_replicas" : 0
        },
        "analysis": {
          "analyzer": {
            "fulltext_analyzer": {
              "type": "custom",
              "tokenizer": "whitespace",
              "filter": [
                "lowercase",
                "type_as_payload"
              ]
            }
          }
        }
      }
    }

其次，我们添加一些文档：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        fullname: 'John Doe',
        text: 'test test test '
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      refresh: 'wait_for',
      body: {
        fullname: 'Jane Doe',
        text: 'Another test ...'
      }
    )
    puts response
    
    
    PUT /my-index-000001/_doc/1
    {
      "fullname" : "John Doe",
      "text" : "test test test "
    }
    
    PUT /my-index-000001/_doc/2?refresh=wait_for
    {
      "fullname" : "Jane Doe",
      "text" : "Another test ..."
    }

以下请求返回文档"1"(John Doe)中字段"text"的所有信息和统计信息：

    
    
    response = client.termvectors(
      index: 'my-index-000001',
      id: 1,
      body: {
        fields: [
          'text'
        ],
        offsets: true,
        payloads: true,
        positions: true,
        term_statistics: true,
        field_statistics: true
      }
    )
    puts response
    
    
    GET /my-index-000001/_termvectors/1
    {
      "fields" : ["text"],
      "offsets" : true,
      "payloads" : true,
      "positions" : true,
      "term_statistics" : true,
      "field_statistics" : true
    }

Response:

    
    
    {
      "_index": "my-index-000001",
      "_id": "1",
      "_version": 1,
      "found": true,
      "took": 6,
      "term_vectors": {
        "text": {
          "field_statistics": {
            "sum_doc_freq": 4,
            "doc_count": 2,
            "sum_ttf": 6
          },
          "terms": {
            "test": {
              "doc_freq": 2,
              "ttf": 4,
              "term_freq": 3,
              "tokens": [
                {
                  "position": 0,
                  "start_offset": 0,
                  "end_offset": 4,
                  "payload": "d29yZA=="
                },
                {
                  "position": 1,
                  "start_offset": 5,
                  "end_offset": 9,
                  "payload": "d29yZA=="
                },
                {
                  "position": 2,
                  "start_offset": 10,
                  "end_offset": 14,
                  "payload": "d29yZA=="
                }
              ]
            }
          }
        }
      }
    }

#### 动态生成项向量

未显式存储在索引中的术语向量会自动动态计算。以下请求返回文档"1"中字段的所有信息和统计信息，即使术语尚未显式存储在索引中也是如此。请注意，对于字段"文本"，不会重新生成术语。

    
    
    response = client.termvectors(
      index: 'my-index-000001',
      id: 1,
      body: {
        fields: [
          'text',
          'some_field_without_term_vectors'
        ],
        offsets: true,
        positions: true,
        term_statistics: true,
        field_statistics: true
      }
    )
    puts response
    
    
    GET /my-index-000001/_termvectors/1
    {
      "fields" : ["text", "some_field_without_term_vectors"],
      "offsets" : true,
      "positions" : true,
      "term_statistics" : true,
      "field_statistics" : true
    }

#### 人工文档

也可以为人工文档生成术语向量，即索引中不存在的文档。例如，以下请求将返回与示例 1 中相同的结果。使用的映射由"索引"确定。

**如果启用动态映射(默认)，则将动态创建不在原始映射中的文档字段。

    
    
    response = client.termvectors(
      index: 'my-index-000001',
      body: {
        doc: {
          fullname: 'John Doe',
          text: 'test test test'
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_termvectors
    {
      "doc" : {
        "fullname" : "John Doe",
        "text" : "test test test"
      }
    }

##### 每个字段分析器

此外，可以使用"per_field_analyzer"参数提供与现场分析器不同的分析器。这对于以任何方式生成术语向量非常有用，尤其是在使用人工文档时。为已存储术语向量的字段提供分析器时，将重新生成术语向量。

    
    
    response = client.termvectors(
      index: 'my-index-000001',
      body: {
        doc: {
          fullname: 'John Doe',
          text: 'test test test'
        },
        fields: [
          'fullname'
        ],
        per_field_analyzer: {
          fullname: 'keyword'
        }
      }
    )
    puts response
    
    
    GET /my-index-000001/_termvectors
    {
      "doc" : {
        "fullname" : "John Doe",
        "text" : "test test test"
      },
      "fields": ["fullname"],
      "per_field_analyzer" : {
        "fullname": "keyword"
      }
    }

Response:

    
    
    {
      "_index": "my-index-000001",
      "_version": 0,
      "found": true,
      "took": 6,
      "term_vectors": {
        "fullname": {
           "field_statistics": {
              "sum_doc_freq": 2,
              "doc_count": 4,
              "sum_ttf": 4
           },
           "terms": {
              "John Doe": {
                 "term_freq": 1,
                 "tokens": [
                    {
                       "position": 0,
                       "start_offset": 0,
                       "end_offset": 8
                    }
                 ]
              }
           }
        }
      }
    }

#### 术语筛选

最后，返回的术语可以根据其 tf-idf 分数进行过滤。在下面的示例中，我们从具有给定"plot"字段值的人工文档中获取三个最"有趣"的关键字。请注意，关键字"Tony"或任何停用词都不是响应的一部分，因为它们的tf-idf必须太低。

    
    
    response = client.termvectors(
      index: 'imdb',
      body: {
        doc: {
          plot: 'When wealthy industrialist Tony Stark is forced to build an armored suit after a life-threatening incident, he ultimately decides to use its technology to fight against evil.'
        },
        term_statistics: true,
        field_statistics: true,
        positions: false,
        offsets: false,
        filter: {
          max_num_terms: 3,
          min_term_freq: 1,
          min_doc_freq: 1
        }
      }
    )
    puts response
    
    
    GET /imdb/_termvectors
    {
      "doc": {
        "plot": "When wealthy industrialist Tony Stark is forced to build an armored suit after a life-threatening incident, he ultimately decides to use its technology to fight against evil."
      },
      "term_statistics": true,
      "field_statistics": true,
      "positions": false,
      "offsets": false,
      "filter": {
        "max_num_terms": 3,
        "min_term_freq": 1,
        "min_doc_freq": 1
      }
    }

Response:

    
    
    {
       "_index": "imdb",
       "_version": 0,
       "found": true,
       "term_vectors": {
          "plot": {
             "field_statistics": {
                "sum_doc_freq": 3384269,
                "doc_count": 176214,
                "sum_ttf": 3753460
             },
             "terms": {
                "armored": {
                   "doc_freq": 27,
                   "ttf": 27,
                   "term_freq": 1,
                   "score": 9.74725
                },
                "industrialist": {
                   "doc_freq": 88,
                   "ttf": 88,
                   "term_freq": 1,
                   "score": 8.590818
                },
                "stark": {
                   "doc_freq": 44,
                   "ttf": 47,
                   "term_freq": 1,
                   "score": 9.272792
                }
             }
          }
       }
    }

[« Reindex API](docs-reindex.md) [Multi term vectors API »](docs-multi-
termvectors.md)
