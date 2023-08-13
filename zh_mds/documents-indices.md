

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[What is
Elasticsearch?](elasticsearch-intro.md)

[« What is Elasticsearch?](elasticsearch-intro.md) [Information out: search
and analyze »](search-analyze.md)

## 数据输入：文档和索引

Elasticsearch是一个分布式文档存储。Elasticsearch 不是将信息存储为列式数据行，而是存储已序列化为 JSON 文档的复杂数据结构。当集群中有多个 Elasticsearchnode 时，存储的文档分布在整个集群中，并且可以立即从任何节点访问。

存储文档时，会在 1 秒内近乎实时地对其进行索引和完全搜索。Elasticsearch使用一种称为倒排索引的数据结构，支持非常快速的全文搜索。倒排索引列出任何文档中出现的每个唯一单词，并标识每个单词出现的所有文档。

可以将索引视为文档的优化集合，每个文档都是字段的集合，字段是包含数据的键值对。默认情况下，Elasticsearch 索引每个字段中的所有数据，并且每个索引字段都有一个专用的、优化的数据结构。例如，文本字段存储在倒排索引中，数值和地理字段存储在 BKD 树中。使用每个字段的数据结构来组合和返回搜索结果的能力是 Elasticsearch 如此快速的原因。

Elasticsearch还具有无模式的能力，这意味着可以在不明确指定如何处理文档中可能出现的每个不同字段的情况下对文档进行索引。启用动态映射后，Elasticsearch 会自动检测新字段并将其添加到索引中。这种默认行为使得索引和浏览数据变得容易 - 只需开始索引文档，Elasticsearch 将检测布尔值、浮点和整数值、日期和字符串并将其映射到适当的 Elasticsearch 数据类型。

但是，最终，您比Elasticsearch更了解您的数据以及如何使用它。您可以定义规则来控制动态映射，并显式定义映射以完全控制字段的存储和索引方式。

通过定义自己的映射，您可以：

* 区分全文字符串字段和精确值字符串字段 * 执行特定于语言的文本分析 * 优化字段以进行部分匹配 * 使用自定义日期格式 * 使用无法自动检测的数据类型，如"geo_point"和"geo_shape"

出于不同的目的以不同的方式为同一字段编制索引通常很有用。例如，您可能希望将字符串字段索引为用于全文搜索的文本字段和用于排序或聚合数据的关键字字段。或者，可以选择使用多个语言分析器来处理包含用户输入的字符串字段的内容。

在索引编制期间应用于全文字段的分析链也在搜索时使用。查询全文字段时，在索引中查找术语之前，查询文本将进行相同的分析。

[« What is Elasticsearch?](elasticsearch-intro.md) [Information out: search
and analyze »](search-analyze.md)
