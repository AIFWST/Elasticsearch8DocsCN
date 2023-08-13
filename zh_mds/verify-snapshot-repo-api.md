

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Snapshot and restore APIs](snapshot-restore-apis.md)

[« Create or update snapshot repository API](put-snapshot-repo-api.md)
[Repository analysis API »](repo-analysis-api.md)

## 验证快照存储库API

检查快照存储库中的常见错误配置。请参阅验证存储库。

    
    
    response = client.snapshot.verify_repository(
      repository: 'my_repository'
    )
    puts response
    
    
    POST /_snapshot/my_repository/_verify

###Request

"发布/_snapshot/<repository>/_verify"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。

### 路径参数

`<repository>`

     (Required, string) Name of the snapshot repository to verify. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Specifies the period of time to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Specifies the period of time to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 响应正文

`nodes`

    

(object)

"节点"对象的属性

`<node_id>`

    

(对象)包含有关连接到快照存储库的节点的信息。

键是节点的 ID。

""的属性<node_id>

`name`

    

(字符串)节点的人类可读名称。

您可以使用"elasticsearch.yml"中的"node.name"属性设置此名称。默认为计算机的主机名。

[« Create or update snapshot repository API](put-snapshot-repo-api.md)
[Repository analysis API »](repo-analysis-api.md)
