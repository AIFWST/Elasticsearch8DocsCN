

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Tokenizer reference](analysis-tokenizers.md)

[« Keyword tokenizer](analysis-keyword-tokenizer.md) [Lowercase tokenizer
»](analysis-lowercase-tokenizer.md)

## 字母标记器

"字母"分词器在遇到不是字母的字符时将文本分解为术语。对于大多数欧洲语言来说，它做得很合理，但对于一些亚洲语言来说却做得很糟糕，因为单词没有用空格分隔。

### 示例输出

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'letter',
        text: "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
      }
    )
    puts response
    
    
    POST _analyze
    {
      "tokenizer": "letter",
      "text": "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
    }

上述句子将产生以下术语：

    
    
    [ The, QUICK, Brown, Foxes, jumped, over, the, lazy, dog, s, bone ]

###Configuration

"字母"分词器不可配置。

[« Keyword tokenizer](analysis-keyword-tokenizer.md) [Lowercase tokenizer
»](analysis-lowercase-tokenizer.md)
