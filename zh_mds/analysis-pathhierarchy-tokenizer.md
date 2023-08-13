

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Tokenizer reference](analysis-tokenizers.md)

[« N-gram tokenizer](analysis-ngram-tokenizer.md) [Pattern tokenizer
»](analysis-pattern-tokenizer.md)

## 路径层次结构标记器

"path_hierarchy"分词器采用像文件系统路径这样的分层值，在路径分隔符上拆分，并为树中的每个组件发出一个术语。"path_hierarcy"分词器使用Lucene的PathHierarchyTokenizerunderneath。

### 示例输出

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'path_hierarchy',
        text: '/one/two/three'
      }
    )
    puts response
    
    
    POST _analyze
    {
      "tokenizer": "path_hierarchy",
      "text": "/one/two/three"
    }

上述案文将产生以下术语：

    
    
    [ /one, /one/two, /one/two/three ]

###Configuration

"path_hierarchy"分词器接受以下参数：

`delimiter`

|

要用作路径分隔符的字符。默认为"/"。   ---|---"替换"

|

用于分隔符的可选替换字符。默认为"分隔符"。   "buffer_size"

|

单次传入术语缓冲区的字符数。 默认值为"1024"。术语缓冲区将按此大小增长，直到所有文本都被使用完毕。建议不要更改此设置。   "反转"

|

如果为"true"，则使用 Lucene 的 ReversePathHierarchyTokenizer，它适用于类似域的层次结构。默认为"假"。   "跳过"

|

要跳过的初始令牌数。默认为"0"。   ### 示例配置编辑

在此示例中，我们将"path_hierarchy"分词器配置为拆分为"-"字符，并将它们替换为"/"。跳过前两个标记：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_analyzer: {
                tokenizer: 'my_tokenizer'
              }
            },
            tokenizer: {
              my_tokenizer: {
                type: 'path_hierarchy',
                delimiter: '-',
                replacement: '/',
                skip: 2
              }
            }
          }
        }
      }
    )
    puts response
    
    response = client.indices.analyze(
      index: 'my-index-000001',
      body: {
        analyzer: 'my_analyzer',
        text: 'one-two-three-four-five'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "my_analyzer": {
              "tokenizer": "my_tokenizer"
            }
          },
          "tokenizer": {
            "my_tokenizer": {
              "type": "path_hierarchy",
              "delimiter": "-",
              "replacement": "/",
              "skip": 2
            }
          }
        }
      }
    }
    
    POST my-index-000001/_analyze
    {
      "analyzer": "my_analyzer",
      "text": "one-two-three-four-five"
    }

上面的示例生成以下术语：

    
    
    [ /three, /three/four, /three/four/five ]

如果我们将"反向"设置为"true"，它将产生以下内容：

    
    
    [ one/two/three/, two/three/, three/ ]

### 详细示例

"path_hierarchy"分词器的一个常见用例是按文件路径过滤结果。如果将文件路径与数据一起编制索引，则使用"path_hierarchy"标记器分析路径允许按文件路径字符串的不同部分过滤结果。

此示例将索引配置为具有两个自定义分析器，并将这些分析器应用于将存储文件名的"file_path"文本字段的多字段。两个分析器之一使用反向标记化。然后对一些示例文档编制索引，以表示两个不同用户的照片文件夹中的照片的某些文件路径。

    
    
    response = client.indices.create(
      index: 'file-path-test',
      body: {
        settings: {
          analysis: {
            analyzer: {
              custom_path_tree: {
                tokenizer: 'custom_hierarchy'
              },
              custom_path_tree_reversed: {
                tokenizer: 'custom_hierarchy_reversed'
              }
            },
            tokenizer: {
              custom_hierarchy: {
                type: 'path_hierarchy',
                delimiter: '/'
              },
              custom_hierarchy_reversed: {
                type: 'path_hierarchy',
                delimiter: '/',
                reverse: 'true'
              }
            }
          }
        },
        mappings: {
          properties: {
            file_path: {
              type: 'text',
              fields: {
                tree: {
                  type: 'text',
                  analyzer: 'custom_path_tree'
                },
                tree_reversed: {
                  type: 'text',
                  analyzer: 'custom_path_tree_reversed'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'file-path-test',
      id: 1,
      body: {
        file_path: '/User/alice/photos/2017/05/16/my_photo1.jpg'
      }
    )
    puts response
    
    response = client.index(
      index: 'file-path-test',
      id: 2,
      body: {
        file_path: '/User/alice/photos/2017/05/16/my_photo2.jpg'
      }
    )
    puts response
    
    response = client.index(
      index: 'file-path-test',
      id: 3,
      body: {
        file_path: '/User/alice/photos/2017/05/16/my_photo3.jpg'
      }
    )
    puts response
    
    response = client.index(
      index: 'file-path-test',
      id: 4,
      body: {
        file_path: '/User/alice/photos/2017/05/15/my_photo1.jpg'
      }
    )
    puts response
    
    response = client.index(
      index: 'file-path-test',
      id: 5,
      body: {
        file_path: '/User/bob/photos/2017/05/16/my_photo1.jpg'
      }
    )
    puts response
    
    
    PUT file-path-test
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "custom_path_tree": {
              "tokenizer": "custom_hierarchy"
            },
            "custom_path_tree_reversed": {
              "tokenizer": "custom_hierarchy_reversed"
            }
          },
          "tokenizer": {
            "custom_hierarchy": {
              "type": "path_hierarchy",
              "delimiter": "/"
            },
            "custom_hierarchy_reversed": {
              "type": "path_hierarchy",
              "delimiter": "/",
              "reverse": "true"
            }
          }
        }
      },
      "mappings": {
        "properties": {
          "file_path": {
            "type": "text",
            "fields": {
              "tree": {
                "type": "text",
                "analyzer": "custom_path_tree"
              },
              "tree_reversed": {
                "type": "text",
                "analyzer": "custom_path_tree_reversed"
              }
            }
          }
        }
      }
    }
    
    POST file-path-test/_doc/1
    {
      "file_path": "/User/alice/photos/2017/05/16/my_photo1.jpg"
    }
    
    POST file-path-test/_doc/2
    {
      "file_path": "/User/alice/photos/2017/05/16/my_photo2.jpg"
    }
    
    POST file-path-test/_doc/3
    {
      "file_path": "/User/alice/photos/2017/05/16/my_photo3.jpg"
    }
    
    POST file-path-test/_doc/4
    {
      "file_path": "/User/alice/photos/2017/05/15/my_photo1.jpg"
    }
    
    POST file-path-test/_doc/5
    {
      "file_path": "/User/bob/photos/2017/05/16/my_photo1.jpg"
    }

根据文本字段搜索特定文件路径字符串与所有示例文档匹配，Bob 的文档排名最高，因为"bob"也是标准分析器创建的术语之一，提高了 Bob 文档的相关性。

    
    
    response = client.search(
      index: 'file-path-test',
      body: {
        query: {
          match: {
            file_path: '/User/bob/photos/2017/05'
          }
        }
      }
    )
    puts response
    
    
    GET file-path-test/_search
    {
      "query": {
        "match": {
          "file_path": "/User/bob/photos/2017/05"
        }
      }
    }

使用"file_path.tree"字段将文档与特定目录中存在的文件路径进行匹配或过滤非常简单。

    
    
    response = client.search(
      index: 'file-path-test',
      body: {
        query: {
          term: {
            "file_path.tree": '/User/alice/photos/2017/05/16'
          }
        }
      }
    )
    puts response
    
    
    GET file-path-test/_search
    {
      "query": {
        "term": {
          "file_path.tree": "/User/alice/photos/2017/05/16"
        }
      }
    }

使用此分词器的反向参数，还可以从文件路径的另一端进行匹配，例如单个文件名或深层子目录。以下示例显示如何通过配置为在映射中使用反向参数的"file_path.tree_reversed"字段搜索任何目录中名为"my_photo1.jpg"的所有文件。

    
    
    response = client.search(
      index: 'file-path-test',
      body: {
        query: {
          term: {
            "file_path.tree_reversed": {
              value: 'my_photo1.jpg'
            }
          }
        }
      }
    )
    puts response
    
    
    GET file-path-test/_search
    {
      "query": {
        "term": {
          "file_path.tree_reversed": {
            "value": "my_photo1.jpg"
          }
        }
      }
    }

查看使用正向和反向生成的令牌具有指导意义，可显示为同一文件路径值创建的令牌。

    
    
    response = client.indices.analyze(
      index: 'file-path-test',
      body: {
        analyzer: 'custom_path_tree',
        text: '/User/alice/photos/2017/05/16/my_photo1.jpg'
      }
    )
    puts response
    
    response = client.indices.analyze(
      index: 'file-path-test',
      body: {
        analyzer: 'custom_path_tree_reversed',
        text: '/User/alice/photos/2017/05/16/my_photo1.jpg'
      }
    )
    puts response
    
    
    POST file-path-test/_analyze
    {
      "analyzer": "custom_path_tree",
      "text": "/User/alice/photos/2017/05/16/my_photo1.jpg"
    }
    
    POST file-path-test/_analyze
    {
      "analyzer": "custom_path_tree_reversed",
      "text": "/User/alice/photos/2017/05/16/my_photo1.jpg"
    }

当与其他类型的搜索结合使用时，能够使用文件路径进行过滤也很有用，例如此示例查找带有"16"的任何文件路径也必须在 Alice 的照片目录中。

    
    
    response = client.search(
      index: 'file-path-test',
      body: {
        query: {
          bool: {
            must: {
              match: {
                file_path: '16'
              }
            },
            filter: {
              term: {
                "file_path.tree": '/User/alice'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET file-path-test/_search
    {
      "query": {
        "bool" : {
          "must" : {
            "match" : { "file_path" : "16" }
          },
          "filter": {
            "term" : { "file_path.tree" : "/User/alice" }
          }
        }
      }
    }

[« N-gram tokenizer](analysis-ngram-tokenizer.md) [Pattern tokenizer
»](analysis-pattern-tokenizer.md)
