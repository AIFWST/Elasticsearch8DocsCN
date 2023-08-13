

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Configure text analysis](configure-text-
analysis.md)

[« Create a custom analyzer](analysis-custom-analyzer.md) [Built-in analyzer
reference »](analysis-analyzers.md)

## 指定分析器

Elasticsearch 提供了多种方法来指定内置或自定义分析器：

* 按"文本"字段、索引或查询 * 用于索引或搜索时间

### 保持简单

在不同级别和不同时间指定分析仪的灵活性非常好......_but仅在needed_时。

在大多数情况下，简单的方法效果最好：为每个"文本"字段指定分析器，如指定字段的分析器中所述。

此方法与 Elasticsearch 的默认行为配合得很好，允许您使用相同的分析器进行索引和搜索。它还允许您使用获取映射 API 快速查看哪个分析器适用于哪个字段。

如果通常不为索引创建映射，则可以使用索引模板来实现类似的效果。

### Elasticsearch 如何确定索引分析器

Elasticsearch 通过按顺序检查以下参数来确定要使用的索引分析器：

1. 字段的"分析器"映射参数。请参阅为字段指定分析器。  2. "分析.分析器.默认"索引设置。请参阅指定索引的默认分析器。

如果未指定这些参数，则使用"标准"分析器。

### 指定字段的分析器

映射索引时，可以使用"分析器"映射参数为每个"文本"字段指定分析器。

以下创建索引 APIrequest 将"空格"分析器设置为"标题"字段的分析器。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            title: {
              type: 'text',
              analyzer: 'whitespace'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "title": {
            "type": "text",
            "analyzer": "whitespace"
          }
        }
      }
    }

### 指定索引的默认分析器

除了字段级分析器之外，您还可以设置回退分析器以使用"analysis.analyzer.default"设置。

以下创建索引 APIrequest 将"简单"分析器设置为"my-index-000001"的回退分析器。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              default: {
                type: 'simple'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "default": {
              "type": "simple"
            }
          }
        }
      }
    }

### Elasticsearch 如何确定搜索分析器

在大多数情况下，不需要指定不同的搜索分析器。这样做可能会对相关性产生负面影响，并导致意外的搜索结果。

如果选择指定单独的搜索分析器，建议在生产中部署之前全面测试分析配置。

在搜索时，Elasticsearch 通过按顺序检查以下参数来确定要使用的分析器：

1. 搜索查询中的"分析器"参数。请参阅为查询指定搜索分析器。  2. 字段的"search_analyzer"映射参数。请参阅为字段指定搜索分析器。  3. "analysis.analyzer.default_search"索引设置。请参阅指定索引的默认搜索分析器。  4. 字段的"分析器"映射参数。请参阅为字段指定分析器。

如果未指定这些参数，则使用"标准"分析器。

### 指定查询的搜索分析器

编写全文查询时，可以使用"分析器"参数指定搜索分析器。如果提供，这将覆盖任何其他搜索分析器。

以下搜索 API 请求将"停止"分析器设置为"匹配"查询的搜索分析器。

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          match: {
            message: {
              query: 'Quick foxes',
              analyzer: 'stop'
            }
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "query": {
        "match": {
          "message": {
            "query": "Quick foxes",
            "analyzer": "stop"
          }
        }
      }
    }

### 指定字段的搜索分析器

映射索引时，可以使用"search_analyzer"映射参数为每个"文本"字段指定搜索分析器。

如果提供了搜索分析器，则还必须使用"analyzer"参数指定索引分析器。

以下创建索引 APIrequest 将"简单"分析器设置为"标题"字段的搜索分析器。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            title: {
              type: 'text',
              analyzer: 'whitespace',
              search_analyzer: 'simple'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "title": {
            "type": "text",
            "analyzer": "whitespace",
            "search_analyzer": "simple"
          }
        }
      }
    }

### 指定索引的默认搜索分析器

创建索引时，可以使用"analysis.analyzer.default_search"设置设置默认搜索分析器。

如果提供了搜索分析器，则还必须使用"analysis.analyzer.default"设置指定默认索引分析器。

以下创建索引 APIrequest 将"空格"分析器设置为"my-index-000001"索引的默认搜索分析器。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              default: {
                type: 'simple'
              },
              default_search: {
                type: 'whitespace'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "default": {
              "type": "simple"
            },
            "default_search": {
              "type": "whitespace"
            }
          }
        }
      }
    }

[« Create a custom analyzer](analysis-custom-analyzer.md) [Built-in analyzer
reference »](analysis-analyzers.md)
