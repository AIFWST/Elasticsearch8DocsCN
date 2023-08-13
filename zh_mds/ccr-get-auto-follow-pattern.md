

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cross-cluster replication APIs](ccr-apis.md)

[« Delete auto-follow pattern API](ccr-delete-auto-follow-pattern.md) [Pause
auto-follow pattern API »](ccr-pause-auto-follow-pattern.md)

## 获取自动关注模式API

获取自动跟随模式。

###Request

    
    
    response = client.ccr.get_auto_follow_pattern
    puts response
    
    
    GET /_ccr/auto_follow/
    
    
    GET /_ccr/auto_follow/<auto_follow_pattern_name>

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对包含追随者索引的集群具有"manage_ccr"集群权限。有关详细信息，请参阅安全权限。

###Description

此 API 配置自动关注模式。此 API 将返回指定的自动跟随模式集合。

### 路径参数

`<auto_follow_pattern_name>`

     (Optional, string) Specifies the auto-follow pattern collection that you want to retrieve. If you do not specify a name, the API returns information for all collections. 

###Examples

此示例检索有关名为"my_auto_follow_pattern"的自动跟随模式集合的信息：

    
    
    response = client.ccr.get_auto_follow_pattern(
      name: 'my_auto_follow_pattern'
    )
    puts response
    
    
    GET /_ccr/auto_follow/my_auto_follow_pattern

API 返回以下结果：

    
    
    {
      "patterns": [
        {
          "name": "my_auto_follow_pattern",
          "pattern": {
            "active": true,
            "remote_cluster" : "remote_cluster",
            "leader_index_patterns" :
            [
              "leader_index*"
            ],
            "leader_index_exclusion_patterns":
            [
              "leader_index_001"
            ],
            "follow_index_pattern" : "{{leader_index}}-follower"
          }
        }
      ]
    }

[« Delete auto-follow pattern API](ccr-delete-auto-follow-pattern.md) [Pause
auto-follow pattern API »](ccr-pause-auto-follow-pattern.md)
