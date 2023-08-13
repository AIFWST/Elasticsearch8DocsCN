

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Alias exists API](indices-alias-exists.md) [Analyze API »](indices-
analyze.md)

## 别名API

在单个原子操作中执行一个或多个别名操作。

    
    
    response = client.indices.update_aliases(
      body: {
        actions: [
          {
            add: {
              index: 'my-data-stream',
              alias: 'my-alias'
            }
          }
        ]
      }
    )
    puts response
    
    
    POST _aliases
    {
      "actions": [
        {
          "add": {
            "index": "my-data-stream",
            "alias": "my-alias"
          }
        }
      ]
    }

###Request

"发布_aliases"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有以下索引权限：

    * To use the `add` or `remove` action, you must have the `manage` index privilege for the alias and its data streams or indices. 
    * To use the `remove_index` action, you must have the `manage` index privilege for the index. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 请求正文

`actions`

    

(必需，对象数组)要执行的操作。

"操作"对象的属性

`<action>`

    

(必填，对象)关键是操作类型。至少需要一个操作。

有效的<action>""键

`add`

     Adds a data stream or index to an alias. If the alias doesn't exist, the `add` action creates it. 
`remove`

     Removes a data stream or index from an alias. 
`remove_index`

     Deletes an index. You cannot use this action on aliases or data streams. 

对象正文包含别名的选项。支持空对象。

""的属性<action>

`alias`

     (Required*, string) Alias for the action. Index alias names support [date math](api-conventions.html#api-date-math-index-names "Date math support in index and index alias names"). If `aliases` is not specified, the `add` and `remove` actions require this parameter. For the `remove` action, this parameter supports wildcards (`*`). The `remove_index` action doesn't support this parameter. 
`aliases`

     (Required*, array of strings) Aliases for the action. Index alias names support [date math](api-conventions.html#api-date-math-index-names "Date math support in index and index alias names"). If `alias` is not specified, the `add` and `remove` actions require this parameter. For the `remove` action, this parameter supports wildcards (`*`). The `remove_index` action doesn't support this parameter. 

`filter`

    

(可选，查询 DSL 对象 用于限制别名可以访问的文档的查询。

只有"添加"操作支持此参数。

`index`

     (Required*, string) Data stream or index for the action. Supports wildcards (`*`). If `indices` is not specified, this parameter is required. For the `add` and `remove_index` actions, wildcard patterns that match both data streams and indices return an error. 
`indices`

     (Required*, array of strings) Data streams or indices for the action. Supports wildcards (`*`). If `index` is not specified, this parameter is required. For the `add` and `remove_index` actions, wildcard patterns that match both data streams and indices return an error. 

`index_routing`

    

(可选，字符串)用于将索引操作路由到特定分片的值。如果指定，这将覆盖索引操作的"路由"值。数据流别名不支持此参数。

只有"添加"操作支持此参数。

`is_hidden`

    

(可选，布尔值)如果为"true"，则隐藏别名。默认为"假"。别名的所有数据流或索引必须具有相同的"is_hidden"值。

只有"添加"操作支持此参数。

`is_write_index`

    

(可选，布尔值)如果为"true"，则设置别名的写入索引或数据流。

如果别名指向多个索引或数据流，并且未设置"is_write_index"，则该别名将拒绝写入请求。如果索引别名指向 oneindex 并且未设置"is_write_index"，则该索引会自动充当写入索引。数据流别名不会自动设置写入数据流，即使别名指向一个数据流也是如此。

只有"添加"操作支持此参数。

`must_exist`

     (Optional, Boolean) If `true`, the alias must exist to perform the action. Defaults to `false`. Only the `remove` action supports this parameter. 

`routing`

    

(可选，字符串)用于将索引和搜索操作路由到特定分片的值。数据流别名不支持此参数。

只有"添加"操作支持此参数。

`search_routing`

    

(可选，字符串)用于将搜索操作路由到特定分片的值。如果指定，这将覆盖搜索操作的"路由"值。数据流别名不支持此参数。

只有"添加"操作支持此参数。

[« Alias exists API](indices-alias-exists.md) [Analyze API »](indices-
analyze.md)
