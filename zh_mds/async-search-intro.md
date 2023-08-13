

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Search your
data](search-your-data.md)

[« Highlighting](highlighting.md) [Near real-time search »](near-real-
time.md)

## 长时间运行的搜索

Elasticsearch 通常允许您快速搜索大量数据。在某些情况下，搜索在多个分片上执行，可能针对大型数据集或多个远程集群执行，其结果预计不会在毫秒内返回。当您需要执行长时间运行的搜索时，同步等待返回其结果并不理想。相反，异步搜索允许您提交_异步_执行的搜索请求，监视请求的进度，并在稍后阶段检索结果。您还可以在部分结果可用时但在搜索完成之前检索部分结果。

您可以使用提交异步搜索 API 提交异步搜索请求。获取异步搜索 API 允许您监视异步搜索请求的进度并检索其结果。可以通过删除异步搜索 API 删除正在进行的异步搜索。

[« Highlighting](highlighting.md) [Near real-time search »](near-real-
time.md)
