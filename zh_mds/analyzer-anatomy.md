

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Text analysis concepts](analysis-concepts.md)

[« Text analysis concepts](analysis-concepts.md) [Index and search analysis
»](analysis-index-search-time.md)

## 分析仪剖析

_analyzer_ - 无论是内置的还是自定义的 - 只是一个包含三个较低级别的构建块的包：_character filters_，_tokenizers_和_token filters_。

内置分析器将这些构建基块预先打包到适用于不同语言和文本类型的分析器中。Elasticsearch还公开了各个构建块，以便可以将它们组合在一起以定义新的"自定义"分析器。

### 字符筛选器

_character filter_以字符流的形式接收原始文本，并可以通过添加、删除或更改字符来转换流。例如，字符过滤器可用于将印度教-阿拉伯数字 (٠١٢٣٤٥٦٧٨٩) 转换为阿拉伯-拉丁等效数字 (0123456789)，或<b>从流中删除 HTML 元素(如"')。

分析器可以具有按顺序应用的零个或多个字符筛选器。

###Tokenizer

_tokenizer_ 接收字符流，将其分解为individual_tokens_(通常是单个单词)，并输出 _tokens_ 流。例如，"空格"分词器在看到任何空格时将文本分解为标记。它将转换文本"快速棕色狐狸！"变成"[快，棕色，狐狸！`.

分词器还负责记录每个术语的顺序或_位置_以及术语所代表的原始单词的开始和结束_character offsets_。

分析器必须具有"恰好一个"标记器。

### 令牌筛选器

_token filter_接收令牌流，可以添加、删除或更改令牌。例如，"小写"令牌筛选器将所有令牌转换为小写，"stop"令牌筛选器从令牌流中删除常用单词(_stop words_)，如"the"，"同义词"令牌筛选器将同义词引入令牌流。

不允许令牌筛选器更改每个令牌的位置或字符偏移量。

分析器可以具有按顺序应用的标记筛选器，这些筛选器按顺序应用。

[« Text analysis concepts](analysis-concepts.md) [Index and search analysis
»](analysis-index-search-time.md)
