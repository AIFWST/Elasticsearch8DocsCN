

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Create index API](indices-create-index.md) [Create or update component
template API »](indices-component-template.md)

## 创建或更新别名API

将数据流或索引添加到别名。

    
    
    response = client.indices.put_alias(
      index: 'my-data-stream',
      name: 'my-alias'
    )
    puts response
    
    
    PUT my-data-stream/_alias/my-alias

###Request

"发布<target>/_alias/<alias>"

"发布<target>/_aliases/<alias>"

"放<target>/_alias/<alias>"

"放<target>/_aliases/<alias>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则必须对别名及其数据流或索引具有"管理"索引权限。

### 路径参数

`<alias>`

     (Required, string) Alias to update. If the alias doesn't exist, the request creates it. Index alias names support [date math](api-conventions.html#api-date-math-index-names "Date math support in index and index alias names"). 
`<target>`

     (Required, string) Comma-separated list of data streams or indices to add. Supports wildcards (`*`). Wildcard patterns that match both data streams and indices return an error. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 请求正文

`filter`

     (Optional, [Query DSL object](query-dsl.html "Query DSL") Query used to limit documents the alias can access. 
`index_routing`

     (Optional, string) Value used to route indexing operations to a specific shard. If specified, this overwrites the `routing` value for indexing operations. Data stream aliases don't support this parameter. 
`is_hidden`

     (Optional, Boolean) If `true`, the alias is [hidden](api-conventions.html#multi-hidden "Hidden data streams and indices"). Defaults to `false`. All data streams or indices for the alias must have the same `is_hidden` value. 
`is_write_index`

    

(可选，布尔值)如果为"true"，则设置别名的写入索引或数据流。

如果别名指向多个索引或数据流，并且未设置"is_write_index"，则该别名将拒绝写入请求。如果索引别名指向 oneindex 并且未设置"is_write_index"，则该索引会自动充当写入索引。数据流别名不会自动设置写入数据流，即使别名指向一个数据流也是如此。

`routing`

     (Optional, string) Value used to route indexing and search operations to a specific shard. Data stream aliases don't support this parameter. 
`search_routing`

     (Optional, string) Value used to route search operations to a specific shard. If specified, this overwrites the `routing` value for search operations. Data stream aliases don't support this parameter. 

[« Create index API](indices-create-index.md) [Create or update component
template API »](indices-component-template.md)
