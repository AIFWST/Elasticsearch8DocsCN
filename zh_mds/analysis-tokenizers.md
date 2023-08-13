

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md)

[« Whitespace analyzer](analysis-whitespace-analyzer.md) [Character group
tokenizer »](analysis-chargroup-tokenizer.md)

## 分词器引用

_tokenizer_ 接收字符流，将其分解为individual_tokens_(通常是单个单词)，并输出 _tokens_ 流。例如，"空格"分词器在看到任何空格时将文本分解为标记。它将转换文本"快速棕色狐狸！"变成"[快，棕色，狐狸！`.

分词器还负责记录以下内容：

* 每个术语的顺序或_位置_(用于短语和单词邻近查询) * 术语所代表的原始单词的开始和结束_character offsets_(用于突出显示搜索片段)。  * _Token type_，产生的每个术语的分类，如"<ALPHANUM>"、"<HANGUL>"或"<NUM>"。更简单的分析器仅生成"字"令牌类型。

Elasticsearch有许多内置的分词器，可用于构建自定义分析器。

### 面向单词的分词器

以下分词器通常用于将全文标记为单个单词：

标准分词器

     The `standard` tokenizer divides text into terms on word boundaries, as defined by the Unicode Text Segmentation algorithm. It removes most punctuation symbols. It is the best choice for most languages. 
[Letter Tokenizer](analysis-letter-tokenizer.html "Letter tokenizer")

     The `letter` tokenizer divides text into terms whenever it encounters a character which is not a letter. 
[Lowercase Tokenizer](analysis-lowercase-tokenizer.html "Lowercase tokenizer")

     The `lowercase` tokenizer, like the `letter` tokenizer, divides text into terms whenever it encounters a character which is not a letter, but it also lowercases all terms. 
[Whitespace Tokenizer](analysis-whitespace-tokenizer.html "Whitespace
tokenizer")

     The `whitespace` tokenizer divides text into terms whenever it encounters any whitespace character. 
[UAX URL Email Tokenizer](analysis-uaxurlemail-tokenizer.html "UAX URL email
tokenizer")

     The `uax_url_email` tokenizer is like the `standard` tokenizer except that it recognises URLs and email addresses as single tokens. 
[Classic Tokenizer](analysis-classic-tokenizer.html "Classic tokenizer")

     The `classic` tokenizer is a grammar based tokenizer for the English Language. 
[Thai Tokenizer](analysis-thai-tokenizer.html "Thai tokenizer")

     The `thai` tokenizer segments Thai text into words. 

### 部分词词元

这些分词器将文本或单词分解为小片段，以进行部分单词匹配：

N-gram 分词器

     The `ngram` tokenizer can break up text into words when it encounters any of a list of specified characters (e.g. whitespace or punctuation), then it returns n-grams of each word: a sliding window of continuous letters, e.g. `quick` -> `[qu, ui, ic, ck]`. 
[Edge N-Gram Tokenizer](analysis-edgengram-tokenizer.html "Edge n-gram
tokenizer")

     The `edge_ngram` tokenizer can break up text into words when it encounters any of a list of specified characters (e.g. whitespace or punctuation), then it returns n-grams of each word which are anchored to the start of the word, e.g. `quick` -> `[q, qu, qui, quic, quick]`. 

### 结构化文本分词器

以下分词器通常与结构化文本(如标识符、电子邮件地址、邮政编码和路径)一起使用，而不是与全文一起使用：

关键字分词器

     The `keyword` tokenizer is a "noop" tokenizer that accepts whatever text it is given and outputs the exact same text as a single term. It can be combined with token filters like [`lowercase`](analysis-lowercase-tokenfilter.html "Lowercase token filter") to normalise the analysed terms. 
[Pattern Tokenizer](analysis-pattern-tokenizer.html "Pattern tokenizer")

     The `pattern` tokenizer uses a regular expression to either split text into terms whenever it matches a word separator, or to capture matching text as terms. 
[Simple Pattern Tokenizer](analysis-simplepattern-tokenizer.html "Simple
pattern tokenizer")

     The `simple_pattern` tokenizer uses a regular expression to capture matching text as terms. It uses a restricted subset of regular expression features and is generally faster than the `pattern` tokenizer. 
[Char Group Tokenizer](analysis-chargroup-tokenizer.html "Character group
tokenizer")

     The `char_group` tokenizer is configurable through sets of characters to split on, which is usually less expensive than running regular expressions. 
[Simple Pattern Split Tokenizer](analysis-simplepatternsplit-tokenizer.html
"Simple pattern split tokenizer")

     The `simple_pattern_split` tokenizer uses the same restricted regular expression subset as the `simple_pattern` tokenizer, but splits the input at matches rather than returning the matches as terms. 
[Path Tokenizer](analysis-pathhierarchy-tokenizer.html "Path hierarchy
tokenizer")

     The `path_hierarchy` tokenizer takes a hierarchical value like a filesystem path, splits on the path separator, and emits a term for each component in the tree, e.g. `/foo/bar/baz` -> `[/foo, /foo/bar, /foo/bar/baz ]`. 

[« Whitespace analyzer](analysis-whitespace-analyzer.md) [Character group
tokenizer »](analysis-chargroup-tokenizer.md)
