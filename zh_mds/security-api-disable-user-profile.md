

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Activate user profile API](security-api-activate-user-profile.md) [Enable
user profile API »](security-api-enable-user-profile.md)

## 禁用用户配置文件API

用户配置文件功能仅供 Kibana 和 Elastic 的可观测性、企业级搜索和 Elastic 安全解决方案使用。个人用户和外部应用程序不应直接调用此 API。Elastic 保留在未来版本中更改或删除此功能的权利，恕不另行通知。

禁用用户配置文件，使其在用户配置文件搜索中不可见。

###Request

'发布/_security/个人资料/<uid>/_disable"

'PUT /_security/profile/<uid>/_disable'

###Prerequisites

若要使用此 API，必须具有"manage_user_profile"群集权限。

###Description

激活用户配置文件后，它会自动启用并在用户配置文件搜索中显示。可以使用禁用用户配置文件 API 禁用用户配置文件，使其在这些搜索中不可见。

要重新启用已禁用的用户配置文件，请使用启用用户配置文件 API 。

### 路径参数

`<uid>`

     (Required, string) Unique identifier for the user profile. 

### 查询参数

`refresh`

     (Optional, enum) If `true`, Elasticsearch refreshes the affected shards to make this operation visible to search, if `wait_for` then wait for a refresh to make this operation visible to search, if `false` do nothing with refreshes. Valid values: `true`, `false`, `wait_for`. Default: `false`. 

###Examples

以下请求禁用"uid"匹配"u_79HkWkwmnBH5gqFKwoxggWPjEBOur1zLPXQPEl1VBW0_0"的用户配置文件：

    
    
    POST /_security/profile/u_79HkWkwmnBH5gqFKwoxggWPjEBOur1zLPXQPEl1VBW0_0/_disable

[« Activate user profile API](security-api-activate-user-profile.md) [Enable
user profile API »](security-api-enable-user-profile.md)
