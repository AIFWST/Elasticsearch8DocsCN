

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Text analysis concepts](analysis-concepts.md)

[« Stemming](stemming.md) [Configure text analysis »](configure-text-
analysis.md)

## 代币图

当分词器将文本转换为标记流时，它还会记录以下内容：

* 流中每个代币的"位置" * "位置长度"，令牌跨越的位置数

使用这些，您可以为流创建一个有向无环图，称为 _tokengraph_。在令牌图中，每个位置代表一个节点。每个令牌表示一条边或弧，指向下一个位置。

！令牌图形 QBF EX

###Synonyms

某些令牌筛选器可以将新令牌(如同义词)添加到现有令牌流。这些同义词通常跨越与现有令牌相同的位置。

在下图中，"quick"及其同义词"fast"的位置均为"0"。它们跨越相同的位置。

！令牌图 QBF 同义词 ex

### 多仓位代币

某些令牌筛选器可以添加跨多个位置的令牌。这些可以包括多字同义词的标记，例如使用"atm"作为"自动取款机"的同义词。

但是，只有一些令牌过滤器(称为_graph令牌filters_)准确记录多位置令牌的"位置长度"。这些筛选器包括：

* "synonym_graph" * "word_delimiter_graph"

一些分词器，例如"nori_tokenizer"，也可以准确地将复合代币分解为多位置代币。

在下图中，"域名系统"及其同义词"dns"的位置均为"0"。但是，"dns"的"位置长度"为"3"。图中的其他标记的默认"位置长度"为"1"。

！令牌图形 DNS 同义词 EX

#### 使用令牌图进行搜索

索引忽略"位置长度"属性，不支持包含多位置令牌的令牌图。

但是，查询(如"匹配"或"match_phrase"查询)可以使用这些图形从单个查询字符串生成多个子查询。

**Example**

用户使用"match_phrase"查询运行以下短语的搜索：

"域名系统很脆弱"

在搜索分析期间，"dns"("域名系统"的同义词)将添加到查询字符串的令牌流中。"dns"令牌的"位置长度"为"3"。

！令牌图形 DNS 同义词 EX

"match_phrase"查询使用此图为以下短语生成子查询：

    
    
    dns is fragile
    domain name system is fragile

这意味着查询匹配包含"dns 很脆弱"_或_"域名系统很脆弱"的文档。

#### 无效的令牌图

以下令牌筛选器可以添加跨多个位置的令牌，但仅记录默认的"位置长度""1"：

* "同义词" * "word_delimiter"

这意味着这些筛选器将为包含此类令牌的流生成无效的令牌图。

在下图中，"dns"是"域名系统"的多位置同义词。但是，"dns"的默认"位置长度"值为"1"，导致图形无效。

！令牌图 DNS 无效 ex

避免使用无效的令牌图进行搜索。无效图表可能会导致意外的搜索结果。

[« Stemming](stemming.md) [Configure text analysis »](configure-text-
analysis.md)
