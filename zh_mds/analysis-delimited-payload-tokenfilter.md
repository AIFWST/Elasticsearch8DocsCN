

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Decimal digit token filter](analysis-decimal-digit-tokenfilter.md)
[Dictionary decompounder token filter »](analysis-dict-decomp-
tokenfilter.md)

## 分隔有效负载令牌筛选器

旧名称"delimited_payload_filter"已弃用，不应与新索引一起使用。请改用"delimited_payload"。

根据指定的分隔符将令牌流分隔为令牌和有效负载。

例如，您可以将"delimited_payload"过滤器与"|"分隔符一起使用，将"the|1 quick|2 fox|3"拆分为标记"the"、"quick"和"fox"，有效负载分别为"1"、"2"和"3"。

此过滤器使用 Lucene 的 DelimitPayloadTokenFilter。

### 有效负载

有效负载是与令牌位置关联的用户定义的二进制数据，并存储为 base64 编码的字节。

默认情况下，Elasticsearch 不存储令牌有效负载。要存储有效负载，您必须：

* 将存储有效负载的任何字段的"term_vector"映射参数设置为"with_positions_payloads"或"with_positions_offsets_payloads"。  * 使用包含"delimited_payload"过滤器的索引分析器

您可以使用术语向量 API 查看存储的有效负载。

###Example

以下分析 API 请求使用带有默认"|"分隔符的"delimited_payload"筛选器将"the|0brown|10 fox|5 is|0 quick|10"拆分为令牌和有效负载。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        filter: [
          'delimited_payload'
        ],
        text: 'the|0 brown|10 fox|5 is|0 quick|10'
      }
    )
    puts response
    
    
    GET _analyze
    {
      "tokenizer": "whitespace",
      "filter": ["delimited_payload"],
      "text": "the|0 brown|10 fox|5 is|0 quick|10"
    }

筛选器生成以下标记：

    
    
    [ the, brown, fox, is, quick ]

请注意，分析 API 不会返回存储的有效负载。有关包含返回的有效负载的示例，请参阅返回存储的有效负载。

### 添加到分析器

以下创建索引 APIrequest 使用"分隔有效负载"筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'delimited_payload',
      body: {
        settings: {
          analysis: {
            analyzer: {
              whitespace_delimited_payload: {
                tokenizer: 'whitespace',
                filter: [
                  'delimited_payload'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT delimited_payload
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "whitespace_delimited_payload": {
              "tokenizer": "whitespace",
              "filter": [ "delimited_payload" ]
            }
          }
        }
      }
    }

### 可配置参数

`delimiter`

     (Optional, string) Character used to separate tokens from payloads. Defaults to `|`. 
`encoding`

    

(可选，字符串)存储有效负载的数据类型。有效值为：

`float`

     (Default) Float 
`identity`

     Characters 
`int`

     Integer 

### 自定义并添加到分析器

要自定义"delimited_payload"筛选器，请复制它以创建新的自定义令牌筛选器的基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下创建索引 API 请求使用自定义"delimited_payload"筛选器来配置新的自定义分析器。自定义"delimited_payload"筛选器使用"+"分隔符将令牌与有效负载分开。有效负载编码为整数。

    
    
    response = client.indices.create(
      index: 'delimited_payload_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              whitespace_plus_delimited: {
                tokenizer: 'whitespace',
                filter: [
                  'plus_delimited'
                ]
              }
            },
            filter: {
              plus_delimited: {
                type: 'delimited_payload',
                delimiter: '+',
                encoding: 'int'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT delimited_payload_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "whitespace_plus_delimited": {
              "tokenizer": "whitespace",
              "filter": [ "plus_delimited" ]
            }
          },
          "filter": {
            "plus_delimited": {
              "type": "delimited_payload",
              "delimiter": "+",
              "encoding": "int"
            }
          }
        }
      }
    }

### 返回存储的有效负载

使用创建索引 API 创建索引，该索引：

* 包括一个字段，用于存储带有有效负载的术语向量。  * 使用带有"delimited_payload"过滤器的自定义索引分析器。

    
    
    response = client.indices.create(
      index: 'text_payloads',
      body: {
        mappings: {
          properties: {
            text: {
              type: 'text',
              term_vector: 'with_positions_payloads',
              analyzer: 'payload_delimiter'
            }
          }
        },
        settings: {
          analysis: {
            analyzer: {
              payload_delimiter: {
                tokenizer: 'whitespace',
                filter: [
                  'delimited_payload'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT text_payloads
    {
      "mappings": {
        "properties": {
          "text": {
            "type": "text",
            "term_vector": "with_positions_payloads",
            "analyzer": "payload_delimiter"
          }
        }
      },
      "settings": {
        "analysis": {
          "analyzer": {
            "payload_delimiter": {
              "tokenizer": "whitespace",
              "filter": [ "delimited_payload" ]
            }
          }
        }
      }
    }

将包含有效负载的文档添加到索引。

    
    
    response = client.index(
      index: 'text_payloads',
      id: 1,
      body: {
        text: 'the|0 brown|3 fox|4 is|0 quick|10'
      }
    )
    puts response
    
    
    POST text_payloads/_doc/1
    {
      "text": "the|0 brown|3 fox|4 is|0 quick|10"
    }

使用术语向量 API 返回文档的令牌和 base64 编码的有效负载。

    
    
    response = client.termvectors(
      index: 'text_payloads',
      id: 1,
      body: {
        fields: [
          'text'
        ],
        payloads: true
      }
    )
    puts response
    
    
    GET text_payloads/_termvectors/1
    {
      "fields": [ "text" ],
      "payloads": true
    }

API 返回以下响应：

    
    
    {
      "_index": "text_payloads",
      "_id": "1",
      "_version": 1,
      "found": true,
      "took": 8,
      "term_vectors": {
        "text": {
          "field_statistics": {
            "sum_doc_freq": 5,
            "doc_count": 1,
            "sum_ttf": 5
          },
          "terms": {
            "brown": {
              "term_freq": 1,
              "tokens": [
                {
                  "position": 1,
                  "payload": "QEAAAA=="
                }
              ]
            },
            "fox": {
              "term_freq": 1,
              "tokens": [
                {
                  "position": 2,
                  "payload": "QIAAAA=="
                }
              ]
            },
            "is": {
              "term_freq": 1,
              "tokens": [
                {
                  "position": 3,
                  "payload": "AAAAAA=="
                }
              ]
            },
            "quick": {
              "term_freq": 1,
              "tokens": [
                {
                  "position": 4,
                  "payload": "QSAAAA=="
                }
              ]
            },
            "the": {
              "term_freq": 1,
              "tokens": [
                {
                  "position": 0,
                  "payload": "AAAAAA=="
                }
              ]
            }
          }
        }
      }
    }

[« Decimal digit token filter](analysis-decimal-digit-tokenfilter.md)
[Dictionary decompounder token filter »](analysis-dict-decomp-
tokenfilter.md)
