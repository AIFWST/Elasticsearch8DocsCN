

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Searchable snapshots APIs](searchable-snapshots-
apis.md)

[« Mount snapshot API](searchable-snapshots-api-mount-snapshot.md)
[Searchable snapshot statistics API »](searchable-snapshots-api-stats.md)

## 缓存统计信息API

检索有关部分装入索引的共享高速缓存的统计信息。

###Request

'获取/_searchable_snapshots/缓存/统计"

'GET /_searchable_snapshots//<node_id>cache/stats'

###Prerequisites

如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。有关更多信息，请参阅安全权限。

### 路径参数

`<node_id>`

     (Optional, string) The names of particular nodes in the cluster to target. For example, `nodeId1,nodeId2`. For node selection options, see [Node specification](cluster.html#cluster-nodes "Node specification"). 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 响应正文

`nodes`

    

(对象)包含请求选择的节点的统计信息。

"节点"的属性

`<node_id>`

    

(对象)包含具有给定标识符的节点的统计信息。

""的属性<node_id>

`shared_cache`

    

(对象)包含有关共享缓存文件的统计信息。

"shared_cache"的属性

`reads`

     (long) Number of times the shared cache is used to read data from. 
`bytes_read_in_bytes`

     (long) The total of bytes read from the shared cache. 
`writes`

     (long) Number of times data from the blob store repository is written in the shared cache. 
`bytes_written_in_bytes`

     (long) The total of bytes written in the shared cache. 
`evictions`

     (long) Number of regions evicted from the shared cache file. 
`num_regions`

     (integer) Number of regions in the shared cache file. 
`size_in_bytes`

     (long) The total size in bytes of the shared cache file. 
`region_size_in_bytes`

     (long) The size in bytes of a region in the shared cache file. 

###Examples

从所有数据节点获取有关部分挂载索引的共享缓存的统计信息：

    
    
    response = client.searchable_snapshots.cache_stats
    puts response
    
    
    GET /_searchable_snapshots/cache/stats

API 返回以下响应：

    
    
    {
      "nodes" : {
        "eerrtBMtQEisohZzxBLUSw" : {
          "shared_cache" : {
            "reads" : 6051,
            "bytes_read_in_bytes" : 5448829,
            "writes" : 37,
            "bytes_written_in_bytes" : 1208320,
            "evictions" : 5,
            "num_regions" : 65536,
            "size_in_bytes" : 1099511627776,
            "region_size_in_bytes" : 16777216
          }
        }
      }
    }

[« Mount snapshot API](searchable-snapshots-api-mount-snapshot.md)
[Searchable snapshot statistics API »](searchable-snapshots-api-stats.md)
