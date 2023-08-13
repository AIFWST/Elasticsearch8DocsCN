

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Snapshot and restore APIs](snapshot-restore-apis.md)

[« Clean up snapshot repository API](clean-up-snapshot-repo-api.md) [Create
snapshot API »](create-snapshot-api.md)

## 克隆快照接口

将部分或全部快照克隆到新快照中。

    
    
    response = client.snapshot.clone(
      repository: 'my_repository',
      snapshot: 'source_snapshot',
      target_snapshot: 'target_snapshot',
      body: {
        indices: 'index_a,index_b'
      }
    )
    puts response
    
    
    PUT /_snapshot/my_repository/source_snapshot/_clone/target_snapshot
    {
      "indices": "index_a,index_b"
    }

###Request

"放 /_snapshot/<repository>/<source_snapshot>/_clone<target_snapshot>/"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。

###Description

克隆快照 API 允许在同一存储库中创建全部或部分现有快照的副本。

### 路径参数

`<repository>`

     (Required, string) Name of the snapshot repository that both source and target snapshot belong to. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Specifies the period of time to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Specifies the period of time to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`indices`

     (Required, string) A comma-separated list of indices to include in the snapshot. [multi-target syntax](api-conventions.html#api-multi-index "Multi-target syntax") is supported. 

[« Clean up snapshot repository API](clean-up-snapshot-repo-api.md) [Create
snapshot API »](create-snapshot-api.md)
