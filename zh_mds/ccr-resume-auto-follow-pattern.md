

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cross-cluster replication APIs](ccr-apis.md)

[« Pause auto-follow pattern API](ccr-pause-auto-follow-pattern.md) [Data
stream APIs »](data-stream-apis.md)

## 恢复自动关注模式API

恢复自动跟随模式。

###Request

"发布/_ccr/auto_follow/<auto_follow_pattern_name>/简历"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对包含追随者索引的集群具有"manage_ccr"集群权限。有关详细信息，请参阅安全权限。

###Description

此 API 恢复已使用暂停自动关注模式 API 暂停的自动关注模式。当此 API 返回时，自动关注模式将恢复为远程集群上与其模式匹配的新创建的索引配置以下索引。模式暂停时创建的远程索引也将遵循，除非在此期间它们已被删除或关闭。

### 路径参数

`<auto_follow_pattern_name>`

     (Required, string) Specifies the name of the auto-follow pattern to resume. 

###Examples

此示例恢复名为"my_auto_follow_pattern"的暂停自动关注模式的活动：

    
    
    response = client.ccr.resume_auto_follow_pattern(
      name: 'my_auto_follow_pattern'
    )
    puts response
    
    
    POST /_ccr/auto_follow/my_auto_follow_pattern/resume

API 返回以下结果：

    
    
    {
      "acknowledged" : true
    }

[« Pause auto-follow pattern API](ccr-pause-auto-follow-pattern.md) [Data
stream APIs »](data-stream-apis.md)
