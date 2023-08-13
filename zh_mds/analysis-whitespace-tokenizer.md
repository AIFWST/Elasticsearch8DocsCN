

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Tokenizer reference](analysis-tokenizers.md)

[« UAX URL email tokenizer](analysis-uaxurlemail-tokenizer.md) [Token filter
reference »](analysis-tokenfilters.md)

## 空格标记器

"空格"分词器在遇到空格字符时将文本分解为术语。

### 示例输出

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'whitespace',
        text: "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
      }
    )
    puts response
    
    
    POST _analyze
    {
      "tokenizer": "whitespace",
      "text": "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
    }

上述句子将产生以下术语：

    
    
    [ The, 2, QUICK, Brown-Foxes, jumped, over, the, lazy, dog's, bone. ]

###Configuration

"空格"分词器接受以下参数：

`max_token_length`

|

最大令牌长度。如果看到超过此长度的令牌，则以"max_token_length"间隔拆分。默认为"255"。   ---|--- « UAX URL 电子邮件标记器 令牌过滤器参考 »