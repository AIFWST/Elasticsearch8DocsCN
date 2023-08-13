

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cross-cluster replication APIs](ccr-apis.md)

[« Resume follower API](ccr-post-resume-follow.md) [Forget follower API
»](ccr-post-forget-follower.md)

## 取消关注API

将从属索引转换为常规索引。

###Request

    
    
    POST /<follower_index>/_ccr/unfollow

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，则必须对关注者索引具有"manage_follow_index"索引权限。有关详细信息，请参阅安全权限。

###Description

此 API 将停止与关注方索引关联的以下任务，并删除与跨集群复制关联的索引元数据和设置。这使索引能够被视为常规索引。在调用取消关注 API 之前，必须暂停并关闭关注者索引。

目前，跨集群复制不支持将现有常规索引转换为追随者索引。将追随者索引转换为常规索引是不可逆的操作。

### 路径参数

`<follower_index>`

     (Required, string) The name of the follower index. 

###Examples

此示例将"follower_index"从关注者索引转换为常规索引：

    
    
    response = client.ccr.unfollow(
      index: 'follower_index'
    )
    puts response
    
    
    POST /follower_index/_ccr/unfollow

API 返回以下结果：

    
    
    {
      "acknowledged" : true
    }

[« Resume follower API](ccr-post-resume-follow.md) [Forget follower API
»](ccr-post-forget-follower.md)
