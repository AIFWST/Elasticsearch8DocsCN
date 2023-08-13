

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Enrich APIs](enrich-apis.md)

[« Get enrich policy API](get-enrich-policy-api.md) [Enrich stats API
»](enrich-stats-api.md)

## 执行扩充策略API

执行现有的扩充策略。

    
    
    response = client.enrich.execute_policy(
      name: 'my-policy'
    )
    puts response
    
    
    PUT /_enrich/policy/my-policy/_execute

###Request

"放置/_enrich/策略/<enrich-policy>/_execute"

"发布/_enrich/策略/<enrich-policy>/_execute"

###Prerequisites

如果您使用 Elasticsearch 安全功能，则必须具备：

* 使用的任何索引的"读取"索引权限 * "enrich_user"内置角色

###Description

使用执行扩充策略 API 为现有扩充策略创建扩充索引。

_enrich index_包含来自策略源索引的文档。扩充索引始终以".enrich-*"开头，是只读的，并且是强制合并的。

扩充索引应仅由扩充处理器使用。避免将扩充索引用于其他目的。

创建后，无法将文档更新或索引到扩充索引。相反，请更新源索引并再次执行扩充策略。这会从更新的源索引创建新的扩充索引。以前的扩充索引将因维护作业延迟而被删除。默认情况下，每 15 分钟完成一次。

由于此 API 请求执行多个操作，因此可能需要一段时间才能返回响应。

### 路径参数

`<enrich-policy>`

     (Required, string) Enrich policy to execute. 

### 查询参数

`wait_for_completion`

     (Required, Boolean) If `true`, the request blocks other enrich policy execution requests until complete. Defaults to `true`. 

[« Get enrich policy API](get-enrich-policy-api.md) [Enrich stats API
»](enrich-stats-api.md)
