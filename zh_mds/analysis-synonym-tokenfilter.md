

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Stop token filter](analysis-stop-tokenfilter.md) [Synonym graph token
filter »](analysis-synonym-graph-tokenfilter.md)

## 同义词令牌筛选器

"同义词"令牌过滤器允许在分析过程中轻松处理同义词。同义词是使用配置文件配置的。下面是一个例子：

    
    
    response = client.indices.create(
      index: 'test_index',
      body: {
        settings: {
          index: {
            analysis: {
              analyzer: {
                synonym: {
                  tokenizer: 'whitespace',
                  filter: [
                    'synonym'
                  ]
                }
              },
              filter: {
                synonym: {
                  type: 'synonym',
                  synonyms_path: 'analysis/synonym.txt'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /test_index
    {
      "settings": {
        "index": {
          "analysis": {
            "analyzer": {
              "synonym": {
                "tokenizer": "whitespace",
                "filter": [ "synonym" ]
              }
            },
            "filter": {
              "synonym": {
                "type": "synonym",
                "synonyms_path": "analysis/synonym.txt"
              }
            }
          }
        }
      }
    }

上面配置了一个"同义词"过滤器，路径为"分析/同义词.txt"(相对于"配置"位置)。然后使用过滤器配置"同义词"分析器。

此筛选器使用链中出现在它之前的任何标记器和标记筛选器标记同义词。

其他设置包括：

* "可更新"(默认为"假")。如果"true"允许重新加载搜索分析器以选取对同义词文件的更改。仅用于搜索分析器。  * "展开"(默认为"true")。  * "宽松"(默认为"假")。如果"true"在解析同义词配置时忽略异常。请务必注意，只有那些无法解析的同义词规则才会被忽略。例如，请考虑以下请求：

    
    
    response = client.indices.create(
      index: 'test_index',
      body: {
        settings: {
          index: {
            analysis: {
              analyzer: {
                synonym: {
                  tokenizer: 'standard',
                  filter: [
                    'my_stop',
                    'synonym'
                  ]
                }
              },
              filter: {
                my_stop: {
                  type: 'stop',
                  stopwords: [
                    'bar'
                  ]
                },
                synonym: {
                  type: 'synonym',
                  lenient: true,
                  synonyms: [
                    'foo, bar => baz'
                  ]
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /test_index
    {
      "settings": {
        "index": {
          "analysis": {
            "analyzer": {
              "synonym": {
                "tokenizer": "standard",
                "filter": [ "my_stop", "synonym" ]
              }
            },
            "filter": {
              "my_stop": {
                "type": "stop",
                "stopwords": [ "bar" ]
              },
              "synonym": {
                "type": "synonym",
                "lenient": true,
                "synonyms": [ "foo, bar => baz" ]
              }
            }
          }
        }
      }
    }

通过上述请求，单词"bar"被跳过，但仍然添加了映射"foo => baz"。但是，如果添加的映射是"foo， baz => bar"，则不会将任何内容添加到同义词列表中。这是因为映射的目标词本身被消除了，因为它是一个停用词。同样，如果映射是"bar，foo，baz"并且"expand"设置为"false"，则不会添加映射，因为当"expand=false"时，目标映射是第一个单词。但是，如果"expand=true"，则添加的映射将等效于"foo，baz => foo，baz"，即除停用词以外的所有映射。

#### "分词器"和"ignore_case"已弃用

"分词器"参数控制将用于标记同义词的分词器，此参数用于向后兼容 6.0 之前创建的索引。"ignore_case"参数仅适用于"分词器"参数。

支持两种同义词格式：Solr，WordNet。

#### 索尔同义词

以下是该文件的示例格式：

    
    
    # Blank lines and lines starting with pound are comments.
    
    # Explicit mappings match any token sequence on the LHS of "=>"
    # and replace with all alternatives on the RHS.  These types of mappings
    # ignore the expand parameter in the schema.
    # Examples:
    i-pod, i pod => ipod
    sea biscuit, sea biscit => seabiscuit
    
    # Equivalent synonyms may be separated with commas and give
    # no explicit mapping.  In this case the mapping behavior will
    # be taken from the expand parameter in the schema.  This allows
    # the same synonym file to be used in different synonym handling strategies.
    # Examples:
    ipod, i-pod, i pod
    foozball , foosball
    universe , cosmos
    lol, laughing out loud
    
    # If expand==true, "ipod, i-pod, i pod" is equivalent
    # to the explicit mapping:
    ipod, i-pod, i pod => ipod, i-pod, i pod
    # If expand==false, "ipod, i-pod, i pod" is equivalent
    # to the explicit mapping:
    ipod, i-pod, i pod => ipod
    
    # Multiple synonym mapping entries are merged.
    foo => foo bar
    foo => baz
    # is equivalent to
    foo => foo bar, baz

您也可以直接在配置文件中定义过滤器的同义词(注意使用"同义词"而不是"synonyms_path")：

    
    
    response = client.indices.create(
      index: 'test_index',
      body: {
        settings: {
          index: {
            analysis: {
              filter: {
                synonym: {
                  type: 'synonym',
                  synonyms: [
                    'i-pod, i pod => ipod',
                    'universe, cosmos'
                  ]
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /test_index
    {
      "settings": {
        "index": {
          "analysis": {
            "filter": {
              "synonym": {
                "type": "synonym",
                "synonyms": [
                  "i-pod, i pod => ipod",
                  "universe, cosmos"
                ]
              }
            }
          }
        }
      }
    }

但是，建议使用"synonyms_path"定义文件中设置的大型同义词，因为以内联方式指定它们会不必要地增加簇大小。

#### 词网同义词

基于WordNet格式的同义词可以使用"格式"声明：

    
    
    response = client.indices.create(
      index: 'test_index',
      body: {
        settings: {
          index: {
            analysis: {
              filter: {
                synonym: {
                  type: 'synonym',
                  format: 'wordnet',
                  synonyms: [
                    "s(100000001,1,'abstain',v,1,0).",
                    "s(100000001,2,'refrain',v,1,0).",
                    "s(100000001,3,'desist',v,1,0)."
                  ]
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /test_index
    {
      "settings": {
        "index": {
          "analysis": {
            "filter": {
              "synonym": {
                "type": "synonym",
                "format": "wordnet",
                "synonyms": [
                  "s(100000001,1,'abstain',v,1,0).",
                  "s(100000001,2,'refrain',v,1,0).",
                  "s(100000001,3,'desist',v,1,0)."
                ]
              }
            }
          }
        }
      }
    }

还支持使用"synonyms_path"在文件中定义WordNet同义词。

### 解析同义词文件

Elasticsearch 将使用 atokenizer 链中同义词过滤器前面的令牌过滤器来解析同义词文件中的条目。因此，例如，如果将同义词过滤器放置在词干分析器之后，则词干分析器也将应用于同义词条目。由于同义词映射中的条目不能具有堆叠位置，因此某些令牌筛选器可能会导致此处出现问题。生成多个版本的令牌的令牌过滤器可以选择在解析同义词时发出哪个版本的令牌，例如"asciifolding"将仅生成令牌的折叠版本。其他的，例如"多路复用器"，"word_delimiter_graph"或"ngram"将抛出错误。

如果需要生成同时包含多标记筛选器和同义词筛选器的分析器，请考虑使用多路复用器筛选器，在一个分支中具有多标记筛选器，在另一个分支中具有同义词筛选器。

[« Stop token filter](analysis-stop-tokenfilter.md) [Synonym graph token
filter »](analysis-synonym-graph-tokenfilter.md)
