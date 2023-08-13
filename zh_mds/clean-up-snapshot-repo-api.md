

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Snapshot and restore APIs](snapshot-restore-apis.md)

[« Delete snapshot repository API](delete-snapshot-repo-api.md) [Clone
snapshot API »](clone-snapshot-api.md)

## 清理快照存储库API

触发对快照存储库内容的审查，并删除现有快照未引用的任何过时数据。请参阅清理存储库。

    
    
    response = client.snapshot.cleanup_repository(
      repository: 'my_repository'
    )
    puts response
    
    
    POST /_snapshot/my_repository/_cleanup

###Request

"发布/_snapshot/<repository>/_cleanup"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。

### 路径参数

`<repository>`

     (Required, string) Name of the snapshot repository to review and clean up. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 响应正文

`results`

    

(对象)包含清理操作的统计信息。

"结果"的属性

`deleted_bytes`

     (integer) Number of bytes freed by cleanup operations. 
`deleted_blobs`

     (integer) Number of binary large objects (blobs) removed from the snapshot repository during cleanup operations. Any non-zero value implies that unreferenced blobs were found and subsequently cleaned up. 

###Examples

    
    
    response = client.snapshot.cleanup_repository(
      repository: 'my_repository'
    )
    puts response
    
    
    POST /_snapshot/my_repository/_cleanup

API 返回以下响应：

    
    
    {
      "results": {
        "deleted_bytes": 20,
        "deleted_blobs": 5
      }
    }

[« Delete snapshot repository API](delete-snapshot-repo-api.md) [Clone
snapshot API »](clone-snapshot-api.md)
