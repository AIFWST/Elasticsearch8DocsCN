

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Get user profiles API](security-api-get-user-profile.md) [Update user
profile data API »](security-api-update-user-profile-data.md)

## 建议用户配置文件API

用户配置文件功能仅供 Kibana 和 Elastic 的可观测性、企业级搜索和 Elastic 安全解决方案使用。个人用户和外部应用程序不应直接调用此 API。Elastic 保留在未来版本中更改或删除此功能的权利，恕不另行通知。

获取与指定搜索条件匹配的用户配置文件的建议。

###Request

"获取/_security/配置文件/_suggest"

"发布/_security/个人资料/_suggest"

###Prerequisites

要使用此 API，您必须具有_at least_"read_security"群集特权(或更大的特权，例如"manage_user_profile"或"manage_security")。

### 查询参数

`data`

     (Optional, string) Comma-separated list of filters for the `data` field of the profile document. To return all content, use `data=*`. To return a subset of content, use `data=<key>` to retrieve the content nested under the specified `<key>`. Defaults to returning no content. 

### 请求正文

`name`

     (Optional, string) Query string used to match name-related fields in [user profile documents](security-api-activate-user-profile.html#security-api-activate-user-profile-desc "Description"). Name-related fields are the user's `username`, `full_name` and `email`. 
`size`

     (Optional, integer) Number of profiles to return. Defaults to `10`. 
`data`

     (Optional, string) Comma-separated list of filters for the `data` field of the profile document. It works the same way as the [`data` query parameter](security-api-suggest-user-profile.html#security-api-suggest-user-profile-query-params "Query parameters"). 

将"data"同时指定为查询参数和请求正文字段是错误的。

`hint`

    

(可选，对象)额外的搜索条件以提高建议结果的相关性。与指定提示匹配的配置文件在响应中排名较高。但是，不匹配提示不会从响应中排除配置文件，只要它与"name"字段查询匹配即可。

"提示"的属性：

`uids`

     (Optional, list of strings) A list of Profile UIDs to match against. 
`labels`

     (Optional, object) A single key-value pair to match against the `labels` section of a profile. The key must be a string and the value must be either a string or a list of strings. A profile is considered matching if it matches at least one of the strings. 

### 响应正文

`total`

     (object) Metadata about the number of matching profiles. 
`took`

     (integer) Milliseconds it took Elasticsearch to execute the request. 
`profiles`

     (array of objects) List of profile documents, ordered by relevance, that match the search criteria. 

###Examples

以下请求获取有关名称相关字段与"jack"匹配的配置文件文档的建议。它指定了"uid"和"标签"提示以提高相关性：

    
    
    POST /_security/profile/_suggest
    {
      "name": "jack",  __"hint": {
        "uids": [ __"u_8RKO7AKfEbSiIHZkZZ2LJy2MUSDPWDr3tMI_CkIGApU_0",
          "u_79HkWkwmnBH5gqFKwoxggWPjEBOur1zLPXQPEl1VBW0_0"
        ],
        "labels": {
          "direction": ["north", "east"] __}
      }
    }

__

|

配置文件的名称相关字段必须与"jack"匹配，才能包含在响应中。   ---|---    __

|

"uids"提示包括用户"jackspa"和"jacknich"的配置文件UID。   __

|

如果"方向"标签与"北"或"东"匹配，则"标签"提示会将配置文件排名更高。   该 API 返回：

    
    
    {
      "took": 30,
      "total": {
        "value": 3,
        "relation": "eq"
      },
      "profiles": [
        {
          "uid": "u_79HkWkwmnBH5gqFKwoxggWPjEBOur1zLPXQPEl1VBW0_0",
          "user": {
            "username": "jacknich",    __"roles": [ "admin", "other_role1" ],
            "realm_name": "native",
            "email" : "jacknich@example.com",
            "full_name": "Jack Nicholson"
          },
          "labels": {
            "direction": "north"
          },
          "data": {}
        },
        {
          "uid": "u_8RKO7AKfEbSiIHZkZZ2LJy2MUSDPWDr3tMI_CkIGApU_0",
          "user": {
            "username": "jackspa", __"roles": [ "user" ],
            "realm_name": "native",
            "email" : "jackspa@example.com",
            "full_name": "Jack Sparrow"
          },
          "labels": {
            "direction": "south"
          },
          "data": {}
        },
        {
          "uid": "u_P_0BMHgaOK3p7k-PFWUCbw9dQ-UFjt01oWJ_Dp2PmPc_0",
          "user": {
            "username": "jackrea", __"roles": [ "admin" ],
            "realm_name": "native",
            "email" : "jackrea@example.com",
            "full_name": "Jack Reacher"
          },
          "labels": {
            "direction": "west"
          },
          "data": {}
        }
      ]
    }

__

|

用户"jacknich"排名最高，因为配置文件与"uids"和"labels"提示---|---__匹配

|

用户"jackspa"排名第二，因为配置文件仅与"uids"提示匹配__

|

用户"jackrea"排名最低，因为配置文件与任何提示都不匹配。但是，它不会从响应中排除，因为它与"name"查询匹配。   « 获取用户配置文件 API 更新用户配置文件数据 API »