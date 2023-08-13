

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Snapshot and restore APIs](snapshot-restore-apis.md)

[« Get snapshot repository API](get-snapshot-repo-api.md) [Clean up snapshot
repository API »](clean-up-snapshot-repo-api.md)

## 删除快照存储库API

注销一个或多个快照存储库。

取消注册存储库时，Elasticsearch 仅删除对存储库存储快照位置的引用。快照本身保持不变并保留在原位。

    
    
    response = client.snapshot.delete_repository(
      repository: 'my_repository'
    )
    puts response
    
    
    DELETE /_snapshot/my_repository

###Request

"删除/_snapshot/<repository>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。

### 路径参数

`<repository>`

     (Required, string) Name of the snapshot repository to unregister. Wildcard (`*`) patterns are supported. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Specifies the period of time to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Specifies the period of time to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

[« Get snapshot repository API](get-snapshot-repo-api.md) [Clean up snapshot
repository API »](clean-up-snapshot-repo-api.md)
