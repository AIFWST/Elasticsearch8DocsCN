

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Delete dangling index API](dangling-index-delete.md) [Delete index API
»](indices-delete-index.md)

## 删除别名接口

从别名中删除数据流或索引。

    
    
    response = client.indices.delete_alias(
      index: 'my-data-stream',
      name: 'my-alias'
    )
    puts response
    
    
    DELETE my-data-stream/_alias/my-alias

###Request

"删除<target>/_alias/<alias>"

"删除<target>/_aliases/<alias>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则必须具有别名及其数据流或索引的"管理"索引权限。

### 路径参数

`<alias>`

     (Required, string) Comma-separated list of aliases to remove. Supports wildcards (`*`). To remove all aliases, use `*` or `_all`. 
`<target>`

     (Required, string) Comma-separated list of data streams or indices used to limit the request. Supports wildcards (`*`). 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

[« Delete dangling index API](dangling-index-delete.md) [Delete index API
»](indices-delete-index.md)
