

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search APIs](search.md)

[« Reciprocal rank fusion](rrf.md) [Clear scroll API »](clear-scroll-
api.md)

## 滚动接口

我们不再建议使用滚动 API 进行深度分页。如果需要在分页超过 10，000 次命中时保留索引状态，请将"search_after"参数与时间点 (PIT) 一起使用。

检索滚动搜索的下一批结果。

    
    
    GET /_search/scroll
    {
      "scroll_id" : "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAD4WYm9laVYtZndUQlNsdDcwakFMNjU1QQ=="
    }

###Request

'GET /_search/scroll/' [7.0.0<scroll_id>] 在 7.0.0 中已弃用。

"获取/_search/滚动"

"POST /_search/scroll/" [7.0.0<scroll_id>] 在 7.0.0 中已弃用。

"发布/_search/滚动"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"读取"索引权限。

###Description

您可以使用滚动 API 从单滚动搜索请求中检索大量结果。

滚动 API 需要滚动 ID。要获取滚动 ID，请提交包含"滚动"查询参数的搜索 API 请求。"scroll"参数指示 Elasticsearch 应保留请求的搜索上下文多长时间。

搜索响应在"_scroll_id"响应正文参数中返回滚动 ID。然后，您可以将滚动 ID 与滚动 API 一起使用，以检索请求的下一批结果。如果启用了 Elasticsearch 安全功能，则对特定滚动 ID 结果的访问仅限于提交搜索的用户或 API 密钥。

您还可以使用滚动 API 指定新的"滚动"参数，以延长或缩短搜索上下文的保留期。

请参阅滚动搜索结果。

滚动搜索的结果反映了初始搜索请求时的索引状态。后续索引或文档更改仅影响以后的搜索和滚动请求。

### 路径参数

`<scroll_id>`

    

[7.0.0] 在 7.0.0 中已弃用。 (可选，字符串)搜索的滚动 ID。

滚动 ID 可以很长。我们建议仅使用"scroll_id"请求正文参数指定滚动 ID。

### 查询参数

`scroll`

    

(可选，时间值)句点保留用于滚动的搜索上下文。请参阅滚动搜索结果。

此值将覆盖原始搜索 API 请求的"scroll"参数设置的持续时间。

默认情况下，此值不能超过"1d"(24 小时)。您可以使用"search.max_keep_alive"群集级别设置更改此限制。

您还可以使用"scroll"请求正文参数指定此值。如果同时指定了这两个参数，则仅使用查询参数。

`scroll_id`

    

[7.0.0] 在 7.0.0 中已弃用。 (可选，字符串)用于搜索的滚动 ID。

滚动 ID 可以很长。我们建议仅使用"scroll_id"请求正文参数指定滚动 ID。

`rest_total_hits_as_int`

     (Optional, Boolean) If `true`, the API response's `hit.total` property is returned as an integer. If `false`, the API response's `hit.total` property is returned as an object. Defaults to `false`. 

### 请求正文

`scroll`

    

(可选，时间值)句点保留用于滚动的搜索上下文。请参阅滚动搜索结果。

此值将覆盖原始搜索 API 请求的"scroll"参数设置的持续时间。

默认情况下，此值不能超过"1d"(24 小时)。您可以使用"search.max_keep_alive"群集级别设置更改此限制。

您还可以使用"scroll"查询参数指定此值。如果同时指定了这两个参数，则仅使用查询参数。

`scroll_id`

     (Required, string) Scroll ID for the search. 

### 响应正文

滚动 API 返回与搜索 API 相同的响应正文。请参阅搜索 API 的响应正文参数。

[« Reciprocal rank fusion](rrf.md) [Clear scroll API »](clear-scroll-
api.md)
