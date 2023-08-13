

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Tokenizer reference](analysis-tokenizers.md)

[« Standard tokenizer](analysis-standard-tokenizer.md) [UAX URL email
tokenizer »](analysis-uaxurlemail-tokenizer.md)

## 泰语词汇器

"泰语"分词器使用 Java 附带的泰语分词算法将泰语文本分割成单词。通常，其他语言的文本将被视为与"标准"分词器相同。

并非所有 JRE 都支持此分词器。众所周知，它可以与Sun/Oracle和OpenJDK一起使用。如果您的应用程序需要完全可移植，请考虑使用 ICUTokenizer。

### 示例输出

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'thai',
        text: 'การที่ได้ต้องแสดงว่างานดี'
      }
    )
    puts response
    
    
    POST _analyze
    {
      "tokenizer": "thai",
      "text": "การที่ได้ต้องแสดงว่างานดี"
    }

上述句子将产生以下术语：

    
    
    [ การ, ที่, ได้, ต้อง, แสดง, ว่า, งาน, ดี ]

###Configuration

"泰式"分词器不可配置。

[« Standard tokenizer](analysis-standard-tokenizer.md) [UAX URL email
tokenizer »](analysis-uaxurlemail-tokenizer.md)
