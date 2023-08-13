

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[Conventions and Terminology](sql-concepts.md)

[« Conventions and Terminology](sql-concepts.md) [Security »](sql-
security.md)

## 跨 SQL 和 Elasticsearch 的映射概念

虽然SQL和Elasticsearch对数据的组织方式有不同的术语(以及不同的语义)，但本质上它们的用途是相同的。

因此，让我们从底部开始;这些大致是：

SQL |弹性搜索 |描述 ---|---|--- '列'

|

`field`

|

在这两种情况下，在最低级别，数据存储在包含_one_value的各种数据类型的 _named_ 条目中。SQL 将这样的条目称为 _column_，而 Elasticsearch 称为 _field_。请注意，在 Elasticsearch 中，字段可以包含相同类型的 _multiple_ 值(本质上是一个列表)，而在 SQL 中，_column_ 可以包含所述类型的 _exactly_ onevalue。Elasticsearch SQL将尽最大努力保留SQL语义，并根据查询拒绝那些返回具有多个值的字段。   "行"

|

`document`

|

"列"和"字段"本身不存在;它们是"行"或"文档"的一部分。两者的语义略有不同："行"倾向于_strict_(并且有更多的强制)，而"文档"往往更灵活或松散(同时仍然具有结构)。   "表"

|

`index`

|

执行查询(无论是在 SQL 还是 Elasticsearch 中)的目标。   "架构"

|

_implicit_

|

在RDBMS中，"schema"主要是表的命名空间，通常用作安全边界。Elasticsearch没有为它提供等效的概念。但是，当启用安全性时，Elasticsearch 会自动应用安全实施，以便角色只能看到允许它看到的数据(在 SQL 术语中，其 _schema_ )。   "目录"或"数据库"

|

"集群"实例

|

在SQL中，"目录"或"数据库"可以互换使用，并表示一组模式，即许多表。在 Elasticsearch 中，可用的索引集被分组在一个"集群"中。语义也略有不同;a'database'本质上是另一个命名空间(这可能会对数据的存储方式产生一些影响)，而Elasticsearch的'cluster'是一个运行时实例，或者更确切地说是一组至少一个Elasticsearch实例(通常运行分布式)。在实践中，这意味着在SQL中，一个实例中可以有多个目录，而在Elasticsearchone中，只能使用_one_。   "集群"

|

"群集"(联合)

|

传统上，在SQL中，_cluster_是指单个RDBMS实例，其中包含许多"目录"或"数据库"(见上文)。同一个词也可以在Elasticsearch中重复使用，但它的语义澄清了一点。

虽然RDBMS往往只有一个正在运行的实例，但在一台机器上(_not_分布式)，Elasticsearch则相反，默认情况下，它是分布式的和多实例的。

此外，Elasticsearch的"集群"可以以_federated_的方式连接到其他"集群"，因此"集群"意味着：

单个集群：：多个 Elasticsearch 实例通常分布在机器上，在同一命名空间内运行。多个集群：：多个集群，每个集群都有自己的命名空间，在联合设置中相互连接(请参阅跨集群搜索)。   正如人们所看到的，虽然概念之间的映射并不完全是一对一的，语义也有些不同，但共同点多于差异。事实上，由于SQL声明性的性质，许多概念可以在Elasticsearch中透明地移动，并且两者的术语可能会在材料的其余部分互换使用。

[« Conventions and Terminology](sql-concepts.md) [Security »](sql-
security.md)
