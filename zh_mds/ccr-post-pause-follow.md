

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cross-cluster replication APIs](ccr-apis.md)

[« Create follower API](ccr-put-follow.md) [Resume follower API »](ccr-post-
resume-follow.md)

## 暂停关注者API

暂停关注者索引。

###Request

    
    
    POST /<follower_index>/_ccr/pause_follow

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对包含追随者索引的集群具有"manage_ccr"集群权限。有关详细信息，请参阅安全权限。

###Description

此 API 暂停关注者索引。当此 API 返回时，追随者索引将不会从领导者索引获取任何其他操作。您可以使用简历关注者 API 恢复关注。暂停和恢复关注者索引可用于更改以下任务的配置。

### 路径参数

`<follower_index>`

     (Required, string) The name of the follower index. 

###Examples

此示例暂停名为"follower_index"的关注者索引：

    
    
    response = client.ccr.pause_follow(
      index: 'follower_index'
    )
    puts response
    
    
    POST /follower_index/_ccr/pause_follow

API 返回以下结果：

    
    
    {
      "acknowledged" : true
    }

[« Create follower API](ccr-put-follow.md) [Resume follower API »](ccr-post-
resume-follow.md)
