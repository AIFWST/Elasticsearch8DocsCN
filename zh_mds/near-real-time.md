

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Search your
data](search-your-data.md)

[« Long-running searches](async-search-intro.md) [Paginate search results
»](paginate-search-results.md)

## 近实时搜索

文档和索引的概述表明，当文档存储在 Elasticsearch 中时，它会在 1 秒内以实际time_\-_near进行索引和完全搜索。什么定义了近实时搜索？

Lucene，Elasticsearch所基于的Java库，引入了每段搜索的概念。_segment_ 类似于倒排索引，但 Lucene 中的 _index_ 一词表示"段的集合加上一个提交点"。提交后，将新段添加到提交点并清除缓冲区。

位于Elasticsearch和磁盘之间的是文件系统缓存。内存中索引缓冲区中的文档(图 4)被写入一个新段(图 5)。新段首先写入文件系统缓存(这很便宜)，然后再刷新到磁盘(这很昂贵)。但是，在文件进入缓存后，可以像打开和读取任何其他文件一样打开和读取它。

!内存缓冲区中具有新文档的 Lucene 索引

图4.内存缓冲区中具有新文档的 Lucene 索引

Lucene 允许写入和打开新的段，使它们包含的文档可供搜索，而无需执行完整提交。这是一个比提交到磁盘的过程轻得多的过程，并且可以经常执行而不会降低性能。

!缓冲区内容将写入可搜索但尚未提交的段

图5.缓冲区内容写入可搜索但尚未提交的段

在 Elasticsearch 中，编写和打开新段的过程称为 _refresh_。刷新使自上次刷新以来对索引执行的所有操作都可用于搜索。您可以通过以下方式控制刷新：

* 等待刷新间隔 * 设置 ？refresh 选项 * 使用刷新 API 显式完成刷新("POST _refresh")

默认情况下，Elasticsearch 每秒定期刷新索引，但仅限于在过去 30 秒内收到一个或更多搜索请求的索引。这就是为什么我们说 Elasticsearch 有 _near_ 实时搜索：文档更改不会立即搜索，但会在此时间范围内变得可见。

[« Long-running searches](async-search-intro.md) [Paginate search results
»](paginate-search-results.md)
