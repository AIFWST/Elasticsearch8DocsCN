

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Text analysis concepts](analysis-concepts.md)

[« Anatomy of an analyzer](analyzer-anatomy.md) [Stemming »](stemming.md)

## 索引和搜索分析

文本分析在两次发生：

索引时间

     When a document is indexed, any [`text`](text.html "Text type family") field values are analyzed. 
Search time

    

对"文本"字段运行全文搜索时，将分析查询字符串(用户正在搜索的文本)。

搜索时间也称为_query time_。

每次使用的分析器或一组分析规则分别称为 _indexanalyzer_ 或 _search analyzer_。

### 索引和搜索分析器如何协同工作

在大多数情况下，应在索引和搜索时使用相同的分析器。这可确保字段的值和查询字符串更改为相同形式的标记。反过来，这可确保令牌在搜索期间按预期匹配。

**Example**

文档在"文本"字段中使用以下值编制索引：

    
    
    The QUICK brown foxes jumped over the dog!

字段的索引分析器将值转换为标记并规范化它们。在这种情况下，每个标记代表一个单词：

    
    
    [ quick, brown, fox, jump, over, dog ]

然后对这些令牌编制索引。

稍后，用户在同一"文本"字段中搜索：

    
    
    "Quick fox"

用户希望此搜索与之前索引的句子"QUICKbrown 狐狸跳过狗！

但是，查询字符串不包含文档原始文本中使用的确切单词：

* "快速"与"快速" * "狐狸"与"狐狸"

为此，使用相同的分析器分析查询字符串。此分析器生成以下令牌：

    
    
    [ quick, fox ]

为了执行搜索，Elasticsearch 将这些查询字符串标记与"文本"字段中索引的标记进行比较。

代币 |查询字符串 |"文本"字段---|---|---"快速"

|

X

|

X'棕色'

|

|

X"狐狸"

|

X

|

X"跳跃"

|

|

X "结束"

|

|

X"狗"

|

|

X 由于字段值和查询字符串的分析方式相同，因此它们创建了类似的标记。令牌"quick"和"fox"完全匹配。这意味着搜索与包含"快速棕色狐狸跳过狗！'，正如用户所期望的那样。

### 何时使用其他搜索分析器

虽然不太常见，但有时在索引和搜索时间使用不同的分析器是有意义的。为了实现这一点，Elasticsearch 允许您指定一个单独的搜索分析器。

通常，仅当对字段值使用相同的标记形式时，才应指定单独的搜索分析器，并且查询字符串将创建意外或不相关的搜索匹配项。

**Example**

Elasticsearch用于创建一个搜索引擎，该搜索引擎仅匹配以提供的前缀开头的单词。例如，搜索"tr"应该返回"电车"或"比喻"，但绝不返回"出租车"或"蝙蝠"。

文档被添加到搜索引擎的索引中;本文档在"文本"字段中包含一个这样的单词：

    
    
    "Apple"

字段的索引分析器将值转换为标记并规范化它们。在这种情况下，每个标记都表示单词的潜在前缀：

    
    
    [ a, ap, app, appl, apple]

然后对这些令牌编制索引。

稍后，用户在同一"文本"字段中搜索：

    
    
    "appli"

用户希望此搜索仅匹配以"appli"开头的单词，例如"设备"或"应用程序"。搜索不应与"苹果"匹配。

但是，如果使用索引分析器分析此查询字符串，它将生成以下标记：

    
    
    [ a, ap, app, appl, appli ]

当 Elasticsearch 将这些查询字符串标记与为"apple"编制索引的标记进行比较时，它会找到多个匹配项。

代币 |"应用" |"苹果" ---|---|--- "a"

|

X

|

X 'ap'

|

X

|

X"应用程序"

|

X

|

X 'appl'

|

X

|

X 'appli'

|

|

X 这意味着搜索会错误地匹配"苹果"。不仅如此，它还会匹配任何以"a"开头的单词。

若要解决此问题，可以为"text"字段上使用的查询字符串指定不同的搜索分析器。

在这种情况下，可以指定生成单个标记而不是一组前缀的搜索分析器：

    
    
    [ appli ]

此查询字符串令牌仅匹配以"appli"开头的单词的标记，这更符合用户的搜索预期。

[« Anatomy of an analyzer](analyzer-anatomy.md) [Stemming »](stemming.md)
