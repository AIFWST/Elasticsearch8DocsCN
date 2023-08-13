

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Remove duplicates token filter](analysis-remove-duplicates-
tokenfilter.md) [Shingle token filter »](analysis-shingle-tokenfilter.md)

## 反向令牌筛选器

反转流中的每个令牌。例如，您可以使用"反向"过滤器将"cat"更改为"tac"。

反向标记对于基于后缀的搜索非常有用，例如查找以"-ion"结尾的单词或按扩展名搜索文件名。

此过滤器使用 Lucene 的 ReverseStringFilter。

###Example

以下分析 API 请求使用"反向"过滤器来反转"快速狐狸跳转"中的每个令牌：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        filter: [
          'reverse'
        ],
        text: 'quick fox jumps'
      }
    )
    puts response
    
    
    GET _analyze
    {
      "tokenizer" : "standard",
      "filter" : ["reverse"],
      "text" : "quick fox jumps"
    }

筛选器生成以下标记：

    
    
    [ kciuq, xof, spmuj ]

### 添加到分析器

以下创建索引 APIrequest 使用"反向"筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'reverse_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              whitespace_reverse: {
                tokenizer: 'whitespace',
                filter: [
                  'reverse'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT reverse_example
    {
      "settings" : {
        "analysis" : {
          "analyzer" : {
            "whitespace_reverse" : {
              "tokenizer" : "whitespace",
              "filter" : ["reverse"]
            }
          }
        }
      }
    }

[« Remove duplicates token filter](analysis-remove-duplicates-
tokenfilter.md) [Shingle token filter »](analysis-shingle-tokenfilter.md)
