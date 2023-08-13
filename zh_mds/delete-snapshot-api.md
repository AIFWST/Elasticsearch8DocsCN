

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Snapshot and restore APIs](snapshot-restore-apis.md)

[« Restore snapshot API](restore-snapshot-api.md) [Snapshot lifecycle
management APIs »](snapshot-lifecycle-management-api.md)

## 删除快照接口

删除快照。

    
    
    response = client.snapshot.delete(
      repository: 'my_repository',
      snapshot: 'my_snapshot'
    )
    puts response
    
    
    DELETE /_snapshot/my_repository/my_snapshot

###Request

"删除/_snapshot/<repository><snapshot>/"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。

### 路径参数

`<repository>`

     (Required, string) Name of the repository to delete a snapshot from. 
`<snapshot>`

     (Required, string) Comma-separated list of snapshot names to delete. Also accepts wildcards (`*`). 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Example

以下请求从名为"my_repository"的存储库中删除"snapshot_2"和"snapshot_3"。

    
    
    response = client.snapshot.delete(
      repository: 'my_repository',
      snapshot: 'snapshot_2,snapshot_3'
    )
    puts response
    
    
    DELETE /_snapshot/my_repository/snapshot_2,snapshot_3

API 返回以下响应：

    
    
    {
      "acknowledged" : true
    }

[« Restore snapshot API](restore-snapshot-api.md) [Snapshot lifecycle
management APIs »](snapshot-lifecycle-management-api.md)
