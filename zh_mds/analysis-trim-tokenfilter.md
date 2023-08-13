

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Synonym graph token filter](analysis-synonym-graph-tokenfilter.md)
[Truncate token filter »](analysis-truncate-tokenfilter.md)

## 修剪令牌筛选器

从流中的每个标记中删除前导和尾随空格。虽然这可以更改令牌的长度，但"修剪"过滤器不会更改令牌的偏移量。

"trim"过滤器使用Lucene的TrimFilter。

许多常用的分词器(如"标准"或"空白"分词器)默认删除空格。使用这些分词器时，无需添加单独的"修剪"过滤器。

###Example

要查看"trim"过滤器的工作原理，您首先需要生成一个包含空格的标记。

以下分析 API 请求使用"关键字"分词器为"fox"生成令牌。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'keyword',
        text: ' fox '
      }
    )
    puts response
    
    
    GET _analyze
    {
      "tokenizer" : "keyword",
      "text" : " fox "
    }

API 返回以下响应。请注意，""fox""标记包含原始文本的空格。请注意，尽管更改了令牌的长度，但"start_offset"和"end_offset"保持不变。

    
    
    {
      "tokens": [
        {
          "token": " fox ",
          "start_offset": 0,
          "end_offset": 5,
          "type": "word",
          "position": 0
        }
      ]
    }

要删除空格，请将"trim"筛选器添加到上一个分析 API请求。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'keyword',
        filter: [
          'trim'
        ],
        text: ' fox '
      }
    )
    puts response
    
    
    GET _analyze
    {
      "tokenizer" : "keyword",
      "filter" : ["trim"],
      "text" : " fox "
    }

API 返回以下响应。返回的"fox"标记不包含任何前导或尾随空格。

    
    
    {
      "tokens": [
        {
          "token": "fox",
          "start_offset": 0,
          "end_offset": 5,
          "type": "word",
          "position": 0
        }
      ]
    }

### 添加到分析器

以下创建索引 APIrequest 使用"trim"筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'trim_example',
      body: {
        settings: {
          analysis: {
            analyzer: {
              keyword_trim: {
                tokenizer: 'keyword',
                filter: [
                  'trim'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT trim_example
    {
      "settings": {
        "analysis": {
          "analyzer": {
            "keyword_trim": {
              "tokenizer": "keyword",
              "filter": [ "trim" ]
            }
          }
        }
      }
    }

[« Synonym graph token filter](analysis-synonym-graph-tokenfilter.md)
[Truncate token filter »](analysis-truncate-tokenfilter.md)
