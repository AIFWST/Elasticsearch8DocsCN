

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[How
to](how-to.md) ›[Recipes](recipes.md)

[« Mixing exact search with stemming](mixing-exact-search-with-stemming.md)
[Incorporating static relevance signals into the score »](static-scoring-
signals.md)

## 获得一致的评分

Elasticsearch 使用分片和副本运行的事实增加了在获得良好评分方面的挑战。

#### 分数不可重现

假设同一个用户连续两次运行相同的请求，并且文档两次都没有以相同的顺序返回，这是一种非常糟糕的体验，不是吗？不幸的是，如果您有副本('index.number_of_replicas'大于 0)，则可能会发生这种情况。原因是 Elasticsearch 以循环方式选择查询应该转到的分片，因此如果您连续运行两次相同的查询，它很可能会转到同一分片的不同副本。

现在为什么这是一个问题？指数统计是分数的重要组成部分。由于已删除的文档，这些索引统计信息可能在同一分片的副本之间有所不同。如您所知，当文档被删除或更新时，旧文档不会立即从索引中删除，它只是标记为已删除，并且只有在下次合并此旧文档所属的段时才会从磁盘中删除。但是，出于实际原因，索引统计信息会考虑这些已删除的文档。因此，假设主分片刚刚完成了删除大量已删除文档的大型合并，那么它可能具有与副本(仍然有大量已删除文档)完全不同的索引统计信息，因此分数也不同。

解决此问题的建议方法是使用字符串来标识已登录的用户(例如用户 ID 或会话 ID)作为首选项。这可确保给定用户的所有查询始终会命中相同的分片，因此分数在查询之间保持更加一致。

这种解决方法还有另一个好处：当两个文档具有相同的分数时，默认情况下，它们将按其内部Lucene文档ID(与"_id"无关)进行排序。但是，这些文档 ID 可能在同一分片的副本之间有所不同。因此，通过始终点击相同的分片，我们将获得具有相同分数的文档的更一致的排序。

#### 相关性看起来错误

如果您注意到具有相同内容的两个文档获得不同的分数，或者完全匹配项未排在第一位，则问题可能与分片有关。默认情况下，Elasticsearch 让每个分片负责生成自己的分数。但是，由于索引统计信息是分数的重要贡献者，因此这仅在分片具有类似的索引统计信息时才有效。假设由于文档默认均匀地路由到分片，因此索引统计信息应该非常相似，并且评分将按预期工作。但是，如果您：

* 在索引时使用路由，* 查询多个 _index_ ，* 或索引中的数据太少

那么很有可能 searchRequest 中涉及的所有分片都没有类似的索引统计信息，相关性可能很差。

如果你有一个小数据集，解决此问题的最简单方法是将所有内容索引到具有单个分片('index.number_of_shards：1')的索引中，这是默认值。然后索引统计信息对于所有文档都是相同的，并且分数将是一致的。

否则，解决此问题的建议方法是使用"dfs_query_then_fetch"搜索类型。这将使 Elasticsearch 对所有涉及的分片执行初始往返，询问它们相对于查询的索引统计信息，然后协调节点将合并这些统计信息，并在要求分片执行"查询"阶段时将合并的统计信息与请求一起发送，以便分片可以使用这些全局统计信息而不是自己的统计信息来进行评分。

在大多数情况下，这种额外的往返旅行应该非常便宜。但是，如果您的查询包含大量字段/术语或模糊查询，请注意，单独收集统计信息可能并不便宜，因为必须在术语字典中查找所有术语才能查找统计信息。

[« Mixing exact search with stemming](mixing-exact-search-with-stemming.md)
[Incorporating static relevance signals into the score »](static-scoring-
signals.md)
