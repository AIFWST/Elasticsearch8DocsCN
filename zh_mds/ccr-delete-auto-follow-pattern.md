

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cross-cluster replication APIs](ccr-apis.md)

[« Create auto-follow pattern API](ccr-put-auto-follow-pattern.md) [Get
auto-follow pattern API »](ccr-get-auto-follow-pattern.md)

## 删除自动关注模式API

删除自动跟随模式。

###Request

    
    
    DELETE /_ccr/auto_follow/<auto_follow_pattern_name>

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对包含追随者索引的集群具有"manage_ccr"集群权限。有关详细信息，请参阅安全权限。

###Description

此 API 删除已配置的自动关注模式集合。

### 路径参数

`<auto_follow_pattern_name>`

     (Required, string) Specifies the auto-follow pattern collection to delete. 

###Examples

此示例删除名为"my_auto_follow_pattern"的自动跟随模式集合：

    
    
    response = client.ccr.delete_auto_follow_pattern(
      name: 'my_auto_follow_pattern'
    )
    puts response
    
    
    DELETE /_ccr/auto_follow/my_auto_follow_pattern

API 返回以下结果：

    
    
    {
      "acknowledged" : true
    }

[« Create auto-follow pattern API](ccr-put-auto-follow-pattern.md) [Get
auto-follow pattern API »](ccr-get-auto-follow-pattern.md)
