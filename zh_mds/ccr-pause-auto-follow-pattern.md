

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cross-cluster replication APIs](ccr-apis.md)

[« Get auto-follow pattern API](ccr-get-auto-follow-pattern.md) [Resume
auto-follow pattern API »](ccr-resume-auto-follow-pattern.md)

## 暂停自动关注模式API

暂停自动跟随模式。

###Request

"发布/_ccr/auto_follow/<auto_follow_pattern_name>/暂停"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对包含追随者索引的集群具有"manage_ccr"集群权限。有关详细信息，请参阅安全权限。

###Description

此 API 暂停自动关注模式。当此 API 返回时，自动关注模式处于非活动状态，并忽略在远程集群上创建的任何与自动关注模式匹配的新索引。在 GET 自动关注模式 API 中，将显示暂停的自动关注模式，其中"活动"字段设置为"false"。

您可以使用恢复自动关注模式 API 恢复自动关注。恢复后，自动关注模式将再次处于活动状态，并自动为远程集群上与其模式匹配的新创建索引配置关注者索引。模式暂停时创建的远程索引也将遵循，除非在此期间它们已被删除或关闭。

### 路径参数

`<auto_follow_pattern_name>`

     (Required, string) Name of the auto-follow pattern to pause. 

###Examples

此示例暂停名为"my_auto_follow_pattern"的自动跟随模式：

    
    
    response = client.ccr.pause_auto_follow_pattern(
      name: 'my_auto_follow_pattern'
    )
    puts response
    
    
    POST /_ccr/auto_follow/my_auto_follow_pattern/pause

API 返回以下结果：

    
    
    {
      "acknowledged" : true
    }

[« Get auto-follow pattern API](ccr-get-auto-follow-pattern.md) [Resume
auto-follow pattern API »](ccr-resume-auto-follow-pattern.md)
