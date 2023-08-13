

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Index recovery API](indices-recovery.md) [Index shard stores API
»](indices-shards-stores.md)

## 索引段接口

返回有关索引分片中 Lucene 段的低级别信息。对于数据流，API 返回有关流的支持索引的信息。

    
    
    response = client.indices.segments(
      index: 'my-index-000001'
    )
    puts response
    
    
    GET /my-index-000001/_segments

###Request

"获取/<target>/_segments"

"得到/_segments"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"监控"或"管理"索引权限。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases used to limit the request. Supports wildcards (`*`). To target all data streams and indices, omit this parameter or use `*` or `_all`. 

### 查询参数

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

### 响应正文

`<segment>`

     (String) Name of the segment, such as `_0`. The segment name is derived from the segment generation and used internally to create file names in the directory of the shard. 
`generation`

     (Integer) Generation number, such as `0`. Elasticsearch increments this generation number for each segment written. Elasticsearch then uses this number to derive the segment name. 
`num_docs`

     (Integer) The number of documents as reported by Lucene. This excludes deleted documents and counts any [nested documents](nested.html "Nested field type") separately from their parents. It also excludes documents which were indexed recently and do not yet belong to a segment. 
`deleted_docs`

     (Integer) The number of deleted documents as reported by Lucene, which may be higher or lower than the number of delete operations you have performed. This number excludes deletes that were performed recently and do not yet belong to a segment. Deleted documents are cleaned up by the [automatic merge process](index-modules-merge.html "Merge") if it makes sense to do so. Also, Elasticsearch creates extra deleted documents to internally track the recent history of operations on a shard. 
`size_in_bytes`

     (Integer) Disk space used by the segment, such as `50kb`. 
`committed`

    

(布尔值)如果为"true"，则段将同步到磁盘。同步的分段可以在硬重启后幸存下来。

如果为"false"，则来自未提交段的数据也存储在事务日志中，以便 Elasticsearch 能够在下一次启动时重放更改。

`search`

    

(布尔值)如果为"true"，则细分受众群是可搜索的。

如果为"false"，则段很可能已写入磁盘，但需要刷新才能搜索。

`version`

     (String) Version of Lucene used to write the segment. 
`compound`

     (Boolean) If `true`, Lucene merged all files from the segment into a single file to save file descriptors. 
`attributes`

     (Object) Contains information about whether high compression was enabled. 

###Examples

#### 获取特定数据流或索引的段信息

    
    
    response = client.indices.segments(
      index: 'test'
    )
    puts response
    
    
    GET /test/_segments

#### 获取多个数据流和索引的段信息

    
    
    response = client.indices.segments(
      index: 'test1,test2'
    )
    puts response
    
    
    GET /test1,test2/_segments

#### 获取集群中所有数据流和索引的分段信息

    
    
    response = client.indices.segments
    puts response
    
    
    GET /_segments

API 返回以下响应：

    
    
    {
      "_shards": ...
      "indices": {
        "test": {
          "shards": {
            "0": [
              {
                "routing": {
                  "state": "STARTED",
                  "primary": true,
                  "node": "zDC_RorJQCao9xf9pg3Fvw"
                },
                "num_committed_segments": 0,
                "num_search_segments": 1,
                "segments": {
                  "_0": {
                    "generation": 0,
                    "num_docs": 1,
                    "deleted_docs": 0,
                    "size_in_bytes": 3800,
                    "committed": false,
                    "search": true,
                    "version": "7.0.0",
                    "compound": true,
                    "attributes": {
                    }
                  }
                }
              }
            ]
          }
        }
      }
    }

[« Index recovery API](indices-recovery.md) [Index shard stores API
»](indices-shards-stores.md)
