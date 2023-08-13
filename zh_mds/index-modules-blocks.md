

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Index
modules](index-modules.md)

[« Index-level data tier allocation filtering](data-tier-shard-filtering.md)
[Mapper »](index-modules-mapper.md)

## 索引块

索引块限制特定索引上可用的操作类型。这些块有不同的风格，允许阻止写入、读取或元数据操作。可以使用动态索引设置设置/删除块，也可以使用专用 API 添加块，这也确保写入块一旦成功返回给用户，索引的所有分片都正确考虑了块，例如，添加写入块后，所有正在进行的对索引的写入都已完成。

### 索引块设置

以下 _dynamic_ 索引设置确定索引上存在的块：

`index.blocks.read_only`

     Set to `true` to make the index and index metadata read only, `false` to allow writes and metadata changes. 
`index.blocks.read_only_allow_delete`

    

与"index.blocks.write"类似，但也允许删除索引以使更多资源可用。基于磁盘的分片分配器可以自动添加和删除此块。

从索引中删除文档以释放资源(而不是删除索引本身)可能会随着时间的推移增加索引大小。当"index.blocks.read_only_allow_delete"设置为"true"时，不允许删除文档。但是，删除索引本身会释放只读索引块，并使资源几乎立即可用。

当磁盘利用率超过泛洪阶段水位线时，Elasticsearch 会自动添加只读索引块，由 thecluster.routing.allocation.disk.watermark.flood_stage andcluster.routing.allocation.disk.watermark.flood_stage.max_headroom 设置控制，当磁盘利用率低于高水位线时自动删除该块，由 cluster.routing.allocation.disk.watermark.high 和 cluster.routing.allocation.disk.watermark.high.max_ 控制。动态余量设置。请参阅修复水印错误以解决水印问题。

`index.blocks.read`

     Set to `true` to disable read operations against the index. 
`index.blocks.write`

     Set to `true` to disable data write operations against the index. Unlike `read_only`, this setting does not affect metadata. For instance, you can adjust the settings of an index with a `write` block, but you cannot adjust the settings of an index with a `read_only` block. 
`index.blocks.metadata`

     Set to `true` to disable index metadata reads and writes. 

### 添加索引块API

将索引块添加到索引。

    
    
    PUT /my-index-000001/_block/write

####Request

'把 /<index>/_block/<block>'

#### 路径参数

`<index>`

    

(可选，字符串)索引名称的逗号分隔列表或通配符表达式用于限制请求。

默认情况下，您必须显式命名要向其添加块的索引。要允许使用"_all"、"*"或其他通配符表达式向索引添加块，请将"action.destructive_requires_name"设置更改为"false"。您可以在"elasticsearch.yml"文件中或使用群集更新设置 API 更新此设置。

`<block>`

    

(必需，字符串)要添加到索引的块类型。

""的有效值<block>

`metadata`

     Disable metadata changes, such as closing the index. 
`read`

     Disable read operations. 
`read_only`

     Disable write operations and metadata changes. 
`write`

     Disable write operations. However, metadata changes are still allowed. 

#### 查询参数

`allow_no_indices`

    

(可选，布尔值)如果为"false"，则当任何通配符表达式、索引别名或"_all"值仅针对缺少或关闭的索引时，请求将返回错误。即使请求以其他打开的索引为目标，此行为也适用。例如，如果索引以"foo"开头但没有索引以"bar"开头，则以"foo*，bar*"为目标的请求将返回错误。

默认为"真"。

`expand_wildcards`

    

(可选，字符串)通配符模式可以匹配的索引类型。如果请求可以以数据流为目标，则此参数确定通配符表达式是否与隐藏的数据流匹配。支持逗号分隔的值，例如"打开，隐藏"。有效值为：

`all`

     Match any data stream or index, including [hidden](api-conventions.html#multi-hidden "Hidden data streams and indices") ones. 
`open`

     Match open, non-hidden indices. Also matches any non-hidden data stream. 
`closed`

     Match closed, non-hidden indices. Also matches any non-hidden data stream. Data streams cannot be closed. 
`hidden`

     Match hidden data streams and hidden indices. Must be combined with `open`, `closed`, or both. 
`none`

     Wildcard patterns are not accepted. 

默认为"打开"。

`ignore_unavailable`

     (Optional, Boolean) If `false`, the request returns an error if it targets a missing or closed index. Defaults to `false`. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

####Examples

以下示例演示如何添加索引块：

    
    
    PUT /my-index-000001/_block/write

API 返回以下响应：

    
    
    {
      "acknowledged" : true,
      "shards_acknowledged" : true,
      "indices" : [ {
        "name" : "my-index-000001",
        "blocked" : true
      } ]
    }

[« Index-level data tier allocation filtering](data-tier-shard-filtering.md)
[Mapper »](index-modules-mapper.md)
