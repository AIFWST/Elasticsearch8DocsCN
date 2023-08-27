

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[What is
Elasticsearch?](elasticsearch-intro.md)

[« What is Elasticsearch?](elasticsearch-intro.md) [Information out: search
and analyze »](search-analyze.md)

# Data In：文档和索引

## Elasticsearch的文档以JSON形式存储
Elasticsearch是一个分布式文档存储。Elasticsearch 不是将信息存储为列式数据行，而是存储已序列化为 JSON 文档的复杂数据结构。当集群中有多个 Elasticsearch node 时，存储的文档分布在整个集群中，并且可以立即从任何节点访问。

存储文档时，会在 1 秒内近乎实时地对其进行索引和完全搜索。Elasticsearch使用一种称为倒排索引的数据结构，支持非常快速的全文搜索。倒排索引列出任何文档中出现的每个唯一单词，并标识每个单词出现的所有文档。

可以将索引视为文档的优化集合，每个文档都是字段的集合，字段是包含数据的键值对。
默认情况下，在Elasticsearch 索引创建阶段，会索引每个字段中的所有数据，并且每个索引字段都有一个专用的、优化的数据结构。例如，文本字段存储在倒排索引中，数值和地理字段存储在 BKD 树中。
- 使用每个字段的数据结构来组合和返回搜索结果的能力是 Elasticsearch 如此快速的原因。

## Elasticsearch的Schema-Less 模式
### 什么是schema?
对于Elasticsearch的一个索引库来说使用`GET /index_name`
可以查看索引中的所有字段和各个字段的类型，即schema。
### 什么是schema-less?
Elasticsearch还具有**schema-less**的能力，这意味着可以不明确定义索引的schema。
向索引中添加schema中没有定义的字段，ElasticSearch也可以对文档进行索引。
启用**动态映射**（dynamic mapping）后，Elasticsearch 会自动检测新字段的类型，如布尔值、浮点和整数值、日期和字符串等，并将其映射到适当的 Elasticsearch 数据类型添加到索引库中。
### schema-less模式的优缺点
优势：这种默认行为使得索引和浏览数据变得容易。
劣势：当用户错误地导入数据时，会破坏索引的结构，不会报错或者提示。我在使用ElasticSearch的动态映射功能时，常常苦恼于其他同事的错误操作，而导致重新刷库。此外，Elasticsearch远没有用户自己了解数据和使用意图，它只能识别出数据的简单类型，而无法自动了解用户的意图，定义更复杂的数据类型。

例如，用户通过定义规则来控制动态映射，可以显式定义自己的映射，更好地控制字段的存储和索引方式：
 
* 区分full-text 字符串字段和精确值（exact value）字符串字段 
* 执行特定语言的文本分析
* 优化字段以进行部分匹配 
* 使用自定义的日期格式
* 使用无法自动检测的数据类型，如"geo_point"和"geo_shape"

在实际的搜索索引中，还会出于不同的目的为同一字段定义不同的数据类型。
例如，可能希望将字符串字段title索引为用于全文搜索的文本text字段和用于排序或聚合数据的关键字keyword字段。
或者，希望选择使用多个语言分析器来处理包含用户输入的字符串字段的内容。

在创建索引的期间，应用于全文字段的分析链也在搜索时使用。
查询全文字段时，在索引中查找术语之前，查询文本将进行相同的分析。

[« What is Elasticsearch?](elasticsearch-intro.md) [Information out: search
and analyze »](search-analyze.md)
