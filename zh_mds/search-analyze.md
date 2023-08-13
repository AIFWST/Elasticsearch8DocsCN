

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[What is
Elasticsearch?](elasticsearch-intro.md)

[« Data in: documents and indices](documents-indices.md) [Scalability and
resilience: clusters, nodes, and shards »](scalability.md)

## 信息输出：搜索和分析

虽然您可以将 Elasticsearch 用作文档存储并检索文档及其元数据，但真正的力量来自于能够轻松访问基于 Apache Lucene 搜索引擎库构建的全套搜索功能。

Elasticsearch 提供了一个简单、一致的 REST API，用于管理集群、索引和搜索数据。出于测试目的，您可以直接从命令行或通过 Kibana 中的开发者控制台轻松提交请求。在您的应用程序中，您可以将Elasticsearchclient用于您选择的语言：Java，JavaScript，Go，.NET，PHP，Perl，Python或Ruby。

#### 搜索您的数据

Elasticsearch REST API 支持结构化查询、全文查询和结合两者的复杂查询。结构化查询类似于可以在 SQL 中构造的查询类型。例如，您可以在"员工"索引中搜索"性别"和"年龄"字段，并按"hire_date"字段对匹配项进行排序。全文查询查找与查询字符串匹配的所有文档，并返回按 _relevance_ 排序的文档 - 它们对搜索词的匹配程度。

除了搜索单个字词外，您还可以执行短语搜索、相似性搜索和前缀搜索，并获取自动完成建议。

有要搜索的地理空间或其他数值数据？Elasticsearch在优化的数据结构中索引非文本数据，支持高性能地理和数字查询。

您可以使用Elasticsearch全面的JSON样式查询语言(Query DSL)访问所有这些搜索功能。您还可以构建 SQL 样式的查询来在 Elasticsearch 中本地搜索和聚合数据，JDBC 和 ODBC 驱动程序使广泛的第三方应用程序能够通过 SQL 与 Elasticsearch 进行交互。

#### 分析您的数据

Elasticsearch 聚合使您能够构建复杂的数据摘要，并深入了解关键指标、模式和趋势。聚合不是简单地找到众所周知的"大海捞针"，而是使您能够回答以下问题：

* 大海捞针有多少针？  * 针的平均长度是多少？  * 针的中位数长度是多少，按制造商细分？  * 在过去六个月中，每年大海捞针中添加了多少针？

您还可以使用聚合来回答更微妙的问题，例如：

* 您最受欢迎的针头制造商是什么？  * 是否有任何不寻常或异常的针块？

由于聚合利用了用于搜索的相同数据结构，因此它们也非常快。这使您能够实时分析和可视化数据。您的报告和仪表板会随着数据的变化而更新，因此您可以根据最新信息采取措施。

此外，聚合与搜索请求一起运行。您可以在单个请求中同时搜索文档、筛选结果并针对相同的数据执行分析。而且，由于聚合是在特定搜索的上下文中计算的，因此您不仅显示所有 size70 针的计数，还显示与用户搜索条件匹配的 70 号针的计数，例如，所有 70 号_non条embroidery_needles。

##### 但是等等，还有更多

想要自动分析时间序列数据？您可以使用机器学习功能在数据中创建正常行为的准确基线并识别异常模式。通过机器学习，您可以检测：

* 与值、计数或频率的时间偏差相关的异常 * 统计稀有度 * 群体成员的异常行为

最好的部分是什么？无需指定算法、模型或其他与数据科学相关的配置即可执行此操作。

[« Data in: documents and indices](documents-indices.md) [Scalability and
resilience: clusters, nodes, and shards »](scalability.md)
