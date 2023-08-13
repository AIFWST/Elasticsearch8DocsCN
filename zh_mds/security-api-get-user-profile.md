

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Enable user profile API](security-api-enable-user-profile.md) [Suggest
user profile API »](security-api-suggest-user-profile.md)

## 获取用户配置文件API

用户配置文件功能仅供 Kibana 和 Elastic 的可观测性、企业级搜索和 Elastic 安全解决方案使用。个人用户和外部应用程序不应直接调用此 API。Elastic 保留在未来版本中更改或删除此功能的权利，恕不另行通知。

使用唯一配置文件 ID 列表检索用户配置文件。

###Request

'获取/_security/配置文件/<uid>"

###Prerequisites

要使用此 API，您必须具有_at least_"read_security"群集特权(或更大的特权，例如"manage_user_profile"或"manage_security")。

###Description

获取用户配置文件 API 返回与指定的"uid"匹配的用户配置文件文档，该文档在激活用户配置文件时生成。

### 路径参数

`uid`

     (Required, string) The unique identifier for the user profile. You can specify multiple IDs as a comma-separated list. 

### 查询参数

`data`

     (Optional, string) Comma-separated list of filters for the `data` field of the profile document. To return all content, use `data=*`. To return a subset of content, use `data=<key>` to retrieve the content nested under the specified `<key>`. Defaults to returning no content. 

### 响应正文

成功的调用将返回用户配置文件的 JSON 表示形式及其内部版本控制编号。如果未找到提供的"uid"的配置文件文档，则 API 将返回一个空对象。默认情况下不返回"data"字段的内容，以避免反序列化潜在的大型有效负载。

###Examples

    
    
    GET /_security/profile/u_79HkWkwmnBH5gqFKwoxggWPjEBOur1zLPXQPEl1VBW0_0

API 为"uid"匹配"u_79HkWkwmnBH5gqFKwoxggWPjEBOur1zLPXQPEl1VBW0_0"返回以下响应：

    
    
    {
      "profiles": [
        {
          "uid": "u_79HkWkwmnBH5gqFKwoxggWPjEBOur1zLPXQPEl1VBW0_0",
          "enabled": true,
          "last_synchronized": 1642650651037,
          "user": {
            "username": "jacknich",
            "roles": [
              "admin", "other_role1"
            ],
            "realm_name": "native",
            "full_name": "Jack Nicholson",
            "email": "jacknich@example.com"
          },
          "labels": {
            "direction": "north"
          },
          "data": {}, __"_doc": {
            "_primary_term": 88,
            "_seq_no": 66
          }
        }
      ]
    }

__

|

默认情况下，"数据"字段中不返回任何内容。   ---|--- 以下请求检索嵌套在键"app1"下的"数据"子集以及用户的配置文件：

    
    
    GET /_security/profile/u_79HkWkwmnBH5gqFKwoxggWPjEBOur1zLPXQPEl1VBW0_0?data=app1.key1
    
    
    {
      "profiles": [
        {
          "uid": "u_79HkWkwmnBH5gqFKwoxggWPjEBOur1zLPXQPEl1VBW0_0",
          "enabled": true,
          "last_synchronized": 1642650651037,
          "user": {
            "username": "jacknich",
            "roles": [
              "admin", "other_role1"
            ],
            "realm_name": "native",
            "full_name": "Jack Nicholson",
            "email": "jacknich@example.com"
          },
          "labels": {
            "direction": "north"
          },
          "data": {
            "app1": {
              "key1": "value1"
            }
          },
          "_doc": {
            "_primary_term": 88,
            "_seq_no": 66
          }
        }
      ]
    }

如果在检索用户配置文件时出现任何错误，则会在"错误"字段中返回这些错误：

    
    
    {
      "profiles": [],
      "errors": {
        "count": 1,
        "details": {
           "u_FmxQt3gr1BBH5wpnz9HkouPj3Q710XkOgg1PWkwLPBW_5": {
             "type": "resource_not_found_exception",
             "reason": "profile document not found"
           }
        }
      }
    }

[« Enable user profile API](security-api-enable-user-profile.md) [Suggest
user profile API »](security-api-suggest-user-profile.md)
