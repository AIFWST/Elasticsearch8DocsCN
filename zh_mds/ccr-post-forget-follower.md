

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cross-cluster replication APIs](ccr-apis.md)

[« Unfollow API](ccr-post-unfollow.md) [Get follower stats API »](ccr-get-
follow-stats.md)

## 忘记追随者API

从领导者中删除从属程序保留租约。

###Request

    
    
    POST /<leader_index>/_ccr/forget_follower
    {
      "follower_cluster" : "<follower_cluster>",
      "follower_index" : "<follower_index>",
      "follower_index_uuid" : "<follower_index_uuid>",
      "leader_remote_cluster" : "<leader_remote_cluster>"
    }
    
    
    {
      "_shards" : {
        "total" : 1,
        "successful" : 1,
        "failed" : 0,
        "failures" : [ ]
      }
    }

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则必须具有领导者索引的"manage_leader_index"索引权限。有关详细信息，请参阅安全权限。

###Description

以下索引在其领导者索引上取出保留租约。这些保留租约用于增加领导者索引的分片保留以下索引的分片执行复制所需的操作历史记录的可能性。当通过取消关注 API 将关注者索引转换为常规索引(通过显式执行此 API 或通过索引生命周期管理隐式执行)时，将删除这些保留租约。但是，删除这些保留租约可能会失败(例如，如果包含 leaderindex 的远程集群不可用)。虽然这些保留租约最终会自行过期，但它们的延长存在可能会导致领导者索引保留不必要的历史记录，并阻止索引生命周期管理对领导者索引执行某些操作。此 API 的存在是为了在取消关注的 API 无法执行此操作时启用手动删除这些保留租约。

此 API 不会通过以下索引停止复制。如果使用此 API 针对仍在活动关注的追随者索引，则以下索引将在领导者上添加回保留租约。此 API 的唯一用途是在调用取消关注的 API 后处理无法删除以下保留租约的情况。

### 路径参数

`<leader_index>`

     (Required, string) The name of the leader index. 

### 请求正文

`follower_cluster`

     (Required, string) The name of the cluster containing the follower index. 
`follower_index`

     (Required, string) The name of the follower index. 
`follower_index_uuid`

     (Required, string) The UUID of the follower index. 
`leader_remote_cluster`

     (Required, string) The alias (from the perspective of the cluster containing the follower index) of the [remote cluster](remote-clusters.html "Remote clusters") containing the leader index. 

###Examples

此示例从"leader_index"中删除"follower_index"的从属程序保留租约。

    
    
    response = client.ccr.forget_follower(
      index: 'leader_index',
      body: {
        follower_cluster: 'follower_cluster',
        follower_index: 'follower_index',
        follower_index_uuid: 'vYpnaWPRQB6mNspmoCeYyA',
        leader_remote_cluster: 'leader_cluster'
      }
    )
    puts response
    
    
    POST /leader_index/_ccr/forget_follower
    {
      "follower_cluster" : "follower_cluster",
      "follower_index" : "follower_index",
      "follower_index_uuid" : "vYpnaWPRQB6mNspmoCeYyA",
      "leader_remote_cluster" : "leader_cluster"
    }

API 返回以下结果：

    
    
    {
      "_shards" : {
        "total" : 1,
        "successful" : 1,
        "failed" : 0,
        "failures" : [ ]
      }
    }

[« Unfollow API](ccr-post-unfollow.md) [Get follower stats API »](ccr-get-
follow-stats.md)
