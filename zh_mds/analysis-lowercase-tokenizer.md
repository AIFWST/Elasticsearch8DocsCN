

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Tokenizer reference](analysis-tokenizers.md)

[« Letter tokenizer](analysis-letter-tokenizer.md) [N-gram tokenizer
»](analysis-ngram-tokenizer.md)

## 小写标记器

"小写"分词器，如"字母"分词器，每当遇到不是字母的字符时，都会将文本分解为术语，但它也会小写所有术语。它在功能上等同于"字母"标记器与"小写"标记筛选器的组合，但效率更高，因为它在一次传递中执行这两个步骤。

### 示例输出

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'lowercase',
        text: "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
      }
    )
    puts response
    
    
    POST _analyze
    {
      "tokenizer": "lowercase",
      "text": "The 2 QUICK Brown-Foxes jumped over the lazy dog's bone."
    }

上述句子将产生以下术语：

    
    
    [ the, quick, brown, foxes, jumped, over, the, lazy, dog, s, bone ]

###Configuration

"小写"分词器不可配置。

[« Letter tokenizer](analysis-letter-tokenizer.md) [N-gram tokenizer
»](analysis-ngram-tokenizer.md)
