

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md)

[« Specify an analyzer](specify-analyzer.md) [Fingerprint analyzer
»](analysis-fingerprint-analyzer.md)

## 内置分析器参考

Elasticsearch 附带了广泛的内置分析器，无需进一步配置即可在任何索引中使用：

标准分析仪

     The `standard` analyzer divides text into terms on word boundaries, as defined by the Unicode Text Segmentation algorithm. It removes most punctuation, lowercases terms, and supports removing stop words. 
[Simple Analyzer](analysis-simple-analyzer.html "Simple analyzer")

     The `simple` analyzer divides text into terms whenever it encounters a character which is not a letter. It lowercases all terms. 
[Whitespace Analyzer](analysis-whitespace-analyzer.html "Whitespace analyzer")

     The `whitespace` analyzer divides text into terms whenever it encounters any whitespace character. It does not lowercase terms. 
[Stop Analyzer](analysis-stop-analyzer.html "Stop analyzer")

     The `stop` analyzer is like the `simple` analyzer, but also supports removal of stop words. 
[Keyword Analyzer](analysis-keyword-analyzer.html "Keyword analyzer")

     The `keyword` analyzer is a "noop" analyzer that accepts whatever text it is given and outputs the exact same text as a single term. 
[Pattern Analyzer](analysis-pattern-analyzer.html "Pattern analyzer")

     The `pattern` analyzer uses a regular expression to split the text into terms. It supports lower-casing and stop words. 
[Language Analyzers](analysis-lang-analyzer.html "Language analyzers")

     Elasticsearch provides many language-specific analyzers like `english` or `french`. 
[Fingerprint Analyzer](analysis-fingerprint-analyzer.html "Fingerprint
analyzer")

     The `fingerprint` analyzer is a specialist analyzer which creates a fingerprint which can be used for duplicate detection. 

### 自定义分析器

如果找不到适合您需求的分析器，可以创建一个"自定义"分析器，该分析器结合了相应的字符筛选器、分词器和标记筛选器。

[« Specify an analyzer](specify-analyzer.md) [Fingerprint analyzer
»](analysis-fingerprint-analyzer.md)
