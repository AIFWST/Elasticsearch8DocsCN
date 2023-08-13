

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Fingerprint token filter](analysis-fingerprint-tokenfilter.md) [Hunspell
token filter »](analysis-hunspell-tokenfilter.md)

## 展平图形标记筛选器

展平由图形令牌筛选器生成的令牌图，例如"synonym_graph"或"word_delimiter_graph"。

展平包含多位置令牌的令牌图会使该图适合索引。否则，索引不支持包含多位置令牌的令牌图。

展平图形是一个有损的过程。

如果可能，请避免使用"flatten_graph"过滤器。请只在搜索分析器中使用图形令牌筛选器。这消除了对"flatten_graph"过滤器的需求。

"flatten_graph"过滤器使用 Lucene 的 FlattenGraphFilter。

###Example

要查看"flatten_graph"过滤器的工作原理，您首先需要生成一个包含多位置令牌的代币图。

以下分析 API 请求使用"synonym_graph"筛选器在文本"域名系统脆弱"中添加"dns"作为"域名系统"的多位置同义词：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        filter: [
          {
            type: 'synonym_graph',
            synonyms: [
              'dns, domain name system'
            ]
          }
        ],
        text: 'domain name system is fragile'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer": "standard",
      "filter": [
        {
          "type": "synonym_graph",
          "synonyms": [ "dns, domain name system" ]
        }
      ],
      "text": "domain name system is fragile"
    }

筛选器生成以下令牌图，其中"dns"作为多位置令牌。

！令牌图形 DNS 同义词 EX

索引不支持包含多位置令牌的令牌图。为了使此令牌图适合索引，需要将其展平。

若要平展令牌图，请在上一个分析 API 请求中的"synonym_graph"筛选器之后添加"flatten_graph"筛选器。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        filter: [
          {
            type: 'synonym_graph',
            synonyms: [
              'dns, domain name system'
            ]
          },
          'flatten_graph'
        ],
        text: 'domain name system is fragile'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer": "standard",
      "filter": [
        {
          "type": "synonym_graph",
          "synonyms": [ "dns, domain name system" ]
        },
        "flatten_graph"
      ],
      "text": "domain name system is fragile"
    }

筛选器生成以下平展令牌图，适用于索引。

！令牌图 DNS 无效 ex

### 添加到分析器

以下创建索引 APIrequest 使用"flatten_graph"令牌筛选器来配置新的自定义分析器。

在此分析器中，自定义"word_delimiter_graph"筛选器生成包含串联多位置令牌的令牌图。"flatten_graph"过滤这些令牌图，使它们适合索引。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_custom_index_analyzer: {
                type: 'custom',
                tokenizer: 'standard',
                filter: [
                  'my_custom_word_delimiter_graph_filter',
                  'flatten_graph'
                ]
              }
            },
            filter: {
              my_custom_word_delimiter_graph_filter: {
                type: 'word_delimiter_graph',
                catenate_all: true
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "my_custom_index_analyzer": {
              "type": "custom",
              "tokenizer": "standard",
              "filter": [
                "my_custom_word_delimiter_graph_filter",
                "flatten_graph"
              ]
            }
          },
          "filter": {
            "my_custom_word_delimiter_graph_filter": {
              "type": "word_delimiter_graph",
              "catenate_all": true
            }
          }
        }
      }
    }

[« Fingerprint token filter](analysis-fingerprint-tokenfilter.md) [Hunspell
token filter »](analysis-hunspell-tokenfilter.md)
