

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Tokenizer reference](analysis-tokenizers.md)

[« Edge n-gram tokenizer](analysis-edgengram-tokenizer.md) [Letter tokenizer
»](analysis-letter-tokenizer.md)

## 关键字词词器

"关键字"分词器是一个"noop"分词器，它接受给定的任何文本，并输出与单个术语完全相同的文本。它可以与令牌过滤器结合使用以规范输出，例如小写电子邮件地址。

### 示例输出

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'keyword',
        text: 'New York'
      }
    )
    puts response
    
    
    POST _analyze
    {
      "tokenizer": "keyword",
      "text": "New York"
    }

上述句子将产生以下术语：

    
    
    [ New York ]

### 与令牌筛选器结合使用

您可以将"关键字"分词器与分词过滤器结合使用，以规范结构化数据，例如产品 ID 或电子邮件地址。

例如，以下分析 APIrequest 使用"关键字"分词器和"小写"筛选器将电子邮件地址转换为小写。

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'keyword',
        filter: [
          'lowercase'
        ],
        text: 'john.SMITH@example.COM'
      }
    )
    puts response
    
    
    POST _analyze
    {
      "tokenizer": "keyword",
      "filter": [ "lowercase" ],
      "text": "john.SMITH@example.COM"
    }

该请求生成以下令牌：

    
    
    [ john.smith@example.com ]

###Configuration

"关键字"分词器接受以下参数：

`buffer_size`

|

单次传入术语缓冲区的字符数。 默认值为"256"。术语缓冲区将按此大小增长，直到所有文本都被使用完毕。建议不要更改此设置。   ---|--- « 边缘 n-gram 分词器 字母分词器