

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Index
modules](index-modules.md)

[« Merge](index-modules-merge.md) [Slow Log »](index-modules-slowlog.md)

## 相似性模块

相似性(评分/排名模型)定义了如何对匹配的文档进行评分。相似性是每个字段的，这意味着通过映射可以定义每个字段的不同相似性。

配置自定义相似性被视为专家功能，内置相似性很可能足以满足"相似性"中所述。

### 配置相似性

大多数现有或自定义相似性都有配置选项，可以通过索引设置进行配置，如下所示。创建索引或更新索引设置时，可以提供索引选项。

    
    
    response = client.indices.create(
      index: 'index',
      body: {
        settings: {
          index: {
            similarity: {
              my_similarity: {
                type: 'DFR',
                basic_model: 'g',
                after_effect: 'l',
                normalization: 'h2',
                "normalization.h2.c": '3.0'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /index
    {
      "settings": {
        "index": {
          "similarity": {
            "my_similarity": {
              "type": "DFR",
              "basic_model": "g",
              "after_effect": "l",
              "normalization": "h2",
              "normalization.h2.c": "3.0"
            }
          }
        }
      }
    }

在这里，我们配置 DFR 相似性，以便可以在映射中将其引用为"my_similarity"，如以下示例所示：

    
    
    response = client.indices.put_mapping(
      index: 'index',
      body: {
        properties: {
          title: {
            type: 'text',
            similarity: 'my_similarity'
          }
        }
      }
    )
    puts response
    
    
    PUT /index/_mapping
    {
      "properties" : {
        "title" : { "type" : "text", "similarity" : "my_similarity" }
      }
    }

### 可用相似之处

#### BM25 相似性( **默认**)

基于 TF/IDF 的相似性，具有内置的 tf 规范化，应该更适合短字段(如名称)。SeeOkapi_BM25了解更多详情。这种相似性有以下选项：

`k1`

|

控制非线性项频率归一化(饱和)。默认值为"1.2"。   ---|--- 'b'

|

控制文档长度规范化 tf 值的程度。默认值为"0.75"。   "discount_overlaps"

|

确定在计算范数时是否忽略重叠标记(位置增量为 0 的标记)。默认情况下，这是真的，这意味着重叠标记在计算范数时不计算在内。   类型名称： "BM25"

#### DFR相似性

实现随机性框架背离的相似性。这种相似性有以下选项：

`basic_model`

|

可能的值："g"、"if"、"in"和"ine"。   ---|--- "after_effect"

|

可能的值："b'and'l"。   "正常化"

|

可能的值："否"、"h1"、"h2"、"h3"和"z"。   除第一个选项外，所有选项都需要规范化值。

类型名称："DFR"

#### DFI相似性

实现独立性背离模型的相似性。这种相似性有以下选项：

`independence_measure`

|

可能的值"标准化"、"饱和"、"卡方"。   ---|--- 使用这种相似性时，强烈建议删除停用词以获得良好的相关性。另请注意，频率低于预期频率的术语将获得等于 0 的分数。

类型名称： "DFI"

#### IB相似性。

基于信息的模型。该算法基于以下概念：任何符号_分布_序列中的信息内容主要由其基本元素的重复使用决定。对于书面文本，这一挑战对应于比较不同作者的写作风格。这种相似性具有以下选项：

`distribution`

|

可能的值："将"和"spl"。   ---|--- "lambda"

|

可能的值："df"和"ttf"。   "正常化"

|

与"DFR"相似之处相同。   类型名称："IB"

#### LM 狄利克雷相似性。

LM狄利克雷相似性。这种相似性有以下选项：

`mu`

|

默认为"2000"。   ---|--- 论文中的评分公式将负分分配给出现次数少于语言模型预测的术语，这对Lucene来说是非法的，因此此类术语的得分为0。

类型名称： 'LMDirichlet'

#### LM Jelinek Mercersimilarity.

LM Jelinek Mercersimilarity。该算法试图捕获文本中的重要模式，同时排除噪音。这种相似性有以下选项：

`lambda`

|

最佳值取决于集合和查询。标题查询的最佳值约为"0.1"，长查询的最佳值约为"0.7"。默认值为"0.1"。当值接近"0"时，匹配更多查询词的文档的排名将高于匹配较少字词的文档。   ---|--- 类型名称："LMJelinekMercer"

#### 脚本相似性

一种相似性，允许您使用脚本来指定应如何计算分数。例如，下面的示例演示如何重新实现 TF-IDF：

    
    
    response = client.indices.create(
      index: 'index',
      body: {
        settings: {
          number_of_shards: 1,
          similarity: {
            scripted_tfidf: {
              type: 'scripted',
              script: {
                source: 'double tf = Math.sqrt(doc.freq); double idf = Math.log((field.docCount+1.0)/(term.docFreq+1.0)) + 1.0; double norm = 1/Math.sqrt(doc.length); return query.boost * tf * idf * norm;'
              }
            }
          }
        },
        mappings: {
          properties: {
            field: {
              type: 'text',
              similarity: 'scripted_tfidf'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'index',
      id: 1,
      body: {
        field: 'foo bar foo'
      }
    )
    puts response
    
    response = client.index(
      index: 'index',
      id: 2,
      body: {
        field: 'bar baz'
      }
    )
    puts response
    
    response = client.indices.refresh(
      index: 'index'
    )
    puts response
    
    response = client.search(
      index: 'index',
      explain: true,
      body: {
        query: {
          query_string: {
            query: 'foo^1.7',
            default_field: 'field'
          }
        }
      }
    )
    puts response
    
    
    PUT /index
    {
      "settings": {
        "number_of_shards": 1,
        "similarity": {
          "scripted_tfidf": {
            "type": "scripted",
            "script": {
              "source": "double tf = Math.sqrt(doc.freq); double idf = Math.log((field.docCount+1.0)/(term.docFreq+1.0)) + 1.0; double norm = 1/Math.sqrt(doc.length); return query.boost * tf * idf * norm;"
            }
          }
        }
      },
      "mappings": {
        "properties": {
          "field": {
            "type": "text",
            "similarity": "scripted_tfidf"
          }
        }
      }
    }
    
    PUT /index/_doc/1
    {
      "field": "foo bar foo"
    }
    
    PUT /index/_doc/2
    {
      "field": "bar baz"
    }
    
    POST /index/_refresh
    
    GET /index/_search?explain=true
    {
      "query": {
        "query_string": {
          "query": "foo^1.7",
          "default_field": "field"
        }
      }
    }

这会产生：

    
    
    {
      "took": 12,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": {
            "value": 1,
            "relation": "eq"
        },
        "max_score": 1.9508477,
        "hits": [
          {
            "_shard": "[index][0]",
            "_node": "OzrdjxNtQGaqs4DmioFw9A",
            "_index": "index",
            "_id": "1",
            "_score": 1.9508477,
            "_source": {
              "field": "foo bar foo"
            },
            "_explanation": {
              "value": 1.9508477,
              "description": "weight(field:foo in 0) [PerFieldSimilarity], result of:",
              "details": [
                {
                  "value": 1.9508477,
                  "description": "score from ScriptedSimilarity(weightScript=[null], script=[Script{type=inline, lang='painless', idOrCode='double tf = Math.sqrt(doc.freq); double idf = Math.log((field.docCount+1.0)/(term.docFreq+1.0)) + 1.0; double norm = 1/Math.sqrt(doc.length); return query.boost * tf * idf * norm;', options={}, params={}}]) computed from:",
                  "details": [
                    {
                      "value": 1.0,
                      "description": "weight",
                      "details": []
                    },
                    {
                      "value": 1.7,
                      "description": "query.boost",
                      "details": []
                    },
                    {
                      "value": 2,
                      "description": "field.docCount",
                      "details": []
                    },
                    {
                      "value": 4,
                      "description": "field.sumDocFreq",
                      "details": []
                    },
                    {
                      "value": 5,
                      "description": "field.sumTotalTermFreq",
                      "details": []
                    },
                    {
                      "value": 1,
                      "description": "term.docFreq",
                      "details": []
                    },
                    {
                      "value": 2,
                      "description": "term.totalTermFreq",
                      "details": []
                    },
                    {
                      "value": 2.0,
                      "description": "doc.freq",
                      "details": []
                    },
                    {
                      "value": 3,
                      "description": "doc.length",
                      "details": []
                    }
                  ]
                }
              ]
            }
          }
        ]
      }
    }

虽然脚本相似性提供了很大的灵活性，但它们需要满足一组规则。如果不这样做，可能会使 Elasticsearch 静默地返回错误的热门点击，或者在搜索时因内部错误而失败：

* 返回的分数必须为正数。  * 所有其他变量保持不变，分数不得在"doc.freq"增加时降低。  * 所有其他变量保持不变，当"doc.length"增加时，分数不得增加。

您可能已经注意到，上述脚本的很大一部分依赖于每个文档相同的统计信息。通过提供一个"weight_script"可以使上述方法稍微更有效，该将计算分数中与文档无关的部分，并将在"权重"变量下可用。如果未提供"weight_script"，则"权重"等于"1"。"weight_script"可以访问与"脚本"相同的变量，除了"文档"，因为它应该计算与文档无关的分数贡献。

以下配置将给出相同的 tf-idf 分数，但效率略高：

    
    
    response = client.indices.create(
      index: 'index',
      body: {
        settings: {
          number_of_shards: 1,
          similarity: {
            scripted_tfidf: {
              type: 'scripted',
              weight_script: {
                source: 'double idf = Math.log((field.docCount+1.0)/(term.docFreq+1.0)) + 1.0; return query.boost * idf;'
              },
              script: {
                source: 'double tf = Math.sqrt(doc.freq); double norm = 1/Math.sqrt(doc.length); return weight * tf * norm;'
              }
            }
          }
        },
        mappings: {
          properties: {
            field: {
              type: 'text',
              similarity: 'scripted_tfidf'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /index
    {
      "settings": {
        "number_of_shards": 1,
        "similarity": {
          "scripted_tfidf": {
            "type": "scripted",
            "weight_script": {
              "source": "double idf = Math.log((field.docCount+1.0)/(term.docFreq+1.0)) + 1.0; return query.boost * idf;"
            },
            "script": {
              "source": "double tf = Math.sqrt(doc.freq); double norm = 1/Math.sqrt(doc.length); return weight * tf * norm;"
            }
          }
        }
      },
      "mappings": {
        "properties": {
          "field": {
            "type": "text",
            "similarity": "scripted_tfidf"
          }
        }
      }
    }

类型名称："脚本化"

#### 默认相似性

默认情况下，Elasticsearch 将使用配置为"默认"的任何相似性。

您可以在创建索引时更改索引中所有字段的默认相似性：

    
    
    response = client.indices.create(
      index: 'index',
      body: {
        settings: {
          index: {
            similarity: {
              default: {
                type: 'boolean'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /index
    {
      "settings": {
        "index": {
          "similarity": {
            "default": {
              "type": "boolean"
            }
          }
        }
      }
    }

如果要在创建索引后更改默认相似性，则必须关闭索引，发送以下请求并在之后再次打开它：

    
    
    response = client.indices.close(
      index: 'index'
    )
    puts response
    
    response = client.indices.put_settings(
      index: 'index',
      body: {
        index: {
          similarity: {
            default: {
              type: 'boolean'
            }
          }
        }
      }
    )
    puts response
    
    response = client.indices.open(
      index: 'index'
    )
    puts response
    
    
    POST /index/_close
    
    PUT /index/_settings
    {
      "index": {
        "similarity": {
          "default": {
            "type": "boolean"
          }
        }
      }
    }
    
    POST /index/_open

[« Merge](index-modules-merge.md) [Slow Log »](index-modules-slowlog.md)
