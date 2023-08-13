

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Suggest user profile API](security-api-suggest-user-profile.md) [Has
privileges user profile API »](security-api-has-privileges-user-profile.md)

## 更新用户配置文件数据接口

用户配置文件功能仅供 Kibana 和 Elastic 的可观测性、企业级搜索和 Elastic 安全解决方案使用。个人用户和外部应用程序不应直接调用此 API。Elastic 保留在未来版本中更改或删除此功能的权利，恕不另行通知。

更新与指定唯一 ID 关联的用户配置文件的特定数据。

###Request

"发布/_security/个人资料/<uid>/_data"

###Prerequisites

要使用此 API，您必须具有以下权限之一：

* "manage_user_profile"群集权限。  * 请求中引用的命名空间的"update_profile_data"全局权限。

###Description

更新用户配置文件 API 使用 JSON 对象更新现有用户配置文件文档的"标签"和"数据"字段。新键及其值将添加到配置文件文档中，冲突的键将替换为请求中包含的数据。

对于"标签"和"数据"，内容由顶级字段命名。"update_profile_data"全局权限授予仅更新允许的命名空间的权限。

### 路径参数

`uid`

     (Required, string) A unique identifier for the user profile. 

### 查询参数

`if_seq_no`

     (Optional, integer) Only perform the operation if the document has this sequence number. See [Optimistic concurrency control](docs-index_.html#optimistic-concurrency-control-index "Optimistic concurrency control"). 
`if_primary_term`

     (Optional, integer) Only perform the operation if the document has this primary term. See [Optimistic concurrency control](docs-index_.html#optimistic-concurrency-control-index "Optimistic concurrency control"). 
`refresh`

     (Optional, enum) If `true`, Elasticsearch refreshes the affected shards to make this operation visible to search, if `wait_for` then wait for a refresh to make this operation visible to search, if `false` do nothing with refreshes. Valid values: `true`, `false`, `wait_for`. Default: `false`. 
`uid`

     (Required, string) A unique identifier for the user profile. 

### 请求正文

`labels`

     (Required*, object) Searchable data that you want to associate with the user profile. This field supports a nested data structure. Within the `labels` object, top-level keys cannot begin with an underscore (`_`) or contain a period (`.`). 
`data`

     (Required*, object) Non-searchable data that you want to associate with the user profile. This field supports a nested data structure. Within the `data` object, top-level keys cannot begin with an underscore (`_`) or contain a period (`.`) The `data` object is not searchable, but can be retrieved with the [Get user profile API](security-api-get-user-profile.html "Get user profiles API"). 

*表示在某些(但不是所有)情况下都需要该设置。

### 响应正文

成功的更新用户配置文件数据 API 调用将返回一个 JSON 结构，指示请求已确认：

    
    
    {
      "acknowledged": true
    }

###Examples

以下请求更新"uid"匹配的配置文件文档u_P_0BMHgaOK3p7k-PFWUCbw9dQ-UFjt01oWJ_Dp2PmPc_0"：

    
    
    POST /_security/profile/u_P_0BMHgaOK3p7k-PFWUCbw9dQ-UFjt01oWJ_Dp2PmPc_0/_data
    {
      "labels": {
        "direction": "east"
      },
      "data": {
        "app1": {
          "theme": "default"
        }
      }
    }

您可以更新配置文件数据以替换某些密钥并添加新密钥：

    
    
    POST /_security/profile/u_P_0BMHgaOK3p7k-PFWUCbw9dQ-UFjt01oWJ_Dp2PmPc_0/_data
    {
      "labels": {
        "direction": "west"
      },
      "data": {
        "app1": {
          "font": "large"
        }
      }
    }

如果立即获取配置文件，将返回合并的配置文件数据：

    
    
    GET /_security/profile/u_P_0BMHgaOK3p7k-PFWUCbw9dQ-UFjt01oWJ_Dp2PmPc_0?data=*
    
    
    {
      "profiles": [
        {
          "uid": "u_P_0BMHgaOK3p7k-PFWUCbw9dQ-UFjt01oWJ_Dp2PmPc_0",
          "enabled": true,
          "last_synchronized": 1642650651037,
          "user": {
            "username": "jackrea",
            "roles": [
              "admin"
            ],
            "realm_name": "native",
            "full_name": "Jack Reacher",
            "email": "jackrea@example.com"
          },
          "labels": {
            "direction": "west"
          },
          "data": {
            "app1": {
              "theme": "default",
              "font": "large"
            }
          },
          "_doc": {
            "_primary_term": 88,
            "_seq_no": 66
          }
        }
      ]
    }

[« Suggest user profile API](security-api-suggest-user-profile.md) [Has
privileges user profile API »](security-api-has-privileges-user-profile.md)
